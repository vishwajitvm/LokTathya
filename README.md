# LokTathya

## Project Purpose
LokTathya is a comprehensive Civic Intelligence platform that grounds LLM interactions in deterministically verified historical data, elections, and public representatives.

## Architecture
- **Frontend**: Next.js 14.2.3, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL with PostGIS and pgvector
- **Cache/Broker**: Redis
- **Storage**: MinIO
- **Tasks**: Celery (Worker & Scheduler)
- **Deployment**: Strictly Dockerized

## Local Development
Everything MUST run inside Docker. Do not run `npm` or `pip` on the host machine.

### Start the Stack
```bash
docker compose up -d --build
```
This automatically maps:
- Frontend -> localhost:3000
- Backend -> localhost:8001 (Internally port 8000)
- PostgreSQL -> localhost:5432
- MinIO -> localhost:9000 & 9001
- Redis -> localhost:6379

### Environment Variables
Copy `.env.example` to `.env` and fill in the required credentials. See `.env.example` for the required keys.

### Migrations
```bash
docker compose exec backend alembic upgrade head
```

### Testing
```bash
docker compose exec backend pytest
```

### Checking Logs
```bash
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f worker
docker compose logs -f scheduler
```
