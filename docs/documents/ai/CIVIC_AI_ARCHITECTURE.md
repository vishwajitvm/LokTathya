# Civic AI Architecture Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | AI & Retrieval System Architecture |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | AI Subsystem |

---

## 1. Purpose
This document specifies the architecture, component interaction, search pipeline, and security constraints of the **Civic AI** assistant. The Civic AI assistant is a grounded question-answering interface, not a generic chatbot. It converts user questions into structured database context lookups and generates verified, cited answers.

---

## 2. Background
Generative AI chatbots are prone to hallucinating facts, statistics, and citations. In a public civic intelligence context, a single hallucinated detail undermines the credibility of the entire platform. The Civic AI subsystem is built with strict grounding layers and vector retrieval architectures to ensure that all answers are backed by verified database records.

---

## 3. Core System Architecture

The Civic AI assistant acts as a natural language gateway to the Postgres database. It does not execute raw SQL queries; instead, it uses pre-defined analytical tools to retrieve data.

```
       +---------------------------------------------+
       |                 User Client                 |
       +---------------------------------------------+
                              |
                              | POST /api/v1/chat/
                              v
       +---------------------------------------------+
       |             FastAPI Chat Router             |
       +---------------------------------------------+
                              |
                              v
       +---------------------------------------------+
       |                Chat Service                 |
       +---------------------------------------------+
         /                                         \
        /                                           \
       v                                             v
+-----------------------------+               +-----------------------------+
|    Semantic Search Index    |               |    Predefined CivicTools    |
|   (pgvector Embeddings)     |               |    (Deterministic APIs)     |
+-----------------------------+               +-----------------------------+
```

### A. Semantic Search Index (`pgvector`)
* Description: Stores vector embeddings of candidate profiles, project descriptions, and budget items.
* Embeddings Model: `text-embedding-3-small` (1536 dimensions).
* Index Type: HNSW index configured on the vector columns for fast similarity lookups.

### B. Predefined CivicTools
The LLM is restricted from generating SQL queries directly. Instead, the planner routes queries to specific database functions (`CivicTools`):
* `get_representative_disclosures(rep_id: UUID)`: Fetches verified asset and criminal profiles.
* `get_constituency_projects(const_id: UUID)`: Retrieves active infrastructure works.
* `get_election_results(election_id: UUID)`: Retrieves vote counts and swing metrics.

### C. Search, Retrieval & Vector Storage Strategy
* **Full Text Search**: PostgreSQL `to_tsvector` is utilized using lexical matching for both English and Hindi text.
* **Hybrid Retrieval**: Combines Full Text Search (FTS) with pgvector outputs utilizing Reciprocal Rank Fusion (RRF) algorithms.
* **Metadata Filtering**: Source, jurisdiction, date, and document type filters must restrict candidate pools before semantic ranking is performed.
* **Vector Storage Partitioning**: Storage relies solely on PostgreSQL with the `pgvector` extension. Database tables are partitioned by vector dimensions (e.g. `ai_embedding_1024`, `ai_embedding_1536`) to enforce HNSW/IVFFlat indexing constraints without adding external vector database instances.
* **Reranking**: An abstract Reranker pipeline exists for top-K refinement, disabled until baseline metrics require it.

---

## 4. Grounded Retrieval-Augmented Generation (RAG) Pipeline

```
[User Question]
       |
       v
[Semantic & Keyword Search] ---> [Query pgvector & Postgres Tables]
                                              |
                                              v
[Context Extraction] ------------> [Build Grounded Prompt Template]
                                              |
                                              v
[Prompt Validation] -------------> [Request LLM Completion (Inference)]
                                              |
                                              v
[Citation Check Engine] ---------> [Stream Response + Source Citations]
```

1. **Query Analysis**: The `Planner` determines if the query requires semantic search, database lookup tools, or a direct response.
2. **Context Retrieval**: Runs keyword and vector similarity searches against the database indexes, filtering results by confidence score.
3. **Prompt Compilation**: Injects the retrieved records as a raw text block into the system prompt template.
4. **LLM Inference**: The LLM processes the prompt and generates a factual response.
5. **Citation Validation**: The system parses the generated text and verifies that all references map back to a verified record in the `sources` registry.

---

## 5. Security & Hallucination Defenses

* **No Arbitrary SQL Execution**: The LLM cannot write or execute raw SQL. All data queries go through typed, pre-defined methods to prevent SQL injection vulnerabilities.
* **Factual Constraint Guidelines**: The system prompt instructs the LLM to return `DATA_NOT_AVAILABLE` if the retrieved context is insufficient to answer the question.
* **Prompt Injection Shield**: Input queries are sanitized to filter out system instruction override attempts.

---

## 6. Related Documents
* [CIVIC_AI_RAG.md](file:///c:/python/LokTathya/docs/features/08-ai/CIVIC_AI_RAG.md)
* [AI_MODEL_REGISTRY.md](file:///c:/python/LokTathya/docs/documents/ai-models/AI_MODEL_REGISTRY.md)
