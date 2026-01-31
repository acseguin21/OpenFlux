# OpenFlux Backend (Phase 3)

The OpenFlux IDE talks to a **local API server** for indexing, search, and agent features. By default it uses `http://localhost:8000`.

## Quick start: run the backend manually

From the **OpenFlux repo root** (or wherever you have the OpenFlux source):

```bash
./scripts/start_server.sh
```

This script:

- Creates a Python virtual environment (`venv`) if needed
- Installs dependencies from `requirements.txt`
- Starts the API with: `uvicorn core.api.server:app --host 0.0.0.0 --port 8000 --reload`

The server will be at **http://localhost:8000**. The OpenFlux extension is already configured to use this URL by default.

### Manual start (without the script)

```bash
cd /path/to/openflux
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn core.api.server:app --host 0.0.0.0 --port 8000 --reload
```

---

## Optional: run the backend as a service (start at login)

If you want the backend to start automatically when you log in (so you don’t have to run `start_server.sh` every time), you can install it as a service.

### macOS (launchd)

From the **repo root**:

```bash
./scripts/install_backend_service.sh
```

This installs a **user** launchd job so the OpenFlux backend runs at login and keeps running. See the script for uninstall and log location.

### Linux (systemd user service)

Create a user unit (example; adjust paths):

```ini
# ~/.config/systemd/user/openflux-backend.service
[Unit]
Description=OpenFlux API backend
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/openflux
ExecStart=/path/to/openflux/venv/bin/python -m uvicorn core.api.server:app --host 127.0.0.1 --port 8000
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

Then:

```bash
systemctl --user daemon-reload
systemctl --user enable --now openflux-backend.service
```

---

## Troubleshooting

- **Port 8000 in use**  
  Stop the other process using port 8000, or set a different port and update the OpenFlux setting `openflux.apiUrl` (e.g. `http://localhost:8001`).

- **Extension says “backend offline”**  
  Start the backend with `./scripts/start_server.sh` (or your service). Ensure the URL in **OpenFlux > API URL** matches (default `http://localhost:8000`).

- **Ollama / embeddings**  
  For local indexing you need [Ollama](https://ollama.com) and the embedding model (e.g. `ollama pull nomic-embed-text`). See `QUICKSTART.md`.

---

## Phase 3 Option A (future): backend bundled with the app

In a future version, the OpenFlux app can ship and auto-start the backend:

1. Backend is packaged (e.g. with PyInstaller) into a single executable or small bundle.
2. It is placed inside the app (e.g. `OpenFlux.app/Contents/Resources/backend/` on macOS).
3. The IDE starts it on launch (e.g. via an extension or a small patch to the shell).

For now, use the manual or service approach above. To experiment with packaging:

- **Package the backend:** From repo root run `bash shell/scripts/package_backend.sh`. Output goes to `.build/openflux-backend/dist/openflux-backend/`.
- **Bundle with the app:** Copy that folder into the built app (e.g. `OpenFlux.app/Contents/Resources/backend/` on macOS). Auto-start from the IDE would require an extension or shell patch that spawns the binary on launch (see Phase 3 Option A in `docs/STANDALONE_IDE_ROADMAP.md`).
