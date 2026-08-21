# API Architecture

Base URL: /api/v1/

## Principles
- Versioning
- Pagination
- Filtering & Sorting
- Rate Limiting
- Source References
- Provenance details on every record
- OpenAPI documentation

## Endpoints (Proposed)
- /locations
- /administrative-divisions
- /representatives
- /projects
- /elections
- /sources
- /documents
"@

    "DEVELOPMENT.md" = @"
# Development Guide

- Stack: Next.js, FastAPI, PostgreSQL, MinIO, Redis, Celery.
- Use Docker Compose for local environment.
- Do not commit API keys or Stitch credentials.
