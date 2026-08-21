class EmbeddingRegistry:
    def register_model(self, model_id: str, provider: str, dim: int, status: str = "EXPERIMENTAL"):
        # Status: PRIMARY, FALLBACK, EXPERIMENTAL
        return {"model_id": model_id, "dimensions": dim, "status": status}
    
    def get_primary_model(self):
        return {"model_id": "bge-m3", "dimensions": 1024, "status": "PRIMARY"}

class HybridSearchEngine:
    """Combines Lexical (PostgreSQL FTS) + Semantic (pgvector)."""
    
    def search(self, query: str, filters: Dict[str, Any], top_k: int = 5):
        # 1. Lexical Search (FTS)
        lexical_results = self._fts_search(query, filters)
        
        # 2. Semantic Search (pgvector)
        vector_results = self._vector_search(query, filters)
        
        # 3. RRF (Reciprocal Rank Fusion) or scoring fallback
        return self._fuse_results(lexical_results, vector_results, top_k)
        
    def _fts_search(self, query, filters):
        return [{"chunk_id": "1", "score": 0.8}]
        
    def _vector_search(self, query, filters):
        return [{"chunk_id": "1", "score": 0.9}, {"chunk_id": "2", "score": 0.85}]
        
    def _fuse_results(self, lex, vec, top_k):
        # Dummy fusion, ensures metadata citation remains attached
        return [{
            "chunk_id": "1",
            "text": "Budget allocation 2024",
            "citation": {
                "source_id": "SRC-IN-MOF-001",
                "document_id": "doc123",
                "page": 10
            }
        }]
