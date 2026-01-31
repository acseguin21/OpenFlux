#!/usr/bin/env bash
# Package built OpenFlux output into release artifacts (zip/tar.gz).
# Run from repo root after clone_and_build.sh + bundle_extensions.sh.
# Uses OPENFLUX_VERSION (default: 0.1.0 or git describe --tags), VSCODIUM_DIR, OPENFLUX_RELEASE_DIR.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VSCODIUM_DIR="${1:-$REPO_ROOT/.build/openflux-shell/vscodium}"
RELEASE_DIR="${OPENFLUX_RELEASE_DIR:-$REPO_ROOT/.build/openflux-shell/release}"

# Version: env (strip v if present), or git tag, or default
if [[ -n "$OPENFLUX_VERSION" ]]; then
  VERSION="${OPENFLUX_VERSION#v}"
elif git -C "$REPO_ROOT" describe --tags --exact-match 2>/dev/null; then
  VERSION="$(git -C "$REPO_ROOT" describe --tags --exact-match | sed 's/^v//')"
else
  VERSION="0.1.0"
fi

cd "$REPO_ROOT"
mkdir -p "${OPENFLUX_RELEASE_DIR:-$REPO_ROOT/.build/openflux-shell/release}"
RELEASE_DIR="$(cd "${OPENFLUX_RELEASE_DIR:-$REPO_ROOT/.build/openflux-shell/release}" && pwd)"
rm -f "$RELEASE_DIR"/OpenFlux-*.zip "$RELEASE_DIR"/OpenFlux-*.tar.gz

echo "=== Phase 4: Package release artifacts ==="
echo "Version:   $VERSION"
echo "Build dir: $VSCODIUM_DIR"
echo "Output:    $RELEASE_DIR"
echo ""

# macOS: VSCode-darwin-{arch}/ contains OpenFlux.app (or *.app)
for dir in "$VSCODIUM_DIR"/VSCode-darwin-*; do
  if [[ -d "$dir" ]]; then
    arch="${dir##*-}"
    out="$RELEASE_DIR/OpenFlux-${VERSION}-darwin-${arch}.zip"
    echo "Packaging macOS ($arch)..."
    (cd "$VSCODIUM_DIR" && zip -r -q "$out" "VSCode-darwin-${arch}")
    echo "  -> $out"
  fi
done

# Linux: VSCode-linux-{arch}/
for dir in "$VSCODIUM_DIR"/VSCode-linux-*; do
  if [[ -d "$dir" ]]; then
    arch="${dir##*-}"
    out="$RELEASE_DIR/OpenFlux-${VERSION}-linux-${arch}.tar.gz"
    echo "Packaging Linux ($arch)..."
    (cd "$VSCODIUM_DIR" && tar czf "$out" "VSCode-linux-${arch}")
    echo "  -> $out"
  fi
done

# Windows: VSCode-win32-{arch}/
for dir in "$VSCODIUM_DIR"/VSCode-win32-*; do
  if [[ -d "$dir" ]]; then
    arch="${dir##*-}"
    out="$RELEASE_DIR/OpenFlux-${VERSION}-win32-${arch}.zip"
    echo "Packaging Windows ($arch)..."
    (cd "$VSCODIUM_DIR" && zip -r -q "$out" "VSCode-win32-${arch}")
    echo "  -> $out"
  fi
done

count=$(ls -1 "$RELEASE_DIR"/OpenFlux-*.zip "$RELEASE_DIR"/OpenFlux-*.tar.gz 2>/dev/null | wc -l)
echo ""
echo "Done. $count artifact(s) in $RELEASE_DIR"
