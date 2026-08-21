# Citation Flow
```mermaid
graph TD
    DB[(PostgreSQL)] --> Internal[SQLAlchemy Model + prov_claim]
    Internal --> Transform[DTO Transformation]
    Transform --> Cit[CitationDTO]
    Cit --> JSON[API Response]
    JSON --> Client
```
