import pytest

from app import create_app
from catalog_service import sync_catalog
from models import db


@pytest.fixture()
def app(tmp_path, monkeypatch):
    database_path = tmp_path / "music-hub-test.sqlite3"
    monkeypatch.setenv("RADIO_STATION_NAME", "Test Yorushika Radio")
    monkeypatch.setenv("RADIO_STREAM_URL", "/hls/yorushika.m3u8")

    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key-only",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SEND_FILE_MAX_AGE_DEFAULT": 0,
        }
    )

    with application.app_context():
        db.create_all()
        sync_catalog()

    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
