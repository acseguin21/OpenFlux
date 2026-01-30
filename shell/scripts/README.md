# Shell Build Scripts

- **`clone_and_build.sh`** – Main entry: clones the upstream editor, copies OpenCode branding and `opencode-post-prepare.sh`, patches `build.sh`, runs `./dev/build.sh`, then runs `bundle_extensions.sh` (Phase 2). Run from repo root or from this directory.
- **`opencode-post-prepare.sh`** – Run from the upstream repo root after `prepare_vscode.sh`; replaces upstream product name with OpenCode/opencode in package.json, manifest, electron.ts, and Linux/Windows packaging files.
- **`bundle_extensions.sh`** – Builds `opencode-ai-tools` and copies it plus `opencode-theme-scarlet-jade` into the built app’s `resources/app/extensions/`. Run after the upstream build; accepts optional path to upstream clone.
- **`package_backend.sh`** – (Phase 3 Option A) Packages the Python backend with PyInstaller into `.build/opencode-backend/`. For bundling with the app and auto-start, see `docs/BACKEND.md` and `docs/STANDALONE_IDE_ROADMAP.md`.
- **`package_release_artifacts.sh`** – (Phase 4) After build, creates `OpenCode-{version}-darwin-{arch}.zip`, `OpenCode-{version}-linux-{arch}.tar.gz`, and (if built) `OpenCode-{version}-win32-{arch}.zip` in `.build/opencode-shell/release/`. Use `OPENCODE_VERSION` or git tag. CI uses this in `.github/workflows/release.yml` on tag push.

See `shell/README.md` for usage and the [upstream howto-build](https://github.com/VSCodium/vscodium/blob/master/docs/howto-build.md) for dependencies.
