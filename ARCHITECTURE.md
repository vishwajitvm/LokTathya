# Architecture

LokTathya architecture is based on a modern, open-source stack designed for scalability, provenance, and hybrid AI search.

## Overview
- **Frontend**: Next.js, TypeScript, Tailwind CSS, TanStack Query
- **Backend**: Python, FastAPI, Pydantic, SQLAlchemy
- **Database**: PostgreSQL, PostGIS, pgvector
- **Background Jobs**: Celery, Redis
- **Object Storage**: MinIO (local), S3-compatible
- **Search**: PostgreSQL full-text, pgvector, Hybrid retrieval
- **Observability**: TraceNest, Prometheus/Grafana (optional)
- **Infrastructure**: Docker, Docker Compose, Nginx

## Core Concepts
- **Official-Source-First**: Government sources are the primary truth.
- **Provenance**: Data must be traceable to its origin.
- **Hybrid Retrieval**: SQL for structured data + Vector Search for unstructured.
- **Extensible Ingestion**: Scheduler -> Fetcher -> Parser -> Normalizer -> DB/Index.
