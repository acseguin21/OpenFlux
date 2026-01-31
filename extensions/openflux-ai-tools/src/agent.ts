import * as vscode from "vscode";
import { OpenFluxClient } from "./client";

export interface AgentProviderOptions {
    onAgentStart?: () => void;
    onAgentEnd?: () => void;
}

export class AgentProvider {
    constructor(
        private client: OpenFluxClient,
        private options: AgentProviderOptions = {}
    ) {}

    async startAgent(): Promise<void> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showErrorMessage("No workspace folder open");
            return;
        }

        const workspacePath = workspaceFolders[0].uri.fsPath;

        // Get goal from user
        const goal = await vscode.window.showInputBox({
            prompt: "What would you like the agent to do?",
            placeHolder: "e.g., Refactor the login logic, Add error handling to API routes",
        });

        if (!goal) {
            return;
        }

        // Check if server is running
        const isHealthy = await this.client.healthCheck();
        if (!isHealthy) {
            vscode.window.showErrorMessage(
                "OpenFlux API server is not running. Please start it with: ./scripts/start_server.sh"
            );
            return;
        }

        this.options.onAgentStart?.();
        vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: "Agent executing task",
                cancellable: false,
            },
            async (progress) => {
                progress.report({ increment: 0, message: "Planning..." });

                try {
                    const result = await this.client.executeAgentTask(
                        goal,
                        workspacePath
                    );

                    progress.report({ increment: 100 });

                    if (result.status === "success") {
                        vscode.window.showInformationMessage(
                            `Agent completed successfully in ${result.iterations} iteration(s)!`
                        );
                    } else {
                        vscode.window.showWarningMessage(
                            `Agent task ${result.status}: ${result.message}`
                        );
                    }

                    // Show plan in output channel
                    const outputChannel = vscode.window.createOutputChannel("OpenFlux Agent");
                    outputChannel.appendLine(`Goal: ${goal}`);
                    outputChannel.appendLine(`Status: ${result.status}`);
                    outputChannel.appendLine(`Message: ${result.message}`);
                    if (result.plan) {
                        outputChannel.appendLine(`\nPlan:`);
                        outputChannel.appendLine(JSON.stringify(result.plan, null, 2));
                    }
                    outputChannel.show();
                } catch (error: any) {
                    vscode.window.showErrorMessage(
                        `Agent execution failed: ${error.message}`
                    );
                } finally {
                    this.options.onAgentEnd?.();
                }
            }
        );
    }
}
