.PHONY: up down build logs restart shell migrate super-user

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

migrate:
	docker compose exec app alembic upgrade head

super-user:
	docker compose exec app python -m src.scripts.create_super_user

shell:
	docker compose exec app bash
