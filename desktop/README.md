# OpenFlux Desktop

Standalone native app: one window, connect to your OpenFlux backend, use the agent. **Download DMG → open → use.**

Built with **Tauri v2** + **Vite** + **React**. No VSCode fork; one command to build installers.

## Prerequisites

- **Node.js** 18+ and npm (or bun)
- **Rust** (stable): [rustup](https://rustup.rs/)
- **Platform:** [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/) (e.g. macOS Xcode, Windows Visual Studio build tools, Linux webkit2gtk)

## Development

From repo root:

```bash
cd desktop
npm install
npm run tauri dev
```

Starts the Vite dev server and opens the native window. Backend URL defaults to `http://localhost:8000`.

## Build (DMG / .app / installers)

From `desktop/`:

```bash
npm install
npm run tauri build
```

Outputs go to `src-tauri/target/release/bundle/`:

- **macOS:** `dmg/` (OpenFlux_0.1.0_aarch64.dmg or x64), `macos/` (.app)
- **Windows:** `msi/`, `nsis/` (installer .exe)
- **Linux:** `deb/`, `rpm/`, `appimage/` (if in targets)

One command; no clone of VSCode or other IDEs.

## App icons (optional)

`tauri.conf.json` uses an empty `bundle.icon` by default. If `tauri build` fails with an icon-related error, add at least one icon under `src-tauri/icons/` (e.g. `32x32.png`, `128x128.png`) and set `bundle.icon` in `tauri.conf.json`. See `src-tauri/icons/README.md` and [Tauri icons](https://v2.tauri.app/develop/icons/).

## Backend

The app talks to the OpenFlux API (default `http://localhost:8000`). Start the backend from the repo root:

```bash
./scripts/start_server.sh
```

Then in the app: set the backend URL if needed, click **Connect**, and use the composer to run the agent.
