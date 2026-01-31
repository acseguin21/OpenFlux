#!/usr/bin/env python3
"""
Entry point for packaging the OpenFlux backend (e.g. PyInstaller).
Runs uvicorn with core.api.server:app. Use from repo root or set PYTHONPATH.
"""
import sys
import os

# Ensure repo root is on path when packaged or run from elsewhere
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

if __name__ == "__main__":
    import uvicorn
    from core.api.server import app
    host = os.environ.get("OPENFLUX_HOST", "127.0.0.1")
    port = int(os.environ.get("OPENFLUX_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
