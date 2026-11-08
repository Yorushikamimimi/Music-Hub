import datetime
import io
import json

import pytest

from app import create_app, is_new_release
from catalog_service import sync_catalog
from models import db
from routes import local_studio
from routes.local_studio import normalize_title

MEDIA = "a" * 32


@pytest.fixture()
def studio_client(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key-only",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'studio.sqlite3'}",
            "STUDIO_URL": "http://studio.test",
        }
    )
    with application.app_context():
        db.create_all()
        sync_catalog()
    yield application.test_client()
    with application.app_context():
        db.session.remove()
        db.drop_all()


class _Resp(io.BytesIO):
    def __init__(self, body, kind="application/json"):
        super().__init__(body)
        self.headers = type("H", (), {"get_content_type": lambda _self: kind})()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@pytest.fixture(autouse=True)
def _fresh_cache():
    local_studio._cache.clear()
    yield
    local_studio._cache.clear()


def _fake_studio(monkeypatch, items):
    def fake_urlopen(url, timeout):
        if url.endswith("/api/showcase"):
            return _Resp(json.dumps({"items": items}).encode())
        return _Resp(b"\x89PNG", "image/png")

    monkeypatch.setattr(local_studio.urllib.request, "urlopen", fake_urlopen)


def test_new_release_window_is_thirty_days():
    day = datetime.date(2026, 10, 14)
    assert is_new_release(day, today=datetime.date(2026, 11, 8))
    assert is_new_release(day, today=datetime.date(2026, 11, 13))
    assert not is_new_release(day, today=datetime.date(2026, 11, 14))
    assert not is_new_release(day, today=datetime.date(2026, 10, 13))
    assert not is_new_release(None)


def test_normalize_title_ignores_width_case_and_spaces_but_not_scene_labels():
    assert normalize_title("ＡＢＣ　春泥棒") == normalize_title("abc春泥棒")
    assert normalize_title("盗作 · 舞台剪影") != normalize_title("盗作")


def test_studio_routes_are_off_without_studio_url(client):
    assert client.get("/local/studio/frames/spring-thief").status_code == 404
    assert client.get(f"/local/studio/media/{MEDIA}").status_code == 404
    assert b"data-studio-frames" not in client.get("/songs/spring-thief").data


def test_frames_match_song_title_and_link_back_to_studio(studio_client, monkeypatch):
    _fake_studio(
        monkeypatch,
        [
            {"id": "c1", "title": "春泥棒", "source_label": "第 3 场", "timecode": "01:24",
             "thumbnail": f"/media/{MEDIA}", "lyric": "  一句  "},
            {"id": "c2", "title": "盗作 · 舞台剪影", "thumbnail": f"/media/{MEDIA}"},
            {"id": "c3", "title": "春泥棒", "thumbnail": "https://elsewhere/x.png"},
        ],
    )
    data = studio_client.get("/local/studio/frames/spring-thief").get_json()
    assert data["online"] is True
    assert [f["id"] for f in data["frames"]] == ["c1"]
    frame = data["frames"][0]
    assert frame["lyric"] == "一句"
    assert frame["image"] == f"/local/studio/media/{MEDIA}"
    assert frame["href"] == "http://studio.test/#c=c1&v=c1"
    assert b"data-studio-frames" in studio_client.get("/songs/spring-thief").data


def test_frames_report_offline_when_studio_is_down(studio_client, monkeypatch):
    def down(url, timeout):
        raise OSError("refused")

    monkeypatch.setattr(local_studio.urllib.request, "urlopen", down)
    data = studio_client.get("/local/studio/frames/spring-thief").get_json()
    assert data == {"online": False, "frames": []}


def test_media_proxy_only_passes_images(studio_client, monkeypatch):
    _fake_studio(monkeypatch, [])
    resp = studio_client.get(f"/local/studio/media/{MEDIA}")
    assert resp.status_code == 200 and resp.mimetype == "image/png"
    assert studio_client.get("/local/studio/media/not-hex").status_code == 404


def test_song_by_title_redirects_to_song_or_search(client):
    resp = client.get("/songs/by-title", query_string={"t": "春泥棒"})
    assert resp.status_code == 302 and resp.headers["Location"].endswith("/songs/spring-thief")
    resp = client.get("/songs/by-title", query_string={"t": "不存在的歌"})
    assert "/search" in resp.headers["Location"]


def test_home_shows_new_release_strip_while_new(client, monkeypatch):
    import app as app_module

    real = app_module.is_new_release
    monkeypatch.setitem(
        client.application.jinja_env.globals,
        "is_new_release",
        lambda d, today=None: real(d, today=datetime.date(2026, 11, 8)),
    )
    page = client.get("/").get_data(as_text=True)
    assert "release-new-strip" in page and "雲を抜け風下へ私だけ" in page
    monkeypatch.setitem(
        client.application.jinja_env.globals,
        "is_new_release",
        lambda d, today=None: real(d, today=datetime.date(2027, 1, 1)),
    )
    assert "release-new-strip" not in client.get("/").get_data(as_text=True)


def test_songs_endpoint_counts_frames_per_song(studio_client, monkeypatch):
    _fake_studio(
        monkeypatch,
        [
            {"id": "c1", "title": "春泥棒", "thumbnail": f"/media/{MEDIA}"},
            {"id": "c2", "title": "春泥棒", "thumbnail": f"/media/{MEDIA}"},
            {"id": "c3", "title": "夜行", "thumbnail": "/media/bad"},
        ],
    )
    data = studio_client.get("/local/studio/songs").get_json()
    assert data == {"online": True, "counts": {"spring-thief": 2}}
    assert b'data-studio-slug="spring-thief"' in studio_client.get("/discography").data


def test_list_tags_are_absent_without_studio(client):
    assert client.get("/local/studio/songs").status_code == 404
    assert b"data-studio-slug" not in client.get("/discography").data


def test_studio_routes_refuse_foreign_host(studio_client):
    for path in ("/local/studio/songs", f"/local/studio/media/{MEDIA}", "/local/studio/frames/haru-dorobou"):
        assert studio_client.get(path, headers={"Host": "evil.example"}).status_code == 403
        assert studio_client.get(path, headers={"Host": "evil.example:61705"}).status_code == 403
