#!/bin/bash
# Run tests for OpenCode

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "Running OpenCode tests..."
echo "=========================="

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Python tests
echo ""
echo "Running Python unit tests..."
python3 -m pytest tests/ -v || python3 -m unittest discover -s tests -p "test_*.py" -v

echo ""
echo "Tests completed!"
