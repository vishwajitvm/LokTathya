# Phase 3 Final Completion Matrix

This document tracks all Phase 3 requirements, their technical implementations, verifying test modules, physical evidence observed, final statuses, and remaining risks.

---

## Complete Requirements Matrix

| Requirement | Technical Implementation | Test File / Case | Physical Evidence | Status | Remaining Risk |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Source Registry Expansion** | Whitelisted 25+ attributes in `Source` model (`backend/models/source.py`) | `alembic upgrade head` | Database table `src_source` contains expanded column definitions | `PASS` | None. All fields are version-safe. |
| **Endpoint Registry Expansion** | Whitelisted columns on `SourceEndpoint` for conditional HTTP caching and retries | `alembic upgrade head` | Database table `src_endpoint` contains ETag/modified properties | `PASS` | None. Standard HTTP cache compliance. |
| **Website support** | Base class representation for HTML-driven authorities | `tests/test_completion_gate.py:test_webpage_cosmetic_vs_semantic_versioning` | Database `src_web_page` and `src_web_page_version` rows link correctly | `PASS` | Dynamic HTML formatting changes require custom parsing rules. |
| **Controlled Discovery** | Filter outbound sitemap, RSS, and page HTML paths to registered domains | `tests/test_discovery.py` | Out-of-domain links return empty collections | `PASS` | Subdomain wildcards require manual audit verification. |
| **URL Canonicalization** | `URLCanonicalizer` strips UTM codes, parameters, and fragments | `tests/test_url_utils.py` | Returns standardized string formats deterministically | `PASS` | None. Parameters are fully whitelisted. |
| **Format Factory** | Dispatcher class routes MIME/magic matching to target parsers | `tests/test_parsers.py` | Dispatches dynamically to HTML/PDF/CSV/XLSX/JSON/GIS | `PASS` | None. |
| **GIS Parser** | Custom `GISParser` extracts placemarks and coordinates cleanly | `tests/test_parsers.py` | Parsed coordinates verified on geojson/kml buffers | `PASS` | Heavy GIS shapes require spatial indexing checks. |
| **XML Parser** | XMLParser parses child tags and properties | `tests/test_parsers.py` | Valid root tags match raw structures | `PASS` | None. |
| **Celery Partitioning** | CPU-heavy parsing and fetching bound to separate queues | `tests/test_celery_routes.py` | Routing dictionary maps names to queues | `PASS` | None. |
| **API Endpoints** | REST endpoints for candidate listings, discovery runs, and quarantine retry | `tests/test_api_extensions.py` | API client receives expected JSON records with HTTP 200 | `PASS` | None. |
| **SSRF Safety** | Recursive checks on redirect target IP ranges | `tests/test_security_hardening.py` | Localhost loopbacks trigger fetch aborts | `PASS` | DNS dynamic TTL rebinding attacks. |
| **Data Lineage** | Observations track lineage from ContentVersion back to Source | `tests/test_end_to_end_vertical.py` | Provenance database relations link cleanly | `PASS` | Complex revision mappings require transaction safety. |
| **Cosmetic vs Semantic** | Ignore cosmetic noise (cookie notices, timestamps) | `tests/test_completion_gate.py:test_webpage_cosmetic_vs_semantic_versioning` | Normalized page hashes match despite timestamp differences | `PASS` | Dynamic page elements lacking noise classes might trigger versions. |
| **PDF versioning** | Track version transitions when identical URL content changes | `tests/test_completion_gate.py:test_pdf_versioning_and_government_correction` | Separate ContentVersions created with distinct MinIO storage keys | `PASS` | None. |
| **Government correction** | Support links indicating corrections or supersessions | `tests/test_completion_gate.py:test_pdf_versioning_and_government_correction` | Related document keys and status flags verify correct association | `PASS` | Complex multi-stage corrections require human checks. |
| **Same content / Different URL** | Deduplicate identical bytes pointing to multiple URLs | `tests/test_completion_gate.py:test_same_content_different_url` | ContentVersions map to a single logical Document ID | `PASS` | None. |
| **Source Disappearance** | Retain data history if a source returns 404 | `tests/test_completion_gate.py:test_source_disappearance_scenario` | Target source marked DEGRADED, previous runs and versions remain intact | `PASS` | None. Data is immutable. |
| **XML XXE Protection** | Block entity declaration and DOCTYPE structures | `tests/test_security_hardening.py` | XXE payloads return error strings without executing parsing | `PASS` | None. |
| **Zip Slip Protection** | Prevent path traversals inside ZIP and Shapefiles | `tests/test_security_hardening.py` | Archives with relative paths (`../`) are blocked | `PASS` | None. |
| **XLSM safety** | Disable macro code execution during sheet loading | `tests/test_parsers.py` | Openpyxl configuration loads sheets without VBA triggers | `PASS` | None. |
| **Quarantine Flow** | Isolate corrupt/malformed files into quarantine records | `tests/test_api_extensions.py` | API fetches quarantined lists with HTTP 200 OK | `PASS` | High quarantine frequency indicates scraper target format changes. |

---

## 2. Risk Mitigation Summary
To address SSRF risks, the HTTP client follows redirect headers manually, validating each destination before socket creation. Dynamic presentation elements are stripped during normalizer phases to prevent semantic version bloating. Archive files are inspected for directory traversal signatures before raw parsing occurs.
