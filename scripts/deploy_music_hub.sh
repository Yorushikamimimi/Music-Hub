#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="${APP_DIR:-/var/www/My_Homepage}"
SERVICE_NAME="${SERVICE_NAME:-musichub.service}"
RADIO_SERVICE_NAME="${RADIO_SERVICE_NAME:-yorushika-radio.service}"
HOST_HEADER="${HOST_HEADER:-81.68.72.245}"
BRANCH="${BRANCH:-main}"
REPO_URL="${REPO_URL:-https://github.com/Yorushikamimimi/Music-Hub.git}"
TMP_DIR="${TMP_DIR:-/tmp/music-hub-release}"
BACKUP_ROOT="${BACKUP_ROOT:-/var/backups/music-hub}"

KEEP_ENV_FILE="${KEEP_ENV_FILE:-.env}"
if [[ "$(id -u)" -eq 0 ]]; then
  SUDO=""
else
  SUDO="sudo"
fi

log() {
  echo "[$(date '+%F %T')] $*"
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing command: $1" >&2
    exit 1
  }
}

need_cmd git
need_cmd rsync
need_cmd curl

ts="$(date '+%F_%H%M%S')"
backup_dir="${BACKUP_ROOT}/${ts}"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

log "Start deploy: repo=${REPO_URL}, branch=${BRANCH}"
rm -rf "${TMP_DIR}"
git clone --depth 1 --branch "${BRANCH}" "${REPO_URL}" "${TMP_DIR}"

log "Prepare app and backup directories"
${SUDO} mkdir -p "${APP_DIR}" "${backup_dir}"

log "Sync code to ${APP_DIR}"
${SUDO} rsync -a --delete \
  --exclude ".git/" \
  --exclude "venv/" \
  --exclude "__pycache__/" \
  --exclude "${KEEP_ENV_FILE}" \
  --backup --backup-dir="${backup_dir}" \
  "${TMP_DIR}/" "${APP_DIR}/"

if [[ ! -x "${APP_DIR}/venv/bin/pip" ]]; then
  log "Create venv because ${APP_DIR}/venv not found"
  ${SUDO} python3 -m venv "${APP_DIR}/venv"
fi

log "Install dependencies"
${SUDO} "${APP_DIR}/venv/bin/pip" install \
  --require-hashes \
  -r "${APP_DIR}/requirements.txt"

log "Run compile check"
${SUDO} "${APP_DIR}/venv/bin/python" -m compileall -q "${APP_DIR}"

log "Apply additive database migrations"
(
  cd "${APP_DIR}"
  ${SUDO} "${APP_DIR}/venv/bin/flask" --app wsgi:app db upgrade
)

log "Synchronize the curated catalog"
(
  cd "${APP_DIR}"
  ${SUDO} "${APP_DIR}/venv/bin/flask" --app wsgi:app catalog-sync
)

log "Restart service ${SERVICE_NAME}"
${SUDO} systemctl restart "${SERVICE_NAME}"
${SUDO} systemctl is-active --quiet "${SERVICE_NAME}"

if ${SUDO} systemctl cat "${RADIO_SERVICE_NAME}" >/dev/null 2>&1; then
  log "Restart radio service ${RADIO_SERVICE_NAME}"
  ${SUDO} systemctl restart "${RADIO_SERVICE_NAME}"
  ${SUDO} systemctl is-active --quiet "${RADIO_SERVICE_NAME}"
fi

log "Run local health check (Nginx -> Gunicorn)"
curl -fsS -I -H "Host: ${HOST_HEADER}" http://127.0.0.1 >/dev/null
curl -fsS -I -H "Host: ${HOST_HEADER}" http://127.0.0.1/radio >/dev/null
curl -fsS -I -H "Host: ${HOST_HEADER}" http://127.0.0.1/hls/yorushika.m3u8 >/dev/null

log "Deploy finished"
log "Incremental backup path: ${backup_dir}"
