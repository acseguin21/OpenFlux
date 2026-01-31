# OpenFlux AI Tools Extension

Editor extension (Code-compatible) that provides AI-powered code indexing, search, and autonomous agent capabilities for OpenFlux.

## Features

- **Codebase Indexing**: Index your codebase using Tree-sitter for semantic understanding
- **Semantic Search**: Search your codebase using natural language queries
- **Autonomous Agents**: Let AI agents plan and execute code changes with verification

## Requirements

- Python 3.10+ with dependencies installed (`pip install -r requirements.txt`)
- OpenFlux API server running (start with `./scripts/start_server.sh`)
- Ollama installed and running (for local embeddings/models)

## Usage

1. **Index Codebase**: Run `OpenFlux: Index Codebase` command
2. **Search**: Run `OpenFlux: Search Codebase` command
3. **Start Agent**: Run `OpenFlux: Start Autonomous Agent` command

## Configuration

- `openflux.apiUrl`: URL of the OpenFlux API server (default: `http://localhost:8000`)
- `openflux.useOllama`: Use Ollama for local models (default: `true`)
- `openflux.embeddingModel`: Ollama model for embeddings (default: `nomic-embed-text`)
