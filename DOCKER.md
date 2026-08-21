# Docker Architecture

Docker is required for local development.

## Services
- rontend: Next.js development server.
- ackend: FastAPI server.
- worker: Celery worker.
- scheduler: Celery beat scheduler.
- postgres: PostgreSQL + PostGIS + pgvector.
- edis: Redis for Celery and caching.
- minio: S3-compatible local object storage.
