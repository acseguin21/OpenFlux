# Build & Setup Guide for OpenCode

This guide outlines how to build your own version of OpenCode from source or set it up as a "Pro-Extension" kit.

## Option 1: The "Pro-Extension" Kit (Fastest)

If you don't want to manage a full editor fork yet, you can use a Code-compatible editor (e.g. from your package manager) with our bundled configuration.

1. **Install a Code-compatible editor**: e.g. `brew install --cask vscodium` (macOS) or use the built OpenCode app from this repo.
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

1. **Clone the upstream editor** (see `shell/README.md` for the recommended build; the script clones the upstream repo and applies our patches):
   ```bash
   ./shell/scripts/clone_and_build.sh   # from repo root
   ```
   Or manually: clone the upstream Code-compatible editor repo, then apply OpenCode patches from `shell/patches/`.
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
