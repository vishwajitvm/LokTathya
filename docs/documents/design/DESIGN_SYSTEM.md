# Design System Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | UI & UX Design System Specification |
| Status | BLOCKED_EXTERNAL_TOOL_ACCESS |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Frontend User Interface |

---

## 1. Purpose
This document specifies the design system guidelines, color typography maps, collapsible components, and responsive grid layouts of the LokTathya platform. It defines UI rendering specifications for web, mobile, and tablet viewports.

---

## 2. Design System Framework

LokTathya utilizes **Tailwind CSS** utility classes to configure styling. Colors and layouts match dark and light mode configurations.

```
       +---------------------------------------------+
       |             Tailwind Base Layer             |
       +---------------------------------------------+
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
+-----------------------------+               +-----------------------------+
|      Light Mode Theme       |               |       Dark Mode Theme       |
|    (Slate-50 Background)    |               |    (Slate-950 Background)   |
+-----------------------------+               +-----------------------------+
```

### A. Theme Colors Map
* **Light Mode Background**: `rgb(248, 250, 252)` (`bg-slate-50`).
* **Light Mode Text**: `rgb(15, 23, 42)` (`text-slate-900`).
* **Dark Mode Background**: `rgb(2, 6, 23)` (Custom root background).
* **Dark Mode Text**: `rgb(248, 250, 252)` (`text-slate-50`).
* **Accent Colors**: Slate blue (`text-blue-600` / `text-blue-400`) for navigation links and action items.

### B. Typography Hierarchy
* **Primary Sans-Serif Font**: `Inter` or standard system sans-serif (`font-sans`).
* **Data Monospace Font**: `JetBrains Mono` or standard system monospace (`font-mono`) for values, budget rates, and vote counts to ensure clean tabular alignment.
* **Size Hierarchy**:
  * Page Title: `text-3xl` (30px), bold.
  * Section Header: `text-xl` (20px), semibold.
  * Card Header: `text-lg` (18px), medium.
  * Body Text: `text-base` (16px), regular.

---

## 3. Responsive Grid Layouts

The interface adjusts layouts based on device viewports:

### A. Mobile Viewports (Width < 768px)
* Layout compiles as a single-column block.
* Navigation menus collapse into a mobile drawer interface.
* Charts and data tables are simplified, replacing detailed columns with summary blocks.

### B. Tablet Viewports (768px <= Width < 1024px)
* Layout compiles as a double-pane grid interface.
* Sidebars collapse to optimize reading spaces.

### C. Desktop Viewports (Width >= 1024px)
* Layout compiles as a multi-pane split interface.
* Interactive maps and comparative charts are displayed side-by-side with detail panels.

---

## 4. Accessibility & Navigation Controls

* **Interactive Elements**: All buttons and anchor tags must include valid `aria-label` or `aria-expanded` attributes.
* **Keyboard Navigation**: Navigating through the platform (including sidebar filters) must support standard focus rings and tab controls (`focus:ring-2`).

---

## 5. Stitch Tool Block
* **Status**: `BLOCKED_EXTERNAL_TOOL_ACCESS`
* **Notes**: The legacy Stitch design translation tools are unavailable in this environment. Styling changes are implemented directly using Next.js components and Tailwind CSS configurations to ensure maintainability.

---

## 6. Related Documents
* [FRONTEND_ARCHITECTURE.md](file:///c:/python/LokTathya/docs/documents/frontend/FRONTEND_ARCHITECTURE.md)
* [PLATFORM_CORE.md](file:///c:/python/LokTathya/docs/features/00-platform/PLATFORM_CORE.md)
