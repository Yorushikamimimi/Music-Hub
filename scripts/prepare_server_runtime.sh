#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="${APP_DIR:-/var/www/My_Homepage}"
LEGACY_RADIO_DIR="${LEGACY_RADIO_DIR:-/root/projects/archived/Yorushika-24h-Radio/assets/music}"
RADIO_MUSIC_DIR="${RADIO_MUSIC_DIR:-/srv/media/yorushika-radio/music}"

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

install -m 0644 "${APP_DIR}/deploy/systemd/musichub.service" \
  /etc/systemd/system/musichub.service
install -m 0644 "${APP_DIR}/deploy/systemd/yorushika-radio.service" \
  /etc/systemd/system/yorushika-radio.service
install -m 0644 "${APP_DIR}/deploy/nginx/musichub-ip.conf" \
  /etc/nginx/conf.d/musichub-ip.conf

systemctl daemon-reload
nginx -t

echo "Preparation complete. No service was restarted."
echo "Keep the legacy radio directory until browser playback is accepted."
