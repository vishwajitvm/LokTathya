# API INVENTORY

| METHOD | PATH | DOMAIN | PURPOSE | SCHEMA | SERVICE | DATABASE | AUTH | PROVENANCE | TEST | STATUS |
|---|---|---|---|---|---|---|---|---|---|---|
| GET | /api/v1/sources | Sources | List sources | SourceResponse | SourceService | src_source | NONE | NO | NO | PARTIAL |
| POST | /api/v1/sources | Sources | Create source | SourceCreate | SourceService | src_source | NONE | NO | NO | PARTIAL |
| GET | /api/v1/sources/{id}/history | Sources | Source history | - | - | src_source | NONE | YES | NO | STUB |
| GET | /api/v1/documents/{id}/versions | Content | Content versions | - | - | src_content_version | NONE | YES | NO | STUB |
| GET | /api/v1/documents/{id}/diff | Content | Document diff | - | - | - | NONE | NO | NO | STUB |
| GET | /api/v1/elections | Elections | List elections | - | - | elec_election | NONE | NO | NO | STUB |
| GET | /api/v1/geography | Geography | List geography | - | - | geo_entity | NONE | NO | NO | STUB |
| GET | /api/v1/geographies_history | Geography | Geohistory | - | - | - | NONE | NO | NO | STUB |
| GET | /api/v1/analytics | Analytics | Analytics metrics | - | - | - | NONE | NO | NO | STUB |
| GET | /api/v1/data_quality | Data Quality | Data quality metrics | - | - | - | NONE | NO | NO | STUB |
| GET | /api/v1/representatives | Representatives | List reps | - | - | - | NONE | NO | NO | STUB |
| GET | /api/v1/search | Search | Semantic search | - | - | ai_embedding | NONE | NO | NO | STUB |
