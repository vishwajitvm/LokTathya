# Docker Architecture & Usage Guide

All LokTathya runtime components run inside Docker. There is no need to install Python, Node.js, PostgreSQL, or Redis directly on the host machine.

## Prerequisites
- Docker
- Docker Compose
- Git

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd LokTathya
   ```
2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

## Starting the Stack
To build and start all services in the background:
```bash
docker compose up -d --build
```
Alternatively, using the provided Makefile:
```bash
make build
make up
```

## Viewing Logs
To view logs for all services:
```bash
docker compose logs -f
```
Or use the Makefile:
```bash
make logs
```

## Running Migrations
Alembic runs INSIDE the backend container.
```bash
docker compose exec backend alembic upgrade head
```
Or:
```bash
make migrate
```

## Running Tests
Run Python tests inside the backend container:
```bash
docker compose exec backend pytest
```
Run frontend tests:
```bash
docker compose exec frontend npm test
```

## Accessing Services
- **Frontend:** http://localhost:3000
- **Backend API Docs:** http://localhost:8000/docs
- **MinIO Console:** http://localhost:9001 (Credentials: minioadmin / minioadmin by default)

## Stopping the Stack
```bash
docker compose down
```

## Resetting the Database
WARNING: This destroys all local database data, Redis cache, and MinIO storage.
```bash
docker compose down -v
```
Or:
```bash
make db-reset
```

## Backing Up & Restoring the Database
To create a logical backup of the PostgreSQL database:
```bash
docker compose exec -T postgres pg_dump -U loktathya_user loktathya_db > backup.sql
```
To restore a backup:
```bash
cat backup.sql | docker compose exec -T postgres psql -U loktathya_user -d loktathya_db
```

## Troubleshooting
- **Ports already in use:** Ensure ports 3000, 8000, 5432, 6379, 9000, and 9001 are free on your host.
- **Dependency sync issues:** Avoid running `pip install` or `npm install` on your host. If you add a dependency to `requirements.txt` or `package.json`, run `docker compose build` to rebuild the images.
