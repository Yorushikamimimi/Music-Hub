# Operations Guide

## Target Runtime

> This is the versioned target for the next controlled deployment. The live
> server continues to use the previous root services until that deployment is accepted.

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
3. Builds a deterministic FFmpeg concat playlist from 24 reviewed Yorushika files.
4. Probes the real duration of each track and writes `radio-schedule.json`.
5. Starts an audio-only FFmpeg HLS stream.
6. Regenerates runtime files after service restart or server reboot.

The repository intentionally excludes the MP3 collection, generated HLS segments,
`.env`, databases and virtual environments. Unknown MP3 files are ignored.

The stream is a private, IP-restricted personal listening tool. It does not
autoplay, expose a download feature, provide public indexing, or reproduce full lyrics.

## One-time Non-root Preparation

```bash
cd /var/www/My_Homepage
sudo bash scripts/prepare_server_runtime.sh
```

This creates locked service users, copies (without deleting) legacy audio into
`/srv/media/yorushika-radio/music`, limits `.env` to `root:musichub` with mode
`0640` without reading it, installs the target unit/Nginx files, runs `nginx -t`,
and stops before restarting anything.

Before activation, verify:

```bash
id musichub
id musichub-radio
sudo -u musichub-radio test -r /srv/media/yorushika-radio/music
systemd-analyze verify deploy/systemd/musichub.service
systemd-analyze verify deploy/systemd/yorushika-radio.service
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
```

Browser acceptance should additionally prove:

1. Current track, approximate progress, and next track are populated.
2. Initial audio volume is `0.25`.
3. Playback advances with `readyState=4` and no media error.
4. Mobile layout has no horizontal overflow.
5. `https://yoruming.cn/` remains healthy because it is a separate project.

## Deployment

`scripts/deploy_music_hub.sh` keeps `.env` and `venv/`, installs hash-locked
dependencies, compiles the app, applies the additive migration, synchronizes
the catalog, restarts both services, and checks the local Nginx route.

Because the script writes the database and restarts services, it requires an
explicit maintenance confirmation. Do not run it as a routine read-only check.

Before deploying, keep a known-good Git commit and the existing cloud snapshot.
Do not delete the legacy audio directory until live Radio playback is accepted.
The Git repository covers source and deployment configuration, not the MP3
collection, database or complete server state.

## MySQL Network Boundary

The current Docker port publication must not be described as localhost-only
until live inspection proves it. The preferred end state is a container
published as `127.0.0.1:3306:3306` plus no cloud firewall rule for 3306.

Changing the port binding requires a controlled container recreation with the
existing named volume and a user-supplied protected environment file. Do not
extract or print the running container's environment to reconstruct it. The
sequence must include a volume check, downtime notice, rollback container name,
local application query, and external port probe.
