# P2 Document Versioning Policy

## Purpose
Establishes clear guidelines on how LokTathya versions both webpages and document artifacts without silently overwriting historical facts.

## Versioning Workflow Diagram
Refer to [document-versioning.mmd](file:///c:/python/LokTathya/docs/diagrams/13-versioning/document-versioning.mmd) for versioning checks.

## Key Policies
1. **Same URL, Same Content**: Record FetchEvent. No new ContentVersion created.
2. **Same URL, Changed Content**: Generate new ContentVersion. Previous version remains immutable.
3. **Temporal Diffing**: The system performs semantic and layout difference checks to flag the category of modification (e.g. metadata vs structural updates).
