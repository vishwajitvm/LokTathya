# Phase 7 Source Registry Schema & Catalog

This document details the database catalog schema for official sources and endpoints.

---

## 1. DB Models
- **src_source**: Core metadata table tracking the official authority name, government level, priority, contact parameters, and legal access policy.
- **src_endpoint**: Endpoints mapping to the parent source, tracking URL, canonical URL format, ETag, Last-Modified checksums, and scheduler states.
