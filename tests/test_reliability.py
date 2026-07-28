import gzip
import io
import os
import pathlib
import tarfile

import pytest

from scripts import health_check, mysql_backup, release_snapshot


def test_health_check_covers_web_database_and_radio(monkeypatch):
    monkeypatch.setattr(health_check, "service_is_active", lambda _service: None)

    responses = {
        "/healthz": b'{"status":"ok"}',
        "/hls/yorushika.m3u8": b"#EXTM3U\nsegment-0001.ts\n",
        "/hls/radio-schedule.json": b'{"private":true,"tracks":[{"title":"Elma"}]}',
    }
    monkeypatch.setattr(
        health_check,
        "fetch",
        lambda _base_url, _host_header, path: responses[path],
    )

    result = health_check.run_checks(
        "http://127.0.0.1",
        "81.68.72.245",
        ("musichub.service", "yorushika-radio.service"),
    )

    assert result["status"] == "ok"
    assert result["failures"] == []
    assert result["checks"]["http:/healthz"] == "ok"
    assert result["checks"]["http:/hls/yorushika.m3u8"] == "ok"


def test_mysql_retention_only_deletes_managed_backup_names(tmp_path):
    managed = []
    for index in range(4):
        path = tmp_path / f"musichub-mysql-2026072{index}T032000Z.sql.gz"
        path.write_bytes(b"backup")
        path.with_name(f"{path.name}.sha256").write_text("checksum\n", encoding="ascii")
        os.utime(path, (index + 1, index + 1))
        managed.append(path)
    unrelated = tmp_path / "yorushika-mysql-all-20260728-115222.sql.gz"
    unrelated.write_bytes(b"manual")

    candidates = mysql_backup.prune_backups(tmp_path, keep=2, apply=True)

    assert {path.name for path in candidates} == {
        managed[0].name,
        managed[1].name,
    }
    assert all(not path.exists() for path in candidates)
    assert managed[2].exists()
    assert managed[3].exists()
    assert unrelated.exists()


def test_mysql_dump_validation_rejects_unrelated_gzip(tmp_path):
    valid = tmp_path / "valid.sql.gz"
    with gzip.open(valid, "wb") as output:
        output.write(b"-- MySQL dump 10.13\nCREATE TABLE example (id int);\n")
    mysql_backup.verify_gzip_dump(valid)

    invalid = tmp_path / "invalid.sql.gz"
    with gzip.open(invalid, "wb") as output:
        output.write(b"not a database backup")
    with pytest.raises(RuntimeError, match="does not look"):
        mysql_backup.verify_gzip_dump(invalid)


def test_mysql_client_values_are_quoted_for_temporary_option_file():
    assert mysql_backup.mysql_option_value('pa"ss\\word#1') == '"pa\\"ss\\\\word#1"'
    with pytest.raises(ValueError, match="control character"):
        mysql_backup.mysql_option_value("line1\nline2")


def test_release_snapshot_excludes_secrets_runtime_and_uploads(tmp_path):
    app_dir = tmp_path / "app"
    backup_dir = tmp_path / "backups"
    app_dir.mkdir()
    (app_dir / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (app_dir / ".env").write_text("DO_NOT_ARCHIVE=secret\n", encoding="utf-8")
    (app_dir / "venv").mkdir()
    (app_dir / "venv/bin").mkdir()
    (app_dir / "venv/bin/python").write_text("", encoding="utf-8")
    uploads = app_dir / "static/uploads"
    uploads.mkdir(parents=True)
    (uploads / "private.png").write_bytes(b"private")

    result = release_snapshot.create_snapshot(
        app_dir=app_dir,
        backup_dir=backup_dir,
        keep=5,
        prune_mode="report",
        state_file=tmp_path / "state.json",
    )

    with tarfile.open(result["snapshot"], "r:gz") as archive:
        names = archive.getnames()
    assert "app/app.py" in names
    assert "app/.env" not in names
    assert not any(name.startswith("app/venv") for name in names)
    assert not any(name.startswith("app/static/uploads") for name in names)


def test_snapshot_validation_rejects_path_traversal(tmp_path):
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    snapshot = backup_dir / "predeploy-20260728T032000Z-abcdef0.tar.gz"
    with tarfile.open(snapshot, "w:gz") as archive:
        member = tarfile.TarInfo(name="../../escape")
        member.size = 4
        archive.addfile(member, io.BytesIO(b"oops"))
    snapshot.with_name(f"{snapshot.name}.json").write_text(
        '{"sha256":"' + release_snapshot.sha256_file(snapshot) + '"}\n',
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="unsafe snapshot member"):
        release_snapshot.validate_snapshot(snapshot, backup_dir)


def test_deployed_version_state_round_trips_without_configuration(tmp_path):
    state_file = tmp_path / "monitor/deployed-version.json"
    release_snapshot.record_deployed_version(
        state_file=state_file,
        commit="a" * 40,
        branch="codex/musichub-hardening",
        source="test",
    )

    assert release_snapshot.load_deployed_version(state_file) == (
        "a" * 40,
        "codex/musichub-hardening",
    )
    assert state_file.stat().st_mode & 0o777 == 0o640
