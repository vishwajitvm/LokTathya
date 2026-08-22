# PRIORITY 1 HARDENING VALIDATION

## SUMMARY
This document proves the physical validation of Priority 1 components, explicitly resolving the previous ambiguities in PostGIS management, Format Detection, and SSRF/Conditional testing.

## ALEMBIC & POSTGIS VALIDATION
- **Issue**: Alembic was incorrectly dropping the `loader_lookuptables` and other tables maintained by `postgis_tiger_geocoder`.
- **Resolution**: Updated `env.py` `include_object` to check `getattr(object, "schema", None)` for `tiger`, `tiger_data`, and `topology` schemas in addition to checking table names. Removed duplicate `create_index` statements for GiST indexes generated automatically by `geoalchemy2`. Added a manual UUID cast (`postgresql_using='source_id::uuid'`).
- **Validation**: `alembic upgrade head` now successfully executes from a fresh start to `89ab2f750dee` without any PostGIS errors.

## FORMAT DETECTOR VALIDATION
- **Issue**: FormatDetector was a stub and lacked actual inspection of bytes.
- **Resolution**: Implemented `FormatDetector` in `backend/core/format_detector.py`. Added python-magic fallback to Content-Type.
- **CSV Encoding**: Explicitly parses byte headers for `\xef\xbb\xbf` (UTF-8-SIG/BOM) and `\xff\xfe` (UTF-16). Falls back to `chardet` for statistical analysis if available.
- **Shapefile / GIS**: Automatically opens `application/zip` in-memory. Recursively searches the internal zip manifest. Distinguishes generic ZIPs from valid Shapefiles by confirming `.shp`, `.shx`, and `.dbf` are present.
- **Validation**: Covered by `pytest tests/test_format_detector.py`. (4 tests pass).

## FETCH & HTTP CLIENT VALIDATION
- **Issue**: SSRF and conditionals were untested.
- **Resolution**: `ResilientHTTPClient` parses hostnames to reject `localhost`, `127.x.x.x`, and private/internal IP schemas.
- **Conditional Handling**: Verifies `If-None-Match` returns HTTP 304 and safely propagates the `NOT_MODIFIED` state.
- **Validation**: Covered by `pytest tests/test_http_client.py`. (4 tests pass).

All required subsystems for the Fetch Engine have moved from STUB to TESTED.
