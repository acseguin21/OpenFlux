#!/usr/bin/env python3
"""
Debug script to check OpenFlux installation and identify issues.
"""
import sys
from pathlib import Path

def check_import(module_name, package_name=None):
    """Check if a module can be imported."""
    try:
        __import__(module_name)
        print(f"✓ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"✗ {package_name or module_name}: {e}")
        return False

def check_file_exists(file_path):
    """Check if a file exists."""
    path = Path(file_path)
    if path.exists():
        print(f"✓ {file_path}")
        return True
    else:
        print(f"✗ {file_path} (not found)")
        return False

def main():
    print("OpenFlux Debug Check")
    print("=" * 50)
    print()
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print()
    
    # Check core dependencies
    print("Checking core dependencies...")
    deps_ok = True
    deps_ok &= check_import("tree_sitter", "tree-sitter")
    deps_ok &= check_import("lancedb", "lancedb")
    deps_ok &= check_import("ollama", "ollama")
    deps_ok &= check_import("fastapi", "fastapi")
    deps_ok &= check_import("uvicorn", "uvicorn")
    deps_ok &= check_import("numpy", "numpy")
    deps_ok &= check_import("pydantic", "pydantic")
    print()
    
    # Check optional tree-sitter language bindings
    print("Checking tree-sitter language bindings...")
    check_import("tree_sitter_python", "tree-sitter-python")
    check_import("tree_sitter_javascript", "tree-sitter-javascript")
    check_import("tree_sitter_typescript", "tree-sitter-typescript")
    print()
    
    # Check core modules
    print("Checking core modules...")
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    try:
        from core.indexer import IndexingEngine
        print("✓ core.indexer.IndexingEngine")
    except Exception as e:
        print(f"✗ core.indexer.IndexingEngine: {e}")
    
    try:
        from core.orchestrator import AgentOrchestrator
        print("✓ core.orchestrator.AgentOrchestrator")
    except Exception as e:
        print(f"✗ core.orchestrator.AgentOrchestrator: {e}")
    
    try:
        from core.api.server import app
        print("✓ core.api.server")
    except Exception as e:
        print(f"✗ core.api.server: {e}")
    print()
    
    # Check important files
    print("Checking project files...")
    project_root = Path(__file__).parent.parent
    check_file_exists(project_root / "requirements.txt")
    check_file_exists(project_root / "core" / "indexer" / "engine.py")
    check_file_exists(project_root / "core" / "orchestrator" / "agent.py")
    check_file_exists(project_root / "core" / "api" / "server.py")
    check_file_exists(project_root / "scripts" / "start_server.sh")
    print()
    
    # Summary
    print("=" * 50)
    if deps_ok:
        print("✓ Core dependencies are installed")
    else:
        print("✗ Some dependencies are missing")
        print("  Run: pip install -r requirements.txt")
    print()
    print("To start the server:")
    print("  ./scripts/start_server.sh")
    print()
    print("To run tests:")
    print("  ./scripts/run_tests.sh")

if __name__ == "__main__":
    main()
