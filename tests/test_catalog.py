from pathlib import Path

from catalog_data import CATALOG_TRACKS
from catalog_service import _clean_external_url, sync_catalog
from models import MusicYorushika, db


def test_catalog_contains_curated_official_records(app):
    with app.app_context():
        songs = MusicYorushika.query.order_by(MusicYorushika.display_order).all()

        assert len(songs) == 20
        assert [song.display_order for song in songs] == list(range(1, 21))
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

        assert first_count == second_count == 20
        assert result == {"created": 0, "updated": 20, "total": 20}


def test_external_source_url_is_restricted_to_official_domain():
    assert (
        _clean_external_url("https://yorushika.com/discography/detail/37/?x=1#top")
        == "https://yorushika.com/discography/detail/37/"
    )
    assert _clean_external_url("https://example.com/fake") is None
    assert _clean_external_url("javascript:alert(1)") is None
