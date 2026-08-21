# Development Guide

Welcome to LokTathya! This project uses a strictly Docker-based workflow.

## The Standard Workflow

Do **NOT** use `python -m venv` or install local dependencies.

1. **Clone the project:**
   ```bash
   git clone <url>
   cd LokTathya
   ```
2. **Setup secrets:**
   ```bash
   cp .env.example .env
   ```
3. **Build and start the environment:**
   ```bash
   docker compose build
   docker compose up -d
   ```
4. **Provision the database:**
   ```bash
   docker compose exec backend alembic upgrade head
   ```

## Hot Reload
- The backend uses `uvicorn --reload` inside the container. Editing a `.py` file in `backend/` will automatically restart the server.
- The frontend uses `next dev` inside the container. Edits to `frontend/` files reflect instantly.

## Dependencies
- To add a Python dependency, add it to `backend/requirements.txt` and run `docker compose build backend`.
- To add a Node dependency, run `docker compose exec frontend npm install <package>`.

## Important Rules
- Do not commit API keys or Stitch credentials. Use `.env`.
- No `pip install` on host.
- No `npm install` on host.
- No PostgreSQL installation on host.
