from pathlib import Path


def test_web_service_can_read_private_environment_and_share_socket():
    unit = Path("deploy/systemd/musichub.service").read_text(encoding="utf-8")

    assert "User=musichub" in unit
    assert "Group=www-data" in unit
    assert "SupplementaryGroups=musichub" in unit
    assert "--umask 007" in unit
    assert "--no-control-socket" in unit
    assert "ExecStart=/usr/bin/env RADIO_STREAM_URL=/hls/yorushika.m3u8" in unit
