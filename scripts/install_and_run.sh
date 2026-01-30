#!/bin/bash
# One-command install + run: chains quick_start then start_server (background).
# Run from repo root: ./scripts/install_and_run.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

"$SCRIPT_DIR/quick_start.sh"
echo ""
echo "Starting backend in background..."
"$SCRIPT_DIR/start_server.sh" &
BACKEND_PID=$!
sleep 3
echo ""
echo "✅ OpenCode is ready."
echo "   Backend: http://localhost:8000 (PID $BACKEND_PID)"
echo "   Stop it: kill $BACKEND_PID"
echo "   Or run in foreground next time: ./scripts/start_server.sh"
echo "   See QUICKSTART.md for using the extension (F5 in the editor)."
