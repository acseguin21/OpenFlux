"""
FastAPI backend server for OpenCode.
Provides REST API for indexing, search, and agent orchestration.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from pathlib import Path

from core.indexer import IndexingEngine
from core.orchestrator import AgentOrchestrator, TaskPlan, TaskStatus


app = FastAPI(title="OpenCode API", version="0.1.0")

# CORS middleware for the editor extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to the editor extension origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances (initialized on startup)
indexer: Optional[IndexingEngine] = None
orchestrator: Optional[AgentOrchestrator] = None


# Request/Response models
class IndexRequest(BaseModel):
    workspace_path: str
    use_ollama: bool = True
    embedding_model: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    top_k: int = 10


class AgentRequest(BaseModel):
    goal: str
    workspace_path: str
    max_iterations: int = 5


class AgentResponse(BaseModel):
    status: str
    message: str
    iterations: Optional[int] = None
    plan: Optional[Dict] = None


@app.on_event("startup")
async def startup_event():
    """Initialize global services."""
    global indexer, orchestrator
    # These will be initialized per-request with workspace paths
    print("OpenCode API server started")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "OpenCode API"}


@app.post("/api/index")
async def index_codebase(request: IndexRequest, background_tasks: BackgroundTasks):
    """
    Index a codebase using Tree-sitter and vector embeddings.
    """
    global indexer
    
    try:
        workspace_path = Path(request.workspace_path)
        if not workspace_path.exists():
            raise HTTPException(status_code=400, detail="Workspace path does not exist")
        
        vector_db_path = workspace_path / ".opencode" / "index"
        
        indexer = IndexingEngine(
            workspace_path=str(workspace_path),
            vector_db_path=str(vector_db_path),
            embedding_model=request.embedding_model
        )
        
        # Run indexing in background
        background_tasks.add_task(indexer.index, use_ollama=request.use_ollama)
        
        return {
            "status": "started",
            "message": "Indexing started in background",
            "workspace": str(workspace_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search")
async def search_codebase(request: SearchRequest):
    """
    Search the indexed codebase for similar code chunks.
    """
    global indexer
    
    if indexer is None:
        raise HTTPException(status_code=400, detail="Indexer not initialized. Run /api/index first.")
    
    try:
        results = indexer.search(request.query, top_k=request.top_k)
        return {
            "query": request.query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent/execute", response_model=AgentResponse)
async def execute_agent_task(request: AgentRequest):
    """
    Execute an agent task with plan-execute-verify loop.
    """
    global indexer, orchestrator
    
    try:
        workspace_path = Path(request.workspace_path)
        if not workspace_path.exists():
            raise HTTPException(status_code=400, detail="Workspace path does not exist")
        
        # Initialize orchestrator if needed
        if orchestrator is None or str(orchestrator.workspace_path) != str(workspace_path):
            model_config = {
                "planning_model": os.getenv("OPENCODE_PLANNING_MODEL", "llama3.1:8b"),
                "editing_model": os.getenv("OPENCODE_EDITING_MODEL", "llama3.1:8b"),
                "verification_model": os.getenv("OPENCODE_VERIFICATION_MODEL", "llama3.1:8b"),
                "use_shadow_branch": True,
            }
            
            # Try to reuse existing indexer if workspace matches
            if indexer and str(indexer.workspace_path) == str(workspace_path):
                orchestrator = AgentOrchestrator(
                    workspace_path=str(workspace_path),
                    model_config=model_config,
                    indexer=indexer
                )
            else:
                orchestrator = AgentOrchestrator(
                    workspace_path=str(workspace_path),
                    model_config=model_config,
                    indexer=None
                )
        
        # Execute the task
        result = orchestrator.run_loop(request.goal, max_iterations=request.max_iterations)
        
        # Serialize plan properly
        plan_dict = None
        if result.get("plan"):
            plan = result["plan"]
            plan_dict = {
                "goal": plan.goal,
                "steps": [
                    {
                        "file_path": step.file_path,
                        "operation": step.operation,
                        "content": step.content,
                        "start_line": step.start_line,
                        "end_line": step.end_line,
                        "replacement": step.replacement,
                        "metadata": step.metadata or {},
                    }
                    for step in plan.steps
                ],
                "test_command": plan.test_command,
                "verification_commands": plan.verification_commands or [],
            }
        
        return AgentResponse(
            status=result["status"],
            message=result["message"],
            iterations=result.get("iterations"),
            plan=plan_dict
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def get_status():
    """Get current status of services."""
    return {
        "indexer_initialized": indexer is not None,
        "orchestrator_initialized": orchestrator is not None,
        "indexer_workspace": str(indexer.workspace_path) if indexer else None,
        "orchestrator_workspace": str(orchestrator.workspace_path) if orchestrator else None,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
