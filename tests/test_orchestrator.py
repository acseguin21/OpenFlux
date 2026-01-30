"""
Basic tests for the agent orchestrator.
"""
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.orchestrator import AgentOrchestrator, EditInstruction, TaskPlan, TaskStatus
    ORCHESTRATOR_AVAILABLE = True
except ImportError as e:
    ORCHESTRATOR_AVAILABLE = False
    print(f"Warning: Could not import AgentOrchestrator: {e}")


class TestOrchestrator(unittest.TestCase):
    """Test cases for AgentOrchestrator."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not ORCHESTRATOR_AVAILABLE:
            self.skipTest("Orchestrator dependencies not available")
        
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.test_dir) / "workspace"
        self.workspace_path.mkdir()
        
        self.model_config = {
            "planning_model": "test-model",
            "editing_model": "test-model",
            "verification_model": "test-model",
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_orchestrator_initialization(self):
        """Test that orchestrator can be initialized."""
        orchestrator = AgentOrchestrator(
            workspace_path=str(self.workspace_path),
            model_config=self.model_config
        )
        self.assertIsNotNone(orchestrator)
        self.assertEqual(str(orchestrator.workspace_path), str(self.workspace_path))
    
    def test_edit_instruction_creation(self):
        """Test EditInstruction dataclass."""
        edit = EditInstruction(
            file_path="test.py",
            operation="create",
            content="print('hello')"
        )
        self.assertEqual(edit.file_path, "test.py")
        self.assertEqual(edit.operation, "create")
        self.assertEqual(edit.content, "print('hello')")
    
    def test_apply_edit_create(self):
        """Test applying a create edit."""
        orchestrator = AgentOrchestrator(
            workspace_path=str(self.workspace_path),
            model_config=self.model_config
        )
        
        edit = EditInstruction(
            file_path="test.py",
            operation="create",
            content="print('hello')"
        )
        
        result = orchestrator.apply_edit(edit, dry_run=False)
        self.assertTrue(result)
        
        test_file = self.workspace_path / "test.py"
        self.assertTrue(test_file.exists())
        self.assertEqual(test_file.read_text(), "print('hello')")
    
    def test_apply_edit_modify(self):
        """Test applying a modify edit."""
        orchestrator = AgentOrchestrator(
            workspace_path=str(self.workspace_path),
            model_config=self.model_config
        )
        
        # Create initial file
        test_file = self.workspace_path / "test.py"
        test_file.write_text("line1\nline2\nline3\nline4\n")
        
        edit = EditInstruction(
            file_path="test.py",
            operation="modify",
            start_line=2,
            end_line=3,
            replacement="new_line"
        )
        
        result = orchestrator.apply_edit(edit, dry_run=False)
        self.assertTrue(result)
        
        content = test_file.read_text()
        self.assertIn("new_line", content)
        self.assertNotIn("line2", content)
    
    def test_apply_edit_delete(self):
        """Test applying a delete edit."""
        orchestrator = AgentOrchestrator(
            workspace_path=str(self.workspace_path),
            model_config=self.model_config
        )
        
        # Create file
        test_file = self.workspace_path / "test.py"
        test_file.write_text("content")
        
        edit = EditInstruction(
            file_path="test.py",
            operation="delete"
        )
        
        result = orchestrator.apply_edit(edit, dry_run=False)
        self.assertTrue(result)
        self.assertFalse(test_file.exists())


if __name__ == "__main__":
    unittest.main()
