# OpenFlux: The Transparent, Open-Source AI IDE

**Download OpenFlux** — standalone desktop app, open source, build from GitHub. **VibeCoders United** is the organization behind OpenFlux: one native window (like [OpenCode](https://opencode.ai/)) that connects to your OpenFlux backend. Community-driven, privacy-first, no vendor lock-in or hidden telemetry.

## Install: Desktop app (recommended)

**One command** → DMG / .app / installer. No VSCode clone.

```bash
cd desktop
npm install
npm run tauri build
```

Output: `desktop/src-tauri/target/release/bundle/` — **macOS:** `.dmg` and `.app`; **Windows:** `.exe` installer; **Linux:** `.deb`, `.rpm`, AppImage. Double-click to run.

Then start the backend (from repo root):

```bash
./scripts/start_server.sh
```

Open the app → set backend URL `http://localhost:8000` → **Connect** → use the composer. See **`desktop/README.md`** and **`QUICKSTART.md`**.

## 🚀 The Vision

- **100% Open Source**: Built on an open editor base and other open-source projects; clone, build, and ship from GitHub.
- **Standalone IDE**: A single application experience (like commercial AI coding tools), not just a plugin—fully buildable from source.
- **Model Agnostic**: Plug in Ollama, vLLM, or any compatible API provider; use your own keys or local models.
- **Local-First RAG**: High-performance codebase indexing that stays on your machine.
- **Community Owned**: No hidden trackers, no proprietary "secret sauce" edit models.

## Why OpenFlux

| | Subscription-based (typical) | OpenFlux |
|--|-------------------------------|----------|
| **Cost** | ~$20/mo subscription | Free; BYOK or local models (pay provider only) |
| **Model choice** | Curated by vendor | Any model (Ollama or any compatible API) |
| **Privacy** | Code on their infra | 100% local indexing; editor never sees code on our servers |
| **Telemetry** | Opt-out (mostly) | Disabled by default |

**BYOK:** Use your own API keys or local Ollama—zero markup. **Local-first:** Index and run models on your machine; no central server. **Editor ecosystem:** Same extensions, zero-friction switch. **Linux-first:** First-class support where others lag. See **`docs/STRATEGY.md`** for full positioning (BYOK, local-first, missing pieces, “VLC of AI editors”).

## 🌌 The Aesthetic: Scarlet & Jade (VibeCoders United)

OpenFlux uses **Scarlet** and **Jade** accent colours with **complementary neutral tones** so the UI stays clear and the accents pop. High-density, high-agency UI—less like a plain text editor, more like a **Strategic Command Center** for AI orchestration.

## 📂 Project Structure

- **`desktop/`**: **Tauri desktop app** — one window, composer + backend connection. **Primary install path** (DMG / .app / installers).
- `core/`: High-performance backends for indexing and agent orchestration.
- `extensions/`: Editor extensions (use inside Cursor/VSCode or a Code-compatible editor).
- `scripts/`: Backend and dev automation.
- `docs/`: Technical specifications and API documentation.
- `tests/`: Integration and unit tests for the AI loop.
- `shell/`: **Deprecated** for installability — legacy Code-based IDE build; use `desktop/` for “download and open” instead.

## 🛠️ Architecture

OpenFlux is designed as an ecosystem of best-in-class open-source tools:

1. **The Desktop App**: Tauri-native window (composer + backend URL). Download DMG → open → use.
2. **The Backend**: Local API (indexing + agent) at `http://localhost:8000`.
3. **The Indexer**: Semantic codebase search using Tree-sitter and vector embeddings.
4. **The Runtime**: Support for [Ollama](https://ollama.com/) for a fully offline experience.
5. **Optional**: Use **OpenFlux AI Tools** extension inside Cursor/VSCode for in-editor features.

## 📂 Repository Structure

- `/src`: Custom modifications to the editor shell.
- `/extensions`: Core bundled extensions for AI features.
- `/scripts`: Build and distribution scripts for macOS, Linux, and Windows.
- `/docs`: Architecture, roadmap, and contribution guides.

## 📦 Releases

Build the desktop app with `cd desktop && npm run tauri build`; artifacts are in `desktop/src-tauri/target/release/bundle/`. For CI releases, add a workflow that runs `tauri build` per platform and uploads the DMG / .app / installers to GitHub Releases. See `desktop/README.md` and [Tauri distribution](https://v2.tauri.app/distribute/).

## 🔧 Backend (Phase 3)

The IDE’s indexing and agent features use a **local API** at `http://localhost:8000`. To run it:

- **Quick:** From repo root run `./scripts/start_server.sh`.
- **Optional (start at login):** Run `./scripts/install_backend_service.sh` (macOS launchd).

See **`docs/BACKEND.md`** for manual start, Linux systemd, and packaging the backend with the app (Option A).

---

*This is a work in progress. Join us in building the future of open-source development.*

<sub>open-source · AI IDE · BYOK · Ollama · local-first · code editor · semantic search · privacy</sub>
