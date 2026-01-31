# Standalone App Like OpenCode: Download DMG, Open Right Away

[OpenCode](https://opencode.ai/) ships a **standalone desktop app**: users download a `.dmg` (macOS) or `.exe` (Windows), open it, and get a native window with their AI coding UI—no terminal, no build-from-source. This doc explains **how they do it** and how OpenFlux can do the same **without** the convoluted VSCode-fork build.

---

## How OpenCode Does It (Simple)

OpenCode’s desktop app is **not** a full IDE. It is:

1. **A Tauri v2 app** = one native window + one web view.
2. **The “frontend”** = their existing web app (Solid.js + Vite), the same UI used in “opencode web” and in the desktop.
3. **One build command** → DMG / .app / NSIS / deb / rpm.

There is **no** VSCode fork, no Code clone, no multi-step “clone upstream → patch → build.sh → package.” Just:

```bash
cd packages/desktop
bun run tauri build
```

Tauri produces the installers (e.g. `opencode-desktop-darwin-aarch64.dmg`) from that. User experience: **download → open → use**.

### What’s Inside the Repo

| Piece | Role |
|-------|------|
| **packages/desktop** | Tauri app: `src/` = React/Solid UI, `src-tauri/` = Rust shell, `tauri.conf.json` = bundle config. |
| **tauri.conf.json** | `beforeBuildCommand: "bun run build"` (Vite), `frontendDist: "../dist"`, `targets: ["deb", "rpm", "dmg", "nsis", "app"]`. |
| **tauri.prod.conf.json** | Overrides for prod: icons, updater, Linux appstream. |
| **@opencode-ai/app** | Shared UI package used by both web and desktop. |

The desktop window is literally their **web app** loaded in Tauri’s WebView. The “full IDE” experience (if any) is a **separate** path (e.g. IDE extension); the **standalone app** is intentionally this simple shell.

### CI (Simplified)

1. **build-cli** – Build the `opencode` CLI (used as optional sidecar).
2. **build-tauri** – Per platform (macOS x64/arm, Windows, Linux):
   - Install Rust, deps (e.g. `libwebkit2gtk` on Linux).
   - `cd packages/desktop && bun ./scripts/prepare.ts` (version, sidecar).
   - **`tauri build`** (or `cargo tauri build`) with `tauri.prod.conf.json`.
3. **tauri-action** uploads artifacts to GitHub Release (e.g. `opencode-desktop-darwin-aarch64.dmg`).

No VSCode, no monorepo editor build—just Tauri + frontend.

---

## How OpenFlux Does It Today (Convoluted)

OpenFlux’s **current** standalone story is the **full IDE**:

- **shell/** – Clone VSCodium/Code, patch `build.sh`, run upstream `./dev/build.sh` (large C++/TS build), then bundle extensions and run `package_release_artifacts.sh`.
- **Result**: Zips/tarballs of a full Code-based IDE. Heavy, slow, and not “download DMG and open.”

So today we have “build the whole IDE from source,” not “one app you download and run.”

---

## What We Need: “Download DMG, Open Right Away”

Goal: **same UX as OpenCode** – a single standalone app (e.g. `.dmg`) that users can download and open immediately, without building VSCode or anything else.

Two ways to get there:

---

### Option A – Tauri “OpenFlux Desktop” (Recommended)

Add a **second** deliverable: a **Tauri app** that wraps a small OpenFlux UI (composer/chat + backend connection). No Code fork.

1. **New package**: e.g. `desktop/` or `app-desktop/`.
   - **Tauri v2** (Rust + one window).
   - **Frontend**: Minimal Vite + React/Solid/TS app: welcome, composer/chat, “Connect to backend” (e.g. `http://localhost:8000`), optional “Start backend” button (spawns `python -m core.api.server` or a shipped binary).
   - **Config**: `tauri.conf.json` with `targets: ["dmg", "app", "nsis", "deb", "rpm"]`, `beforeBuildCommand: "npm run build"` (or `bun run build`).

2. **Build** (from repo root or `packages/desktop`):
   ```bash
   cd desktop   # or packages/desktop
   npm install  # or bun install
   npx tauri build   # or bun run tauri build
   ```
   Output: `src-tauri/target/release/bundle/` → DMG, .app, etc.

3. **Backend**: Either:
   - **Simple**: “Start backend” in the app runs a bundled Python binary or `pip install openflux && openflux serve` (if we ship a PyPI package); or
   - **Simpler**: User runs backend themselves (`./scripts/start_server.sh`); app only connects to `localhost:8000`. Still “download app → open → point at backend.”

4. **CI**: One job per platform: install Node/Bun + Rust, deps, then `tauri build`. Upload artifacts to GitHub Release (e.g. `openflux-desktop-darwin-aarch64.dmg`).

**Result**: Users get **OpenFlux Desktop** = one download, one double-click, one window. Full IDE (Code-based shell) stays optional for those who want it.

---

### Option B – Keep Only the Full IDE

Continue **only** with the VSCode-fork build. Then “standalone” will always mean “build from source or download a pre-built IDE zip,” not “one small DMG like OpenCode.” Possible, but it won’t match the “download DMG, open right away” experience.

---

## Recommendation

- **Do Option A**: Add a **Tauri-based OpenFlux Desktop** app that:
  - Builds with **one command**: `tauri build`.
  - Produces **DMG / .app / NSIS / deb / rpm** like OpenCode.
  - Shows a simple UI (composer, chat, connect to backend); backend can be user-started or later bundled.
- **Keep** the existing **shell/** build for the **full IDE** (Code-based) as an advanced path.
- **Document** clearly:
  - **OpenFlux Desktop** = download DMG → open → use (Tauri app).
  - **OpenFlux IDE** = build from source or download full IDE zip (Code-based).

That way we get the same “standalone app, download and open” experience as [OpenCode](https://opencode.ai/) without tying it to the heavy, convoluted IDE build.

---

## References (OpenCode)

- **Desktop package**: `.lafufu/opencode/packages/desktop/` (package.json, src/, src-tauri/).
- **Tauri config**: `packages/desktop/src-tauri/tauri.conf.json`, `tauri.prod.conf.json`.
- **Build**: `bun run --cwd packages/desktop tauri build` (see README).
- **Publish workflow**: `.lafufu/opencode/.github/workflows/publish.yml` (build-cli → build-tauri matrix → tauri-action → release).
- **App entry**: `packages/desktop/src/index.tsx` (wraps `@opencode-ai/app` with Tauri plugins: store, updater, deep-link, etc.).
