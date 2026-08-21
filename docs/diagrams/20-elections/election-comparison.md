# Election Data Flow
```mermaid
graph TD
    Raw[Official ECI Source] --> Extract[Extract Raw Names]
    Extract --> Recon[Data Quality Reconciliation]
    Recon --> Cannon[Canonical Result Table]
    Cannon --> Math[Deterministic Vote Share / Margin]
    Math --> API[/api/v1/elections]
    API --> Cit[Frontend + Citation Component]
```
