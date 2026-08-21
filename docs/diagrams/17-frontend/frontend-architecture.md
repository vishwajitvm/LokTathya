# Frontend Architecture
```mermaid
graph TD
    Browser[Client Browser] --> NextServer[Next.js SSR Node]
    NextServer -->|Server Fetch| API[FastAPI Backend /api/v1/]
    Browser -->|Client Fetch| API
    API --> PostGIS[(PostgreSQL)]
```
