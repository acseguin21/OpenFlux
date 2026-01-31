import os
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

try:
    import tree_sitter_python as tspython
except ImportError:
    tspython = None

try:
    import tree_sitter_javascript as tsjavascript
except ImportError:
    tsjavascript = None

try:
    import tree_sitter_typescript as tstypescript
except ImportError:
    tstypescript = None

from tree_sitter import Language, Parser, Node
import lancedb
import pyarrow as pa
import numpy as np


@dataclass
class CodeChunk:
    """Represents a semantically meaningful chunk of code."""
    file_path: str
    content: str
    start_line: int
    end_line: int
    node_type: str
    language: str
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        """Convert chunk to dictionary for storage."""
        return {
            "file_path": self.file_path,
            "content": self.content,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "node_type": self.node_type,
            "language": self.language,
            "metadata": self.metadata,
        }


class IndexingEngine:
    """
    OpenFlux Indexing Engine:
    Uses Tree-sitter for syntax-aware chunking and a local vector DB for retrieval.
    """
    
    # Supported file extensions mapped to their tree-sitter languages
    LANGUAGE_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
    }
    
    # Minimum lines for a chunk to be indexed
    MIN_CHUNK_LINES = 4
    
    def __init__(self, workspace_path: str, vector_db_path: str, embedding_model: Optional[str] = None):
        self.workspace_path = Path(workspace_path)
        self.vector_db_path = Path(vector_db_path)
        self.embedding_model = embedding_model or "nomic-embed-text"  # Default Ollama model
        
        # Initialize tree-sitter parsers
        self.parsers = self._init_parsers()
        
        # Initialize vector database
        self.db = self._init_vector_db()
        self.table = None
        
    def _init_parsers(self) -> Dict[str, Parser]:
        """Initialize tree-sitter parsers for supported languages."""
        parsers = {}
        
        # Python parser
        if tspython:
            try:
                py_lang = Language(tspython.language())
                parser = Parser()
                parser.set_language(py_lang)
                parsers["python"] = parser
            except Exception as e:
                print(f"Warning: Could not load Python parser: {e}")
        
        # JavaScript parser
        if tsjavascript:
            try:
                js_lang = Language(tsjavascript.language())
                parser = Parser()
                parser.set_language(js_lang)
                parsers["javascript"] = parser
            except Exception as e:
                print(f"Warning: Could not load JavaScript parser: {e}")
        
        # TypeScript parser
        if tstypescript:
            try:
                ts_lang = Language(tstypescript.language())
                parser = Parser()
                parser.set_language(ts_lang)
                parsers["typescript"] = parser
            except Exception as e:
                print(f"Warning: Could not load TypeScript parser: {e}")
        
        return parsers
    
    def _init_vector_db(self):
        """Initialize LanceDB connection."""
        db_path = self.vector_db_path / "openflux_index"
        db_path.mkdir(parents=True, exist_ok=True)
        return lancedb.connect(str(db_path))
    
    def _get_language(self, file_path: Path) -> Optional[str]:
        """Determine language from file extension."""
        ext = file_path.suffix.lower()
        return self.LANGUAGE_MAP.get(ext)
    
    def _should_index_file(self, file_path: Path) -> bool:
        """Check if file should be indexed based on .openfluxignore rules."""
        # Check for .openfluxignore file
        ignore_file = self.workspace_path / ".openfluxignore"
        if ignore_file.exists():
            with open(ignore_file, "r") as f:
                ignore_patterns = [line.strip() for line in f if line.strip()]
            
            file_str = str(file_path.relative_to(self.workspace_path))
            for pattern in ignore_patterns:
                if pattern in file_str or file_str.endswith(pattern):
                    return False
        
        # Default ignore patterns
        default_ignores = [
            ".git", "node_modules", "__pycache__", ".venv", "venv",
            "dist", "build", ".next", ".vscode", ".idea"
        ]
        file_str = str(file_path)
        for ignore in default_ignores:
            if ignore in file_str:
                return False
        
        return True
    
    def scan_workspace(self) -> List[Path]:
        """Scan workspace and return list of files to index."""
        files = []
        
        for root, dirs, filenames in os.walk(self.workspace_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if self._should_index_file(Path(root) / d)]
            
            for filename in filenames:
                file_path = Path(root) / filename
                if self._should_index_file(file_path) and self._get_language(file_path):
                    files.append(file_path)
        
        return files
    
    def _extract_chunks_from_node(
        self, 
        node: Node, 
        source_code: bytes, 
        file_path: Path,
        language: str
    ) -> List[CodeChunk]:
        """Recursively extract semantic chunks from a tree-sitter node."""
        chunks = []
        
        # Extract meaningful node types (functions, classes, methods, etc.)
        meaningful_types = {
            "python": ["function_definition", "class_definition", "decorated_definition"],
            "javascript": ["function_declaration", "class_declaration", "method_definition", "arrow_function"],
            "typescript": ["function_declaration", "class_declaration", "method_definition", "arrow_function"],
        }
        
        node_types = meaningful_types.get(language, [])
        
        if node.type in node_types:
            start_point = node.start_point
            end_point = node.end_point
            
            # Only include if it's large enough
            if end_point[0] - start_point[0] >= self.MIN_CHUNK_LINES:
                content = source_code[node.start_byte:node.end_byte].decode("utf-8")
                
                chunk = CodeChunk(
                    file_path=str(file_path.relative_to(self.workspace_path)),
                    content=content,
                    start_line=start_point[0] + 1,  # 1-indexed
                    end_line=end_point[0] + 1,
                    node_type=node.type,
                    language=language,
                    metadata={
                        "start_byte": node.start_byte,
                        "end_byte": node.end_byte,
                    }
                )
                chunks.append(chunk)
        
        # Recursively process children
        for child in node.children:
            chunks.extend(self._extract_chunks_from_node(child, source_code, file_path, language))
        
        return chunks
    
    def chunk_file(self, file_path: Path) -> List[CodeChunk]:
        """Parse a file and extract semantic chunks using tree-sitter."""
        language = self._get_language(file_path)
        if not language or language not in self.parsers:
            return []
        
        try:
            with open(file_path, "rb") as f:
                source_code = f.read()
            
            parser = self.parsers[language]
            tree = parser.parse(source_code)
            
            if tree.root_node:
                chunks = self._extract_chunks_from_node(
                    tree.root_node, 
                    source_code, 
                    file_path,
                    language
                )
                return chunks
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return []
    
    def generate_embeddings(self, chunks: List[CodeChunk], use_ollama: bool = True) -> List[np.ndarray]:
        """Generate embeddings for code chunks using Ollama or cloud API."""
        embeddings = []
        
        if use_ollama:
            try:
                import ollama
                
                for chunk in chunks:
                    # Use Ollama to generate embedding
                    response = ollama.embeddings(
                        model=self.embedding_model,
                        prompt=chunk.content
                    )
                    embedding = np.array(response["embedding"], dtype=np.float32)
                    embeddings.append(embedding)
            except ImportError:
                print("Warning: ollama not installed, falling back to simple hash-based embeddings")
                # Fallback: use hash-based pseudo-embeddings (not ideal, but works)
                for chunk in chunks:
                    hash_obj = hashlib.sha256(chunk.content.encode())
                    # Convert hash to numpy array (take first 128 bytes, convert to float32)
                    hash_bytes = hash_obj.digest()[:128]
                    # Pad to 384 bytes if needed (384 * 4 bytes per float32 = 1536 bytes, but we only have 128)
                    # So we'll repeat the hash to fill
                    while len(hash_bytes) < 1536:  # 384 floats * 4 bytes
                        hash_bytes += hash_obj.digest()
                    embedding = np.frombuffer(hash_bytes[:1536], dtype=np.float32)
                    embeddings.append(embedding[:384])
        else:
            # TODO: Add cloud API support (e.g. third-party LLM/embedding providers)
            raise NotImplementedError("Cloud API embeddings not yet implemented")
        
        return embeddings
    
    def _create_table_schema(self):
        """Create the LanceDB table schema."""
        return pa.schema([
            pa.field("id", pa.string()),
            pa.field("file_path", pa.string()),
            pa.field("content", pa.string()),
            pa.field("start_line", pa.int32()),
            pa.field("end_line", pa.int32()),
            pa.field("node_type", pa.string()),
            pa.field("language", pa.string()),
            pa.field("vector", pa.list_(pa.float32())),
            pa.field("metadata", pa.string()),  # JSON string
        ])
    
    def index(self, use_ollama: bool = True):
        """Main entry point for indexing the entire codebase."""
        print(f"Indexing workspace: {self.workspace_path}")
        
        # Scan for files
        files = self.scan_workspace()
        print(f"Found {len(files)} files to index")
        
        all_chunks = []
        all_embeddings = []
        
        # Process each file
        for i, file_path in enumerate(files):
            if (i + 1) % 10 == 0:
                print(f"Processing file {i + 1}/{len(files)}...")
            
            chunks = self.chunk_file(file_path)
            if chunks:
                embeddings = self.generate_embeddings(chunks, use_ollama=use_ollama)
                all_chunks.extend(chunks)
                all_embeddings.extend(embeddings)
        
        print(f"Extracted {len(all_chunks)} chunks")
        
        # Store in vector database
        if all_chunks:
            self._store_in_db(all_chunks, all_embeddings)
            print(f"Indexed {len(all_chunks)} chunks in vector database")
    
    def _store_in_db(self, chunks: List[CodeChunk], embeddings: List[np.ndarray]):
        """Store chunks and embeddings in LanceDB."""
        import json
        
        # Prepare data
        data = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = hashlib.sha256(
                f"{chunk.file_path}:{chunk.start_line}:{chunk.end_line}".encode()
            ).hexdigest()
            
            data.append({
                "id": chunk_id,
                "file_path": chunk.file_path,
                "content": chunk.content,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "node_type": chunk.node_type,
                "language": chunk.language,
                "vector": embedding.tolist(),
                "metadata": json.dumps(chunk.metadata),
            })
        
        # Create or update table
        if self.table is None:
            self.table = self.db.create_table("code_index", data)
        else:
            self.table.add(data)
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search for similar code chunks."""
        if self.table is None:
            # Try to open existing table
            try:
                self.table = self.db.open_table("code_index")
            except Exception:
                raise ValueError("Index not found. Please run index() first.")
        
        # Generate query embedding
        query_chunk = CodeChunk(
            file_path="query",
            content=query,
            start_line=0,
            end_line=0,
            node_type="query",
            language="query"
        )
        query_embedding = self.generate_embeddings([query_chunk])[0]
        
        # Search
        results = self.table.search(query_embedding).limit(top_k).to_pandas()
        
        return results.to_dict("records")
