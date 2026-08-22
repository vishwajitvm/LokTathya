# Phase 7 Source Discovery Engine

This document details sitemap and feed discovery logic.

---

## 1. Discovery Mechanisms
- **Sitemap index**: Handles nested sitemap indexing dynamically by querying `<sitemapindex>` roots and fetching children recursively.
- **RSS & Atom**: Inspects update entries, parsing publication details and filtering candidate targets against domain limitations.
- **Review Queue**: Discovered items start in `CANDIDATE` state. Admin endpoints approve or reject candidates to prevent random crawling.
