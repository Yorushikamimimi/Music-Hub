import sqlalchemy as sa
from flask_migrate import downgrade, upgrade

from app import create_app
from catalog_service import sync_catalog
from models import (
    MusicYorushika,
    YorushikaRelease,
    YorushikaReleaseTrack,
    db,
)


def _migration_app(database_path):
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "migration-test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )


def test_migration_creates_fresh_catalog_schema(tmp_path):
    application = _migration_app(tmp_path / "fresh.sqlite3")

    with application.app_context():
        upgrade(directory="migrations")
        columns = {
            column["name"]
            for column in sa.inspect(db.engine).get_columns("music_yorushika")
        }
        assert {
            "slug",
            "album_title",
            "release_date",
            "track_number",
            "story_summary",
            "source_checked_at",
            "display_order",
            "is_featured",
        }.issubset(columns)
        assert {
            "music_yorushika",
            "yorushika_release",
            "yorushika_release_track",
        }.issubset(sa.inspect(db.engine).get_table_names())

        result = sync_catalog()
        assert result["created"] == 111
        assert MusicYorushika.query.count() == 111
        assert YorushikaRelease.query.count() == 22
        assert YorushikaReleaseTrack.query.count() == 124


def test_migration_preserves_legacy_row_and_columns(tmp_path):
    application = _migration_app(tmp_path / "legacy.sqlite3")

    with application.app_context():
        with db.engine.begin() as connection:
            connection.exec_driver_sql(
                """
                CREATE TABLE music_yorushika (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(255) NOT NULL,
                    album VARCHAR(255),
                    rating INTEGER,
                    release_year INTEGER,
                    cover_path VARCHAR(255),
                    link VARCHAR(255)
                )
                """
            )
            connection.exec_driver_sql(
                """
                INSERT INTO music_yorushika
                    (title, album, rating, release_year, cover_path, link)
                VALUES
                    ('Sunny', 'legacy', 99, 2024, 'sunny.jpg', 'https://example.com'),
                    ('Legacy extra', 'legacy', 88, 2016, 'extra.jpg', 'https://example.com')
                """
            )

        upgrade(directory="migrations")
        columns = {
            column["name"]
            for column in sa.inspect(db.engine).get_columns("music_yorushika")
        }
        assert "album" in columns
        assert "rating" in columns
        assert "album_title" in columns
        assert "release_date" in columns
        assert "track_number" in columns
        assert "source_checked_at" in columns
        assert "yorushika_release" in sa.inspect(db.engine).get_table_names()
        assert "yorushika_release_track" in sa.inspect(db.engine).get_table_names()

        result = sync_catalog()
        assert result["created"] == 110
        assert MusicYorushika.query.count() == 112
        assert YorushikaRelease.query.count() == 22
        assert YorushikaReleaseTrack.query.count() == 124
        sunny = MusicYorushika.query.filter_by(slug="haru").one()
        assert sunny.id == 1
        assert sunny.album_title == "晴る"
        assert sunny.track_number == 1
        extra = MusicYorushika.query.filter_by(title="Legacy extra").one()
        assert extra.is_featured is False


def test_release_normalization_downgrade_keeps_legacy_track_data(tmp_path):
    application = _migration_app(tmp_path / "downgrade.sqlite3")

    with application.app_context():
        upgrade(directory="migrations")
        sync_catalog()
        track_count = MusicYorushika.query.count()

        downgrade(revision="20260728_0002", directory="migrations")

        tables = set(sa.inspect(db.engine).get_table_names())
        assert "yorushika_release" not in tables
        assert "yorushika_release_track" not in tables
        assert MusicYorushika.query.count() == track_count == 111
