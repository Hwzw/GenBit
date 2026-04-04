.PHONY: dev-backend dev-frontend db-up db-down db-migrate lint test

db-up:
	docker compose up -d

db-down:
	docker compose down

dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

db-migrate:
	cd backend && alembic upgrade head

lint:
	cd backend && ruff check . && ruff format --check .
	cd frontend && npm run lint

test:
	cd backend && python -m pytest
	cd frontend && npm test
