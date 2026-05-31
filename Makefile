.PHONY: up down build logs restart shell migrate super-user

# Docker
up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

logs:
	docker compose logs -f

restart:
	docker compose restart

# Database
migrate:
	docker compose exec app alembic upgrade head

# Super user
super-user:
	docker compose exec app python -m src.scripts.create_super_user

# Dev
shell:
	docker compose exec app bash

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/

format:
	uv run ruff format src/