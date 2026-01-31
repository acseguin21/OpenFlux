import * as vscode from "vscode";

export const REPO_DOCS = "https://github.com/acseguin21/openflux#readme";
export const BACKEND_DOCS = "https://github.com/acseguin21/openflux/blob/master/docs/BACKEND.md";

export function getWelcomeHtml(): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to OpenFlux</title>
    <style>
        body {
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background: var(--vscode-editor-background);
            padding: 1.5rem;
            line-height: 1.6;
        }
        h1 { font-size: 1.5rem; margin-top: 0; color: #F5F5F4; }
        h2 { font-size: 1rem; margin: 1.25rem 0 0.5rem; color: #0D9488; }
        p { margin: 0.5rem 0; }
        ul { margin: 0.5rem 0; padding-left: 1.25rem; }
        a { color: #0D9488; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .tagline { color: #57534E; font-size: 0.9rem; margin-bottom: 1rem; }
        .step { margin: 0.75rem 0; padding: 0.5rem 0; }
        .cta { display: inline-block; margin-top: 0.5rem; padding: 0.35rem 0.75rem; background: #0D9488; color: #F5F5F4; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }
        .cta:hover { background: #0F766E; }
        .warn { color: #C41E3A; font-size: 0.9rem; }
    </style>
</head>
<body>
    <h1>Welcome to OpenFlux</h1>
    <p class="tagline">by VibeCoders United — standalone AI IDE, open source, build from GitHub.</p>

    <h2>Get started</h2>
    <div class="step">
        <p><strong>1. Start the backend</strong></p>
        <p>Indexing and agent features need the OpenFlux API at <code>http://localhost:8000</code>.</p>
        <p>From the repo root run: <code>./scripts/start_server.sh</code></p>
        <p>Or use the command: <strong>OpenFlux: Show backend instructions</strong></p>
        <a href="#" data-cmd="openflux.showBackendInstructions">Show backend instructions</a>
    </div>
    <div class="step">
        <p><strong>2. Index your codebase</strong></p>
        <p>Once the backend is running, index the workspace for search and agent context.</p>
        <a href="#" data-cmd="openflux.indexCodebase">Index Codebase</a>
    </div>
    <div class="step">
        <p><strong>3. Open Composer (chat)</strong></p>
        <p>Describe a goal in natural language; the agent will plan and execute. Scarlet &amp; Jade themed.</p>
        <a href="#" data-cmd="openflux.openComposer">Open Composer</a>
    </div>
    <div class="step">
        <p><strong>4. Optional: Ollama &amp; models</strong></p>
        <p>For local embeddings and models, install <a href="https://ollama.com">Ollama</a> and pull e.g. <code>nomic-embed-text</code>, <code>llama3.1:8b</code>. See the repo docs for cloud API keys.</p>
    </div>

    <h2>Documentation</h2>
    <p><a href="${REPO_DOCS}" data-link="repo">Repository &amp; README</a></p>
    <p><a href="${BACKEND_DOCS}" data-link="backend">Backend setup (docs/BACKEND.md)</a></p>
    <p><a href="#" data-cmd="openflux.openDocumentation">Open Documentation (browser)</a></p>

    <script>
        const vscode = acquireVsCodeApi();
        document.querySelectorAll('[data-cmd]').forEach(el => {
            el.addEventListener('click', e => {
                e.preventDefault();
                vscode.postMessage({ command: el.getAttribute('data-cmd') });
            });
        });
        document.querySelectorAll('[data-link]').forEach(el => {
            el.addEventListener('click', e => {
                e.preventDefault();
                vscode.postMessage({ command: 'openflux.openLink', href: el.getAttribute('href') });
            });
        });
    </script>
</body>
</html>`;
}

export function createWelcomePanel(context: vscode.ExtensionContext): void {
    const panel = vscode.window.createWebviewPanel(
        "openfluxWelcome",
        "Welcome to OpenFlux",
        vscode.ViewColumn.One,
        { enableScripts: true }
    );
    panel.webview.html = getWelcomeHtml();
    panel.webview.onDidReceiveMessage((msg: { command?: string; href?: string }) => {
        if (msg.command === "openflux.openLink" && msg.href) {
            vscode.env.openExternal(vscode.Uri.parse(msg.href));
        } else if (msg.command && msg.command.startsWith("openflux.")) {
            vscode.commands.executeCommand(msg.command);
        }
    });
}
