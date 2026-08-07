# Operations Guide

## Current Runtime

- Entry: `http://81.68.72.245/`
- Access boundary: localhost and Tian's current public IPv4 only
- Reverse proxy: `Nginx`
- App server: `Gunicorn + Flask`
- App service: `musichub.service`
- Radio service: `yorushika-radio.service`
- App path: `/var/www/My_Homepage`
- App socket: `/run/musichub/musichub.sock`
- HLS runtime path: `/run/yorushika-radio/hls`
- Radio library: `/srv/media/yorushika-radio/music`
- Service identities: `musichub` and `musichub-radio` (no login shells)

The retired `music.yoruming.cn` DNS and HTTPS entry are not part of the current runtime.

## Persistent Radio Design

`yorushika-radio.service` performs the full startup sequence:

1. Creates `/run/yorushika-radio/` through systemd `RuntimeDirectory`.
2. Runs `scripts/generate_radio_schedule.py`.
3. Builds a deterministic FFmpeg concat playlist from 13 reviewed 2021 `Live「前世」` files.
4. Probes the real duration of each track and writes `radio-schedule.json`.
5. Starts an audio-only FFmpeg HLS stream.
6. Regenerates runtime files after service restart or server reboot.

The repository intentionally excludes the MP3 collection, generated HLS segments,
`.env`, databases and virtual environments. Unknown MP3 files are ignored.

Before and after every Radio library replacement, archive the complete MP3 directory,
copy it off the server, and verify a SHA-256 manifest. Git preserves the curated order,
display names and runtime code, but is not a backup for the audio bytes.

The stream is a private, IP-restricted personal listening tool. It does not
autoplay, expose a download feature, provide public indexing, or reproduce full lyrics.

## Runtime Preparation

```bash
cd /var/www/My_Homepage
sudo bash scripts/prepare_server_runtime.sh
```

This keeps the locked service users and Radio library permissions, creates dedicated
backup/monitor directories, installs the versioned unit/Nginx files, runs
`nginx -t` and `systemd-analyze verify`, and stops before restarting or enabling
anything. It limits `.env` to `root:musichub` mode `0640` without printing it.

Before activation, verify:

```bash
id musichub
id musichub-radio
sudo -u musichub-radio test -r /srv/media/yorushika-radio/music
systemd-analyze verify deploy/systemd/musichub.service
systemd-analyze verify deploy/systemd/yorushika-radio.service
systemd-analyze verify deploy/systemd/music-hub-health.service
systemd-analyze verify deploy/systemd/music-hub-health.timer
systemd-analyze verify deploy/systemd/music-hub-backup.service
systemd-analyze verify deploy/systemd/music-hub-backup.timer
systemd-analyze verify deploy/systemd/music-hub-failure@.service
```

When Tian's public IPv4 changes, update the `allow` line in the Nginx configuration before expecting remote access.

## Service Checks

```bash
systemctl status musichub.service --no-pager
systemctl status yorushika-radio.service --no-pager
systemctl is-enabled musichub.service yorushika-radio.service
journalctl -u musichub.service -n 100 --no-pager
journalctl -u yorushika-radio.service -n 100 --no-pager
```

## Health Checks

```bash
nginx -t
curl -I -H "Host: 81.68.72.245" http://127.0.0.1/
curl -I -H "Host: 81.68.72.245" http://127.0.0.1/radio
curl -I -H "Host: 81.68.72.245" http://127.0.0.1/hls/yorushika.m3u8
curl -I -H "Host: 81.68.72.245" http://127.0.0.1/hls/radio-schedule.json
python3 scripts/health_check.py
```

Browser acceptance should additionally prove:

1. Current track, approximate progress, and next track are populated.
2. Initial audio volume is `0.25`.
3. Playback advances with `readyState=4` and no media error.
4. Mobile layout has no horizontal overflow.
5. `https://yoruming.cn/` remains healthy because it is a separate project.

## Deployment

`scripts/deploy_music_hub.sh` keeps `.env`, `venv/`, uploads and the current
avatar; creates a complete pre-deploy code snapshot; installs hash-locked
dependencies; creates a verified pre-migration database backup; compiles the
app; applies additive migrations; synchronizes the catalog; restarts both
services; runs the full local health check; and records the commit that passed.

Because the script writes the database and restarts services, it requires an
explicit maintenance confirmation. Do not run it as a routine read-only check.

