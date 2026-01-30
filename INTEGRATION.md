# OpenCode Integration Guide

This document explains how the various components of OpenCode integrate together.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Editor Extension                          │
│  (extensions/opencode-ai-tools/)                            │
│  - UI Commands                                               │
│  - Status Bar                                                │
│  - Search Results Display                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              FastAPI Backend Server                          │
│  (core/api/server.py)                                        │
│  - /api/index                                                │
│  - /api/search                                               │
│  - /api/agent/execute                                        │
└──────────────┬───────────────────────┬──────────────────────┘
               │                       │
    ┌──────────▼──────────┐  ┌────────▼──────────┐
    │   Indexing Engine    │  │ Agent Orchestrator│
    │  (core/indexer/)     │  │ (core/orchestrator│
    │                      │  │  /agent.py)       │
    │  - Tree-sitter       │  │                   │
    │  - LanceDB           │  │  - Plan           │
    │  - Ollama Embeddings │  │  - Execute        │
    └─────────────────────┘  │  - Verify         │
                              └───────────────────┘
```

## Component Details

### 1. Indexing Engine (`core/indexer/engine.py`)

**Purpose**: Parse codebase and create searchable embeddings

**Key Features**:
- Uses Tree-sitter for AST parsing
- Extracts semantic chunks (functions, classes, methods)
- Generates embeddings via Ollama
- Stores in LanceDB vector database

**Usage**:
```python
from core.indexer import IndexingEngine

indexer = IndexingEngine(
    workspace_path="/path/to/workspace",
    vector_db_path="/path/to/.opencode/index",
    embedding_model="nomic-embed-text"
)

# Index the codebase
indexer.index(use_ollama=True)

# Search
results = indexer.search("login authentication", top_k=10)
```

### 2. Agent Orchestrator (`core/orchestrator/agent.py`)

**Purpose**: Autonomous code editing with plan-execute-verify loop

**Key Features**:
- Plans tasks using LLM
- Applies edits safely
- Verifies changes with tests
- Self-corrects on failures

**Usage**:
```python
from core.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(
    workspace_path="/path/to/workspace",
    model_config={
        "planning_model": "llama3.1:8b",
        "editing_model": "llama3.1:8b",
    },
    indexer=indexer  # Optional, for context
)

# Execute a task
result = orchestrator.run_loop("Add error handling to API routes", max_iterations=5)
```

### 3. FastAPI Backend (`core/api/server.py`)

**Purpose**: REST API for the editor extension

**Endpoints**:
- `POST /api/index` - Index a codebase
- `POST /api/search` - Search indexed code
- `POST /api/agent/execute` - Execute agent task
- `GET /api/status` - Get service status

**Start Server**:
```bash
./scripts/start_server.sh
# Or manually:
python -m uvicorn core.api.server:app --host 0.0.0.0 --port 8000
```

### 4. Editor Extension (`extensions/opencode-ai-tools/`)

**Purpose**: User interface and editor integration

**Commands**:
- `opencode.indexCodebase` - Index current workspace
- `opencode.searchCodebase` - Search codebase
- `opencode.startAgent` - Start autonomous agent

**Configuration**:
- `opencode.apiUrl` - API server URL
- `opencode.useOllama` - Use local Ollama models
- `opencode.embeddingModel` - Embedding model name

## Integration Flow

### Indexing Flow

1. User runs `opencode.indexCodebase` command
2. Extension sends POST to `/api/index` with workspace path
3. Backend creates `IndexingEngine` instance
4. Engine scans workspace, parses files with Tree-sitter
5. Chunks are generated and embedded via Ollama
6. Embeddings stored in LanceDB
7. Status returned to extension

### Search Flow

1. User runs `opencode.searchCodebase` command
2. Extension prompts for query
3. Extension sends POST to `/api/search` with query
4. Backend generates query embedding
5. LanceDB performs vector similarity search
6. Results returned and displayed in markdown document

### Agent Flow

1. User runs `opencode.startAgent` command
2. Extension prompts for goal
3. Extension sends POST to `/api/agent/execute`
4. Orchestrator plans task (with optional context from indexer)
5. Edits are applied to files
6. Verification commands run (tests, linters)
7. If verification fails, agent generates fix and retries
8. Final status returned to extension

## Dependencies from .lafufu

The following repositories in `.lafufu` inform our implementation:

- **tree-sitter**: Core parsing library
- **tree-sitter-python/js/ts**: Language grammars
- **lancedb**: Vector database for embeddings
- **ollama**: Local LLM runtime
- **continue**: Reference for editor extension patterns
- **Roo-Code**: Reference for code indexing patterns

## Next Steps

1. **Editor base integration**: Fork the upstream editor and add custom UI components
2. **Enhanced Chunking**: Improve semantic chunking with better Tree-sitter queries
3. **Multi-Model Support**: Add support for third-party LLM APIs (e.g. compatible providers)
4. **Shadow Branching**: Implement git shadow branches for safe edits
5. **Real-time Indexing**: Watch file changes and update index incrementally
