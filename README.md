# 🇮🇳 LokTathya | National Civic Data & Intelligence Platform

[![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-emerald.svg)](https://github.com/vishwajitvm/LokTathya)
[![Docker Support: Enabled](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Tech Stack: FastAPI + Next.js](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Next.js-blueviolet.svg)](#architecture)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **LokTathya (लोक तथ्य)** is India’s open, auditable civic intelligence platform. It grounds conversational artificial intelligence in deterministically verified historical datasets, constituency geographies, and public representative records sourced exclusively from official government archives.

---

## 🗺️ Visual Architecture Overview
Below is a high-level representation of LokTathya's system topology. Detailed flowcharts for RAG querying, ingestion pipelines, security boundaries, and TraceNest request-id propagation are documented inside [`docs/diagrams/README.md`](file:///c:/python/LokTathya/docs/diagrams/README.md).

```
                  +-----------------------------------+
                  |           User Browser            |
                  +-----------------------------------+
                                    |
                                    | HTTP Requests (Port 3000)
                                    v
                  +-----------------------------------+
                  |    Next.js SPA (Reverse Proxy)    |
                  +-----------------------------------+
                                    |
                                    | Proxy Pass (/api/v1/* -> Port 8000)
                                    v
                  +-----------------------------------+
                  |          FastAPI Backend          |
                  +-----------------------------------+
                     /              |              \
                    /               |               \
                   v                v                v
         +------------+      +------------+      +------------+
         | PostgreSQL |      |   Redis    |      |   MinIO    |
         |  Database  |      | Task Queue |      | S3 Storage |
         +------------+      +------------+      +------------+
                                    ^
                                    | Pulls jobs
                                    v
                             +-------------+
                             |   Celery    |
                             | Ingest Task |
                             +-------------+
```

---

## 📌 Project Vision & Scope
In a democratic landscape like India, accessing unified, verified, and cross-referenced civic data remains a bottleneck. LokTathya bridges this gap by acting as a **single source of truth** for public representative histories, constituency boundary changes, and public expenditures.

### Core Guarantees
1. **Zero Hallucination Grounding**: The Civic AI assistant only replies with facts mapped directly to registered database entities. If data is absent, the system returns `DATA_NOT_AVAILABLE` instead of fabricating answers.
2. **Strict Provenance**: Every data point (a vote share, an asset declaration, a budget item) is linked to a source document registered in our registry.
3. **Neutral Reconciliation**: Conflicting data from different sources (e.g. state portals vs central databases) is never silently overwritten. Instead, the engine flags conflicts as `DATA_DISCREPANCY` and routes them to a human review queue.

---

## 🚀 Key Features

| Feature | Description | Sourcing Archives |
| :--- | :--- | :--- |
| **Civic Geography** | Interactive states, districts, and parliamentary/assembly constituencies mapped across delimitation cycles. | Election Commission of India (ECI), Survey of India |
| **Representatives Directory** | Cross-referenced portfolios of MPs and MLAs, including assets, criminal disclosures (ECI affidavits), and attendance. | ECI Affidavits, Parliament/Assembly Gazettes |
| **Election Analytics** | Constituency and polling-booth level vote counts, swings, margin of victories, and candidate details. | ECI Results Portals |
| **Finance & Projects** | Public expenditure tracking, constituency-level development fund (MPLADS/MLACDF) utilization. | Ministry of Finance, State Portals |
| **Civic AI Assistant** | Grounded retrieval chatbot with document citation blocks and integrated developer TraceNest logging. | Internal Verified Database |
| **Data Quality Index** | Real-time tracking of database conflicts, ingestion logs, and reconciliation status. | LokTathya Quality Engine |

---

## 🛠️ Tech Stack & Architecture

LokTathya is engineered as a decoupled, multi-container system:

* **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Local Theme Engine (Light/Dark mode with `localStorage` persistence).
* **Backend**: FastAPI (Python 3.11), SQLAlchemy 2.0 ORM, Alembic migrations.
* **Database**: PostgreSQL (v16) with PostGIS extension for spatial analysis and pgvector for semantic retrieval.
* **Broker & Cache**: Redis (v7) managing Celery background tasks and API response cache.
* **Object Store**: MinIO (S3-compatible) hosting raw source documents (PDFs, CSVs).
* **Tasks**: Celery Worker (data parsing, validation, ingestion) & Celery Scheduler (recurring sync tasks).

---

## ⚙️ Development Setup

The platform is strictly containerized. All installations and services run inside isolated Docker networks.

### Prerequisites
- Docker (Desktop / Engine) v20.10+
- Docker Compose v2.0+

### Step-by-Step Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/vishwajitvm/LokTathya.git
   cd LokTathya
   ```

2. **Configure Environment Variables**
   Copy the example environment configurations and fill in your keys:
   ```bash
   cp .env.example .env
   ```

3. **Build and Boot the Stack**
   Launch all components inside Docker:
   ```bash
   docker compose up -d --build
   ```
   *Note: In development, file changes in the `frontend` folder propagate instantly inside the container using Webpack polling.*

4. **Run Database Migrations**
   Initialize database tables (33 core relational tables + PostGIS/pgvector setups):
   ```bash
   docker compose exec backend alembic upgrade head
   ```

5. **Run Test Suites**
   Run backend pytest cases:
   ```bash
   docker compose exec backend pytest
   ```

### Operational Port Maps
- **Next.js Frontend**: [http://localhost:3000](http://localhost:3000)
- **FastAPI API Documentation**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **MinIO Console**: [http://localhost:9001](http://localhost:9001) (API: port 9000)
- **PostgreSQL Database**: Port 5432
- **Redis Cache**: Port 6379

---

## 📡 API Reference Documentation

All backend endpoints are documented in OpenAPI format at `/docs` (Port 8001). Below are the primary integration endpoints:

### 1. Civic Search
- **Endpoint**: `GET /api/v1/search/`
- **Query Parameters**: `query: str` (e.g. representative name, constituency)
- **Description**: Returns matching representatives, constituencies, or election instances with standard relevance scores.

### 2. Civic AI Chat
- **Endpoint**: `POST /api/v1/chat/`
- **Request Body**:
  ```json
  {
    "question": "Who is the MLA of constituency X?"
  }
  ```
- **Response**: Returns grounded answer blocks with database entity citations and a corresponding `X-Request-ID` header.

### 3. Representative Comparison
- **Endpoint**: `GET /api/v1/intelligence/compare/representatives`
- **Query Parameters**: `rep_a: UUID`, `rep_b: UUID`
- **Description**: Side-by-side analysis of representative details, asset portfolios, and election profiles.

### 4. Data Quality conflicts
- **Endpoint**: `GET /api/v1/data-quality/conflicts`
- **Description**: Lists active database discrepancies that require human auditing or source re-evaluation.

---

## 🔍 TraceNest Observability & Logging
Request lifecycle tracking is managed through **TraceNest**.
* Every request from the frontend is tagged with an `X-Request-ID` header.
* The backend middleware propagates this ID to Python logs, Celery workers, and database transaction queries as comments (`/* request_id: <id> */`).
* If an error occurs, the frontend parses the `X-Request-ID` and renders it on a user-facing Debug Card, making it trivial for administrators to locate transaction exceptions within the container logs.

To track a specific transaction log stream, run:
```bash
docker compose logs -f | grep "YOUR-REQUEST-ID"
```

---

## 🤝 Contributing Guidelines
We welcome contributions to expand India's open civic database.
1. **Data Schema Compliance**: All added schemas must inherit from SQLAlchemy models and contain proper audit columns (`created_at`, `updated_at`, `source_id`).
2. **Migration Files**: Always generate migrations via Alembic:
   ```bash
   docker compose exec backend alembic revision --autogenerate -m "description"
   ```
3. **Anti-regression Policy**: Verify your additions don't break existing layouts or test cases by running `pytest` and Next.js production builds.
