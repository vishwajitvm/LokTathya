# PRIORITY 2: WEB PAGE & DATA PROCESSING FACTORY

## CORE OBJECTIVE MET
This phase expands LokTathya beyond simple PDFs to recognize the `WebPage` as a first-class source of canonical truth.

## COMPONENT IMPLEMENTATIONS

### 1. Source Model Expansion (`models/web_page.py`)
- Created `WebPage` model separating the concept of a Source/Endpoint from a specific web presence.
- Created `WebPageVersion` model enforcing immutable page tracking where only material changes (via hashing) generate new versions.
- Added `ExtractedTable` to store tabular data extracted structurally from HTML.

### 2. Change Detection & Normalization (`ingestion/html_normalizer.py`)
- **HTMLNormalizer**: Uses `BeautifulSoup` to strip noise (`<nav>`, `<header>`, `<footer>`, `<script>`, ad banners) to prevent false-positive version bumps caused by timestamps or tracking pixels.
- **Table Extraction**: Directly extracts structural `<table/tr/th/td>` entities into the `ExtractedTable` schema format for downstream entity resolution.

### 3. Pipeline Integration Path
The standard `FetchEvent` now branches:
1. `FormatDetector` detects `HTML`.
2. Pipeline invokes `HTMLNormalizer.normalize()`.
3. Compares `content_hash` against the latest `WebPageVersion`.
4. If changed, persists `raw_html` and `normalized_text` to MinIO, creates `WebPageVersion`.
5. Extracts and persists `ExtractedTable` rows.

## NEXT STEPS FOR PRIORITY 2 EXECUTION
- Tie `WebPage` to Celery `FetchTask` queue.
- Implement URL canonicalization engine (stripping UTM tracking params, handling trailing slashes deterministically).
- Implement Document Link extraction (detecting embedded PDFs/CSV links and submitting them to the `source_fetch` queue).
