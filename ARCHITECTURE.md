# OpenCode Architecture & Technical Strategy

To build a rival to Cursor as a startup, we must leverage the "Giant's Shoulders" of existing open-source software while adding a unique layer of **Agentic Orchestration** and **Superior Context**.

## 1. The Editor Shell (VSCodium Fork)

We will use **VSCodium** as our base. VSCodium is a community-driven, telemetry-free distribution of Microsoft's VS Code.

### Why VSCodium?
- **Extension Compatibility**: We retain access to the 50,000+ extensions in the Open VSX Registry.
- **License**: MIT-licensed source code allows us to fork and modify the UI (for things like the "Composer" or "Tab" features).
- **Clean Slate**: No Microsoft telemetry or proprietary license restrictions.

## 2. The AI Engine (The Brain)

Instead of building a model from scratch, we use a **Multi-Model Orchestrator**.

### Model Tiers:
- **Fast Completion (Tab)**: Use a local, small model (e.g., StarCoder2 3B or Llama 3 8B) running on the user's NPU/GPU for zero-latency inline suggestions.
- **Reasoning (Chat/Edit)**: Support for Claude 3.5 Sonnet, GPT-4o, or high-end local models (Llama 3 70B via Ollama).
- **Edit Verification**: A dedicated "verification" pass that runs a fast model to check syntax and lint errors after an edit.

## 3. The Context System (Advanced RAG)

This is where OpenCode will win. We move beyond simple vector search.

### Graph-Based Retrieval:
- **Tree-sitter**: We use tree-sitter to parse code into ASTs (Abstract Syntax Trees).
- **Dependency Mapping**: We build a map of function calls and variable usages.
- **Indexing**: Use an open-source vector DB (like **ChromaDB** or **LanceDB**) to store embeddings locally.

## 4. The Agentic Loop (Autonomous SWE)

OpenCode will integrate a "Shadow Terminal" and "Test Runner."

1. **User Goal**: "Refactor the login logic."
2. **Planner**: AI breaks the task into file-level edits.
3. **Executor**: AI applies edits to a hidden branch.
4. **Verifier**: IDE runs tests. If they fail, errors are fed back to the Executor.
5. **Human Review**: User sees a "Verified" badge on the proposed changes.

## 5. Development Roadmap

| Phase | Milestone | Tools |
|-------|-----------|-------|
| 1 | **MVP Shell** | VSCodium + Continue extension bundled |
| 2 | **Local Indexing** | Tree-sitter + local vector DB |
| 3 | **Custom UI** | Forking VSCodium to add "Ghost Text" and "Composer" |
| 4 | **Agentic Loop** | Integrated terminal/test-runner feedback |
