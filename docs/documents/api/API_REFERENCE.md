# API Reference Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | API Interface Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Public REST API Endpoints |

---

## 1. Purpose
This document specifies the public REST API endpoints, request/response schemas, status codes, and security controls of the LokTathya platform. It acts as the technical reference for frontend developers and API consumers.

---

## 2. API Endpoints

### A. Endpoint: Search
* **Method**: `GET`
* **Path**: `/api/v1/search/`
* **Purpose**: Resolves search queries to matching database records (representatives, constituencies, elections, projects).
* **Authentication**: None
* **Request Parameters**:
  * `query` (Query String, Required): The search query.
  * `page` (Query Integer, Optional): Defaults to `1`.
  * `page_size` (Query Integer, Optional): Defaults to `20`.
* **Response Payload (Success - 200 OK)**:
  ```json
  {
    "query": "Conrad",
    "results": [
      {
        "id": "a1b2c3d4-e5f6-7a8b-9c0d-e1f2a3b4c5d6",
        "type": "representative",
        "name": "Conrad Sangma",
        "constituency": "Tura",
        "state": "Meghalaya",
        "party": "NPP"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 1,
      "total_results": 1
    }
  }
  ```
* **Status Codes**:
  * `200 OK`: Request processed successfully.
  * `400 Bad Request`: Query parameter is missing or empty.
  * `500 Internal Server Error`: Database connection failure.

---

### B. Endpoint: Grounded Chat
* **Method**: `POST`
* **Path**: `/api/v1/chat/`
* **Purpose**: Processes natural-language questions and returns grounded answers with citations.
* **Authentication**: None
* **Request Body**:
  ```json
  {
    "question": "Who is the MP of Shillong?"
  }
  ```
* **Response Payload (Success - 200 OK)**:
  ```json
  {
    "answer": "The MP of Shillong is Vincent Pala.",
    "citations": [
      {
        "source_id": "SRC-IN-ECI-001",
        "document_name": "Vincent Pala ECI Nomination Affidavit 2024",
        "url": "https://minio.loktathya.org/affidavits/vincent_pala_2024.pdf"
      }
    ],
    "request_id": "uuid-12345"
  }
  ```
* **Status Codes**:
  * `200 OK`: Request processed successfully.
  * `400 Bad Request`: Request body is invalid or empty.
  * `503 Service Unavailable`: LLM API endpoint timeout or failure.

---

### C. Endpoint: Representative Disclosures
* **Method**: `GET`
* **Path**: `/api/v1/representatives/{id}/disclosures`
* **Purpose**: Retrieves asset, liability, and criminal records disclosures for a representative.
* **Authentication**: None
* **Request Parameters**:
  * `id` (Path UUID, Required): Representative ID.
* **Response Payload (Success - 200 OK)**:
  ```json
  {
    "representative_id": "a1b2c3d4-e5f6-7a8b-9c0d-e1f2a3b4c5d6",
    "assets": {
      "movable": 5000000.00,
      "immovable": 9000000.00,
      "total": 14000000.00
    },
    "liabilities": {
      "bank_loans": 2000000.00,
      "total": 2000000.00
    },
    "criminal_cases": [
      {
        "case_number": "FIR-45/2022",
        "charges": "IPC Section 188",
        "court": "District Court Tura"
      }
    ]
  }
  ```
* **Status Codes**:
  * `200 OK`: Request processed successfully.
  * `404 Not Found`: Representative ID does not exist.

---

## 3. Rate Limiting & Security Controls

* **Rate Limiting**: Public API endpoints are rate-limited to 60 requests per minute per IP address. Administrative endpoints are limited to 10 requests per minute.
* **TraceNest Header**: All API requests and responses carry the `X-Request-ID` transaction token.
* **CORS Policy**: Configured to restrict external API requests to authorized origins.

---

## 4. Related Documents
* [PLATFORM_CORE.md](file:///c:/python/LokTathya/docs/features/00-platform/PLATFORM_CORE.md)
* [CIVIC_AI_RAG.md](file:///c:/python/LokTathya/docs/features/08-ai/CIVIC_AI_RAG.md)
