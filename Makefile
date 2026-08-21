.PHONY: build up down logs migrate restart destroy db-reset test

up:
	docker compose up -d

build:
	docker compose build

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose exec backend alembic upgrade head

migration:
	docker compose exec backend alembic revision --autogenerate -m "auto"

test:
	docker compose exec backend pytest

db-reset:
	docker compose down -v
	docker compose up -d postgres
