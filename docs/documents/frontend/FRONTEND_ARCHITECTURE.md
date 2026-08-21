# Frontend Architecture
LokTathya relies on a Next.js (App Router) + React + Tailwind CSS stack. 
The application acts strictly as a presentation layer consuming the `/api/v1/` endpoints. 
Server components are utilized for initial fast load, while interactive maps and search use client-side fetching.
