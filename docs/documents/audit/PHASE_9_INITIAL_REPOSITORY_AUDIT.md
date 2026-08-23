# Phase 9: Initial Repository Audit

## Executive Summary
This audit was conducted prior to commencing Phase 9 of LokTathya development. The objective was to thoroughly inspect the actual repository code (models, routers, schemas, services, ingestion workers, and configurations) to identify what truly exists, what is stubbed or mocked, what is disconnected, and what requires implementation for the upcoming Dataset Intelligence & Semantic Data Processing Factory.

## 1. Existing Architecture Analysis

### Models
- **`src_source`, `src_endpoint`, `src_document`, `src_content_version`, `src_quarantine`**: Fully implemented and functionally tested in earlier phases. Includes `SourceHistory` and `health_status`.
- **`src_web_page`, `src_web_page_version`, `src_extracted_table`**: Defined in `web_page.py`. This provides document-level versioning and table extraction, but does not extend to semantic datasets.
- **`src_dataset`**: Exists purely as a skeleton model in `source.py` with only `id`, `source_id`, and `name`.
- **Observations (`src_observation`)**: Exists in `observation.py` to capture generic data points, but lacks the overarching dataset mapping schema.

**Missing Models for Phase 9:**
- `DatasetVersion` (to track version lifecycle)
- `DatasetSchema` (to track table headers, types)
- `DatasetField` (to track individual column semantics)
- `DatasetQualityProfile` (to track nulls, duplicates)
- `DatasetClassification` (to store semantic mapping details)
- `DatasetRelationship` (to track lineages like supersedes, derived-from)

### Ingestion & Processing
- The `UniversalConnector` fetches raw files and uses `FormatDetector`.
- `ParserFactory` contains implementations for HTML, PDF, CSV, JSON, XLSX, XML, GeoJSON, KML.
- Celery task routing exists with `worker_discovery`, `worker_fetch`, and `worker_parse`.
- Currently, ingestion maps directly to `Observations` (for HTML tables) or simple metadata summaries.

**Missing Pipeline Components for Phase 9:**
- `Dataset Identification Task`
- `Dataset Version Creation`
- `Schema Inference Engine` (must scan data types, nulls, max/min, distributions)
- `Quality Profiler` (must check for schema validity, corruption, zip bombs)
- `Semantic Mapping Engine` (must link 'dist_name' to 'District')
- `Schema Drift Detector` (comparing v1 vs v2 schemas)

### APIs & Routers
- **Existing**: `sources`, `discovery`, `ingestion`, `geography`, `elections`, `finance`, `projects`, `representatives`, `documents`, `web_pages`.
- **Missing Dataset APIs**: 
  - `/api/v1/datasets`
  - `/api/v1/datasets/{id}/versions`
  - `/api/v1/datasets/{id}/schema`
  - `/api/v1/datasets/{id}/quality`
  - `/api/v1/datasets/{id}/diff`

## 2. Stub and Mock Audit

A thorough search across the backend exposed multiple instances of mocked behavior or incomplete stubs returning hardcoded empty responses.

### Hardcoded Array/Object Returns (Placeholders)
Many API endpoints explicitly return `[]` or `{}` as placeholders rather than actually querying the database relations.
- `geography.py:123`: `get_geography_projects` returns `{"projects": []}`.
- `geography.py:152`: `get_geography_sources` returns `{"sources": []}`.
- `projects.py:98`: `get_project_documents` returns `{"documents": []}`.
- `representatives.py:141`: `get_representative_elections` returns `{"elections": []}`.

### Explicit Mock Strings
- `tests/test_completion_gate.py`: Relies heavily on `b"%PDF-1.4 mock pdf report version 1 bytes"`.
- `ingestion/pdf_processor.py`: Contains comments such as `# Mock objects`, `# Mock OCR extraction`, and `# Mock chunking`. 
- `core/format_detector.py`: Defines a `MockMagic` fallback class when `python-magic` is not available on the host environment.
- `geography/historical.py`: Contains `# Mock logic mimicking PostGIS geometric intersection checks`.

**Classification**: 
- Router endpoints returning `[]` are **PLACEHOLDERS/BUGS** and must be resolved by implementing true database relationship queries or explicitly stating NOT_IMPLEMENTED via HTTP 501.
- Test mocks are **TEST-ONLY** but we must verify that the actual pipeline doesn't rely on them during runtime.
- OCR/PDF mocks in `pdf_processor.py` are **STUBS** and should be wired to Tesseract/real parsers if applicable, or quarantined.

## 3. Storage & Infrastructure
- PostgreSQL is healthy and Alembic migrations correctly map constraints up to `80be1fdb0739`.
- MinIO securely stores raw file blobs with deterministic hashes.
- Redis handles domain-level rate limiting (`DomainRateLimiter`).

**Scalability Risks for Phase 9:**
- The schema inference engine must be heavily buffered. Loading a 1GB CSV into RAM purely to infer column types will OOM the `worker_parse` container. We must implement streaming / chunking (e.g. Pandas `chunksize=1000` or raw python `csv` reader sampling).

## 4. Phase 9 Implementation Roadmap

1. **Schema Generation**: Design and generate Alembic migrations for `DatasetVersion`, `DatasetSchema`, `DatasetField`, `DatasetQualityProfile`.
2. **Dataset Intelligence Engine**: Implement streaming schema inference and profiling within Celery. 
3. **Semantic Classifier**: Introduce rule-based or fuzzy mapping logic for Indian civic terminology (e.g., matching UP, Uttar Pradesh to the standard STATE entity).
4. **Drift Detection**: Implement difference checking between chronological dataset versions.
5. **API Layer**: Develop database-backed FastAPI routes with pagination, filtering, and real provenance tracking for the datasets.
6. **Integration**: Modify `UniversalConnector` to spawn downstream dataset celery tasks instead of raw observation dumps.
7. **Zero-Trust Validation**: Implement the script `scratch/phase9_api_exec.py` and run a real Excel/CSV file entirely through the pipeline to prove it.

## Conclusion
The repository has a very strong baseline from Phases 7 and 8. The ingestion boundary, deduplication, rate limits, and raw persistence are production-ready. The primary deficiency is the total lack of "Dataset Intelligence"—files are treated as opaque binary objects or immediately fragmented into loosely-bound observations. Phase 9 will bridge this gap.
