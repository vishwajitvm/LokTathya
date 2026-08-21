# Report Provenance
```mermaid
graph TD
    Gen[Generate Report] --> Snap[Snapshot Dataset Versions]
    Snap --> Metric[Embed Metric Definitions]
    Metric --> Cit[Attach Source Citations]
    Cit --> PDF[JSON / Downloadable Report]
    PDF --> Archive[(Immutable Record)]
```
