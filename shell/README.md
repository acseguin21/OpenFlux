# OpenFlux Shell (Open Editor Base) — **Deprecated for installability**

**For “download DMG, open right away,” use the Tauri desktop app instead:** see **`desktop/README.md`** and the main **`README.md`**. Build with `cd desktop && npm run tauri build`; no VSCode clone.

This directory holds **patches and branding** for building the OpenFlux **full IDE** from an open editor base (Code-compatible source; see [upstream howto-build](https://github.com/VSCodium/vscodium/blob/master/docs/howto-build.md)). This path is **deprecated as the primary install**: it requires cloning the upstream editor and a long build. Use it only if you need a full Code-based IDE; otherwise use the **desktop** app.

- **`patches/`** – Patches applied to the upstream `build.sh` so our post-prepare runs after `prepare_vscode.sh`.
- **`branding/`** – `product.json` overrides (name “OpenFlux by VibeCoders United”, bundle IDs, etc.) and optional icons.
- **`scripts/`** – `clone_and_build.sh` (main build) and `openflux-post-prepare.sh` (upstream → OpenFlux replacements).

See **`docs/STANDALONE_IDE_ROADMAP.md`** for the full plan (Phase 1–5).

## Quick start (Phase 1)

From the **repo root**:

```bash
./shell/scripts/clone_and_build.sh
```

Or from `shell/scripts/`:

```bash
./clone_and_build.sh
```

**Requirements:** Node 20.18, jq, Python 3.11, rustup, and platform build deps. See [upstream howto-build](https://github.com/VSCodium/vscodium/blob/master/docs/howto-build.md).

**What it does:**

1. Clones the upstream editor into `.build/openflux-shell/vscodium` (or `$OPENFLUX_SHELL_BUILD_DIR`).
2. Copies `shell/branding/product.json` and `shell/scripts/openflux-post-prepare.sh` into the clone.
3. Patches `build.sh` to run `openflux-post-prepare.sh` after `prepare_vscode.sh`.
4. Runs the upstream `./dev/build.sh` (fetches editor source, prepares, compiles).

**Output:** A built editor under the clone dir (platform-specific subdir, e.g. darwin-arm64 on macOS) that shows as **OpenFlux by VibeCoders United**.

### Phase 2: Bundled extensions

After the build, `clone_and_build.sh` runs **`bundle_extensions.sh`**, which:

1. Builds **openflux-ai-tools** (npm install + compile) and **openflux-theme-scarlet-jade** (no build).
2. Copies both into the built app’s `resources/app/extensions/` so they are pre-installed.

**Bundled extensions:**

- **OpenFlux AI Tools** — Indexing, agent, search (default `openflux.apiUrl`: `http://localhost:8000`).
- **OpenFlux Scarlet & Jade** — Dark theme; choose *File > Preferences > Color Theme > OpenFlux Scarlet & Jade (Dark)*.

To run the bundle step alone (e.g. after a manual build):

```bash
bash shell/scripts/bundle_extensions.sh [path/to/upstream-clone]
```
Default path: `.build/openflux-shell/vscodium`.

**Default config:** The OpenFlux AI Tools extension sets `openflux.apiUrl` to `http://localhost:8000`. To use indexing and agent features, start the OpenFlux backend from the repo root: `./scripts/start_server.sh` (see main README and `QUICKSTART.md`).

### Phase 4: Packaging and release

After building (and optionally bundling extensions), create release artifacts:

```bash
bash shell/scripts/package_release_artifacts.sh [path/to/upstream-clone]
```

**Output:** `.build/openflux-shell/release/` (or `$OPENFLUX_RELEASE_DIR`) with:

- `OpenFlux-{version}-darwin-{arch}.zip` (macOS)
- `OpenFlux-{version}-linux-{arch}.tar.gz` (Linux)
- `OpenFlux-{version}-win32-{arch}.zip` (Windows, if built)

**Version:** From `OPENFLUX_VERSION` (e.g. `1.0.0` or `v1.0.0`), or git tag, or default `0.1.0`.

**CI:** Push a tag `v*` (e.g. `v1.0.0`) to trigger `.github/workflows/release.yml`: builds on macOS and Ubuntu, creates a GitHub Release, and uploads the artifacts. See `docs/STANDALONE_IDE_ROADMAP.md`.

### Phase 5: Polish (Welcome & status)

The bundled **OpenFlux AI Tools** extension provides:

- **Welcome:** Shown on first run; also via *OpenFlux: Show Welcome*. “Welcome to OpenFlux by VibeCoders United” with steps to start the backend, index the codebase, and optional Ollama.
- **Status bar (context orb):** “✓ OpenFlux” (Ready), “🔄 OpenFlux (indexing)”, “▶ OpenFlux (agent)”, “⚠ OpenFlux (backend offline)” — Jade/Scarlet semantics per `docs/BRANDING.md`.
- **Open Documentation:** Command *OpenFlux: Open Documentation* opens the repo in the browser.
- **Composer (chat):** Command *OpenFlux: Open Composer* opens a chat-style panel (Scarlet & Jade themed). Type a goal; the agent runs and the response (status, message, plan) is shown. Conversation history stays in the panel.
