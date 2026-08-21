# Architectural Decisions Summary

Refer to docs/documents/architecture-decisions/ for detailed ADRs.

- ADR-0001: MIT License for software; data retains original licenses.
- ADR-0002: PostgreSQL/PostGIS for canonical database.
- ADR-0003: pgvector for vector search instead of a dedicated vector DB initially.
- ADR-0004: Explicit claim-to-version provenance model.
- ADR-0005: Content-hash based versioning.
- ADR-0006: LLM Gateway to abstract providers.
- ADR-0007: Embed only narrative text, use SQL for structured numerical queries.
- ADR-0008: MinIO for local S3-compatible object storage.
- ADR-0009: Celery + Redis for ingestion background processing.
- ADR-0010: PostGIS for primary geographic source of truth.
