# OpenCode: The Transparent, Open-Source AI IDE

OpenCode is a community-driven, privacy-first alternative to Cursor. Our mission is to provide a world-class AI coding experience built entirely on open-source foundations, allowing you to use any model—local or cloud—without vendor lock-in or hidden telemetry.

## 🚀 The Vision

- **100% Open Source**: Built on VSCodium, the telemetry-free version of VS Code.
- **Model Agnostic**: Plug in Ollama, vLLM, Anthropic, OpenAI, or your own custom fine-tuned models.
- **Local-First RAG**: High-performance codebase indexing that stays on your machine.
- **Community Owned**: No hidden trackers, no proprietary "secret sauce" edit models.

## 🌌 The Aesthetic: Neo-Tactical (SV 2026)

OpenCode follows a **Neo-Tactical** design language: Deep Obsidian backgrounds, Hyper-Blue accents, and a focus on high-density, high-agency UI. It feels less like a text editor and more like a **Strategic Command Center** for AI orchestration.

## 📂 Project Structure

- `core/`: High-performance backends for indexing and agent orchestration.
- `shell/`: Patches and branding for the custom VSCodium distribution.
- `extensions/`: Bundled VS Code extensions that provide the AI UI.
- `scripts/`: Automation for building binaries and setting up development environments.
- `docs/`: Technical specifications and API documentation.
- `tests/`: Integration and unit tests for the AI loop.

## 🛠️ Architecture

OpenCode is designed as an ecosystem of best-in-class open-source tools:

1. **The Shell**: A custom fork/distribution of [VSCodium](https://vscodium.com/).
2. **The Intelligence**: Powered by [Continue](https://github.com/continuedev/continue) or [Roo Code](https://github.com/RooVetGit/Roo-Code), integrated deeply into the IDE.
3. **The Indexer**: Semantic codebase search using Tree-sitter and vector embeddings.
4. **The Runtime**: Support for [Ollama](https://ollama.com/) for a fully offline experience.

## 📂 Repository Structure

- `/src`: Custom modifications to the VS Code shell.
- `/extensions`: Core bundled extensions for AI features.
- `/scripts`: Build and distribution scripts for macOS, Linux, and Windows.
- `/docs`: Architecture, roadmap, and contribution guides.

---

*This is a work in progress. Join us in building the future of open-source development.*
