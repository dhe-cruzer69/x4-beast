#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Activate venv if present
if [[ -d .venv ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

# Ensure data dir
mkdir -p data

# Load .env if exists
if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

HOST="${X4_HOST:-127.0.0.1}"
PORT="${X4_PORT:-8787}"
LOG="data/x4-beast.log"
PIDFILE="data/x4-beast.pid"

if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "X4 BEAST is already running (PID $(cat "$PIDFILE"))"
  exit 0
fi

echo "Starting X4 BEAST on http://${HOST}:${PORT}"
nohup python -m x4_beast serve --host "$HOST" --port "$PORT" >> "$LOG" 2>&1 &
echo $! > "$PIDFILE"
echo "PID $(cat "$PIDFILE") — logs: $LOG"
echo "Stop with: ./scripts/stop.sh"
