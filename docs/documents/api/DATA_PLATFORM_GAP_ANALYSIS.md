# DATA PLATFORM GAP ANALYSIS

## ARCHITECTURE GAPS
| COMPONENT | CURRENT | MISSING | REQUIRED | STATUS |
|-----------|---------|---------|----------|--------|
| Source Registry | Models exist | Dynamic refresh policy, conditional HTTP | Resilient HTTP Client | PARTIAL |
| Raw Storage | MinIO configured | Structured path schema (source/endpoint/document) | Object keys matching hash | MISSING |
| Ingestion Queues | Basic Celery | Priority queues, OCR isolation, backpressure | Dedicated Queues | MISSING |
| Database Indexing | Basic PKs | PostGIS spatial indexes, pgvector integration | Indexing strategy | PARTIAL |

## DATA LIFECYCLE GAPS
| COMPONENT | CURRENT | MISSING | REQUIRED | STATUS |
|-----------|---------|---------|----------|--------|
| Hashing | SHA-256 stub | Stream hashing for large files | Block-level stream hashing | PARTIAL |
| Format Detection | None | Magic bytes, Content-Type inspection | python-magic / filetype | MISSING |
| Quarantine | None | Dead-letter queue / Quarantine table | Schema & UI | MISSING |
| Resumability | None | Checkpointing for long batches | Batch persistence | MISSING |
