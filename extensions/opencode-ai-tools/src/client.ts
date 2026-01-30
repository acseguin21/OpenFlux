import axios, { AxiosInstance } from "axios";

export class OpenCodeClient {
    private client: AxiosInstance;

    constructor(baseURL: string) {
        this.client = axios.create({
            baseURL,
            timeout: 300000, // 5 minutes for long-running operations
            headers: {
                "Content-Type": "application/json",
            },
        });
    }

    async healthCheck(): Promise<boolean> {
        try {
            const response = await this.client.get("/");
            return response.data.status === "ok";
        } catch (error) {
            return false;
        }
    }

    async indexCodebase(workspacePath: string, useOllama: boolean = true): Promise<any> {
        const response = await this.client.post("/api/index", {
            workspace_path: workspacePath,
            use_ollama: useOllama,
        });
        return response.data;
    }

    async searchCodebase(query: string, topK: number = 10): Promise<any> {
        const response = await this.client.post("/api/search", {
            query,
            top_k: topK,
        });
        return response.data;
    }

    async executeAgentTask(
        goal: string,
        workspacePath: string,
        maxIterations: number = 5
    ): Promise<any> {
        const response = await this.client.post("/api/agent/execute", {
            goal,
            workspace_path: workspacePath,
            max_iterations: maxIterations,
        });
        return response.data;
    }

    async getStatus(): Promise<any> {
        const response = await this.client.get("/api/status");
        return response.data;
    }
}
