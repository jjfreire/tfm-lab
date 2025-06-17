.PHONY: help db backend frontend install install-backend install-frontend stop clean purge

help:
	@echo "Available commands:"
	@echo "  make db              Start PostgreSQL container"
	@echo "  make backend         Run FastAPI backend (localhost:8000)"
	@echo "  make frontend        Run Vue frontend (localhost:5173)"
	@echo "  make install         Install all dependencies"
	@echo "  make stop            Stop docker containers"
	@echo "  make clean           Stop and remove containers/volumes"
	@echo "  make purge           Remove venv and node_modules (use with caution)"

db:
	docker compose up db

backend:
	PYTHONPATH=./backend ./backend/venv/bin/uvicorn app.main:app --reload --app-dir backend/app

frontend:
	cd frontend && npm run dev

install:
	make install-backend
	make install-frontend

install-backend:
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

stop:
	docker compose stop

clean:
	docker compose down -v

purge:
	rm -rf backend/venv frontend/node_modules frontend/package-lock.json
