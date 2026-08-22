# Phase 4: National Data Acquisition & Processing Factory

## 1. Purpose & Core Objective
The Phase 4 architecture transitions LokTathya into a production-grade civic information engine capable of parsing, validating, and normalising multi-format government resources across thousands of administrative jurisdictions in India.

---

## 2. Ingestion Lifecycle Architecture
```
    DISCOVER -> VERIFY -> REGISTER -> FETCH -> RAW -> CLASSIFY -> PARSE -> NORMALIZE -> VALIDATE -> OBSERVE -> RESOLVE -> RECONCILE -> PUBLISH
```

### A. Source Scheduler Engine
Calculates endpoint retrieval cadences using exponential backoffs, scheduling retry windows under failure states to prevent rate-limiting or service starvation.

### B. Universal Connector Interface
Unifies fetch, parse, and emission sequences, ensuring compliance with the central database schemas and MinIO storage paths.

---

## 3. Large File Safety & Decompression Bomb Protection
- **PDF page limits**: Aborts parsing if file exceeds 500 pages.
- **CSV row limits**: Streams rows to memory, truncating parsing at 100,000 entries.
- **XLSX limits**: Restricts total parsed cells across sheets to 100,000.
- **ZIP Slip protection**: Checks all member names against drive letters, colon tokens, and traversal path elements (`../`).
- **Decompression limit**: Limits maximum total raw uncompressed data size to 200MB.

---

## 4. API Endpoints
All API endpoints map directly to underlying database entities (`IngestionRun`, `Quarantine`, `SourceEndpoint`), replacing mock static arrays.
- `POST /api/v1/discovery/run`: Enrolls the run status to the database.
- `GET /api/v1/discovery/candidates`: Resolves observed endpoints tagged under the candidate stage.
- `GET /api/v1/quarantine`: Standard lists of isolated parse crashes.
- `POST /api/v1/quarantine/{id}/retry`: Sets record state back to pending retry cycles.
