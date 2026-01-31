# OpenFlux Quick Start Guide

Get OpenFlux up and running in minutes. **Recommended:** Desktop app (download DMG → open) + backend.

## Prerequisites

- **Python 3.10+** (backend)
- **Node.js 18+** (desktop app or extension)
- **Ollama** (local models): [ollama.com](https://ollama.com); then `ollama pull llama3.1:8b` and `ollama pull nomic-embed-text`

## Fast path: Desktop app

1. **Build the desktop app** (one command):
   ```bash
   cd desktop
   npm install
   npm run tauri build
   ```
   Open the app from `desktop/src-tauri/target/release/bundle/` (e.g. `.dmg` on macOS).

2. **Start the backend** (from repo root):
   ```bash
   ./scripts/start_server.sh
   ```
   If you haven’t set up Python yet: `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`, then run the script again.

3. **In the app:** Set backend URL to `http://localhost:8000` → **Connect** → type a goal in the composer → **Run agent**.

## Alternative: Extension in an editor

1. **Backend:** From repo root, `./scripts/start_server.sh` (ensure venv and `pip install -r requirements.txt` first).
2. **Extension:** `cd extensions/openflux-ai-tools && npm install && npm run compile`. Load the extension in Cursor/VSCode (e.g. Run → Start Debugging).
3. Set `openflux.apiUrl` to `http://localhost:8000` in settings.

## Running OpenFlux (backend details)

### Start the API server

```bash
# From project root
./scripts/start_server.sh

# Or manually:
source venv/bin/activate
python -m uvicorn core.api.server:app --host 0.0.0.0 --port 8000 --reload
```

Server: `http://localhost:8000`. **Optional (start at login):** `./scripts/install_backend_service.sh` (macOS launchd). See **`docs/BACKEND.md`**.

### Using the desktop app

Open the built app → Connect to `http://localhost:8000` → use the composer to run the agent.

### Using the extension (in-editor)

1. Open a Code-compatible editor with the OpenFlux AI Tools extension loaded.
2. **Index:** `Ctrl+Shift+P` → `OpenFlux: Index Codebase`; wait for indexing (status bar).
3. **Search:** `OpenFlux: Search Codebase` for semantic search.
4. **Agent:** `OpenFlux: Start Autonomous Agent` or open the Composer panel.

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
