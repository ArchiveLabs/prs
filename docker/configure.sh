#!/usr/bin/env bash

ENV_FILE="prs.env"

# Exit if the file already exists
if [ -f "$ENV_FILE" ]; then
  echo "$ENV_FILE already exists. No changes made."
  exit 0
fi

genpass() {
    len=${1:-32}
    dd if=/dev/urandom bs=1 count=$((len * 2)) 2>/dev/null | base64 | tr -dc 'A-Za-z0-9' | head -c "$len"
}

# Network specific env vars
HTTP_PROXY="${HTTP_PROXY:-}"
HTTPS_PROXY="${HTTPS_PROXY:-}"
NO_PROXY="${NO_PROXY:-archive.org,.archive.org}"
PIP_INDEX_URL="${PIP_INDEX_URL:-https://pypi.org/simple}"
APT_MIRROR="${APT_MIRROR:-}"

# Service specific env vars
PRS_HOST="${PRS_HOST:-0.0.0.0}"
PRS_PORT="${PRS_PORT:-8080}"
PRS_BASE_URL="${PRS_BASE_URL:-}"
PRS_WORKERS="${PRS_WORKERS:-1}"
PRS_LOG_LEVEL="${PRS_LOG_LEVEL:-debug}"
PRS_RELOAD="${PRS_RELOAD:-1}"

NEXT_PUBLIC_ENABLE_MANIFEST_ROUTE="${NEXT_PUBLIC_ENABLE_MANIFEST_ROUTE:-true}"
NEXT_PUBLIC_MANIFEST_FORCE_ENABLE="${NEXT_PUBLIC_MANIFEST_FORCE_ENABLE:-true}"
NODE_ENV="${NODE_ENV:-production}"

# Write to lenny.env
cat <<EOF > "$ENV_FILE"
# System Env
HTTP_PROXY=$HTTP_PROXY
HTTPS_PROXY=$HTTPS_PROXY
NO_PROXY=$NO_PROXY
PIP_INDEX_URL=$PIP_INDEX_URL
APT_MIRROR=$APT_MIRROR

# API App (FastAPI)
PRS_HOST=$PRS_HOST
PRS_PORT=$PRS_PORT
PRS_BASE_URL=$PRS_BASE_URL
PRS_WORKERS=$PRS_WORKERS
PRS_LOG_LEVEL=$PRS_LOG_LEVEL
PRS_RELOAD=$PRS_RELOAD

# Thorium web reader
NEXT_PUBLIC_ENABLE_MANIFEST_ROUTE=$NEXT_PUBLIC_ENABLE_MANIFEST_ROUTE
NEXT_PUBLIC_MANIFEST_FORCE_ENABLE=$NEXT_PUBLIC_MANIFEST_FORCE_ENABLE
NODE_ENV=$NODE_ENV

EOF
