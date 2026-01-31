#!/usr/bin/env bash
# OpenFlux post-prepare: replace upstream product name with OpenFlux/openflux in the editor tree.
# Run from the upstream repo root after prepare_vscode.sh.

set -e

VSCODE_DIR="vscode"
[[ -d "$VSCODE_DIR" ]] || { echo "Error: $VSCODE_DIR not found"; exit 1; }

# Portable in-place sed: macOS needs sed -i '', Linux uses sed -i.
sed_i() {
  if [[ "$(uname -s)" == "Darwin" ]]; then
    sed -i '' "$@"
  else
    sed -i "$@"
  fi
}

# Replace upstream product name -> OpenFlux in key files (user-facing / package metadata).
# We do not replace the package name globally so upstream URLs are left intact.
replace_in_file() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  sed_i 's/VSCodium/OpenFlux/g' "$f"
}

# Replace package name "codium" with "openflux" only on Package: line (Linux control.template).
replace_deb_package_name() {
  local f="$VSCODE_DIR/resources/linux/debian/control.template"
  [[ -f "$f" ]] || return 0
  sed_i 's/^Package: codium$/Package: openflux/' "$f"
  sed_i 's/^Package: codium-insiders$/Package: openflux-insiders/' "$f"
}

# In postinst, the package name was set to "codium" by prepare_vscode; change to "openflux".
replace_postinst_package() {
  local f="$VSCODE_DIR/resources/linux/debian/postinst.template"
  [[ -f "$f" ]] || return 0
  sed_i 's/ codium / openflux /g' "$f"
  sed_i 's/^codium$/openflux/' "$f"
}

replace_in_file "$VSCODE_DIR/package.json"
replace_in_file "$VSCODE_DIR/resources/server/manifest.json"
replace_in_file "$VSCODE_DIR/build/lib/electron.ts"

# Linux packaging (display names + package name)
replace_in_file "$VSCODE_DIR/resources/linux/code.appdata.xml"
replace_in_file "$VSCODE_DIR/resources/linux/debian/control.template"
replace_in_file "$VSCODE_DIR/resources/linux/debian/postinst.template"
replace_in_file "$VSCODE_DIR/resources/linux/rpm/code.spec.template"
replace_deb_package_name
replace_postinst_package

# Windows packaging (stable; insider uses code-insider.iss)
for iss in "$VSCODE_DIR/build/win32/code.iss" "$VSCODE_DIR/build/win32/code-insider.iss"; do
  replace_in_file "$iss"
done

echo "OpenFlux post-prepare done."
