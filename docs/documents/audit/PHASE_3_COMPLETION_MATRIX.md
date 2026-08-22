# Phase 3 Completion Matrix

This matrix tracks the implementation status of Phase 3 requirements for the LokTathya National Civic Data Platform.

---

## Subsystem Completion Status

| Requirement | Implementation | Test File / Command | Evidence | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Source Registry Expansion** | Schema fields whitelisted on model and applied via migration | `alembic upgrade head` | Database table columns exist | `PASS` |
| **Endpoint Registry Expansion** | Added expected_format, frequency, check properties | `alembic upgrade head` | Database table columns exist | `PASS` |
| **Website support** | WebPage and WebPageVersion models inherit base | `pytest tests/test_end_to_end_vertical.py` | Pages register and save | `PASS` |
| **Controlled Discovery** | link discovery filter domains | `pytest tests/test_discovery.py` | Excludes external domains | `PASS` |
| **URL Canonicalization** | URLCanonicalizer strips tracking query parameters | `pytest tests/test_url_utils.py` | Strip parameters match | `PASS` |
| **Format Factory** | parser factory handles HTML/PDF/CSV/XLSX/JSON | `pytest tests/test_parsers.py` | Parses standard types | `PASS` |
| **GIS Parser** | Custom GISParser processes GeoJSON, KML, and KMZ | `pytest tests/test_parsers.py` | Placemarks & points extract | `PASS` |
| **XML Parser** | XMLParser reads tag name and attributes | `pytest tests/test_parsers.py` | Root tag validates | `PASS` |
| **Celery Queue Partitioning** | task_routes route CPU tasks to dedicated queues | `pytest tests/test_celery_routes.py` | Routes match expected queues | `PASS` |
| **API Endpoints** | discovery/run, discovery/candidates, quarantine list/retry | `pytest tests/test_api_extensions.py` | Returns HTTP 200 OK | `PASS` |
| **SSRF Security** | host IP range blocking during redirect chains | `pytest tests/test_end_to_end_vertical.py` | 127.0.0.1 blocked | `PASS` |
| **Data Lineage** | Fact -> Claim -> Evidence -> Observation relations | `pytest tests/test_end_to_end_vertical.py` | DB records link successfully | `PASS` |
| **Observed/Valid Dates** | observed_at and valid_from datetime mappings | `pytest tests/test_end_to_end_vertical.py` | Times saved correctly | `PASS` |
| **Mermaid Documentation** | 21 diagrams generated under `docs/diagrams` | Local file validation | Files exist | `PASS` |
| **Mermaid Ink Audit** | Render status document created | `MERMAID_RENDERING_AUDIT.md` | Blocked status logged | `PASS` |
| **Reprocessing engine** | Stored raw bytes can be processed by improved parsers | `pytest tests/test_parsers.py` | Rerunning parser succeeds | `PASS` |
