#!/bin/bash

# OpenCode Neo-Tactical Setup Script (SV 2026)
echo "⚡ Initializing OpenCode Development Environment..."

# Create Python Virtual Env
echo "🐍 Setting up Python Core..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Setup Extension
echo "📦 Setting up Node.js Extension..."
cd extensions/opencode-ai-tools
npm install
cd ../..

echo "✅ Environment Ready. System initialized."
echo "Use 'source .venv/bin/activate' to enter the Neo-Tactical core."
