#!/bin/bash

# Enable strict error handling
set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error
set -o pipefail  # Ensure pipelines fail on first failing command

# # Define variables
APP_DIR="/app"
# LOG_FILE="/var/log/titiler.log"
# ERROR_LOG_FILE="/var/log/titiler_error.log"
HOST="${TITILER_HOST:-0.0.0.0}"
PORT="${TITILER_PORT:-8000}"
ROOT_PATH="${TITILER_ROOT_PATH:-/}"
WORKERS=$(( $(nproc) * 2 + 1 ))
#UVICORN_CMD="uvicorn titiler.application.main:app --host $HOST --port $PORT --workers $WORKERS --root-path $ROOT_PATH --proxy-headers --forwarded-allow-ips='*' "

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1 "
}

# Change to the application directory
cd "$APP_DIR"

cat << "EOF"
  ______   __     ______   __     __         ______     ______
/\__  _\ /\ \   /\__  _\ /\ \   /\ \       /\  ___\   /\  == \
\/_/\ \/ \ \ \  \/_/\ \/ \ \ \  \ \ \____  \ \  __\   \ \  __<
    \ \_\  \ \_\    \ \_\  \ \_\  \ \_____\  \ \_____\  \ \_\ \_\
    \/_/   \/_/     \/_/   \/_/   \/_____/   \/_____/   \/_/ /_/
EOF

# Start Uvicorn server and log outputs
log_message "Starting TiTiler service..."
log_message "Configuration: HOST=$HOST -- PORT=$PORT WORKERS=$WORKERS"
log_message "Configuration: ROOT_PATH=$ROOT_PATH"
log_message "Configuration: "
# exec $UVICORN_CMD >>"$LOG_FILE" 2>>"$ERROR_LOG_FILE"

# Execute uvicorn directly (don't use variable)
exec uvicorn titiler.application.main:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers "$WORKERS" \
    --root-path "$ROOT_PATH" \
    --proxy-headers \
    --forwarded-allow-ips '*'
