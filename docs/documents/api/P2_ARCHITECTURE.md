# P2 Platform Architecture

## Purpose
This document establishes the production architecture guidelines for the LokTathya civic data processing platform. It serves to coordinate secure fetching, raw document tracking, format-independent parsing, and relational observation mapping.

## System Architecture Diagram
Refer to [complete-system.mmd](file:///c:/python/LokTathya/docs/diagrams/99-master/complete-system.mmd) for the system overview layout.

## Core Pipelines
1. **Fetch & Storage Pipeline**: Async requests utilizing ResilientHTTPClient, validating SSRF restrictions at every hop and writing bytes directly to MinIO.
2. **Factory & Parsing**: FormatDetector identifies file types (HTML, CSV, PDF, XLSX, JSON) and directs them to ParserFactory.
3. **Data Quality & Provenance**: Standardized structured fields map through observations, claims, and evidence to canonical database records.

## Security Constraints
- All HTTP requests are strictly bound to SSRF checking policies.
- Internal networks, loopbacks, and cloud-provider metadata endpoints are discarded automatically.
- Redirect chains are validated dynamically after every hop.
