# Build & Setup Guide for OpenCode

This guide outlines how to build your own version of OpenCode from source or set it up as a "Pro-Extension" kit.

## Option 1: The "Pro-Extension" Kit (Fastest)

If you don't want to manage a full VS Code fork yet, you can turn VSCodium into OpenCode using our bundled configuration.

1. **Install VSCodium**: `brew install --cask vscodium` (macOS)
2. **Install Ollama**: [ollama.com](https://ollama.com)
3. **Pull Models**:
   ```bash
   ollama pull llama3.1:8b  # For reasoning
   ollama pull starcoder2:3b # For autocomplete
   ```
4. **Clone OpenCode Config**:
   ```bash
   git clone https://github.com/your-org/opencode-config ~/.config/opencode
   ```
5. **Symlink Extensions**: Our scripts will auto-install `Continue`, `Tree-sitter`, and `LSP` enhancements.

## Option 2: Building the OpenCode Shell (Advanced)

To create a standalone binary with custom branding and UI components.

### Prerequisites
- Node.js 18+
- Python 3.10+
- C++ Compiler (GCC/Clang)

### Steps

1. **Fork VSCodium**:
   ```bash
   git clone https://github.com/VSCodium/vscodium.git
   cd vscodium
   ```
2. **Apply OpenCode Patches**:
   Our patches modify `src/vs/workbench/contrib` to add the custom AI sidecar and Composer UI.
   ```bash
   git apply ../opencode/patches/*.patch
   ```
3. **Build**:
   ```bash
   ./build.sh
   ```
4. **Package**:
   ```bash
   ./package.sh
   ```

## Option 3: Setting up the Indexer

OpenCode requires a local vector database for codebase awareness.

1. **Start the OpenCode-Indexer**:
   ```bash
   docker run -d -p 8000:8000 opencode/indexer
   ```
2. **Point the IDE**: In your settings, set `opencode.indexer.url: "http://localhost:8000"`.
