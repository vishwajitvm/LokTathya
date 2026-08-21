# PHASE 11 SOURCE COVERAGE REVIEW

## Architecture Overview
The National Source Discovery framework formally establishes the ingestion boundary for LokTathya. It strictly prevents unauthorized web scraping or automated hallucinated ingestion by instituting a rigid state machine for candidate sources (`DISCOVER -> VERIFY -> REGISTER -> INGESTIBLE`).

## Coverage Metrics
- The `CoverageEngine` enforces deterministic denominators. A jurisdiction (e.g., State or District) requires explicit linkage to a verified source for a specific category (e.g., `elections` or `budget`) before it can be marked covered. 
- Arbitrary "80% national coverage" marketing metrics are prohibited in favor of exact matrix definitions.

## Source Health & Deprecation
- The `SourceHealthTracker` monitors official endpoints via lightweight ETags/Headers. 
- Crucially, if an official source is taken offline by the government, the system marks the source `DEPRECATED` or `TEMPORARILY_UNAVAILABLE` but completely preserves historical chunks and canonical data tied to that source, acting as a civic archive.

## Security & Licensing
- All data ingestion adheres to tracked `license` and `attribution requirements` per the `DATA_LICENSE_POLICY.md`. 
- No API credentials or auth tokens are checked into code; they are securely proxied via Docker `.env` secrets.

## Known Limitations
- Determining if an HTTP 404 is temporary or permanent often requires manual domain authority review rather than automated scripts.
- Data licenses (NDAP vs explicit copyright vs public domain) vary wildly across sub-departments and require granular tracking mechanisms.

## STOP CONDITION
The Source Coverage Engine and API boundaries are complete and checked into the codebase. 
No mass crawling scripts were instantiated.
Execution is stopped. Awaiting review.
