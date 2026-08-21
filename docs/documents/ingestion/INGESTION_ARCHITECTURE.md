# Ingestion Architecture

The LokTathya ingestion architecture is source-driven, generic, and strictly Docker-based. 

## Flow
`Source Registry -> Connector -> Fetcher -> Raw Artifact -> Content Detection -> Parser -> Normalizer -> Validator -> Entity Resolution -> Canonical Writer -> Provenance -> TraceNest`

## Principles
1. **Idempotency**: Fetching the same unchanged payload (by SHA-256 content hash) halts the parser pipeline.
2. **Raw Storage**: Raw HTML, JSON, and PDFs are dumped to MinIO deterministically `raw/source/dataset/date/content_hash/`.
3. **Quarantine**: Bad data is safely quarantined, not dropped silently.
