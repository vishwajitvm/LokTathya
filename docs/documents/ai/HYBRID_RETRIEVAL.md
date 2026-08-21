# Retrieval (Full Text, Hybrid, Reranking, Metadata)
- **Full Text Search**: PostgreSQL `to_tsvector` using lexical matching (English/Hindi).
- **Hybrid Retrieval**: FTS combined with pgvector outputs via Reciprocal Rank Fusion.
- **Metadata Filtering**: Source, jurisdiction, date, and document type MUST filter candidate pools BEFORE semantic ranking.
- **Reranking**: An abstract Reranker pipeline exists for top-K refinement, disabled until baseline metrics require it.
