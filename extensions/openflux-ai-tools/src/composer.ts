/**
 * OpenFlux Composer — chat-style UI for agent goals, Scarlet & Jade themed.
 */

import * as vscode from "vscode";

const SCARLET = "#C41E3A";
const JADE = "#0D9488";
const BASE = "#1C1917";
const SURFACE = "#292524";
const MUTED = "#57534E";
const HIGHLIGHT = "#F5F5F4";

export function getComposerHtml(): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenFlux Composer</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: var(--vscode-font-family);
            background: ${BASE};
            color: ${HIGHLIGHT};
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: ${SURFACE};
            border-bottom: 1px solid ${MUTED};
            padding: 0.75rem 1rem;
            font-size: 0.9rem;
            color: ${JADE};
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .msg { max-width: 90%; }
        .msg.user {
            align-self: flex-end;
            background: ${SURFACE};
            border-left: 3px solid ${SCARLET};
            padding: 0.6rem 0.9rem;
            border-radius: 6px;
        }
        .msg.assistant {
            align-self: flex-start;
            background: ${SURFACE};
            border-left: 3px solid ${JADE};
            padding: 0.6rem 0.9rem;
            border-radius: 6px;
        }
        .msg .role { font-size: 0.75rem; color: ${MUTED}; margin-bottom: 0.25rem; }
        .msg.assistant .role { color: ${JADE}; }
        .msg.user .role { color: ${SCARLET}; }
        .msg pre, .msg code {
            background: ${BASE};
            padding: 0.5rem;
            border-radius: 4px;
            font-size: 0.85rem;
            overflow-x: auto;
            margin: 0.5rem 0 0;
        }
        .msg .status { color: ${JADE}; font-weight: 600; }
        .msg .error { color: ${SCARLET}; }
        .input-area {
            background: ${SURFACE};
            border-top: 1px solid ${MUTED};
            padding: 0.75rem 1rem;
            display: flex;
            gap: 0.5rem;
        }
        #goal {
            flex: 1;
            background: ${BASE};
            border: 1px solid ${MUTED};
            color: ${HIGHLIGHT};
            padding: 0.5rem 0.75rem;
            border-radius: 4px;
            font-size: 0.9rem;
        }
        #goal:focus { outline: none; border-color: ${JADE}; }
        #send {
            background: ${JADE};
            color: ${HIGHLIGHT};
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
        }
        #send:hover { background: #0F766E; }
        #send:disabled { opacity: 0.6; cursor: not-allowed; }
        .thinking { color: ${MUTED}; font-style: italic; }
    </style>
</head>
<body>
    <div class="header">OpenFlux Composer — by VibeCoders United. Describe a goal; the agent will plan and execute.</div>
    <div class="messages" id="messages"></div>
    <div class="input-area">
        <input type="text" id="goal" placeholder="e.g. Refactor the login logic, Add error handling to API routes" />
        <button id="send">Send</button>
    </div>
    <script>
        const vscode = acquireVsCodeApi();
        const messagesEl = document.getElementById('messages');
        const goalInput = document.getElementById('goal');
        const sendBtn = document.getElementById('send');

        function addMessage(role, content, isHtml) {
            const div = document.createElement('div');
            div.className = 'msg ' + role;
            div.innerHTML = '<div class="role">' + (role === 'user' ? 'You' : 'OpenFlux Agent') + '</div>' + (isHtml ? content : escapeHtml(content));
            messagesEl.appendChild(div);
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }

        function escapeHtml(s) {
            const div = document.createElement('div');
            div.textContent = s;
            return div.innerHTML;
        }

        function addThinking() {
            const div = document.createElement('div');
            div.className = 'msg assistant thinking';
            div.id = 'thinking';
            div.textContent = 'Thinking…';
            messagesEl.appendChild(div);
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }

        function removeThinking() {
            const el = document.getElementById('thinking');
            if (el) el.remove();
        }

        function formatResponse(data) {
            let html = '';
            if (data.status) html += '<p class="status">Status: ' + escapeHtml(data.status) + '</p>';
            if (data.message) html += '<p>' + escapeHtml(data.message) + '</p>';
            if (data.iterations != null) html += '<p>Iterations: ' + data.iterations + '</p>';
            if (data.plan && data.plan.steps && data.plan.steps.length) {
                html += '<p><strong>Plan steps:</strong></p><pre>' + escapeHtml(JSON.stringify(data.plan.steps, null, 2)) + '</pre>';
            }
            if (data.plan && data.plan.test_command) html += '<p>Test: <code>' + escapeHtml(data.plan.test_command) + '</code></p>';
            return html || '<p>' + escapeHtml(JSON.stringify(data)) + '</p>';
        }

        sendBtn.addEventListener('click', send);
        goalInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') send(); });

        function send() {
            const goal = goalInput.value.trim();
            if (!goal) return;
            goalInput.value = '';
            addMessage('user', goal, false);
            addThinking();
            sendBtn.disabled = true;
            vscode.postMessage({ type: 'send', goal });
        }

        window.addEventListener('message', (e) => {
            const msg = e.data;
            removeThinking();
            sendBtn.disabled = false;
            if (msg.type === 'response') {
                addMessage('assistant', formatResponse(msg), true);
            } else if (msg.type === 'error') {
                addMessage('assistant', '<p class="error">' + escapeHtml(msg.message || String(msg)) + '</p>', true);
            }
        });
    </script>
</body>
</html>`;
}

let composerPanel: vscode.WebviewPanel | undefined;

export function createComposerPanel(
    context: vscode.ExtensionContext,
    client: { executeAgentTask: (goal: string, workspacePath: string, maxIterations?: number) => Promise<any> },
    callbacks?: { onAgentStart?: () => void; onAgentEnd?: () => void }
): void {
    if (composerPanel) {
        composerPanel.reveal();
        return;
    }

    const panel = vscode.window.createWebviewPanel(
        "openfluxComposer",
        "OpenFlux Composer",
        vscode.ViewColumn.Beside,
        { enableScripts: true }
    );
    composerPanel = panel;
    panel.webview.html = getComposerHtml();

    panel.onDidDispose(() => {
        composerPanel = undefined;
    });

    panel.webview.onDidReceiveMessage(async (msg: { type: string; goal?: string }) => {
        if (msg.type !== "send" || !msg.goal) return;

        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            panel.webview.postMessage({
                type: "error",
                message: "No workspace folder open. Open a folder first.",
            });
            return;
        }

        const workspacePath = workspaceFolders[0].uri.fsPath;

        callbacks?.onAgentStart?.();
        try {
            const result = await client.executeAgentTask(msg.goal, workspacePath, 5);
            panel.webview.postMessage({ type: "response", ...result });
        } catch (err: any) {
            panel.webview.postMessage({
                type: "error",
                message: err.message || err.response?.data?.detail || String(err),
            });
        } finally {
            callbacks?.onAgentEnd?.();
        }
    });
}
