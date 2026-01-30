# OpenCode Shell (Open Editor Base)

This directory holds **patches and branding** for building the OpenCode standalone IDE from an open editor base (Code-compatible source; see [upstream howto-build](https://github.com/VSCodium/vscodium/blob/master/docs/howto-build.md)).

- **`patches/`** – Patches applied to the upstream `build.sh` so our post-prepare runs after `prepare_vscode.sh`.
- **`branding/`** – `product.json` overrides (name “OpenCode by VibeCoders United”, bundle IDs, etc.) and optional icons.
- **`scripts/`** – `clone_and_build.sh` (main build) and `opencode-post-prepare.sh` (upstream → OpenCode replacements).

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

1. Clones the upstream editor into `.build/opencode-shell/vscodium` (or `$OPENCODE_SHELL_BUILD_DIR`).
2. Copies `shell/branding/product.json` and `shell/scripts/opencode-post-prepare.sh` into the clone.
3. Patches `build.sh` to run `opencode-post-prepare.sh` after `prepare_vscode.sh`.
4. Runs the upstream `./dev/build.sh` (fetches editor source, prepares, compiles).

**Output:** A built editor under the clone dir (platform-specific subdir, e.g. darwin-arm64 on macOS) that shows as **OpenCode by VibeCoders United**.

### Phase 2: Bundled extensions

After the build, `clone_and_build.sh` runs **`bundle_extensions.sh`**, which:

1. Builds **opencode-ai-tools** (npm install + compile) and **opencode-theme-scarlet-jade** (no build).
2. Copies both into the built app’s `resources/app/extensions/` so they are pre-installed.

**Bundled extensions:**

- **OpenCode AI Tools** — Indexing, agent, search (default `opencode.apiUrl`: `http://localhost:8000`).
- **OpenCode Scarlet & Jade** — Dark theme; choose *File > Preferences > Color Theme > OpenCode Scarlet & Jade (Dark)*.

To run the bundle step alone (e.g. after a manual build):

```bash
bash shell/scripts/bundle_extensions.sh [path/to/upstream-clone]
```
Default path: `.build/opencode-shell/vscodium`.

**Default config:** The OpenCode AI Tools extension sets `opencode.apiUrl` to `http://localhost:8000`. To use indexing and agent features, start the OpenCode backend from the repo root: `./scripts/start_server.sh` (see main README and `QUICKSTART.md`).

### Phase 4: Packaging and release

After building (and optionally bundling extensions), create release artifacts:

```bash
bash shell/scripts/package_release_artifacts.sh [path/to/upstream-clone]
```

**Output:** `.build/opencode-shell/release/` (or `$OPENCODE_RELEASE_DIR`) with:

- `OpenCode-{version}-darwin-{arch}.zip` (macOS)
- `OpenCode-{version}-linux-{arch}.tar.gz` (Linux)
- `OpenCode-{version}-win32-{arch}.zip` (Windows, if built)

**Version:** From `OPENCODE_VERSION` (e.g. `1.0.0` or `v1.0.0`), or git tag, or default `0.1.0`.

**CI:** Push a tag `v*` (e.g. `v1.0.0`) to trigger `.github/workflows/release.yml`: builds on macOS and Ubuntu, creates a GitHub Release, and uploads the artifacts. See `docs/STANDALONE_IDE_ROADMAP.md`.

### Phase 5: Polish (Welcome & status)

The bundled **OpenCode AI Tools** extension provides:

- **Welcome:** Shown on first run; also via *OpenCode: Show Welcome*. “Welcome to OpenCode by VibeCoders United” with steps to start the backend, index the codebase, and optional Ollama.
- **Status bar (context orb):** “✓ OpenCode” (Ready), “🔄 OpenCode (indexing)”, “▶ OpenCode (agent)”, “⚠ OpenCode (backend offline)” — Jade/Scarlet semantics per `docs/BRANDING.md`.
- **Open Documentation:** Command *OpenCode: Open Documentation* opens the repo in the browser.
- **Composer (chat):** Command *OpenCode: Open Composer* opens a chat-style panel (Scarlet & Jade themed). Type a goal; the agent runs and the response (status, message, plan) is shown. Conversation history stays in the panel.
