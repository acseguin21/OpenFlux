# Roadmap: Standalone IDE App

This document outlines what’s needed to turn OpenCode into a **standalone desktop IDE**: a single app users download and run, built from open-source projects on GitHub.

---

## Where Things Stand Today

| Component | Status | Notes |
|-----------|--------|--------|
| **Core backend** | ✅ Exists | `core/api`, `core/indexer`, `core/orchestrator` (Python) |
| **Editor extension** | ✅ Exists | `extensions/opencode-ai-tools` (indexing, agent, search) |
| **Editor shell** | ❌ Missing | No upstream editor fork, no `shell/` or patches yet |
| **Bundled extensions** | ⚠️ Partial | Our extension exists; not yet “built into” a custom build |
| **Branding in shell** | ❌ Missing | No OpenCode / VibeCoders United name, icons, or Scarlet & Jade theme in the app |
| **Packaged binary** | ❌ Missing | No .app / .exe / AppImage produced from this repo |
| **Backend bundled with app** | ❌ Missing | User runs API/indexer separately; not shipped inside the IDE |

---

## What "Standalone IDE" Means

1. **One download** – User gets “OpenCode” (or similar name) as a single app for macOS / Windows / Linux.
2. **No "install a separate editor then install extension"** – The editor and AI features are one product.
3. **Branded experience** – Window title, icon, About dialog, and default theme say “OpenCode” / “VibeCoders United” and use Scarlet & Jade.
4. **Backend optional but smooth** – Either the app ships and auto-starts the indexer/API, or it connects to a user-run backend with a simple first-run flow.

---

## What We Need To Do (In Order)

### Phase 1: Shell and build pipeline

**Goal:** Produce a custom-built editor binary (OpenCode shell) from an open editor base (Code-compatible source).

1. **Create a `shell/` area in this repo**  
   - `shell/patches/` – Patches applied on top of the upstream editor (branding, product name, defaults).  
   - `shell/branding/` – Icons, product.json, name “OpenCode”, window title.  
   - `shell/scripts/` – Wrappers that clone the upstream repo, apply our patches, run its build.

