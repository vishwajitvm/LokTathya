# INGESTION CAPABILITY MATRIX

| CAPABILITY | CURRENT | MISSING | REQUIRED | STATUS |
|------------|---------|---------|----------|--------|
| HTTP Client | Requests stub | Circuit breaker, ETag, Streaming | Resilient Async Client | PARTIAL |
| PDF Parsing | Mock Tesseract | Real PDFPlumber / Tesseract integration | OCR queue | STUB |
| CSV Parsing | None | Chunked processing, encoding detection | pandas / csv stream | MISSING |
| Spreadsheet | None | openpyxl / xlrd, multi-sheet, formulas | XLS/XLSX pipeline | MISSING |
| GIS Parsing | None | GeoJSON/Shapefile validation | geopandas integration | MISSING |
| Rate Limits | None | Source-level concurrent limit | Redis token bucket | MISSING |
| Idempotency | Hash check | Batch-level deduplication | DB Constraints | PARTIAL |
