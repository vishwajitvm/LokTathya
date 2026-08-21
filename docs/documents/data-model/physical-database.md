# Physical Database Architecture

The physical database leverages PostgreSQL, PostGIS, and pgvector.

- **Naming Strategy:** Table prefixes denote domains (e.g., geo_district, in_budget, src_document).
- **PostGIS:** WGS84 (SRID 4326) for boundaries.
- **pgvector:** Used for narrative document chunks.
