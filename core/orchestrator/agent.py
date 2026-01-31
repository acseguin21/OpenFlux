import subprocess
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import ollama
from core.indexer import IndexingEngine


class TaskStatus(Enum):
    """Status of an agent task."""
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    SUCCESS = "success"
    FAILED = "failed"
    REVIEW = "review"


@dataclass
class EditInstruction:
    """Represents a file edit instruction."""
    file_path: str
    operation: str  # "create", "modify", "delete"
    content: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    replacement: Optional[str] = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class TaskPlan:
    """Represents a plan for completing a user goal."""
    goal: str
    steps: List[EditInstruction]
    test_command: Optional[str] = None
    verification_commands: List[str] = None
    
    def __post_init__(self):
        if self.verification_commands is None:
            self.verification_commands = []


class AgentOrchestrator:
    """
    OpenFlux Agent Orchestrator:
    Manages the 'Self-Correction Loop' (Plan-Execute-Verify).
    """
    
    def __init__(
        self, 
        workspace_path: str,
        model_config: dict,
        indexer: Optional[IndexingEngine] = None
    ):
        self.workspace_path = Path(workspace_path)
        self.model_config = model_config
        self.indexer = indexer
        
        # Model configuration
        self.planning_model = model_config.get("planning_model", "llama3.1:8b")
        self.editing_model = model_config.get("editing_model", "llama3.1:8b")
        self.verification_model = model_config.get("verification_model", "llama3.1:8b")
        
        # Use shadow branch for safe edits
        self.use_shadow_branch = model_config.get("use_shadow_branch", True)
        self.shadow_branch = "openflux-shadow"
    
    def plan_task(self, user_goal: str, context: Optional[List[Dict]] = None) -> TaskPlan:
        """
        Breaks a high-level goal into specific file edits using AI planning.
        
        Args:
            user_goal: High-level description of what the user wants to accomplish
            context: Optional code context from indexer search
        
        Returns:
            TaskPlan with steps to execute
        """
        # Build context prompt
        context_str = ""
        if context:
            context_str = "\n\nRelevant code context:\n"
            for item in context[:5]:  # Top 5 results
                context_str += f"\n--- {item.get('file_path', 'unknown')} ---\n"
                context_str += item.get('content', '')[:500] + "\n"
        
        # Create planning prompt
        planning_prompt = f"""You are an expert software engineer planning a code change.

User Goal: {user_goal}
{context_str}

Break this goal down into specific file edits. For each edit, provide:
1. file_path: relative path from workspace root
2. operation: "create", "modify", or "delete"
3. For modify: start_line, end_line, and replacement content
4. For create: full content
5. For delete: just file_path

Respond ONLY with valid JSON in this format:
{{
    "steps": [
        {{
            "file_path": "path/to/file.py",
            "operation": "modify",
            "start_line": 10,
            "end_line": 15,
            "replacement": "new code here"
        }}
    ],
    "test_command": "pytest tests/",
    "verification_commands": ["python -m pytest", "flake8"]
}}
"""
        
        try:
            # Call Ollama for planning
            response = ollama.chat(
                model=self.planning_model,
                messages=[
                    {"role": "system", "content": "You are a precise software engineering planner. Always respond with valid JSON only."},
                    {"role": "user", "content": planning_prompt}
                ],
                format="json"
            )
            
            plan_data = json.loads(response["message"]["content"])
            
            # Convert to TaskPlan
            steps = [
                EditInstruction(**step) for step in plan_data.get("steps", [])
            ]
            
            return TaskPlan(
                goal=user_goal,
                steps=steps,
                test_command=plan_data.get("test_command"),
                verification_commands=plan_data.get("verification_commands", [])
            )
        except Exception as e:
            print(f"Error in planning: {e}")
            # Fallback: create a simple plan
            return TaskPlan(
                goal=user_goal,
                steps=[],
                test_command=None
            )
    
    def apply_edit(self, edit: EditInstruction, dry_run: bool = False) -> bool:
        """
        Applies an edit instruction to the file system.
        
        Args:
            edit: EditInstruction to apply
            dry_run: If True, don't actually apply the edit
        
        Returns:
            True if successful, False otherwise
        """
        file_path = self.workspace_path / edit.file_path
        
        try:
            if edit.operation == "create":
                if not dry_run:
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(file_path, "w") as f:
                        f.write(edit.content or "")
                return True
            
            elif edit.operation == "modify":
                if not file_path.exists():
                    print(f"Warning: File {file_path} does not exist for modification")
                    return False
                
                with open(file_path, "r") as f:
                    lines = f.readlines()
                
                if edit.start_line and edit.end_line and edit.replacement:
                    # Replace lines
                    # Handle multi-line replacement
                    replacement_lines = edit.replacement.split("\n")
                    replacement_lines = [line + "\n" if i < len(replacement_lines) - 1 else line 
                                       for i, line in enumerate(replacement_lines)]
                    if replacement_lines and not replacement_lines[-1].endswith("\n"):
                        replacement_lines[-1] += "\n"
                    
                    new_lines = (
                        lines[:edit.start_line - 1] +
                        replacement_lines +
                        lines[edit.end_line:]
                    )
                    
                    if not dry_run:
                        with open(file_path, "w") as f:
                            f.writelines(new_lines)
                    return True
                elif edit.content:
                    # Replace entire file
                    if not dry_run:
                        with open(file_path, "w") as f:
                            f.write(edit.content)
                    return True
            
            elif edit.operation == "delete":
                if not dry_run and file_path.exists():
                    file_path.unlink()
                return True
            
            return False
        except Exception as e:
            print(f"Error applying edit to {file_path}: {e}")
            return False
    
    def verify_changes(self, test_command: Optional[str] = None, verification_commands: Optional[List[str]] = None) -> Tuple[bool, str]:
        """
        Runs verification commands and returns success status.
        
        Args:
            test_command: Command to run tests
            verification_commands: List of commands to verify changes
        
        Returns:
            Tuple of (success: bool, output: str)
        """
        all_commands = []
        if test_command:
            all_commands.append(test_command)
        if verification_commands:
            all_commands.extend(verification_commands)
        
        if not all_commands:
            return True, "No verification commands provided"
        
        for cmd in all_commands:
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=str(self.workspace_path),
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result.returncode != 0:
                    return False, f"Command '{cmd}' failed:\n{result.stderr}\n{result.stdout}"
            except subprocess.TimeoutExpired:
                return False, f"Command '{cmd}' timed out"
            except Exception as e:
                return False, f"Error running '{cmd}': {e}"
        
        return True, "All verification commands passed"
    
    def run_loop(self, user_goal: str, max_iterations: int = 5) -> Dict:
        """
        Orchestrates the planning, execution, and verification loop.
        
        Args:
            user_goal: High-level goal to accomplish
            max_iterations: Maximum number of retry iterations
        
        Returns:
            Dictionary with status and results
        """
        print(f"Executing goal: {user_goal}")
        
        # Get context from indexer if available
        context = None
        if self.indexer:
            try:
                context = self.indexer.search(user_goal, top_k=5)
            except Exception as e:
                print(f"Warning: Could not get context from indexer: {e}")
        
        # Plan the task
        plan = self.plan_task(user_goal, context=context)
        
        if not plan.steps:
            return {
                "status": TaskStatus.FAILED.value,
                "message": "Planning failed: No steps generated",
                "plan": plan
            }
        
        print(f"Plan created with {len(plan.steps)} steps")
        
        # Execute plan with verification loop
        for iteration in range(max_iterations):
            print(f"\n--- Iteration {iteration + 1}/{max_iterations} ---")
            
            # Apply all edits
            success_count = 0
            for i, step in enumerate(plan.steps):
                print(f"Applying step {i + 1}/{len(plan.steps)}: {step.operation} {step.file_path}")
                if self.apply_edit(step):
                    success_count += 1
                else:
                    print(f"Warning: Failed to apply step {i + 1}")
            
            if success_count == 0:
                return {
                    "status": TaskStatus.FAILED.value,
                    "message": "All edit steps failed",
                    "plan": plan
                }
            
            # Verify changes
            print("Verifying changes...")
            success, output = self.verify_changes(
                test_command=plan.test_command,
                verification_commands=plan.verification_commands
            )
            
            if success:
                return {
                    "status": TaskStatus.SUCCESS.value,
                    "message": "Task completed successfully",
                    "plan": plan,
                    "iterations": iteration + 1
                }
            else:
                print(f"Verification failed: {output}")
                
                # If not last iteration, try to fix
                if iteration < max_iterations - 1:
                    # Use AI to generate fix based on error
                    fix_prompt = f"""The following verification failed:
{output}

Original goal: {user_goal}

Generate a fix plan. Respond with JSON in the same format as before."""
                    
                    try:
                        response = ollama.chat(
                            model=self.editing_model,
                            messages=[
                                {"role": "system", "content": "You are a debugging assistant. Respond with valid JSON only."},
                                {"role": "user", "content": fix_prompt}
                            ],
                            format="json"
                        )
                        fix_data = json.loads(response["message"]["content"])
                        plan.steps = [EditInstruction(**step) for step in fix_data.get("steps", [])]
                        print("Generated fix plan, retrying...")
                    except Exception as e:
                        print(f"Error generating fix: {e}")
                        break
        
        return {
            "status": TaskStatus.FAILED.value,
            "message": f"Task failed after {max_iterations} iterations",
            "plan": plan,
            "last_error": output
        }
