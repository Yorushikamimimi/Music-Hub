from pathlib import Path

import catalog_service
from catalog_data import CATALOG_RELEASES, CATALOG_TRACKS
from catalog_service import _clean_bilibili_url, _clean_external_url, sync_catalog
from models import MusicYorushika, db


def test_catalog_contains_curated_official_records(app):
    with app.app_context():
        songs = MusicYorushika.query.order_by(MusicYorushika.display_order).all()

        assert len(songs) == 89
        assert [song.display_order for song in songs] == list(range(1, 90))
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
        assert all(song.release_date for song in songs)
        assert all(song.source_checked_at for song in songs)
        assert all(song.track_number > 0 for song in songs)


def test_catalog_sync_is_idempotent(app):
    with app.app_context():
        first_count = db.session.query(MusicYorushika).count()
        result = sync_catalog()
        second_count = db.session.query(MusicYorushika).count()

        assert first_count == second_count == 89
        assert result == {"created": 0, "updated": 89, "total": 89}


def test_release_track_order_matches_curated_official_catalog():
    assert len(CATALOG_TRACKS) == 89
    assert sum(bool(track["mv_url"]) for track in CATALOG_TRACKS) == 24

    assert {
        release["title"]: len(release["tracks"])
        for release in CATALOG_RELEASES
    } == {
        "晴る": 1,
        "幻燈": 25,
        "創作": 5,
        "盗作": 14,
        "エルマ": 14,
        "だから僕は音楽を辞めた": 14,
        "負け犬にアンコールはいらない": 9,
        "夏草が邪魔をする": 7,
    }
    for release in CATALOG_RELEASES:
        tracks = [
            track
            for track in CATALOG_TRACKS
            if track["album_title"] == release["title"]
        ]
        assert [track["track_number"] for track in tracks] == list(
            range(1, len(release["tracks"]) + 1)
        )

    assert [
        title
        for _slug, title in next(
            release["tracks"]
            for release in CATALOG_RELEASES
            if release["title"] == "盗作"
        )
    ] == [
        "音楽泥棒の自白",
        "昼鳶",
        "春ひさぎ",
        "爆弾魔",
        "青年期、空き巣",
        "レプリカント",
        "花人局",
        "朱夏期、音楽泥棒",
        "盗作",
        "思想犯",
        "逃亡",
        "幼年期、思い出の中",
        "夜行",
        "花に亡霊",
    ]


def test_release_dates_and_sources_follow_official_release_pages():
    releases = {release["title"]: release for release in CATALOG_RELEASES}

    assert releases["晴る"]["release_date"].isoformat() == "2024-01-05"
    assert releases["幻燈"]["release_date"].isoformat() == "2023-04-05"
    assert releases["盗作"]["release_date"].isoformat() == "2020-07-29"
    assert releases["エルマ"]["release_date"].isoformat() == "2019-08-28"
    assert releases["夏草が邪魔をする"]["release_date"].isoformat() == "2017-06-28"
    assert releases["幻燈"]["source_url"].endswith("/discography/detail/30/")
    assert releases["盗作"]["source_url"].endswith("/discography/detail/15/")
    assert all(
        "/discography/detail/" in release["source_url"]
        for release in CATALOG_RELEASES
    )
    assert all(
        track["source_checked_at"].isoformat() == "2026-07-28"
        for track in CATALOG_TRACKS
    )


def test_sync_never_reuses_a_curated_row_only_because_cover_matches(
    app,
    monkeypatch,
):
    first, second = CATALOG_TRACKS[1:3]

    with app.app_context():
        MusicYorushika.query.delete()
        db.session.add(
            MusicYorushika(
                slug=first["slug"],
                title=first["title"],
                cover_path=first["cover_path"],
                is_featured=True,
            )
        )
        db.session.commit()
        monkeypatch.setattr(catalog_service, "CATALOG_TRACKS", (first, second))

        result = sync_catalog()

        assert result == {"created": 1, "updated": 1, "total": 2}
        assert {
            song.slug for song in MusicYorushika.query.order_by(MusicYorushika.id)
        } == {first["slug"], second["slug"]}


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
