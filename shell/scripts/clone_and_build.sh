#!/usr/bin/env bash
# Build OpenCode standalone IDE from the upstream editor (Code-compatible source).
# Run from the mystery-machine repo root, or from shell/scripts (repo root is auto-detected).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Repo root: script lives at repo/shell/scripts/
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SHELL_DIR="$REPO_ROOT/shell"
BUILD_DIR="${OPENCODE_SHELL_BUILD_DIR:-$REPO_ROOT/.build/opencode-shell}"
VSCODIUM_DIR="$BUILD_DIR/vscodium"

cd "$REPO_ROOT"

echo "=== OpenCode shell build (Phase 1) ==="
echo "Repo root: $REPO_ROOT"
echo "Build dir: $BUILD_DIR"
echo ""

# 1. Clone upstream editor if needed
if [[ ! -d "$VSCODIUM_DIR/.git" ]]; then
  echo "Cloning upstream editor..."
  mkdir -p "$BUILD_DIR"
  git clone --depth 1 https://github.com/VSCodium/vscodium.git "$VSCODIUM_DIR"
else
  echo "Using existing upstream clone at $VSCODIUM_DIR"
fi

# 2. Copy OpenCode branding and post-prepare script into the clone
echo "Copying OpenCode branding..."
cp "$SHELL_DIR/branding/product.json" "$VSCODIUM_DIR/product.json"
cp "$SHELL_DIR/scripts/opencode-post-prepare.sh" "$VSCODIUM_DIR/opencode-post-prepare.sh"
chmod +x "$VSCODIUM_DIR/opencode-post-prepare.sh"

# 3. Patch build.sh to run opencode-post-prepare.sh after prepare_vscode.sh
if ! grep -q "opencode-post-prepare" "$VSCODIUM_DIR/build.sh" 2>/dev/null; then
  echo "Patching build.sh..."
  (cd "$VSCODIUM_DIR" && patch -p1 < "$SHELL_DIR/patches/build-add-post-prepare.patch" || true)
  # If patch failed (e.g. context mismatch), try inline sed
  if ! grep -q "opencode-post-prepare" "$VSCODIUM_DIR/build.sh" 2>/dev/null; then
    if [[ "$(uname -s)" == "Darwin" ]]; then
      sed -i '' '/\. prepare_vscode\.sh$/a\
 bash opencode-post-prepare.sh
' "$VSCODIUM_DIR/build.sh"
    else
      sed -i '/\. prepare_vscode\.sh$/a bash opencode-post-prepare.sh' "$VSCODIUM_DIR/build.sh"
    fi
  fi
else
  echo "build.sh already patched."
fi

# 4. Run upstream dev build
echo ""
echo "Starting upstream build (this will fetch editor source, run prepare, and compile; can take 30+ minutes)..."
echo "Requirements: node 20.18, jq, python3 3.11, rustup, and platform build deps. See upstream docs/howto-build.md."
echo ""

cd "$VSCODIUM_DIR"
./dev/build.sh

# Phase 2: Bundle OpenCode extensions into the built app
echo ""
if [[ -f "$SHELL_DIR/scripts/bundle_extensions.sh" ]]; then
  bash "$SHELL_DIR/scripts/bundle_extensions.sh" "$VSCODIUM_DIR"
else
  echo "To bundle OpenCode AI Tools and Scarlet & Jade theme, run:"
  echo "  bash shell/scripts/bundle_extensions.sh $VSCODIUM_DIR"
fi

echo ""
echo "=== Build complete ==="
echo "Output is under $VSCODIUM_DIR (e.g. built app dirs per platform)."
echo "The built app will show as OpenCode by VibeCoders United."
