# 🇮🇳 LokTathya | National Civic Data & Grounded Intelligence Engine

[![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-emerald.svg)](https://github.com/vishwajitvm/LokTathya)
[![Docker Support: Enabled](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Tech Stack: FastAPI + Next.js](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Next.js-blueviolet.svg)](#-architecture-specifications)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **LokTathya (लोक तथ्य)** is India’s open, auditable civic intelligence platform. It grounds conversational artificial intelligence in deterministically verified historical datasets, constituency geographies, and public representative records sourced exclusively from official government archives.

---

## 📖 1. Mission Statement & Motivations

In a massive, complex democracy like India, civic data is often fragmented across hundreds of PDF bulletins, legislative portals, and regional web indices. This fragmentation makes auditing civic activities difficult for citizens, journalists, and researchers.

**LokTathya** was built to solve this problem by providing a centralized, auditable, and neutral repository of verified civic data.

### The Core Problem with Standard AI
Standard LLM chatbot assistants routinely hallucinate civic statistics, election counts, and representative portfolios. A hallucination in a civic database undermines public trust.

### The LokTathya Solution
LokTathya prevents hallucination by implementing a **strict database grounding layer**. Every response from the Civic AI chatbot is mapped directly to a verified record in our PostgreSQL database. If information is not available, the system returns `DATA_NOT_AVAILABLE` instead of guessing.

```
                  +-----------------------------------------+
                  |           Official Data Source          |
                  |     (ECI, Ministry of Finance, etc.)    |
                  +-----------------------------------------+
                                       |
                                       v
                  +-----------------------------------------+
                  |         Reconciliation Engine           |
                  |     (Resolves duplicate records)        |
                  +-----------------------------------------+
                                       |
                                       v
                  +-----------------------------------------+
                  |          Grounded SQL Database          |
                  |     (33 Tables + Vector Embeddings)     |
                  +-----------------------------------------+
                                       |
                                       v
                  +-----------------------------------------+
                  |            Civic AI Agent               |
                  |   (Only replies with database facts)    |
                  +-----------------------------------------+
```

---

## 🗺️ 2. Architectural Flows (Mermaid.ink Rendered)

To ensure the platform is easy to understand, we use [Mermaid.ink](https://mermaid.ink/) to render dynamic flowcharts directly from our source specifications.

### A. System Topology Overview
LokTathya is engineered as a decoupled, multi-container system. The client browser connects to Next.js on port 3000, which handles page rendering and proxies API calls to our FastAPI gateway (internal port 8000).

#### Rendered System Topology
![System Architecture Overview](https://mermaid.ink/img/Zmxvd2NoYXJ0IFRCCiAgICBzdWJncmFwaCBDbGllbnQgWyJDbGllbnQgQnJvd3NlciJdCiAgICAgICAgVUlbIk5leHQuanMgU1BBIChQb3J0IDMwMDApIl0KICAgIGVuZAoKICAgIHN1YmdyYXBoIEZyb250RW5kIFsiRnJvbnRlbmQgTGF5ZXIiXQogICAgICAgIFByb3h5WyJOZXh0LmpzIEFQSSBQcm94eSAoL2FwaS92MS8qKSJdCiAgICBlbmQKCiAgICBzdWJncmFwaCBCYWNrRW5kIFsiRmFzdEFQSSBCYWNrZW5kIExheWVyIChQb3J0IDgwMDAvODAwMSkiXQogICAgICAgIEFQSVsiRmFzdEFQSSBBcHAgKG1haW4ucHkpIl0KICAgICAgICBSb3V0ZXJbIlJvdXRlcnMgKGNoYXQsIGRhdGFfcXVhbGl0eSwgY29tcGFyZSwgcmVwb3J0cywgc291cmNlcykiXQogICAgICAgIFNlcnZpY2VbIlNlcnZpY2VzIChSQUcsIEludGVsbGlnZW5jZSwgRGF0YSBTeW5jKSJdCiAgICAgICAgTW9kZWxzWyJTUUxBbGNoZW15IE1vZGVscyAmIFNjaGVtYXMiXQogICAgICAgIFRyYWNlTmVzdFsiVHJhY2VOZXN0IE9ic2VydmFiaWxpdHkgTWlkZGxld2FyZSJdCiAgICBlbmQKCiAgICBzdWJncmFwaCBRdWV1ZSBbIkJhY2tncm91bmQgVGFzayBRdWV1ZSJdCiAgICAgICAgUmVkaXNbIlJlZGlzIChQb3J0IDYzNzkpIl0KICAgICAgICBDZWxlcnlXb3JrZXJbIkNlbGVyeSBXb3JrZXIiXQogICAgICAgIENlbGVyeVNjaGVkWyJDZWxlcnkgU2NoZWR1bGVyIl0KICAgIGVuZAoKICAgIHN1YmdyYXBoIERhdGEgWyJTdG9yYWdlIExheWVyIl0KICAgICAgICBQb3N0Z3Jlc1soIlBvc3RncmVTUUwgREIgKFBvcnQgNTQzMilcbjMzIFJlbGF0aW9uYWwgVGFibGVzIildCiAgICAgICAgTWluSU9bKCJNaW5JTyBPYmplY3QgU3RvcmFnZVxuUmF3IFBERi9DU1YgRGF0YSBTb3VyY2UiKV0KICAgIGVuZAoKICAgIFVJIC0tPnxIVFRQIFJlcXVlc3RzfCBQcm94eQogICAgUHJveHkgLS0-fFByb3h5IFBhc3MgL2FwaS92MS8gLT4gL3wgQVBJCiAgICAKICAgIEFQSSAtLT4gVHJhY2VOZXN0CiAgICBUcmFjZU5lc3QgLS0-IFJvdXRlcgogICAgUm91dGVyIC0tPiBTZXJ2aWNlCiAgICBTZXJ2aWNlIC0tPiBNb2RlbHMKICAgIAogICAgU2VydmljZSAtLT58VHJpZ2dlciBCYWNrZ3JvdW5kIFN5bmN8IFJlZGlzCiAgICBSZWRpcyAtLT4gQ2VsZXJ5V29ya2VyCiAgICBDZWxlcnlTY2hlZCAtLT58Q3JvbiBUcmlnZ2Vyc3wgUmVkaXMKICAgIAogICAgTW9kZWxzIC0tPnxSZWFkL1dyaXRlIFF1ZXJpZXN8IFBvc3RncmVzCiAgICBDZWxlcnlXb3JrZXIgLS0-fFJlY29uY2lsZSAmIExvYWQgRGF0YXwgUG9zdGdyZXMKICAgIENlbGVyeVdvcmtlciAtLT58RmV0Y2ggUmF3IEZpbGVzfCBNaW5JTwogICAgU2VydmljZSAtLT58UmV0cmlldmUgU291cmNlIERhdGF8IE1pbklP)

---

### B. Ingestion & Reconciliation Pipeline
This sequence details how raw PDF/CSV documents (from official sources like the Election Commission of India) are fetched from MinIO object storage, parsed, reconciled, and audited for anomalies (`DATA_DISCREPANCY` conflicts).

#### Rendered Ingestion Flow
![Ingestion & Reconciliation Sequence](https://mermaid.ink/img/c2VxdWVuY2VEaWFncmFtCiAgICBhdXRvbnVtYmVyCiAgICBhY3RvciBBZG1pbiBhcyBTeXN0ZW0gQWRtaW4gLyBDcm9uCiAgICBwYXJ0aWNpcGFudCBDZWxlcnkgYXMgQ2VsZXJ5IFdvcmtlciAvIEluZ2VzdCBUYXNrCiAgICBwYXJ0aWNpcGFudCBNaW5JTyBhcyBNaW5JTyBTdG9yYWdlIChSYXcgUERGcy9DU1ZzKQogICAgcGFydGljaXBhbnQgREIgYXMgUG9zdGdyZVNRTCAoQ29yZSBUYWJsZXMpCiAgICBwYXJ0aWNpcGFudCBEUSBhcyBQb3N0Z3JlU1FMIChkYXRhX3F1YWxpdHlfY29uZmxpY3RzKQoKICAgIEFkbWluLT4-Q2VsZXJ5OiBUcmlnZ2VyIEluZ2VzdGlvbiAoZS5nLiwgRUNJIEVsZWN0aW9uIFJlc3VsdHMpCiAgICBDZWxlcnktPj5NaW5JTzogRG93bmxvYWQgUmF3IENpdmljIFBERi9DU1YgRGF0YQogICAgTWluSU8tLT4-Q2VsZXJ5OiBSZXR1cm4gUmF3IERhdGEgU3RyZWFtCiAgICBDZWxlcnktPj5DZWxlcnk6IFBhcnNlICYgTm9ybWFsaXplIERhdGEgdG8gU2NoZW1hCiAgICAKICAgIE5vdGUgb3ZlciBDZWxlcnksIERCOiBSZWNvbmNpbGlhdGlvbiBQaGFzZSAoQ2hlY2sgZm9yIGR1cGxpY2F0ZXMvY29uZmxpY3RzKQogICAgQ2VsZXJ5LT4-REI6IENoZWNrIGlmIEVudGl0eSAoZS5nLiwgQ2FuZGlkYXRlLCBDb25zdGl0dWVuY3kpIEV4aXN0cwogICAgREItLT4-Q2VsZXJ5OiBSZXR1cm4gZXhpc3RpbmcgcmVjb3JkIChpZiBhbnkpCiAgICAKICAgIGFsdCBObyBDb25mbGljdCAoTmV3IEVudGl0eSBvciBJZGVudGljYWwgVmFsdWVzKQogICAgICAgIENlbGVyeS0-PkRCOiBJbnNlcnQgLyBVcGRhdGUgRW50aXR5IFJlY29yZAogICAgZWxzZSBDb25mbGljdCBEZXRlY3RlZCAoRGlmZmVyZW50IHZhbHVlcyBmb3Igc2FtZSBmaWVsZCBmcm9tIGRpZmZlcmVudCBzb3VyY2VzKQogICAgICAgIENlbGVyeS0-PkRROiBMb2cgQ29uZmxpY3QgKHN0YXR1cz1QRU5ESU5HLCByZXF1aXJlc19yZXZpZXc9dHJ1ZSkKICAgICAgICBOb3RlIG92ZXIgQ2VsZXJ5LCBEUTogRmxhZ2dlZCBhcyBEQVRBX0RJU0NSRVBBTkNZCiAgICAgICAgQ2VsZXJ5LT4-REI6IEluc2VydCAvIFVwZGF0ZSBFbnRpdHkgd2l0aCBhdWRpdCBmbGFncwogICAgZW5kCiAgICAKICAgIENlbGVyeS0vPj5BZG1pbjogVGFzayBDb21wbGV0ZSAoU3VtbWFyeSBvZiBJbmdlc3RlZCAmIENvbmZsaWN0ZWQgUmVjb3Jkcyk=)

---

### C. Grounded RAG Chatbot Pipeline
This flowchart illustrates the step-by-step query processing flow inside the **Civic AI** page. User input is validated, mapped to database contexts, grounded in SQL tables, and evaluated with anti-hallucination guardrails before responding.

#### Rendered Chatbot Flow
![RAG & Chatbot Pipeline Flow](https://mermaid.ink/img/Zmxvd2NoYXJ0IFRECiAgICBVc2VyKFtVc2VyIGluIFVJXSkgLS0-fFkwayBRdWVzdGlvbnwgQ2hhdFVJWyJDaXZpYyBBSSBQYWdlICgvY2l2aWMtYWkpIl0KICAgIENoYXRVSSAtLT58UE9TVCAvY2hhdC8gd2l0aCBwcm9tcHR8IEFQSVsiRmFzdEFQSSBDaGF0IFJvdXRlciJdCiAgICAKICAgIHN1YmdyYXBoIFJBR19QaXBlbGluZSBbIlJBRyBDb3JlIEluZ2VzdGlvbiAmIFJldHJpZXZhbCJdCiAgICAgICAgQVBJIC0tPnwxLiBQYXJzZSBSZXF1ZXN0fCBDaGF0U2VydmljZVsiQ2hhdCBTZXJ2aWNlIl0KICAgICAgICBDaGF0U2VydmljZSAtLT58Mi4gU2VhcmNoIFJlbGV2YW50IENvbnRleHR8IERCWyJQb3N0Z3JlU1FMIFNlYXJjaCBFbmdpbmUiXQogICAgICAgIERCIC0tPnxRdWVyeSBHZW9ncmFwaGllcywgUmVwcmVzZW50YXRpdmVzLCBFbGVjdGlvbnN8IFBvc3RncmVzVGFibGVzWygiMzMgQ29yZSBUYWJsZXMiKV0KICAgICAgICBQb3N0Z3Jlc1RhYmxlcyAtLT58UmV0dXJuIG1hdGNoZXMgJiBtZXRhZGF0YXwgREIKICAgICAgICBEQiAtLT58My4gUmV0dXJuIFNlbWFudGljIENvbnRleHR8IENoYXRTZXJ2aWNlCiAgICAgICAgCiAgICAgICAgQ2hhdFNlcnZpY2UgLS0-fDQuIEJ1aWxkIEdyb3VuZGVkIFByb21wdFxuKEFkZCBDb250ZXh0ICsgU3RyaWN0IEd1aWRlbGluZXMpfCBQcm9tcHRCdWlsZGVyWyJQcm9tcHQgQnVpbGRlciJdCiAgICAgICAgUHJvbXB0QnVpbGRlciAtLT58NS4gUmVxdWVzdCBSZXNwb25zZXwgTExNWyJMTE0gKENpdmljIEdyb3VuZGVkIEdlbmVyYXRvcikiXQogICAgICAgIExMTSAtLT58Ni4gR2VuZXJhdGUgUmVzcG9uc2Ugd2l0aCBDaXRhdGlvbnN8IFByb21wdEJ1aWxkZXIKICAgICAgICBQcm9tcHRCdWlsZGVyIC0tPnw3LiBGb3JtYXQgb3V0cHV0IGJsb2Nrc3wgQ2hhdFNlcnZpY2UKICAgIGVuZAogICAgCiAgICBDaGF0U2VydmljZSAtLT58OC4gUmV0dXJuIEFuc3dlciBCbG9ja3MgKyBUcmFjZU5lc3QgSUR8IENoYXRVSQogICAgQ2hhdFVJIC0tPnxSZW5kZXIgR3JvdW5kZWQgQW5zd2VyIHdpdGggQ2l0YXRpb25zfCBVc2Vy)

---

### D. Security Boundaries & Isolation Layout
We enforce network isolation. Only Next.js is port-forwarded outside the Docker engine boundary. The operational database, cache, backend REST services, and raw S3 stores remain unexposed to public requests.

#### Rendered Security Boundaries
![Security Architecture](https://mermaid.ink/img/Zmxvd2NoYXJ0IFRCCiAgICBzdWJncmFwaCBFeHRlcm5hbCBbIlB1YmxpYyBOZXR3b3JrIl0KICAgICAgICBDbGllbnRbIlVzZXIgQnJvd3NlciJdCiAgICBlbmQKCiAgICBzdWJncmFwaCBETVogWyJEZW1pbGl0YXJpemVkIFpvbmUgKFBvcnQgRm9yd2FyZGluZykiXQogICAgICAgIFByb3h5WyJOZXh0LmpzIFNlcnZlciAoUG9ydCAzMDAwKSJdCiAgICBlbmQKCiAgICBzdWJncmFwaCBJbnRlcm5hbCBbIkRvY2tlciBOZXR3b3JrIChsb2t0YXRoeWFfbmV0KSJdCiAgICAgICAgQVBJWyJGYXN0QVBJIEJhY2tlbmQgKFBvcnQgODAwMCwgSW50ZXJuYWwgT25seSkiXQogICAgICAgIAogICAgICAgIHN1YmdyYXBoIERhdGFiYXNlcyBbIlNlY3VyZSBEYXRhIExheWVyIl0KICAgICAgICAgICAgUG9zdGdyZXNbKCJQb3N0Z3JlU1FMIChQb3J0IDU0MzIpIildCiAgICAgICAgICAgIFJlZGlzWygiUmVkaXMgQ2FjaGUgKFBvcnQgNjM3OSkiKV0KICAgICAgICAgICAgTWluSU9bKCJNaW5JTyAoUG9ydCA5MDAwKSIpXQogICAgICAgIGVuZAogICAgZW5kCgogICAgQ2xpZW50IC0tPnxIVFRQUyBQb3J0IDMwMDAgT25seXwgUHJveHkKICAgIFByb3h5IC0tPnxJbnRlcm5hbCBQcm94eSBQYXNzfCBBUEkKICAgIAogICAgQVBJIC0tPnxBdXRoZW50aWNhdGVkIGNvbm5lY3Rpb258IFBvc3RncmVzCiAgICBBUEkgLS0-fEF1dGhlbnRpY2F0ZWQgY29ubmVjdGlvbnwgUmVkaXMKICAgIEFQSSAtLT58QXV0aGVudGljYXRlZCBjb25uZWN0aW9ufCBNaW5JTwogICAgCiAgICBjbGFzc0RlZiBzZWN1cmUgZmlsbDojZTFmNWZlLHN0cm9rZTojMDM5YmU1LHN0cm9rZS13aWR0aDoycHg7CiAgICBjbGFzc0RlZiBpc29sYXRlIGZpbGw6I2VmZWJlOSxzdHJva2U6IzVkNDAzNyxzdHJva2Utd2lkdGg6MnB4OwogICAgY2xhc3MgUG9zdGdyZXMsUmVkaXMsTWluSU8gc2VjdXJlOwogICAgY2xhc3MgQVBJIGlzb2xhdGU7)

---

### E. TraceNest Observability & Transaction Logging
TraceNest logs start-to-end request transactions. Request ID tags flow from Next.js, down to FastAPI, to Celery workers, and into SQL logs before outputting on front-end debugging blocks on API failure.

#### Rendered Tracing Flow
![TraceNest Request Tracing Sequence](https://mermaid.ink/img/c2VxdWVuY2VEaWFncmFtCiAgICBhdXRvbnVtYmVyCiAgICBhY3RvciBVc2VyIGFzIFVzZXIgQnJvd3NlcgogICAgcGFydGljaXBhbnQgRkUgYXMgTmV4dC5qcyBGcm9udGVuZAogICAgcGFydGljaXBhbnQgQkUgYXMgRmFzdEFQSSBCYWNrZW5kCiAgICBwYXJ0aWNpcGFudCBMb2dnZXIgYXMgVHJhY2VOZXN0IExvZ2dlcgogICAgcGFydGljaXBhbnQgREIgYXMgUG9zdGdyZVNRTCBEQgoKICAgIFVzZXItPj5GRTogQ2xpY2sgQWN0aW9uIChlLmcuLCBTZWFyY2ggLyBDb21wYXJlKQogICAgTm90ZSBvdmVyIEZFOiBHZW5lcmF0ZSBvciBpbmhlcml0IFgtUmVxdWVzdC1JRAogICAgRkUtPj5CRTogSFRUUCBSZXF1ZXN0IChIZWFkZXI6IFgtUmVxdWVzdC1JRCA9ICJ1dWlkLTEyMyIpCiAgICAKICAgIEJFLT4-QkU6IEluamVjdCBSZXF1ZXN0IElEIGluIENvbnRleHQgVmFyCiAgICBCRS0-PkxvZ2dlcjogTG9nIFN0YXJ0OiAiUmVxdWVzdCAvYXBpL3YxL3NlYXJjaCIgKHJlcXVlc3RfaWQ9InV1aWQtMTIzIikKICAgIAogICAgQkUtPj5EQjogRXhlY3V0ZSBRdWVyeSB3aXRoIHJlcXVlc3RfaWQgY29tbWVudCAvKiByZXF1ZXN0X2lkOiB1dWlkLTEyMyAqLwogICAgREItLT4-QkU6IFJldHVybiBEYXRhYmFzZSBSZXN1bHRzCiAgICAKICAgIGFsdCBTdWNjZXNzCiAgICAgICAgQkUtPj5Mb2dnZXI6IExvZyBFbmQ6ICJTdGF0dXMgMjAwIiAocmVxdWVzdF9pZD0idXVpZC0xMjMiKQogICAgICAgIEJFLS0-PkZFOiBIVFRQIDIwMCBPSyArIFJlc3VsdHMKICAgICAgICBGRS0tPj5Vc2VyOiBSZW5kZXIgUmVzdWx0cyAoQ2xlYW4pCiAgICBlbHNlIEZhaWx1cmUgKGUuZy4sIERCIEVycm9yIC8gVGltZW91dCkKICAgICAgICBCRS0-PkxvZ2dlcjogTG9nIEVycm9yOiAiRGF0YWJhc2UgY29ubmVjdGlvbiBmYWlsZWQiIChyZXF1ZXN0X2lkPSJ1dWlkLTEyMyIsIHRyYWNlPSIuLi4iKQogICAgICAgIEJFLS0-PkZFOiBIVFRQIDUwMCBJbnRlcm5hbCBFcnJvciArIEhlYWRlcjogWC1SZXF1ZXN0LUlEID0gInV1aWQtMTIzIgogICAgICAgIEZFLT4-RkU6IFBhcnNlIFgtUmVxdWVzdC1JRCBmcm9tIHJlc3BvbnNlCiAgICAgICAgRkUtLT4-VXNlcjogUmVuZGVyIEVycm9yIENhcmQgd2l0aCBUcmFjZU5lc3QgSUQgInV1aWQtMTIzIgogICAgZW5k)

---

## 💾 3. Database Schema Completeness (33 Tables)

LokTathya maps civic structures into **33 relational tables** inside PostgreSQL. Below is an overview of the core entities and their configurations:

```
+------------------+         +-----------------------+         +------------------+
|   Geographies    |-------->|    Representatives    |<--------|  Constituencies  |
|  (States/Dist)   |         |     (MPs / MLAs)      |         |  (Boundaries)    |
+------------------+         +-----------------------+         +------------------+
         |                               |                              |
         v                               v                              v
+------------------+         +-----------------------+         +------------------+
|     Sources      |         |       Elections       |         |   Data Quality   |
| (Provenance Reg) |         |   (Vote Counts/BOs)   |         | (Conflicts Logs) |
+------------------+         +-----------------------+         +------------------+
```

### Table Categories

#### 🗺️ 1. Geographic & Boundary Domain
* `states`: Core state mapping (e.g. state code, name, official language).
* `districts`: District names mapped to states.
* `constituencies`: Geographic bounds for Parliamentary and Assembly boundaries.
* `delimitation_cycles`: Tracks delimitation shifts (1952, 1963, 1973, 2002, etc.).

#### 👥 2. Representative Domain
* `representatives`: Profile details of candidates, MLAs, and MPs.
* `representative_terms`: Multi-year terms tracking start/end dates, state constituencies, and houses.
* `representative_assets`: Financial disclosures, declared assets, and liabilities.
* `representative_liabilities`: Detailed listing of debts and loans.
* `representative_criminal_cases`: Declared FIR cases and judicial charges.

#### 🗳️ 3. Election Domain
* `elections`: Metadata for Lok Sabha and Vidhan Sabha elections.
* `candidates`: Profiles of registered candidates.
* `election_results`: Vote tallies, margins, and outcomes per candidate.
* `booth_results`: Granular polling booth metrics.
* `voter_turnout`: Turnout statistics grouped by gender, age, and location.

#### 💰 4. Projects & Financial Domain
* `projects`: Development projects tracking statuses (ongoing, completed, stalled).
* `project_budgets`: Financial values allocated vs utilized.
* `municipal_budgets`: Detailed expenditure records for local municipal corporations.

#### 📝 5. Source Provenance & Quality Control
* `sources`: Verification register for ECI documents, gazette notifications, and financial sheets.
* `data_quality_conflicts`: Audit log tracking conflicting database inputs (`DATA_DISCREPANCY`).
* `observation_records`: Temporary observations parsed from ingestion streams.

---

## 🚀 4. Key Feature Workflows

### 📂 Dynamic Data Ingestion
Celery background workers process civic data. The ingestion task pulls files from MinIO, validates the schema structure, and uses a reconciliation check. If the values differ from an existing entry, the system logs a `DATA_DISCREPANCY` conflict in the quality control table.

### 🧠 Grounded Civic AI (RAG Pipeline)
1. **User Query**: A user asks, *"Who is the current representative of constituency X?"*
2. **Context Retrieval**: The API queries the database for matches and formats the results.
3. **Prompt Construction**: The system builds a prompt combining the user's question, the database context, and grounding rules (e.g. *"Answer the question using only the provided facts. Do not make up any information."*).
4. **LLM Inference**: The LLM generates the final response with source citations.

---

## 🛠️ 5. Technical Specifications & Stack

* **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Dark/Light Mode Theme Toggle.
* **Backend**: FastAPI (Python 3.11), SQLAlchemy 2.0 ORM, Alembic migrations.
* **Database**: PostgreSQL (v16) with PostGIS extension for spatial analysis and pgvector for semantic retrieval.
* **Broker & Cache**: Redis (v7) managing Celery background tasks and API response cache.
* **Object Store**: MinIO (S3-compatible) hosting raw source documents (PDFs, CSVs).
* **Tasks**: Celery Worker (data parsing, validation, ingestion) & Celery Scheduler (recurring sync tasks).

---

## ⚙️ 6. Setup & Development Environment

LokTathya runs strictly inside Docker. All commands must be executed within the containers.

### Prerequisites
* Docker Engine / Desktop v20.10+
* Docker Compose v2.0+

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

### Port Mappings
* **Next.js Frontend**: [http://localhost:3000](http://localhost:3000)
* **FastAPI API Documentation**: [http://localhost:8001/docs](http://localhost:8001/docs)
* **MinIO Console**: [http://localhost:9001](http://localhost:9001)
* **PostgreSQL Database**: Port 5432
* **Redis Cache**: Port 6379

---

## 📡 7. API Reference Documentation

All backend endpoints are documented in OpenAPI format at `/docs` (Port 8001). Below are the primary integration endpoints:

### 1. Civic Search
* **Endpoint**: `GET /api/v1/search/`
* **Query Parameters**: `query: str` (e.g. representative name, constituency)
* **Description**: Returns matching representatives, constituencies, or election instances with standard relevance scores.

### 2. Civic AI Chat
* **Endpoint**: `POST /api/v1/chat/`
* **Request Body**:
  ```json
  {
    "question": "Who is the MLA of constituency X?"
  }
  ```
* **Response**: Returns grounded answer blocks with database entity citations and a corresponding `X-Request-ID` header.

### 3. Representative Comparison
* **Endpoint**: `GET /api/v1/intelligence/compare/representatives`
* **Query Parameters**: `rep_a: UUID`, `rep_b: UUID`
* **Description**: Side-by-side analysis of representative details, asset portfolios, and election profiles.

### 4. Data Quality conflicts
* **Endpoint**: `GET /api/v1/data-quality/conflicts`
* **Description**: Lists active database discrepancies that require human auditing or source re-evaluation.

---

## 🔍 8. TraceNest Request Tracing
Request lifecycle tracking is managed through **TraceNest**.
* Every request from the frontend is tagged with an `X-Request-ID` header.
* The backend middleware propagates this ID to Python logs, Celery workers, and database transaction queries as comments (`/* request_id: <id> */`).
* If an error occurs, the frontend parses the `X-Request-ID` and renders it on a user-facing Debug Card, making it trivial for administrators to locate transaction exceptions within the container logs.

To track a specific transaction log stream, run:
```bash
docker compose logs -f | grep "YOUR-REQUEST-ID"
```

---

## 🤝 9. Contributing Guidelines
We welcome contributions to expand India's open civic database.
1. **Data Schema Compliance**: All added schemas must inherit from SQLAlchemy models and contain proper audit columns (`created_at`, `updated_at`, `source_id`).
2. **Migration Files**: Always generate migrations via Alembic:
   ```bash
   docker compose exec backend alembic revision --autogenerate -m "description"
   ```
3. **Anti-regression Policy**: Verify your additions don't break existing layouts or test cases by running `pytest` and Next.js production builds.
