import pytest

from config import load_runtime_config


def _set_required_environment(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "a-strong-test-secret-value")
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_USER", "music_user")
    monkeypatch.setenv("DB_PASSWORD", "test password/with symbols")
    monkeypatch.setenv("DB_NAME", "music_hub")


def test_runtime_config_encodes_database_password_and_hardens_pool(monkeypatch):
    _set_required_environment(monkeypatch)

    config = load_runtime_config()

    assert "test+password%2Fwith+symbols" in config["SQLALCHEMY_DATABASE_URI"]
    assert config["SQLALCHEMY_ENGINE_OPTIONS"] == {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }
    assert config["SESSION_COOKIE_HTTPONLY"] is True
    assert config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert "81.68.72.245" in config["TRUSTED_HOSTS"]


def test_runtime_config_rejects_missing_required_value(monkeypatch):
    _set_required_environment(monkeypatch)
    monkeypatch.delenv("DB_NAME")

    with pytest.raises(RuntimeError, match="DB_NAME"):
        load_runtime_config()
