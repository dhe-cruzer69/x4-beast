#!/usr/bin/env bash
# Install X4 BEAST as a systemd service (run with sudo)
set -euo pipefail

INSTALL_DIR="${1:-/opt/x4-beast}"
SERVICE_USER="${2:-x4}"

echo "→ Installing X4 BEAST to $INSTALL_DIR"

# Create user if needed
if ! id "$SERVICE_USER" &>/dev/null; then
  useradd --system --home-dir "$INSTALL_DIR" --shell /usr/sbin/nologin "$SERVICE_USER"
fi

# Copy files
mkdir -p "$INSTALL_DIR"
cp -a . "$INSTALL_DIR/"
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"

# Create venv + install
sudo -u "$SERVICE_USER" bash -c "
  cd $INSTALL_DIR
  python3 -m venv .venv
  .venv/bin/pip install -e .
"

# Install service
cp deploy/x4-beast.service /etc/systemd/system/
sed -i "s|/opt/x4-beast|$INSTALL_DIR|g" /etc/systemd/system/x4-beast.service
sed -i "s|User=x4|User=$SERVICE_USER|g" /etc/systemd/system/x4-beast.service
sed -i "s|Group=x4|Group=$SERVICE_USER|g" /etc/systemd/system/x4-beast.service

systemctl daemon-reload
systemctl enable --now x4-beast

echo "✓ X4 BEAST installed and started"
echo "  Status: systemctl status x4-beast"
echo "  Logs:   journalctl -u x4-beast -f"
