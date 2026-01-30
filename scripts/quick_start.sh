#!/bin/bash
# Quick start script for OpenCode

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "🚀 OpenCode Quick Start"
echo "========================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if extension is built
if [ ! -d "extensions/opencode-ai-tools/dist" ]; then
    echo "📦 Building editor extension..."
    cd extensions/opencode-ai-tools
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    npm run compile
    cd "$PROJECT_ROOT"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the API server in one terminal:"
echo "   ./scripts/start_server.sh"
echo ""
echo "2. Open the editor and press F5 to load the extension"
echo ""
echo "3. In the Extension Host window, open a workspace and use:"
echo "   - Ctrl+Shift+P → 'OpenCode: Index Codebase'"
echo "   - Ctrl+Shift+P → 'OpenCode: Search Codebase'"
echo "   - Ctrl+Shift+P → 'OpenCode: Start Autonomous Agent'"
echo ""
echo "📖 See USAGE_GUIDE.md for detailed instructions"
