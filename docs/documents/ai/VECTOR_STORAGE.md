# Vector Storage
Storage relies solely on PostgreSQL + pgvector. 
Tables are partitioned by `dimensions` (e.g., `ai_embedding_1024`, `ai_embedding_1536`) to allow strict indexing constraints for HNSW/IVFFlat without requiring an external vector DB.
