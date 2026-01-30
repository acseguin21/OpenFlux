# OpenCode AI Tools Extension

Editor extension (Code-compatible) that provides AI-powered code indexing, search, and autonomous agent capabilities for OpenCode.

## Features

- **Codebase Indexing**: Index your codebase using Tree-sitter for semantic understanding
- **Semantic Search**: Search your codebase using natural language queries
- **Autonomous Agents**: Let AI agents plan and execute code changes with verification

## Requirements

- Python 3.10+ with dependencies installed (`pip install -r requirements.txt`)
- OpenCode API server running (start with `./scripts/start_server.sh`)
- Ollama installed and running (for local embeddings/models)

## Usage

1. **Index Codebase**: Run `OpenCode: Index Codebase` command
2. **Search**: Run `OpenCode: Search Codebase` command
3. **Start Agent**: Run `OpenCode: Start Autonomous Agent` command

## Configuration

- `opencode.apiUrl`: URL of the OpenCode API server (default: `http://localhost:8000`)
- `opencode.useOllama`: Use Ollama for local models (default: `true`)
- `opencode.embeddingModel`: Ollama model for embeddings (default: `nomic-embed-text`)
