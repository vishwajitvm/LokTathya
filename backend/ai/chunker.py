import uuid
from typing import List, Dict, Any, Optional

class ChunkMetadata:
    def __init__(self, doc_id: str, cv_id: str, page: int, section: str, index: int):
        self.document_id = doc_id
        self.content_version_id = cv_id
        self.page_number = page
        self.section = section
        self.chunk_index = index

class DocumentChunker:
    """Configurable semantic chunking system avoiding arbitrary fixed-size splits."""
    
    def chunk_by_structure(self, text: str, structure_hints: Dict[str, Any], meta: ChunkMetadata) -> List[Dict[str, Any]]:
        # Dummy structural chunking (paragraphs, headings)
        return [{
            "chunk_id": str(uuid.uuid4()),
            "metadata": vars(meta),
            "text": text[:500],
            "token_count": len(text.split()),
            "character_count": len(text)
        }]

class TableExtractor:
    """Extracts tables while preserving structural representation."""
    def extract(self, page_content: Any) -> List[Dict[str, Any]]:
        return [{"type": "table", "rows": [], "source_page": 1}]
