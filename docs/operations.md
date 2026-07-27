# Operations Guide

## Runtime Baseline

- Entry: `http://81.68.72.245/`
- Access boundary: localhost and Tian's current public IPv4 only
- Reverse proxy: `Nginx`
- App server: `Gunicorn + Flask`
- App service: `musichub.service`
- Radio service: `yorushika-radio.service`
- App path: `/var/www/My_Homepage`
- HLS runtime path: `/run/yorushika-radio/hls`

The retired `music.yoruming.cn` DNS and HTTPS entry are not part of the current runtime.

## Persistent Radio Design

`yorushika-radio.service` performs the full startup sequence:

1. Creates `/run/yorushika-radio/` through systemd `RuntimeDirectory`.
2. Runs `scripts/generate_radio_schedule.py`.
3. Builds a deterministic FFmpeg concat playlist from the server's local MP3 collection.
4. Probes the real duration of each track and writes `radio-schedule.json`.
5. Starts an audio-only FFmpeg HLS stream.
6. Regenerates runtime files after service restart or server reboot.

The repository intentionally excludes the MP3 collection, generated HLS segments, `.env`, databases, uploads, and virtual environments.

## Install Versioned Runtime Configuration

```bash
cd /var/www/My_Homepage

sudo install -m 0644 deploy/systemd/musichub.service \
  /etc/systemd/system/musichub.service
sudo install -m 0644 deploy/systemd/yorushika-radio.service \
  /etc/systemd/system/yorushika-radio.service
sudo install -m 0644 deploy/nginx/musichub-ip.conf \
  /etc/nginx/conf.d/musichub-ip.conf

sudo systemctl daemon-reload
sudo nginx -t
sudo systemctl enable --now yorushika-radio.service
sudo systemctl enable --now musichub.service
sudo systemctl reload nginx
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

The existing `scripts/deploy_music_hub.sh` keeps `.env`, `venv/`, uploads, and local avatar state. It now restarts both persistent Music Hub services and checks the local IP-based Nginx route.

Before deploying, keep an external rollback point or a known-good Git commit. The Git repository covers source and deployment configuration, not the MP3 collection, databases, uploads, or complete server state.
