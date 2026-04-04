.PHONY: run test lint migrate seed

run:
	uvicorn app.main:app --reload --port 8000

test:
	python -m pytest

lint:
	ruff check . && ruff format --check .

migrate:
	alembic upgrade head

seed:
	python -m app.seed
