# Hybrid Retrieval
```mermaid
graph TD
    Query --> MetaFilter[Metadata Filter]
    MetaFilter --> FTS[PostgreSQL FTS]
    MetaFilter --> Vec[pgvector Search]
    FTS --> RRF[Reciprocal Rank Fusion]
    Vec --> RRF
    RRF --> Rerank[Optional Reranker]
    Rerank --> Citation[Inject Citations]
    Citation --> Result
```
