#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="${APP_DIR:-/var/www/My_Homepage}"
SERVICE_NAME="${SERVICE_NAME:-musichub.service}"
RADIO_SERVICE_NAME="${RADIO_SERVICE_NAME:-yorushika-radio.service}"
HOST_HEADER="${HOST_HEADER:-81.68.72.245}"
BRANCH="${BRANCH:-codex/yorushika-redesign-prototype}"
REPO_URL="${REPO_URL:-https://github.com/Yorushikamimimi/Music-Hub.git}"
TMP_DIR="${TMP_DIR:-/tmp/music-hub-release}"
BACKUP_ROOT="${BACKUP_ROOT:-/var/backups/music-hub}"
RELEASE_BACKUP_DIR="${RELEASE_BACKUP_DIR:-${BACKUP_ROOT}/releases}"
MYSQL_BACKUP_DIR="${MYSQL_BACKUP_DIR:-${BACKUP_ROOT}/mysql}"
BACKUP_SERVICE_NAME="${BACKUP_SERVICE_NAME:-music-hub-backup.service}"
DEPLOY_STATE_FILE="${DEPLOY_STATE_FILE:-/var/lib/music-hub-monitor/deployed-version.json}"
RELEASE_KEEP="${RELEASE_KEEP:-5}"
MYSQL_KEEP="${MYSQL_KEEP:-14}"

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
need_cmd docker
need_cmd gzip
need_cmd python3

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

log "Start deploy: repo=${REPO_URL}, branch=${BRANCH}"
for attempt in 1 2 3; do
  rm -rf "${TMP_DIR}"
  log "Clone attempt ${attempt}/3 (HTTP/1.1)"
  if git -c http.version=HTTP/1.1 clone \
    --depth 1 \
    --branch "${BRANCH}" \
    "${REPO_URL}" \
    "${TMP_DIR}"; then
    break
  fi

  if [[ "${attempt}" -eq 3 ]]; then
    echo "Unable to clone ${REPO_URL} after 3 attempts" >&2
    exit 1
  fi

  sleep "$((attempt * 3))"
done
source_commit="$(git -C "${TMP_DIR}" rev-parse --verify HEAD)"

log "Prepare app and backup directories"
${SUDO} mkdir -p "${APP_DIR}" "${RELEASE_BACKUP_DIR}" "${MYSQL_BACKUP_DIR}"

if [[ -n "$(${SUDO} find "${APP_DIR}" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
  log "Create a complete pre-deploy code snapshot"
  ${SUDO} python3 "${TMP_DIR}/scripts/release_snapshot.py" create \
    --app-dir "${APP_DIR}" \
    --backup-dir "${RELEASE_BACKUP_DIR}" \
    --keep "${RELEASE_KEEP}" \
    --prune apply
fi

log "Sync code to ${APP_DIR}"
${SUDO} rsync -a --delete \
  --exclude ".git/" \
  --exclude "venv/" \
  --exclude "__pycache__/" \
  --exclude "${KEEP_ENV_FILE}" \
  --exclude "static/uploads/" \
  --exclude "current_avatar.txt" \
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

log "Create a verified pre-migration MySQL backup"
if ${SUDO} systemctl cat "${BACKUP_SERVICE_NAME}" >/dev/null 2>&1; then
  ${SUDO} systemctl start "${BACKUP_SERVICE_NAME}"
else
  ${SUDO} python3 "${APP_DIR}/scripts/mysql_backup.py" backup \
    --backup-dir "${MYSQL_BACKUP_DIR}" \
    --keep "${MYSQL_KEEP}" \
    --prune apply
fi

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
${SUDO} python3 "${APP_DIR}/scripts/health_check.py" \
  --host-header "${HOST_HEADER}"

log "Record the deployed commit after successful health checks"
${SUDO} python3 "${APP_DIR}/scripts/release_snapshot.py" record \
  --commit "${source_commit}" \
  --branch "${BRANCH}" \
  --state-file "${DEPLOY_STATE_FILE}"

log "Deploy finished"
log "Release snapshots: ${RELEASE_BACKUP_DIR}"
log "MySQL backups: ${MYSQL_BACKUP_DIR}"
