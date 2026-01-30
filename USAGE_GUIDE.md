# OpenCode Usage Guide

## Step-by-Step: Using OpenCode

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd /path/to/opencode
./scripts/start_server.sh
```

You should see:
```
Starting OpenCode API server on http://localhost:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open** - the server needs to stay running.

### Step 2: Build the Editor Extension (First Time Only)

Open a **new terminal** and run:

```bash
cd /path/to/opencode/extensions/opencode-ai-tools
npm install
npm run compile
```

This builds the TypeScript extension code.

### Step 3: Load Extension in the Editor

1. Open a Code-compatible editor in the project directory:
   ```bash
   cd /path/to/opencode
   code .   # or open the folder in your editor
   ```

2. Press `F5` (or go to **Run → Start Debugging**)
   - This opens a new editor window with the extension loaded
   - You'll see "Extension Development Host" in the title bar

3. In the new window, open a workspace folder (any project you want to work with)

### Step 4: Index Your Codebase

1. In the Extension Development Host window, open a workspace folder
2. Press `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`) to open the command palette
3. Type: `OpenCode: Index Codebase`
4. Press Enter
5. Wait for indexing to complete (check the status bar)

**Note**: Make sure Ollama is running and you have the embedding model:
```bash
ollama pull nomic-embed-text
```

### Step 5: Search Your Code

1. Press `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)
2. Type: `OpenCode: Search Codebase`
3. Enter a query like: "authentication" or "login function"
4. Results will appear in a new markdown document

### Step 6: Use the Autonomous Agent

1. Press `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)
2. Type: `OpenCode: Start Autonomous Agent`
3. Enter a goal like: "Add error handling to API routes"
4. The agent will:
   - Plan the changes
   - Apply edits to files
   - Run verification (if tests are configured)
   - Show results in the output panel

## Quick Reference

### Commands Available

| Command | Shortcut | Description |
|---------|----------|-------------|
| `OpenCode: Index Codebase` | - | Index the current workspace |
| `OpenCode: Search Codebase` | - | Search indexed code semantically |
| `OpenCode: Start Autonomous Agent` | - | Run an AI agent to make code changes |

### Status Bar

Look for the OpenCode icon in the status bar (bottom right). Click it to search.

### Output Panel

View agent execution logs:
- Go to **View → Output**
- Select "OpenCode Agent" from the dropdown

## Example Workflow

### Example 1: Find All Authentication Code

1. Index your codebase (Step 4)
2. Search for: "authentication login password"
3. Review results in the markdown document

### Example 2: Refactor with Agent

1. Index your codebase
2. Start agent with goal: "Refactor all API routes to use async/await"
3. Review the plan in the output panel
4. Check the changes made to files

## Troubleshooting

### "API server is not running"
- Make sure Step 1 is completed and the server terminal is still running
- Check: `curl http://localhost:8000` should return `{"status":"ok"}`

### "Indexer not initialized"
- Run `OpenCode: Index Codebase` first before searching

### Extension doesn't appear
- Make sure you pressed F5 in the main editor window (not the Extension Host)
- Check the Debug Console for errors
- Rebuild: `cd extensions/opencode-ai-tools && npm run compile`

### Ollama errors
- Ensure Ollama is installed: `ollama --version`
- Pull required models: `ollama pull nomic-embed-text` and `ollama pull llama3.1:8b`
- Check Ollama is running: `ollama list`

## Next Steps

- Try indexing a real project
- Experiment with different search queries
- Test the agent on small refactoring tasks
- Read [INTEGRATION.md](./INTEGRATION.md) to understand the architecture
