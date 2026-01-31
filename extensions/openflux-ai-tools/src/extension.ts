import * as vscode from "vscode";
import { OpenFluxClient } from "./client";
import { IndexingProvider } from "./indexing";
import { AgentProvider } from "./agent";
import { createWelcomePanel, REPO_DOCS } from "./welcome";
import { createComposerPanel } from "./composer";

let client: OpenFluxClient;
let indexingProvider: IndexingProvider;
let agentProvider: AgentProvider;
let statusBarItem: vscode.StatusBarItem;

type StatusState = "idle" | "indexing" | "agent" | "offline";

let statusState: StatusState = "idle";

function updateStatusBar(apiUrl: string): void {
    if (!statusBarItem) return;
    if (statusState === "offline") {
        statusBarItem.text = "$(warning) OpenFlux (backend offline)";
        statusBarItem.tooltip = "Backend not running. Run: ./scripts/start_server.sh — or use command: OpenFlux: Show backend instructions";
        statusBarItem.command = "openflux.showBackendInstructions";
    } else if (statusState === "indexing") {
        statusBarItem.text = "$(sync~spin) OpenFlux (indexing)";
        statusBarItem.tooltip = "Indexing codebase — Jade = in progress";
        statusBarItem.command = "openflux.indexCodebase";
    } else if (statusState === "agent") {
        statusBarItem.text = "$(run) OpenFlux (agent)";
        statusBarItem.tooltip = "Agent running — Jade = active";
        statusBarItem.command = "openflux.startAgent";
    } else {
        statusBarItem.text = "$(check) OpenFlux";
        statusBarItem.tooltip = `OpenFlux AI Tools — backend at ${apiUrl} (Ready)`;
        statusBarItem.command = "openflux.searchCodebase";
    }
    statusBarItem.show();
}

async function updateBackendStatus(apiUrl: string): Promise<void> {
    const testClient = new OpenFluxClient(apiUrl);
    const ok = await testClient.healthCheck();
    if (!ok) statusState = "offline";
    else if (statusState === "offline") statusState = "idle";
    updateStatusBar(apiUrl);
}

export function activate(context: vscode.ExtensionContext) {
    console.log("OpenFlux AI Tools extension is now active!");

    const apiUrl = vscode.workspace.getConfiguration("openflux").get<string>("apiUrl", "http://localhost:8000");
    client = new OpenFluxClient(apiUrl);

    const onIndexingStart = () => { statusState = "indexing"; updateStatusBar(apiUrl); };
    const onIndexingEnd = () => { statusState = "idle"; updateBackendStatus(apiUrl); };
    const onAgentStart = () => { statusState = "agent"; updateStatusBar(apiUrl); };
    const onAgentEnd = () => { statusState = "idle"; updateBackendStatus(apiUrl); };

    indexingProvider = new IndexingProvider(client, { onIndexingStart, onIndexingEnd });
    agentProvider = new AgentProvider(client, { onAgentStart, onAgentEnd });

    const indexCommand = vscode.commands.registerCommand("openflux.indexCodebase", () => indexingProvider.indexWorkspace());
    const agentCommand = vscode.commands.registerCommand("openflux.startAgent", () => agentProvider.startAgent());
    const searchCommand = vscode.commands.registerCommand("openflux.searchCodebase", () => indexingProvider.searchCodebase());

    const showBackendInstructionsCommand = vscode.commands.registerCommand("openflux.showBackendInstructions", () => {
        vscode.window.showInformationMessage(
            "OpenFlux backend: from the repo root run ./scripts/start_server.sh (or install as service — see docs/BACKEND.md)."
        );
    });

    const showWelcomeCommand = vscode.commands.registerCommand("openflux.showWelcome", () => {
        createWelcomePanel(context);
    });

    const openDocumentationCommand = vscode.commands.registerCommand("openflux.openDocumentation", () => {
        vscode.env.openExternal(vscode.Uri.parse(REPO_DOCS));
    });

    const openComposerCommand = vscode.commands.registerCommand("openflux.openComposer", () => {
        createComposerPanel(context, client, {
            onAgentStart: () => { statusState = "agent"; updateStatusBar(apiUrl); },
            onAgentEnd: () => updateBackendStatus(apiUrl),
        });
    });

    context.subscriptions.push(
        indexCommand,
        agentCommand,
        searchCommand,
        showBackendInstructionsCommand,
        showWelcomeCommand,
        openDocumentationCommand,
        openComposerCommand
    );

    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    context.subscriptions.push(statusBarItem);
    updateBackendStatus(apiUrl);

    const welcomeShown = context.globalState.get<boolean>("openflux.welcomeShown");
    if (!welcomeShown) {
        context.globalState.update("openflux.welcomeShown", true);
        createWelcomePanel(context);
    }

    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration((e) => {
            if (e.affectsConfiguration("openflux.apiUrl")) {
                const newUrl = vscode.workspace.getConfiguration("openflux").get<string>("apiUrl", "http://localhost:8000");
                updateBackendStatus(newUrl);
            }
        })
    );
}

export function deactivate() {
    // Cleanup
}
