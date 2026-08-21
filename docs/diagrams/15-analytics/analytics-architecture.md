# Analytics Architecture
```mermaid
graph TD
    Source[Official Source Data] --> Canonical[Canonical Facts]
    Canonical --> Engine[Deterministic Analytics Engine]
    Engine --> Derived[Derived Metrics]
    Derived --> API[Analytics API]
    API --> Client[Client Application]
    API --> AI[AI Explanation Layer]
```
