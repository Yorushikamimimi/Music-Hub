from pathlib import Path

from catalog_data import CATALOG_RELEASES, CATALOG_TRACKS
from catalog_service import _clean_bilibili_url, _clean_external_url, sync_catalog
from models import MusicYorushika, db


def test_catalog_contains_curated_official_records(app):
    with app.app_context():
        songs = MusicYorushika.query.order_by(MusicYorushika.display_order).all()

        assert len(songs) == 63
        assert [song.display_order for song in songs] == list(range(1, 64))
        assert all(song.cover_path.endswith(".webp") for song in songs)
        assert all(
            (Path(app.root_path) / "static" / "images" / song.cover_path).is_file()
            for song in songs
        )
        assert all(song.story_summary for song in songs)
        assert all(
            song.source_url.startswith("https://yorushika.com/")
            for song in songs
        )
        assert {song.slug for song in songs} == {
            track["slug"] for track in CATALOG_TRACKS
        }


def test_catalog_sync_is_idempotent(app):
    with app.app_context():
        first_count = db.session.query(MusicYorushika).count()
        result = sync_catalog()
        second_count = db.session.query(MusicYorushika).count()

        assert first_count == second_count == 63
        assert result == {"created": 0, "updated": 63, "total": 63}


def test_release_track_order_matches_curated_official_catalog():
    assert {
        release["title"]: len(release["tracks"])
        for release in CATALOG_RELEASES
    } == {
        "晴る": 1,
        "幻燈": 16,
        "創作": 5,
        "盗作": 10,
        "エルマ": 10,
        "だから僕は音楽を辞めた": 10,
        "負け犬にアンコールはいらない": 6,
        "夏草が邪魔をする": 5,
    }
    assert [
        title
        for _slug, title in next(
            release["tracks"]
            for release in CATALOG_RELEASES
            if release["title"] == "盗作"
        )
    ] == [
        "昼鳶",
        "春ひさぎ",
        "爆弾魔",
        "レプリカント",
        "花人局",
        "盗作",
        "思想犯",
        "逃亡",
        "夜行",
        "花に亡霊",
    ]


def test_external_source_url_is_restricted_to_official_domain():
    assert (
        _clean_external_url("https://yorushika.com/discography/detail/37/?x=1#top")
        == "https://yorushika.com/discography/detail/37/"
    )
    assert _clean_external_url("https://example.com/fake") is None
    assert _clean_external_url("javascript:alert(1)") is None


def test_bilibili_url_is_restricted_to_video_pages():
    assert (
        _clean_bilibili_url(
            "https://www.bilibili.com/video/BV1dW41137on/?from=search#reply"
        )
        == "https://www.bilibili.com/video/BV1dW41137on/"
    )
    assert _clean_bilibili_url("https://www.bilibili.com/account/history") is None
    assert _clean_bilibili_url("https://example.com/video/BV1dW41137on/") is None
