import * as vscode from "vscode";
import { OpenCodeClient } from "./client";

export interface IndexingProviderOptions {
    onIndexingStart?: () => void;
    onIndexingEnd?: () => void;
}

export class IndexingProvider {
    constructor(
        private client: OpenCodeClient,
        private options: IndexingProviderOptions = {}
    ) {}

    async indexWorkspace(): Promise<void> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showErrorMessage("No workspace folder open");
            return;
        }

        const workspacePath = workspaceFolders[0].uri.fsPath;

        // Check if server is running
        const isHealthy = await this.client.healthCheck();
        if (!isHealthy) {
            vscode.window.showErrorMessage(
                "OpenCode API server is not running. Please start it with: ./scripts/start_server.sh"
            );
            return;
        }

        this.options.onIndexingStart?.();
        vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: "Indexing codebase",
                cancellable: false,
            },
            async (progress) => {
                progress.report({ increment: 0, message: "Starting index..." });

                try {
                    const result = await this.client.indexCodebase(workspacePath);
                    progress.report({ increment: 100, message: "Indexing started" });

                    vscode.window.showInformationMessage(
                        `Indexing started: ${result.message}`
                    );
                } catch (error: any) {
                    vscode.window.showErrorMessage(
                        `Failed to index codebase: ${error.message}`
                    );
                } finally {
                    this.options.onIndexingEnd?.();
                }
            }
        );
    }

    async searchCodebase(): Promise<void> {
        const query = await vscode.window.showInputBox({
            prompt: "Search codebase",
            placeHolder: "Enter your search query...",
        });

        if (!query) {
            return;
        }

        // Check if server is running
        const isHealthy = await this.client.healthCheck();
        if (!isHealthy) {
            vscode.window.showErrorMessage(
                "OpenCode API server is not running. Please start it with: ./scripts/start_server.sh"
            );
            return;
        }

        vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: "Searching codebase",
                cancellable: false,
            },
            async (progress) => {
                progress.report({ increment: 0, message: "Searching..." });

                try {
                    const result = await this.client.searchCodebase(query);
                    progress.report({ increment: 100 });

                    // Show results in a new document
                    const doc = await vscode.workspace.openTextDocument({
                        content: this.formatSearchResults(result),
                        language: "markdown",
                    });
                    await vscode.window.showTextDocument(doc);
                } catch (error: any) {
                    vscode.window.showErrorMessage(
                        `Search failed: ${error.message}`
                    );
                }
            }
        );
    }

    private formatSearchResults(result: any): string {
        let content = `# Search Results\n\n`;
        content += `Query: "${result.query}"\n`;
        content += `Found ${result.count} results\n\n`;
        content += `---\n\n`;

        for (const item of result.results || []) {
            content += `## ${item.file_path}\n\n`;
            content += `**Lines ${item.start_line}-${item.end_line}** (${item.node_type})\n\n`;
            content += `\`\`\`${item.language}\n${item.content}\n\`\`\`\n\n`;
            content += `---\n\n`;
        }

        return content;
    }
}
