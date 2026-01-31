# OpenFlux: The Transparent, Open-Source AI IDE

**Download OpenFlux** — standalone AI IDE, open source, build from GitHub. **VibeCoders United** is the organization behind OpenFlux: a single application (like popular subscription-based AI IDEs) built from **open-source projects** you can pull and build from GitHub. Community-driven, privacy-first, with no vendor lock-in or hidden telemetry.

## One-command install

**From the repo root** (setup + backend in background):

```bash
./scripts/install_and_run.sh
```

**Clone and run** (one line; replace the URL if your fork is elsewhere):

```bash
git clone https://github.com/acseguin21/openflux.git openflux && cd openflux && ./scripts/install_and_run.sh
```

That chains: clone → quick_start (venv, deps, extension build) → start_server (background). Backend at `http://localhost:8000`. See **`QUICKSTART.md`** for using the extension.

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

- `core/`: High-performance backends for indexing and agent orchestration.
- `shell/`: Patches and branding for the custom editor distribution.
- `extensions/`: Bundled editor extensions that provide the AI UI.
- `scripts/`: Automation for building binaries and setting up development environments.
- `docs/`: Technical specifications and API documentation.
- `tests/`: Integration and unit tests for the AI loop.

## 🛠️ Architecture

OpenFlux is designed as an ecosystem of best-in-class open-source tools:

1. **The Shell**: A custom fork/distribution of an open editor base.
2. **The Intelligence**: Powered by compatible AI extensions, integrated deeply into the IDE.
3. **The Indexer**: Semantic codebase search using Tree-sitter and vector embeddings.
4. **The Runtime**: Support for [Ollama](https://ollama.com/) for a fully offline experience.

## 📂 Repository Structure

- `/src`: Custom modifications to the editor shell.
- `/extensions`: Core bundled extensions for AI features.
- `/scripts`: Build and distribution scripts for macOS, Linux, and Windows.
- `/docs`: Architecture, roadmap, and contribution guides.

## 📦 Releases (Phase 4)

Push a tag `v*` (e.g. `v1.0.0`) to trigger a GitHub Release: the workflow builds OpenFlux on macOS and Linux, then uploads `OpenFlux-{version}-darwin-{arch}.zip` and `OpenFlux-{version}-linux-{arch}.tar.gz` to the release. See `shell/README.md` (Phase 4) and `.github/workflows/release.yml`.

## 🔧 Backend (Phase 3)

The IDE’s indexing and agent features use a **local API** at `http://localhost:8000`. To run it:

- **Quick:** From repo root run `./scripts/start_server.sh`.
- **Optional (start at login):** Run `./scripts/install_backend_service.sh` (macOS launchd).

See **`docs/BACKEND.md`** for manual start, Linux systemd, and packaging the backend with the app (Option A).

---

*This is a work in progress. Join us in building the future of open-source development.*

<sub>open-source · AI IDE · BYOK · Ollama · local-first · code editor · semantic search · privacy</sub>
