# Operations Guide

## Runtime Baseline
- Domain: `music.yoruming.cn`
- Reverse proxy: `Nginx`
- App server: `Gunicorn + Flask`
- Service name: `yorushika-web`
- App path: `/var/www/My_Homepage`

## Deployment (Recommended)
### A) Default path (stable on weak network): local package + SCP
```powershell
# Local Windows
cd D:\Workspace\My_Homepage
git archive --format=tar.gz -o Music-Hub-main.tar.gz HEAD
scp .\Music-Hub-main.tar.gz root@<SERVER_IP>:/tmp/
```

```bash
# Server Linux
rm -rf /tmp/music-hub-release && mkdir -p /tmp/music-hub-release
tar --warning=no-unknown-keyword -xzf /tmp/Music-Hub-main.tar.gz -C /tmp/music-hub-release
sudo rsync -a --delete \
  --exclude ".env" \
  --exclude "venv/" \
  --exclude "static/uploads/" \
  --exclude "current_avatar.txt" \
  /tmp/music-hub-release/ /var/www/My_Homepage/
sudo systemctl restart yorushika-web
```

### B) One-click script (when server can access GitHub smoothly)
```bash
cd /var/www/My_Homepage
chmod +x scripts/deploy_music_hub.sh
./scripts/deploy_music_hub.sh
```

## Ops Command Cheat Sheet
```bash
# Service status
sudo systemctl status yorushika-web --no-pager

# Start / Stop / Restart
sudo systemctl start yorushika-web
sudo systemctl stop yorushika-web
sudo systemctl restart yorushika-web

# Enable / Disable on boot
sudo systemctl enable yorushika-web
sudo systemctl disable yorushika-web

# Logs
sudo journalctl -u yorushika-web -f
sudo journalctl -u yorushika-web -n 120 --no-pager

# Nginx check and reload
sudo nginx -t
sudo systemctl reload nginx

# Health checks
curl -Ik https://music.yoruming.cn
curl -I -H "Host: music.yoruming.cn" http://127.0.0.1
```

## Maintenance / Stop Site
### Temporary maintenance
```bash
sudo systemctl stop yorushika-web
# Optional full stop (including gateway):
# sudo systemctl stop nginx
```

### Resume service
```bash
sudo systemctl start yorushika-web
sudo systemctl status yorushika-web --no-pager
curl -Ik https://music.yoruming.cn
```

## Hotfix (single file)
```powershell
# Local: upload one changed file
scp .\templates\radio.html root@<SERVER_IP>:/var/www/My_Homepage/templates/radio.html
```

```bash
# Server: restart and verify
sudo systemctl restart yorushika-web
curl -I https://music.yoruming.cn/radio
```

## Post-change Validation
1. `/` `/search` `/lyrics` `/radio` `/about` all return `200`.
2. `yorushika-web` is `active (running)`.
3. Browser hard refresh shows latest page content.
