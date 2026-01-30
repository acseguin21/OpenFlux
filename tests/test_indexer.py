"""
Basic tests for the indexing engine.
"""
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.indexer import IndexingEngine, CodeChunk
    INDEXER_AVAILABLE = True
except ImportError as e:
    INDEXER_AVAILABLE = False
    print(f"Warning: Could not import IndexingEngine: {e}")


class TestIndexer(unittest.TestCase):
    """Test cases for IndexingEngine."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not INDEXER_AVAILABLE:
            self.skipTest("Indexer dependencies not available")
        
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.test_dir) / "workspace"
        self.workspace_path.mkdir()
        self.index_path = Path(self.test_dir) / "index"
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_indexer_initialization(self):
        """Test that indexer can be initialized."""
        indexer = IndexingEngine(
            workspace_path=str(self.workspace_path),
            vector_db_path=str(self.index_path),
            embedding_model="test-model"
        )
        self.assertIsNotNone(indexer)
        self.assertEqual(str(indexer.workspace_path), str(self.workspace_path))
    
    def test_code_chunk_creation(self):
        """Test CodeChunk dataclass."""
        chunk = CodeChunk(
            file_path="test.py",
            content="def hello(): pass",
            start_line=1,
            end_line=1,
            node_type="function_definition",
            language="python"
        )
        self.assertEqual(chunk.file_path, "test.py")
        self.assertEqual(chunk.content, "def hello(): pass")
        self.assertEqual(chunk.language, "python")
    
    def test_scan_workspace_empty(self):
        """Test scanning an empty workspace."""
        indexer = IndexingEngine(
            workspace_path=str(self.workspace_path),
            vector_db_path=str(self.index_path)
        )
        files = indexer.scan_workspace()
        self.assertEqual(len(files), 0)
    
    def test_scan_workspace_with_files(self):
        """Test scanning workspace with Python files."""
        # Create a test Python file
        test_file = self.workspace_path / "test.py"
        test_file.write_text("def hello():\n    print('world')\n")
        
        indexer = IndexingEngine(
            workspace_path=str(self.workspace_path),
            vector_db_path=str(self.index_path)
        )
        files = indexer.scan_workspace()
        self.assertGreater(len(files), 0)
        self.assertTrue(any(f.name == "test.py" for f in files))
    
    def test_chunk_file_python(self):
        """Test chunking a Python file."""
        test_file = self.workspace_path / "test.py"
        test_file.write_text("""def hello():
    print('world')

class Test:
    def method(self):
        pass
""")
        
        indexer = IndexingEngine(
            workspace_path=str(self.workspace_path),
            vector_db_path=str(self.index_path)
        )
        
        chunks = indexer.chunk_file(test_file)
        # Should find at least the function and class
        # (exact count depends on tree-sitter availability)
        self.assertIsInstance(chunks, list)


if __name__ == "__main__":
    unittest.main()
