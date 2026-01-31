# OpenFlux Quick Start Guide

Get OpenFlux up and running in minutes!

## Prerequisites

1. **Python 3.10+**
   ```bash
   python3 --version
   ```

2. **Node.js 18+** (for the editor extension)
   ```bash
   node --version
   ```

3. **Ollama** (for local models)
   ```bash
   # Install Ollama from https://ollama.com
   ollama --version
   
   # Pull required models
   ollama pull llama3.1:8b
   ollama pull nomic-embed-text
   ```

## Installation

1. **Clone and setup Python environment**
   ```bash
   cd openflux
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Optional: Install language parsers (may require building from source on Python 3.13+)
   pip install -r requirements-optional.txt || echo "Language parsers optional - continuing..."
   ```

2. **Install editor extension dependencies**
   ```bash
   cd extensions/openflux-ai-tools
   npm install
   npm run compile  # Build TypeScript
   ```

## Running OpenFlux

### 1. Start the API Server

```bash
# From project root
./scripts/start_server.sh

# Or manually:
source venv/bin/activate
python -m uvicorn core.api.server:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at `http://localhost:8000`.

**Optional (start at login):** Run `./scripts/install_backend_service.sh` for macOS launchd. See **`docs/BACKEND.md`** for details and Linux.

### 2. Load the Extension in the Editor

1. Open a Code-compatible editor (e.g. from this repo’s built app or a compatible IDE)
2. Press `F5` or go to Run → Start Debugging
3. A new editor window will open with the extension loaded

### 3. Index Your Codebase

1. Open a workspace folder in the editor
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Run command: `OpenFlux: Index Codebase`
4. Wait for indexing to complete (check status bar)

### 4. Search Your Code

1. Press `Ctrl+Shift+P`
2. Run command: `OpenFlux: Search Codebase`
3. Enter your query (e.g., "authentication login")
4. Results will open in a new markdown document

### 5. Use the Agent

1. Press `Ctrl+Shift+P`
2. Run command: `OpenFlux: Start Autonomous Agent`
3. Enter your goal (e.g., "Add error handling to all API routes")
4. Watch as the agent plans, executes, and verifies changes

## Configuration

### Editor Settings

Add to your `settings.json`:

```json
{
  "openflux.apiUrl": "http://localhost:8000",
  "openflux.useOllama": true,
  "openflux.embeddingModel": "nomic-embed-text"
}
```

### Environment Variables

For the API server:

```bash
export OPENFLUX_PLANNING_MODEL="llama3.1:8b"
export OPENFLUX_EDITING_MODEL="llama3.1:8b"
export OPENFLUX_VERIFICATION_MODEL="llama3.1:8b"
```

## Troubleshooting

### Server won't start

- Check Python version: `python3 --version` (needs 3.10+)
- Check dependencies: `pip list | grep -E "(fastapi|uvicorn|lancedb)"`
- Check port 8000 is available: `lsof -i :8000`

### Extension can't connect

- Verify server is running: `curl http://localhost:8000`
- Check `openflux.apiUrl` setting matches server URL
- Check the editor output panel for errors

### Indexing fails

- Ensure Ollama is running: `ollama list`
- Check model exists: `ollama show nomic-embed-text`
- Check workspace path is correct

### Agent fails

- Ensure Ollama models are available: `ollama list`
- Check workspace has write permissions
- Review agent output in the editor output panel

## Next Steps

- Read [INTEGRATION.md](./INTEGRATION.md) for architecture details
- Read [ARCHITECTURE.md](./ARCHITECTURE.md) for design decisions

## Contributing

See the main [README.md](./README.md) for contribution guidelines.