2. **Fork or mirror the upstream build**  
   - Use [upstream howto-build](https://github.com/VSCodium/vscodium/blob/master/docs/howto-build.md) and `build.sh` / `prepare_vscode.sh`.  
   - Our scripts should: clone the upstream repo (or Code + community patches), apply **our** patches from `shell/patches/`, then build.  
   - Output: a built “Code”-like binary with our name and icon (e.g. “OpenCode.app” on macOS).

3. **Branding patches**  
   - Product name: “OpenCode” (or chosen name).  
   - Window title, About dialog: “OpenCode by VibeCoders United”.  
   - Default product.json: application name, extension host, etc.  
   - App icon (Scarlet & Jade style) for macOS/Windows/Linux.

4. **Theme**  
   - Ship a default color theme that uses Scarlet & Jade + neutrals (see `docs/BRANDING.md`).  
   - Can be a built-in theme or a bundled extension that’s set as default.

**Deliverable:** Script(s) in this repo that, when run, produce a standalone “OpenCode” editor binary for at least one platform (e.g. macOS).

---

### Phase 2: Bundled extensions and default config

**Goal:** OpenCode ships with our AI features and sensible defaults; user doesn’t install extensions manually.

1. **Bundle our extension**  
   - Build `extensions/opencode-ai-tools` and include it in the upstream build as a “built-in” extension (the Code-compatible build supports listing extra extensions in the build config).  
   - So the OpenCode binary already contains “OpenCode AI Tools”.

2. **Optional: bundle compatible AI extensions**  
   - If we rely on compatible chat/completion extensions, add them as built-in so the IDE works out of the box.

3. **Default settings**  
   - Point `opencode.apiUrl` (or equivalent) to `http://localhost:8000` (or wherever our backend will run).  
   - Optional: default theme = our Scarlet & Jade theme.  
   - Document in-app or in README how to start the backend (Phase 3).

**Deliverable:** Same binary as Phase 1, but with OpenCode AI Tools (and optionally compatible extensions) pre-installed and pre-configured.

---

### Phase 3: Backend lifecycle (run with the app)

**Goal:** User can “run OpenCode” and have the indexer/API start automatically, or have a clear one-time setup.

**Option A – Backend shipped and started by the app**

1. **Package the Python backend**  
   - Use PyInstaller, Nuitka, or a small Node/py launcher to build a single executable (or a small bundle) for indexer + API.  
   - Include it in the OpenCode app bundle (e.g. `OpenCode.app/Contents/Resources/backend/` on macOS).

2. **IDE starts the backend**  
   - On first launch (or every launch), the Electron main process spawns the backend binary; e.g. listen on `localhost:8000`.  
   - Requires a small patch or extension that runs a “start backend” script or executable when the app starts.

3. **First-run UX**  
   - If backend fails to start (e.g. port in use), show a simple message: “OpenCode backend couldn’t start. Check port 8000 or run it manually.”

**Option B – User runs backend separately (simpler short-term)**

1. **Document and script**  
   - Keep current approach: user runs `./scripts/start_server.sh` (or equivalent) in this repo.  
   - In README and in-app help: “To use indexing and agent features, start the OpenCode backend: …”

2. **Optional installer**  
   - Installer or post-install script that can install Python deps and optionally register a “OpenCode Backend” service (e.g. launchd on macOS) so the backend starts when the user logs in.

**Deliverable:** Either (A) backend starts with the app, or (B) clear docs + scripts so “run OpenCode + run backend” is a one-time or simple step.

---

### Phase 4: Packaging and distribution

**Goal:** One downloadable artifact per platform, (e.g. .app, .exe, AppImage).

1. **macOS**  
   - `.app` bundle (already from the upstream build).  
   - Optionally: `.dmg` for drag-to-Applications (create with a small script or CI).

2. **Windows**  
   - Portable `.exe` or installer (the upstream build produces this; we reuse and rebrand).  
   - Optional: NSIS or other installer that writes “OpenCode” to Start Menu and adds uninstall.

3. **Linux**  
   - AppImage, or .deb/.rpm (the upstream build has patterns for this).  
   - Package name: `opencode` or similar.

4. **CI (e.g. GitHub Actions)**  
   - On tag or release: build shell + extensions for macOS, Windows, Linux.  
   - Upload artifacts to GitHub Releases (e.g. `OpenCode-1.0.0-macos.zip`, `OpenCode-1.0.0-win.exe`, etc.).

**Deliverable:** GitHub (or other) release page where users download “OpenCode” for their OS.

---

### Phase 5: Polish and product-like UX

**Goal:** Feel like a single product, not "generic editor + extension".

1. **Welcome / first run**  
   - “Welcome to OpenCode by VibeCoders United” with:  
     - Link to start backend (if Option B), or “Backend is starting…” (if Option A).  
     - Optional: “Connect to Ollama” / “Add API key” for cloud models.

2. **Context orb / status**  
   - Status bar or panel showing “Indexing”, “Ready”, “Backend disconnected” (using Jade/Scarlet per BRANDING.md).

3. **Composer / chat**  
   - **Implemented:** *OpenCode: Open Composer* opens a chat-style panel (Scarlet & Jade themed). User types a goal; the agent runs plan-execute-verify and the response (status, message, plan steps) is shown in the panel. Conversation history is preserved in the panel.

4. **Docs and branding**  
   - In-app “About” and “Documentation” point to this repo and VibeCoders United.  
   - README and website: “Download OpenCode – standalone AI IDE, open source, build from GitHub.”

---

## Suggested Repo Layout After Phase 1–2

```text
opencode/
├── core/                    # Backend (API, indexer, orchestrator)
├── extensions/               # Editor extensions (opencode-ai-tools, etc.)
├── shell/                   # NEW: Everything for the standalone shell
│   ├── patches/             # Patches applied on top of upstream editor
│   ├── branding/            # Icons, product.json, name
│   ├── theme/               # Optional: Scarlet & Jade theme (JSON or extension)
│   └── scripts/             # clone + patch + build + package
│       ├── clone_and_build.sh
│       └── package_dmg.sh   # (example)
├── scripts/                 # Existing: start_server, quick_start, etc.
├── docs/
│   ├── BRANDING.md
│   ├── STANDALONE_IDE_ROADMAP.md  # this file
│   └── ...
└── .github/workflows/       # Optional: build and release on tag
    └── release.yml
```

---

## Summary Checklist

- [x] **Phase 1:** `shell/` with patches + branding; script to build “OpenCode” from the upstream editor. Run `./shell/scripts/clone_and_build.sh` from repo root.
- [x] **Phase 2:** Our extension (OpenCode AI Tools) and Scarlet & Jade theme built-in; default config (`opencode.apiUrl` = `http://localhost:8000` in extension). Run `clone_and_build.sh` (which runs `bundle_extensions.sh` after the build).
- [x] **Phase 3:** Backend lifecycle. **Option B (done):** `docs/BACKEND.md`, `./scripts/start_server.sh`, optional `./scripts/install_backend_service.sh` (macOS launchd); extension shows backend status and “Show backend instructions” command. **Option A (scaffolding):** `shell/scripts/package_backend.sh` and `scripts/run_backend_entry.py` to package backend; see docs for bundling with app and auto-start.
- [x] **Phase 4:** Packaging for macOS, Linux (and optionally Windows). **Local:** Run `bash shell/scripts/package_release_artifacts.sh` after build; artifacts go to `.build/opencode-shell/release/` (OpenCode-{version}-darwin-{arch}.zip, OpenCode-{version}-linux-{arch}.tar.gz). **CI:** Push tag `v*` (e.g. `v1.0.0`) to trigger `.github/workflows/release.yml` — builds on macOS and Ubuntu, creates GitHub Release and uploads artifacts.
- [x] **Phase 5:** Welcome flow, status bar, Open Documentation, README tagline. **Composer/chat:** *OpenCode: Open Composer* — chat-style panel (Scarlet & Jade), goal → agent execute → response in panel with conversation history.

Once Phase 1–2 are done, you have a **standalone IDE app** that someone can build from this repo and run. Phases 3–5 make it shippable and polished for end users.
