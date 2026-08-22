# AI Model Registry Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | AI System Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | AI Providers & Models Configuration |

---

## 1. Purpose
This document specifies the supported Large Language Models (LLM), embedding models, provider registries, and fallback configurations of the LokTathya platform. It details model capabilities, token limits, and deprecation cycles.

---

## 2. Model Registry

LokTathya uses a registry pattern to configure model interfaces. This decoupling ensures that model upgrades or provider changes do not require refactoring the core RAG services.

| Model ID | Provider | Type | Context Window | Dimensions | Latency (P90) | Target Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `gemini-1.5-flash` | Google AI | LLM | 1M tokens | N/A | 0.8s | Primary Grounded Generator |
| `gemini-1.5-pro` | Google AI | LLM | 2M tokens | N/A | 2.5s | Analytical Dossier Planner |
| `text-embedding-3-small` | OpenAI | Embedding | 8k tokens | 1536 | 0.2s | Semantic Search Encoder |

---

## 3. Model Capabilities & Selection Rationale

### A. Gemini 1.5 Flash
* **Context Limit**: 1,048,576 tokens.
* **Capabilities**: Multimodal native support, high speed, and low latency.
* **Use Case**: Used for real-time grounded conversational queries on the `/civic-ai` interface.

### B. Gemini 1.5 Pro
* **Context Limit**: 2,097,152 tokens.
* **Capabilities**: Complex logical reasoning and high context retention.
* **Use Case**: Used for compiling multi-source dossiers and generating analytical summaries.

### C. OpenAI Text Embedding 3 Small
* **Dimensions**: 1536.
* **Capabilities**: Strong semantic alignment and low dimensions to optimize storage size.
* **Use Case**: Generating vector coordinates for representative records and project descriptions.

---

## 4. Rate Limiting & Cost Constraints

* **Google AI Free Tier**: Subject to a rate limit of 15 Requests Per Minute (RPM) and 1,500 Requests Per Day (RPD).
* **Usage Caps**: The backend enforces local Redis rate-limiting blocks of 10 requests per minute per IP to prevent exhausting API limits.

---

## 5. Fallback & Failover Strategy

To maintain platform availability, the backend implements a secondary provider fallback chain:

```
[User Chat Request]
         |
         v
[Primary Provider API] -----------> (Success) ---> [Return Response]
         |
      (Failure)
         |
         v
[Secondary Fallback API] --------> (Success) ---> [Return Response]
         |
      (Failure)
         |
         v
[Return HTTP 503 Service Unavailable]
```

* **Primary Endpoint**: Google Gemini API (`gemini-1.5-flash`). Handles grounded user chat completions.
* **Secondary Fallback**: Local or secondary provider API endpoints (e.g. Llama 3 via self-hosted Ollama / HuggingFace).
* **Timeout Threshold**: Failover is triggered if the primary endpoint fails to return a completion within 6.0 seconds.

---

## 6. Embedding Registry

Semantic search requires encoding text queries into vector coordinates:
* **Model**: `text-embedding-3-small` (1536 dimensions).
* **Database Storage**: Saved in the `pgvector` column of the `representatives` and `projects` tables.
* **Similarity Metric**: Cosine distance indexes are configured for search.

---

## 7. Model Versioning & Deprecation

* **Stable Alias Mapping**: The codebase references alias configurations (`chat-model-primary`) rather than specific model version IDs. Upgrading the underlying model version is done by modifying the registry settings file.
* **Deprecation Policy**: Model versions are updated annually. Legacy endpoints are phased out within 6 months of a new model release.

---

## 8. Related Documents
* [CIVIC_AI_ARCHITECTURE.md](file:///c:/python/LokTathya/docs/documents/ai/CIVIC_AI_ARCHITECTURE.md)
* [CIVIC_AI_RAG.md](file:///c:/python/LokTathya/docs/features/08-ai/CIVIC_AI_RAG.md)
