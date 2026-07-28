from pathlib import Path


def test_web_service_can_read_private_environment_and_share_socket():
    unit = Path("deploy/systemd/musichub.service").read_text(encoding="utf-8")

    assert "User=musichub" in unit
    assert "Group=www-data" in unit
    assert "SupplementaryGroups=musichub" in unit
    assert "--umask 007" in unit
    assert "--no-control-socket" in unit
    assert "ExecStart=/usr/bin/env RADIO_STREAM_URL=/hls/yorushika.m3u8" in unit


def test_radio_restarts_after_a_clean_playlist_completion():
    unit = Path("deploy/systemd/yorushika-radio.service").read_text(encoding="utf-8")

    assert "Restart=always" in unit
    assert "Restart=on-failure" not in unit
    assert "-stream_loop" not in unit


def test_reliability_units_have_timers_failure_recording_and_narrow_paths():
    health = Path("deploy/systemd/music-hub-health.service").read_text(
        encoding="utf-8"
    )
    health_timer = Path("deploy/systemd/music-hub-health.timer").read_text(
        encoding="utf-8"
    )
    backup = Path("deploy/systemd/music-hub-backup.service").read_text(
        encoding="utf-8"
    )
    backup_timer = Path("deploy/systemd/music-hub-backup.timer").read_text(
        encoding="utf-8"
    )
    failure = Path("deploy/systemd/music-hub-failure@.service").read_text(
        encoding="utf-8"
    )

    assert "OnFailure=music-hub-failure@%n.service" in health
    assert "scripts/health_check.py" in health
    assert "OnUnitActiveSec=5min" in health_timer
    assert "scripts/mysql_backup.py backup --keep 14 --prune apply" in backup
    assert "EnvironmentFile=/var/www/My_Homepage/.env" in backup
    assert "ReadWritePaths=/var/backups/music-hub/mysql" in backup
    assert "OnCalendar=*-*-* 03:20:00" in backup_timer
    assert "scripts/record_unit_failure.py %i" in failure
    assert "ReadWritePaths=/var/lib/music-hub-monitor" in failure


def test_deploy_creates_recovery_points_and_preserves_runtime_data():
    deploy = Path("scripts/deploy_music_hub.sh").read_text(encoding="utf-8")

    assert 'BRANCH="${BRANCH:-codex/yorushika-redesign-prototype}"' in deploy
    assert "for attempt in 1 2 3" in deploy
    assert "git -c http.version=HTTP/1.1 clone" in deploy
    assert "Unable to clone ${REPO_URL} after 3 attempts" in deploy
    assert "release_snapshot.py\" create" in deploy
    assert 'systemctl start "${BACKUP_SERVICE_NAME}"' in deploy
    assert "mysql_backup.py\" backup" in deploy
    assert "health_check.py" in deploy
    assert 'HEALTH_CHECK_ATTEMPTS="${HEALTH_CHECK_ATTEMPTS:-6}"' in deploy
    assert 'HEALTH_CHECK_DELAY_SECONDS="${HEALTH_CHECK_DELAY_SECONDS:-3}"' in deploy
    assert "while true; do" in deploy
    assert (
        "Health check did not pass after ${HEALTH_CHECK_ATTEMPTS} attempts"
        in deploy
    )
    assert 'sleep "${HEALTH_CHECK_DELAY_SECONDS}"' in deploy
    assert "release_snapshot.py\" record" in deploy
    assert '--exclude "static/uploads/"' in deploy
    assert '--exclude "current_avatar.txt"' in deploy
    assert "--backup-dir=" not in deploy


def test_preparation_installs_but_does_not_enable_reliability_timers():
    preparation = Path("scripts/prepare_server_runtime.sh").read_text(
        encoding="utf-8"
    )

    assert "music-hub-health.timer" in preparation
    assert "music-hub-backup.timer" in preparation
    assert "music-hub-failure@.service" in preparation
    assert "systemctl enable" not in preparation
    assert "systemctl restart" not in preparation
