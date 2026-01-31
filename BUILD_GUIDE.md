# Build & Setup Guide for OpenFlux

This guide outlines how to build and run OpenFlux. **Primary install path:** the Tauri desktop app (one command → DMG /.app / installers).

## Option 1: Desktop app (recommended — installable)

**One command** builds the standalone native app. No VSCode/Code clone.

### Prerequisites

- **Node.js** 18+ and npm (or bun)
- **Rust** (stable): [rustup](https://rustup.rs/)
- **Platform:** [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/)

### Build

```bash
cd desktop
npm install
npm run tauri build
```

Output: `desktop/src-tauri/target/release/bundle/` — **macOS:** `.dmg`, `.app`; **Windows:** NSIS `.exe`; **Linux:** `.deb`, `.rpm`, AppImage. Double-click to run.

Then start the backend from repo root: `./scripts/start_server.sh`. Open the app → set backend URL `http://localhost:8000` → **Connect** → use the composer.

See **`desktop/README.md`** for dev (`tauri dev`) and optional app icons.

## Option 2: Pro-Extension (use inside an editor)

Use the OpenFlux AI Tools extension inside a Code-compatible editor (Cursor, VSCode, VSCodium).

1. **Install a Code-compatible editor** (e.g. `brew install --cask vscodium`).
2. **Install Ollama**: [ollama.com](https://ollama.com); pull `llama3.1:8b`, `nomic-embed-text`.
3. Build the extension: `cd extensions/openflux-ai-tools && npm install && npm run compile`.
4. Start the backend: `./scripts/start_server.sh`. Set `openflux.apiUrl` to `http://localhost:8000` in editor settings.

## Option 3: Shell build (deprecated for installability)

The Code-based IDE build in `shell/` is **deprecated** as the install path. Use **Option 1 (desktop)** for “download DMG and open.” The shell build remains for advanced users who want a full Code-fork IDE; see `shell/README.md`. It requires cloning the upstream editor, patching, and a long build.

## Backend / Indexer

OpenFlux desktop and extension talk to a **local API** at `http://localhost:8000`. Start it with `./scripts/start_server.sh` from repo root. The backend runs the indexer and agent; see **`docs/BACKEND.md`**.
