# Frontend Architecture Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Frontend Subsystem Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Web Application Frontend |

---

## 1. Purpose
This document specifies the Next.js App Router structure, client/server rendering models (SSR/CSR), responsive grid systems, Tailwind styles, and state management of the LokTathya frontend application.

---

## 2. Frontend Subsystems & App Routing

LokTathya uses **Next.js 14** app directory structure to manage pages and routing:

```
frontend/app/
├── civic-ai/          # Grounded AI Chat Assistant Page
├── compare/           # Representative Comparison Page
├── data-quality/      # Ingestion & Conflict Auditing Page
├── elections/         # Election Results & Swings Dashboard
├── finance/           # Municipal Budget Analysis Dashboard
├── geography/         # PostGIS Constituency Mapping
├── layout.tsx         # Global Theme Injection Script
└── page.tsx           # Search Centric Homepage
```

### A. Server-Side Rendering (SSR) vs Client Components (CSR)
* **Server Components (Default)**: Static pages (e.g. documentation, homepages) are rendered on the server to optimize loading times and SEO performance.
* **Client Components (`'use client'`)**: Interactive pages (e.g. vector search maps, RAG chat interfaces) leverage client-side hydration to manage UI state changes.

---

## 3. Global Theme & Dark Mode Integration

To prevent background flickering on page load, a theme-checking script is injected directly into the `<head>` of [`layout.tsx`](file:///c:/python/LokTathya/frontend/app/layout.tsx):

```javascript
(function() {
  const theme = localStorage.getItem('theme') || 'dark';
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
})();
```

* **Tailwind darkMode Strategy**: Configured with the `class` strategy in `tailwind.config.js`.
* **Root Background Color Specificity**: Statically styled in `globals.css` using `html.dark` selectors to ensure dark slate backgrounds are rendered consistently.

---

## 4. State Management & URL Synced States

Interactive components (like filters, search terms, map cycles) synchronize their UI state directly with the URL query parameters (using Next.js `useSearchParams` and `useRouter` hooks):
* **Benefits**: Enables link sharing (users can copy the URL and share the exact state of the comparison chart or map boundary filters).
* **Hydration Protection**: All URL query parameters are parsed within `Suspense` boundary wrappers to prevent React hydration mismatches in server-side builds.

---

## 5. Accessibility & Search Engine Optimization (SEO)

* **Semantic HTML**: Frontend utilizes proper structural tags (`<main>`, `<header>`, `<footer>`, `<section>`) to ensure screen reader compatibility.
* **Metadata Configuration**: Each page exports a statically defined `Metadata` block providing unique title, description, and canonical link configurations to optimize search indexing performance.

---

## 6. Performance Optimization & Bundle Splits

To maintain fast page load times across mobile networks, the application implements code-splitting:
* **Dynamic Imports**: Large chart and map packages (e.g., Leaflet, Chart.js) are loaded dynamically using `next/dynamic` with `ssr: false` configurations to minimize the initial javascript bundle size.
* **Image Optimization**: Sourced photos and candidate images are optimized on-demand using the Next.js `<Image>` component to reduce data usage on mobile devices.

---

## 7. Dynamic Route Pre-rendering

For high-traffic constituency and representative profile pages:
* **Dynamic Page Generation**: Uses `generateStaticParams` to pre-compile the top 500 most-searched representative profiles during build time.
* **Incremental Static Regeneration (ISR)**: Sets a revalidation threshold of 24 hours (`export const revalidate = 86400`) to dynamically update profiles in the background when database tables change.

---

## 8. Related Documents
* [DESIGN_SYSTEM.md](file:///c:/python/LokTathya/docs/documents/design/DESIGN_SYSTEM.md)
* [PLATFORM_CORE.md](file:///c:/python/LokTathya/docs/features/00-platform/PLATFORM_CORE.md)