Before deploying, keep a known-good Git commit and the existing cloud snapshot.
Do not delete the legacy audio directory until live Radio playback is accepted.
The Git repository covers source and deployment configuration, not the MP3
collection, database or complete server state.

## Automated Health and Failure State

`music-hub-health.timer` runs every five minutes. The oneshot check proves:

1. `musichub.service`, `yorushika-radio.service` and `nginx.service` are active.
2. `/healthz` can execute a database query through the live Flask process.
3. The HLS playlist contains active media segments.
4. The Radio schedule remains private and contains tracks.

Run it manually before enabling the timer:

```bash
systemctl start music-hub-health.service
systemctl status music-hub-health.service --no-pager
journalctl -u music-hub-health.service -n 100 --no-pager
```

When the health or backup service fails, systemd starts
`music-hub-failure@.service`. The failure remains in journal and the latest
minimal status is written to:

```text
/var/lib/music-hub-monitor/last-failure.json
```

This is local error monitoring, not an off-server notification channel. It does
not send email, SMS or chat messages.

Production activation evidence before the Phase 3 catalog release:

- `music-hub-health.timer` and `music-hub-backup.timer` are enabled and waiting.
- A transient non-production failure invoked `music-hub-failure@.service`,
  produced the expected unit result, and was then cleaned up.
- The last recorded version before the Phase 3 catalog release was
  `04f9199a6bac071e2dfd372e11d0dd0392b118e2`.

## MySQL Backup and Restore Proof

systemd injects the existing protected application database variables into the
backup process. The script passes them to MySQL through a mode-`0600` temporary
option file inside the container, removes that file in `finally`, and never
prints the values or places them in command-line arguments. The dump is
compressed atomically, validated as a MySQL dump, hashed and stored with mode
`0600` under:

```text
/var/backups/music-hub/mysql/
```

The managed prefix is `musichub-mysql-*.sql.gz`. Retention keeps the newest
14 files and only deletes older files with that exact prefix in this dedicated
directory. The older manual backup under `/var/backups/mysql/` is outside this
scope and cannot be removed by the timer.

Manual proof before timer activation:

```bash
python3 scripts/mysql_backup.py backup --keep 14 --prune report
python3 scripts/mysql_backup.py verify \
  /var/backups/music-hub/mysql/<managed-backup>.sql.gz
```

`verify` starts a temporary MySQL 8 container with no published port or volume,
imports the dump, checks for `music_yorushika`, and removes the temporary
container. After one real restore proof passes, activate the scheduled job:

```bash
systemctl enable --now music-hub-backup.timer
systemctl list-timers music-hub-backup.timer --no-pager
```

The daily local backup is not an automatic off-server backup. Disk loss still
requires the separately maintained Mac copy or another off-host destination.

The first production proof created
`musichub-mysql-20260728T053055121496Z.sql.gz`, verified gzip and SHA-256
integrity, restored it in an isolated MySQL 8 container, found the
`music_yorushika` table, and removed the temporary container.

## Release Snapshots and Rollback

Each controlled deployment creates a complete code snapshot under:

```text
/var/backups/music-hub/releases/
```

Snapshots exclude `.env`, virtual environments, runtime caches, uploads and
avatar state. The newest five managed snapshots are retained. Each snapshot has
a checksum manifest and the deployed commit is recorded only after health checks
pass.

Rollback is dry-run-first:

```bash
python3 scripts/release_snapshot.py rollback \
  /var/backups/music-hub/releases/<snapshot>.tar.gz
```

The command above only prints the plan. Applying it requires an explicit flag:

```bash
python3 scripts/release_snapshot.py rollback \
  /var/backups/music-hub/releases/<snapshot>.tar.gz \
  --apply
```

An applied rollback first creates a safety snapshot, restores only application
code, preserves `.env`, `venv/`, uploads and reliability control scripts,
reinstalls locked dependencies, restarts Web and Radio, and checks the private
IP routes. It does not reverse database migrations; current migrations must
remain backward compatible or a separate confirmed database restore is needed.

## MySQL Network Boundary

The live MySQL container is published as `127.0.0.1:3306:3306`. The cloud
firewall still retains a server-self source rule, but the host no longer listens
for remote MySQL clients.

Changing the port binding requires a controlled container recreation with the
existing named volume and a user-supplied protected environment file. Do not
extract or print the running container's environment to reconstruct it. The
sequence must include a volume check, downtime notice, rollback container name,
local application query, and external port probe.
