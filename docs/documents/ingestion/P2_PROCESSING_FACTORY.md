# P2 Processing Factory

## Purpose
This document describes the design of the format-independent document processing factory in LokTathya.

## Pipeline Lifecycle Diagram
Refer to [ingestion-pipeline.mmd](file:///c:/python/LokTathya/docs/diagrams/02-ingestion/ingestion-pipeline.mmd) for the pipeline steps.

## Processing Branches
- **HTML**: Strips cookie banners and navigation panels using HTMLNormalizer. Extracts tables and outbound document links.
- **PDF**: Page layout extraction via `pypdf` with structured page count metrics.
- **Tabular**: Enconding and dialect sniffers for CSVs; multi-sheet cell processors for XLSX workbooks.

## Failure Handling
Unrecognized formats or malformed documents are immediately isolated, flagged with a TraceNest tracking ID, and placed in the quarantine state to protect worker stability.
