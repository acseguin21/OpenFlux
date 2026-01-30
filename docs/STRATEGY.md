# OpenCode Strategy & Pitch (VibeCoders United)

This document captures OpenCode’s strategic advantages and positioning. Names and themes (OpenCode, VibeCoders United, Scarlet & Jade) stay as-is.

---

## 1. The "Bring Your Own Key" (BYOK) Advantage

Subscription-based AI editors rely on monthly fees. OpenCode disrupts this by acting as a **dumb pipe** for LLMs.

- **Zero markup:** Users plug in their own API keys (any compatible provider) or connect to local models via Ollama. You pay the provider directly; OpenCode does not add a usage fee.
- **Privacy pitch:** Market OpenCode as the editor that **never sees your code**—LLM calls happen locally (Ollama, vLLM) or directly between the user and the provider. Code is not sent to OpenCode’s servers because there are none.

*Relevant today:* Model-agnostic backend; `opencode.apiUrl` and provider config stay in the user’s environment; optional BYOK/keys in settings or env.

---

## 2. Win the "Local-First" Crowd

The biggest complaints about AI editors are **latency** and **data privacy**.

- **Local indexing:** OpenCode indexes the codebase **locally** with O(n)-efficient, local-first design. Metadata never leaves the machine; no central server receives your code or index.
- **Small-model optimization:** The UI and workflows are tuned for **lightweight, fast models** that run on a standard laptop GPU (e.g. via Ollama). Low latency and offline use are first-class.

*Relevant today:* Tree-sitter + local vector DB (e.g. LanceDB) in `core/indexer`; backend runs on `localhost`; Ollama as the default path.

---

## 3. Distribution via the Editor Ecosystem

OpenCode is built on an **open editor base**. That gives a big advantage: **extension compatibility**.

- **Zero-friction switch:** Every compatible editor extension works in OpenCode. No need to give up your current extensions.
- **Market as a "mod":** OpenCode can be positioned as a **custom build** or **super-extension**—either a full standalone app (Phases 1–4) or an install that slots into an existing editor setup so users don’t lose their config.

*Relevant today:* Shell is based on an open editor; extensions live in the compatible ecosystem; build produces a standalone IDE or can be used as a configured editor + extensions.

---

## 4. Feature "The Missing Pieces"

Commercial AI editors are strong but not perfect. OpenCode aims to cover what users complain about (e.g. on Reddit and X):

- **Long-context handling:** Roadmap and design should support **better management of 100k+ token contexts** (chunking, summarization, selective context) so large codebases don’t blow the context window.
- **Agentic workflows:** Beyond "chat," OpenCode already leans into **agents** that can run tests and fix bugs autonomously (plan–execute–verify in `core/orchestrator`; Composer and "Start Agent" in the IDE). Double down on this as a differentiator.
- **Linux / niche OS support:** Where some tools lag on specific distros, OpenCode can be the **Linux-first** AI editor—first-class support for mainstream and niche Linux, with CI and packaging for the platform.

*Relevant today:* Agent loop and Composer; local indexing; release workflow includes Linux; Linux-first is an explicit niche to own.

---

## 5. Comparison: Subscription-based vs OpenCode

| Feature | Subscription-based (typical) | OpenCode (VibeCoders United) |
|--------|-------------------------------|------------------------------|
| **Cost** | ~$20/mo subscription | Free; pay-per-token via your keys (BYOK) or free local models |
| **Model choice** | Curated by vendor | Any model (open or closed)—Ollama or any compatible API |
| **Privacy** | Code indexed on their infra | 100% local indexing; no code sent to our servers |
| **Telemetry** | Opt-out (mostly) | Disabled by default; open source, auditable |

---

## 6. Strategy: The "Bitter Lesson"

In AI, hardware and models get **cheaper over time**. A fixed $20/month subscription may look expensive in a year. OpenCode’s goal is to be the **VLC of AI editors**:

- **Free** and open source  
- **Plays everything**—any model, any provider, local or cloud  
- **Lightweight** and fast, especially with small local models  
- **It just works**—BYOK, local-first, extension-compatible, no lock-in  

Names and themes (OpenCode, VibeCoders United, Scarlet & Jade) stay unchanged; this document is about strategy and positioning only.
