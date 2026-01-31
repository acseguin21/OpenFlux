#!/usr/bin/env bash
# Build OpenFlux extensions and copy them into the built app bundle.
# Run from repo root after clone_and_build.sh (or pass upstream clone path).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
EXTENSIONS_SRC="$REPO_ROOT/extensions"
VSCODIUM_DIR="${1:-$REPO_ROOT/.build/openflux-shell/vscodium}"

# Extension folder name in app: publisher.name-version
AI_TOOLS_ID="openflux.openflux-ai-tools-0.1.0"
THEME_ID="openflux.openflux-theme-scarlet-jade-0.1.0"

cd "$REPO_ROOT"

echo "=== Phase 2: Bundle OpenFlux extensions ==="
echo "Repo root: $REPO_ROOT"
echo "Upstream build dir: $VSCODIUM_DIR"
echo ""

# 1. Build openflux-ai-tools
echo "Building openflux-ai-tools..."
cd "$EXTENSIONS_SRC/openflux-ai-tools"
if [[ ! -d node_modules ]]; then
  npm install
fi
npm run compile
cd "$REPO_ROOT"

# 2. Find built app extensions directory (platform-specific)
# macOS: VSCode-darwin-*/OpenFlux.app/Contents/Resources/app/extensions
# Linux: VSCode-linux-*/resources/app/extensions
# Windows: VSCode-win32-*/resources/app/extensions
APP_EXTENSIONS_DIRS=()
if [[ -d "$VSCODIUM_DIR" ]]; then
  for dir in "$VSCODIUM_DIR"/VSCode-darwin-*; do
    if [[ -d "$dir" ]]; then
      # App name from our product.json is OpenFlux
      if [[ -d "$dir/OpenFlux.app" ]]; then
        APP_EXTENSIONS_DIRS+=("$dir/OpenFlux.app/Contents/Resources/app/extensions")
      elif [[ -d "$dir/VSCodium.app" ]]; then
        APP_EXTENSIONS_DIRS+=("$dir/VSCodium.app/Contents/Resources/app/extensions")
      else
        # Fallback: first .app in dir
        for app in "$dir"/*.app; do
          [[ -d "$app" ]] && APP_EXTENSIONS_DIRS+=("$app/Contents/Resources/app/extensions") && break
        done
      fi
    fi
  done
  for dir in "$VSCODIUM_DIR"/VSCode-linux-*; do
    if [[ -d "$dir/resources/app/extensions" ]]; then
      APP_EXTENSIONS_DIRS+=("$dir/resources/app/extensions")
    fi
  done
  for dir in "$VSCODIUM_DIR"/VSCode-win32-*; do
    if [[ -d "$dir/resources/app/extensions" ]]; then
      APP_EXTENSIONS_DIRS+=("$dir/resources/app/extensions")
    fi
  done
fi

if [[ ${#APP_EXTENSIONS_DIRS[@]} -eq 0 ]]; then
  echo "No built app found under $VSCODIUM_DIR (looked for VSCode-darwin-*, VSCode-linux-*, VSCode-win32-*)."
  echo "Run clone_and_build.sh first, or pass the upstream clone path: $0 /path/to/upstream-clone"
  exit 1
fi

# 3. Copy extensions into each found app
for APP_EXT in "${APP_EXTENSIONS_DIRS[@]}"; do
  mkdir -p "$APP_EXT"
  echo "Bundling into: $APP_EXT"

  # OpenFlux AI Tools: package.json, dist/, node_modules, README
  rm -rf "$APP_EXT/$AI_TOOLS_ID"
  mkdir -p "$APP_EXT/$AI_TOOLS_ID"
  cp "$EXTENSIONS_SRC/openflux-ai-tools/package.json" "$APP_EXT/$AI_TOOLS_ID/"
  cp -r "$EXTENSIONS_SRC/openflux-ai-tools/dist" "$APP_EXT/$AI_TOOLS_ID/"
  cp -r "$EXTENSIONS_SRC/openflux-ai-tools/node_modules" "$APP_EXT/$AI_TOOLS_ID/" 2>/dev/null || true
  [[ -d "$EXTENSIONS_SRC/openflux-ai-tools/resources" ]] && cp -r "$EXTENSIONS_SRC/openflux-ai-tools/resources" "$APP_EXT/$AI_TOOLS_ID/" || true
  [[ -f "$EXTENSIONS_SRC/openflux-ai-tools/README.md" ]] && cp "$EXTENSIONS_SRC/openflux-ai-tools/README.md" "$APP_EXT/$AI_TOOLS_ID/" || true

  # OpenFlux Scarlet & Jade theme: package.json + themes/
  rm -rf "$APP_EXT/$THEME_ID"
  mkdir -p "$APP_EXT/$THEME_ID"
  cp "$EXTENSIONS_SRC/openflux-theme-scarlet-jade/package.json" "$APP_EXT/$THEME_ID/"
  cp -r "$EXTENSIONS_SRC/openflux-theme-scarlet-jade/themes" "$APP_EXT/$THEME_ID/"
done

echo ""
echo "=== Extensions bundled ==="
echo "  - $AI_TOOLS_ID"
echo "  - $THEME_ID"
echo "Default config: openflux.apiUrl = http://localhost:8000 (set in extension package.json)."
echo "To use Scarlet & Jade theme: File > Preferences > Color Theme > OpenFlux Scarlet & Jade (Dark)."
