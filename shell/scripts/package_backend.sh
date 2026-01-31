#!/usr/bin/env bash
# Package the OpenFlux Python backend into a standalone executable (Option A scaffolding).
# Run from repo root. Requires: Python venv with requirements.txt installed.
# Output: .build/openflux-backend/ (or OPENFLUX_BACKEND_DIST). To bundle with the app,
# copy contents into OpenFlux.app/Contents/Resources/backend/ (macOS) and have the IDE
# spawn the binary on launch (see docs/BACKEND.md and STANDALONE_IDE_ROADMAP.md).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUTPUT_DIR="${OPENFLUX_BACKEND_DIST:-$REPO_ROOT/.build/openflux-backend}"
VENV="$REPO_ROOT/venv"
ENTRY="$REPO_ROOT/scripts/run_backend_entry.py"

cd "$REPO_ROOT"

echo "=== Package OpenFlux backend (Option A scaffolding) ==="
echo "Repo root: $REPO_ROOT"
echo "Output:    $OUTPUT_DIR"
echo ""

# Ensure venv and deps
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "Creating venv and installing dependencies..."
  python3 -m venv venv
  "$VENV/bin/pip" install -r requirements.txt
fi

# PyInstaller
if ! "$VENV/bin/python" -c "import PyInstaller" 2>/dev/null; then
  echo "Installing PyInstaller..."
  "$VENV/bin/pip" install pyinstaller
fi

mkdir -p "$OUTPUT_DIR"

# Build one-folder bundle. PyInstaller traces from run_backend_entry.py; add hidden imports if needed.
# Run from repo root so core.* is discoverable.
cd "$REPO_ROOT"
"$VENV/bin/pyinstaller" \
  --clean \
  --noconfirm \
  --distpath "$OUTPUT_DIR/dist" \
  --workpath "$OUTPUT_DIR/build" \
  --specpath "$OUTPUT_DIR" \
  --name openflux-backend \
  --hidden-import "uvicorn.logging" \
  --hidden-import "uvicorn.loops.auto" \
  --hidden-import "uvicorn.protocols.http.auto" \
  --hidden-import "uvicorn.protocols.websockets.auto" \
  --hidden-import "uvicorn.lifespan.on" \
  --hidden-import "core.api.server" \
  --hidden-import "core.indexer" \
  --hidden-import "core.orchestrator" \
  "$ENTRY" \
  || true

if [[ -d "$OUTPUT_DIR/dist/openflux-backend" ]]; then
  echo ""
  echo "Backend bundle: $OUTPUT_DIR/dist/openflux-backend/"
  echo "Run: $OUTPUT_DIR/dist/openflux-backend/openflux-backend"
  echo "To bundle with the app: copy that folder to OpenFlux.app/Contents/Resources/backend/"
else
  echo "PyInstaller may have failed (e.g. missing hidden imports). See Option B in docs/BACKEND.md for manual run."
fi
