#!/bin/bash

# OpenCode Neo-Tactical Setup Script (SV 2026)
echo "⚡ Initializing OpenCode Development Environment..."

# Create Python Virtual Env
echo "🐍 Setting up Python Core..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Try to install optional language parsers
echo "📚 Installing optional language parsers..."
if pip install -r requirements-optional.txt 2>/dev/null; then
    echo "✓ Language parsers installed"
else
    echo "⚠ Language parsers optional (code will work without them)"
fi

# Setup Extension
echo "📦 Setting up Node.js Extension..."
cd extensions/opencode-ai-tools
npm install
cd ../..

echo "✅ Environment Ready. System initialized."
echo "Use 'source .venv/bin/activate' to enter the Neo-Tactical core."
