#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIDFILE="$ROOT/data/x4-beast.pid"

if [[ ! -f "$PIDFILE" ]]; then
  echo "No PID file found — X4 BEAST does not appear to be running."
  exit 0
fi

PID=$(cat "$PIDFILE")
if kill -0 "$PID" 2>/dev/null; then
  echo "Stopping X4 BEAST (PID $PID)..."
  kill "$PID"
  sleep 1
  if kill -0 "$PID" 2>/dev/null; then
    kill -9 "$PID"
  fi
  echo "Stopped."
else
  echo "Process $PID is not running."
fi

rm -f "$PIDFILE"
