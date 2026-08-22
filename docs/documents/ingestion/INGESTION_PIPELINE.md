# Ingestion Pipeline Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Ingestion Subsystem Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Data Ingestion Pipelines |

---

## 1. Purpose
This document specifies the data ingestion pipelines, parsing formats, data normalization rules, and validation checks of the LokTathya platform. It details the steps that transform raw government files into verified, reconciled records.

---

## 2. Ingestion Processing Stages

The ingestion pipeline transforms raw file inputs into verified records using a Celery task queue:

```
[Raw Document] ---> [Parsed Data] ---> [Normalized Data] ---> [Validated Data]
                                                                     |
                                                                     v
[Canonical Database] <--- (Resolve) <--- [Reconciliation Engine] <--- (Match)
```

1. **RAW**: Raw PDFs, CSVs, and GeoJSON files are uploaded to MinIO and registered in the `sources` table with a unique cryptographic hash to ensure auditability.
2. **PARSED**: Document contents are extracted. Scanned PDFs are processed using OCR tasks.
3. **NORMALIZED**: Translates values (e.g. spelling variations, currency scales) into standard formats.
4. **VALIDATED**: Ingestion pipelines run data quality validations. Failed files are routed to the **Quarantine** database.
5. **RESOLVED**: Fuzzy name matching matches candidate profiles against existing records.
6. **CANONICAL**: Reconciled data is loaded into the core PostgreSQL tables.
7. **PROVENANCE**: The system creates a link mapping every database record back to its source registry ID.

---

## 3. Task Queuing & Batch Scheduler

* **Redis Message Broker**: Handles task routing between the FastAPI application and Celery workers.
* **Batch Scheduling**: Cron tasks (managed by Celery Beat) trigger sync scripts during off-peak hours (e.g. 2:00 AM) to query government portals for new files.
* **Rate Limiting Policies**: Scrapers target government endpoints (e.g. ECI portals) using a rate limit of 1 request per 3 seconds to avoid overloading public servers and prevent IP blocks.

---

## 4. OCR Extraction & Scanned Document Parsing

Ingesting scanned Form 26 PDFs (nomination affidavits) or budget sheets requires specialized parsing logic:
* **Native Text Extraction Priority**: The parser prioritizes extracting native digital text layers first. OCR operations are strictly a fallback.
* **Tesseract & LayoutLM OCR Fallback**: If the native text density/quality metric falls below a critical threshold, Celery enqueues a layout-aware OCR job (using `TesseractProvider` or `LayoutLM`).
* **Confidence Checks**: If the average OCR character confidence falls below `0.80`, the file is sent to the quarantine folder for manual index verification.
* **Page Mapping Retention**: Extracted text chunks retain mapping references back to their original page numbers to support validation and audit checks.
* **Redaction Filters**: Extracted text is checked by PII redaction filters before being stored.

---

## 5. Database Batch Transaction Controls

To prevent partial imports or database corruption during ingestion crashes:
* **Transactional Enforce**: All changes within a single ingestion task run inside a strict SQL database transaction block (`db.begin()`).
* **Automated Rollback**: If an exception occurs during normalization or validation, the database transaction is rolled back, removing all partial records, and the task state is set to `QUARANTINED`.
* **Idempotent Checks**: The task checks for existing files using the hash key, skipping ingestion if the file has already been processed.

---

## 6. Failures & Quarantine Policies

* **Hashing & Idempotency**: Raw files are hashed (SHA-256) before ingestion. Re-uploading a file with a matching hash is blocked to prevent duplicate records.
* **Quarantine Rules**: Files with parsing errors, schema discrepancies, or failed math checks (e.g. invalid vote counts) are quarantined. The pipeline logs a `DATA_DISCREPANCY` conflict for review.
* **Failure Isolation**: Each ingestion file runs in an isolated Celery task, ensuring that individual file errors do not block the rest of the queue.

---

## 7. Ingestion Logging & TraceNest IDs

* **Trace Propagation**: Every ingestion task is logged in the `ingestion_runs` table, containing fields for started time, completed time, status, and the TraceNest transaction ID (`X-Request-ID`).
* **Error Logs**: If a task fails or is quarantined, the full traceback is saved in the run metadata to assist data engineers in debugging parsing issues.

---

## 8. Ingestion File Size Thresholds

To prevent memory exhaustion in parsing tasks:
* **PDF Size Limit**: Files larger than 50MB are split into individual page batches before running OCR.
* **CSV Row Constraints**: Dataset files (e.g. historical election results) exceeding 100,000 rows are processed in chunked transactions of 5,000 rows each.

---

## 9. Object Storage Structure in MinIO

To maintain raw file archives:
* **Bucket Layout**: Organized under `raw/`, `quarantine/`, and `processed/` buckets.
* **Metadata Tags**: Files are tagged with ingestion timestamps, target state codes, and source registry IDs to optimize file discovery.

---

## 10. Worker Concurrency Settings

* **Task Concurrency**: Celery workers are configured with a concurrency rate of `worker_concurrency=4` to balance memory utilization with processing speeds.
* **Prefetch Limits**: Set to `prefetch_multiplier=1` to ensure that heavy OCR files do not bottleneck the queues.

---

## 11. Related Documents
* [VALIDATION_RECONCILIATION.md](file:///c:/python/LokTathya/docs/documents/data-quality/VALIDATION_RECONCILIATION.md)
* [SOURCE_CATALOG.md](file:///c:/python/LokTathya/docs/documents/source-registry/SOURCE_CATALOG.md)
