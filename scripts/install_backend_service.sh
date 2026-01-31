#!/usr/bin/env bash
# Install OpenFlux backend as a macOS user LaunchAgent (starts at login).
# Run from the OpenFlux repo root. Uninstall: launchctl unload ~/Library/LaunchAgents/com.vibecoders.openflux.backend.plist

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PLIST_ID="com.vibecoders.openflux.backend"
PLIST_NAME="$PLIST_ID.plist"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
PLIST_PATH="$LAUNCH_AGENTS/$PLIST_NAME"
LOG_DIR="$HOME/Library/Logs/OpenFlux"
VENV_PYTHON="$REPO_ROOT/venv/bin/python"

cd "$REPO_ROOT"

# Ensure venv exists
if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
  "$REPO_ROOT/venv/bin/pip" install -r requirements.txt
fi

mkdir -p "$LOG_DIR"

# Build path to uvicorn (same venv)
UVICORN="$REPO_ROOT/venv/bin/uvicorn"
if [[ ! -x "$UVICORN" ]]; then
  echo "Installing dependencies..."
  "$REPO_ROOT/venv/bin/pip" install -r requirements.txt
fi

# Create plist
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$PLIST_ID</string>
  <key>ProgramArguments</key>
  <array>
    <string>$VENV_PYTHON</string>
    <string>-m</string>
    <string>uvicorn</string>
    <string>core.api.server:app</string>
    <string>--host</string>
    <string>127.0.0.1</string>
    <string>--port</string>
    <string>8000</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$REPO_ROOT</string>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$LOG_DIR/backend.log</string>
  <key>StandardErrorPath</key>
  <string>$LOG_DIR/backend.err.log</string>
</dict>
</plist>
EOF

# Unload if already loaded
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"

echo "OpenFlux backend service installed."
echo "  Plist: $PLIST_PATH"
echo "  Logs:  $LOG_DIR/"
echo "  URL:   http://localhost:8000"
echo ""
echo "To stop:  launchctl unload $PLIST_PATH"
echo "To start: launchctl load $PLIST_PATH"
