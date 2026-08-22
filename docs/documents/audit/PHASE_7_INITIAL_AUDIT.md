# Phase 7 Initial Forensic Audit

This document records the initial forensic audit of the LokTathya repository for Phase 7.

---

## 1. Audited Acquisition Architecture and Parsers

- **Formats Supported**: HTML, PDF, CSV, XLSX, XML, GIS.
- **Safety Boundaries**: `parser_factory.py` implements boundary limits (50MB size restrictions, page limits, row/column validation).
- **Orchestration**: Celery task flows (`tasks.py`, `fetch_task.py`) route structured tasks across target queues.

---

## 2. Suspicious Stubs or Placeholders
- **VBA Macro check**: Ingestion of XLSM does not execute macros, but explicit detection of macro/VBA sections inside workbook containers can be hardened.
- **Sitemap discovery**: Discovery engine is present but can be extended to handle sitemap indexes.
