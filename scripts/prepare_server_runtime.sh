#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="${APP_DIR:-/var/www/My_Homepage}"
LEGACY_RADIO_DIR="${LEGACY_RADIO_DIR:-/root/projects/archived/Yorushika-24h-Radio/assets/music}"
RADIO_MUSIC_DIR="${RADIO_MUSIC_DIR:-/srv/media/yorushika-radio/music}"
MYSQL_BACKUP_DIR="${MYSQL_BACKUP_DIR:-/var/backups/music-hub/mysql}"
RELEASE_BACKUP_DIR="${RELEASE_BACKUP_DIR:-/var/backups/music-hub/releases}"
MONITOR_STATE_DIR="${MONITOR_STATE_DIR:-/var/lib/music-hub-monitor}"
LEGACY_NGINX_CONF="${LEGACY_NGINX_CONF:-/etc/nginx/conf.d/musichub-ip.conf}"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Run this one-time preparation script as root." >&2
  exit 1
fi

for user_name in musichub musichub-radio; do
  if ! getent group "${user_name}" >/dev/null 2>&1; then
    groupadd --system "${user_name}"
  fi
  if ! id "${user_name}" >/dev/null 2>&1; then
    useradd \
      --system \
      --gid "${user_name}" \
      --home-dir /nonexistent \
      --shell /usr/sbin/nologin \
      "${user_name}"
  fi
done

if [[ -f "${APP_DIR}/.env" ]]; then
  chown root:musichub "${APP_DIR}/.env"
  chmod 0640 "${APP_DIR}/.env"
fi

install -d -o root -g musichub-radio -m 0750 "${RADIO_MUSIC_DIR}"
if [[ -d "${LEGACY_RADIO_DIR}" ]]; then
  rsync -a --ignore-existing "${LEGACY_RADIO_DIR}/" "${RADIO_MUSIC_DIR}/"
fi
chown -R root:musichub-radio "${RADIO_MUSIC_DIR}"
find "${RADIO_MUSIC_DIR}" -type d -exec chmod 0750 {} +
find "${RADIO_MUSIC_DIR}" -type f -exec chmod 0640 {} +

install -d -o root -g root -m 0700 \
  "${MYSQL_BACKUP_DIR}" \
  "${RELEASE_BACKUP_DIR}"
install -d -o root -g adm -m 0750 "${MONITOR_STATE_DIR}"

install -m 0644 "${APP_DIR}/deploy/systemd/musichub.service" \
  /etc/systemd/system/musichub.service
install -m 0644 "${APP_DIR}/deploy/systemd/yorushika-radio.service" \
  /etc/systemd/system/yorushika-radio.service
install -m 0644 "${APP_DIR}/deploy/systemd/music-hub-health.service" \
  /etc/systemd/system/music-hub-health.service
install -m 0644 "${APP_DIR}/deploy/systemd/music-hub-health.timer" \
  /etc/systemd/system/music-hub-health.timer
install -m 0644 "${APP_DIR}/deploy/systemd/music-hub-backup.service" \
  /etc/systemd/system/music-hub-backup.service
install -m 0644 "${APP_DIR}/deploy/systemd/music-hub-backup.timer" \
  /etc/systemd/system/music-hub-backup.timer
install -m 0644 "${APP_DIR}/deploy/systemd/music-hub-failure@.service" \
  /etc/systemd/system/music-hub-failure@.service
install -d -m 0755 /etc/letsencrypt/renewal-hooks/deploy
install -m 0755 "${APP_DIR}/deploy/certbot/reload-nginx.sh" \
  /etc/letsencrypt/renewal-hooks/deploy/reload-nginx
if [[ -e "${LEGACY_NGINX_CONF}" ]]; then
  echo "Preserving existing server-local legacy IP allowlist: ${LEGACY_NGINX_CONF}"
else
  install -m 0644 "${APP_DIR}/deploy/nginx/musichub-ip.conf" \
    "${LEGACY_NGINX_CONF}"
fi
if [[ -r /etc/letsencrypt/live/radio.yoruming.cn/fullchain.pem \
  && -r /etc/letsencrypt/live/radio.yoruming.cn/privkey.pem \
  && -r /etc/nginx/.htpasswd-radio ]]; then
  install -m 0644 "${APP_DIR}/deploy/nginx/musichub-radio.conf" \
    /etc/nginx/conf.d/musichub-radio.conf
else
  echo "Skipping authenticated domain config: certificate or password hash is missing."
fi

systemctl daemon-reload
nginx -t
systemd-analyze verify \
  /etc/systemd/system/musichub.service \
  /etc/systemd/system/yorushika-radio.service \
  /etc/systemd/system/music-hub-health.service \
  /etc/systemd/system/music-hub-health.timer \
  /etc/systemd/system/music-hub-backup.service \
  /etc/systemd/system/music-hub-backup.timer \
  /etc/systemd/system/music-hub-failure@.service

echo "Preparation complete. No service was restarted."
echo "Reliability timers were installed but not enabled."
echo "Keep the legacy radio directory until browser playback is accepted."
