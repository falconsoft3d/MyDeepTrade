.PHONY: help build up down restart logs logs-worker shell migrate createsuperuser clean test

help:
	@echo "MyDeepTrade - Available commands:"
	@echo "  make build         - Build Docker images"
	@echo "  make up            - Start all services"
	@echo "  make down          - Stop all services"
	@echo "  make restart       - Restart all services"
	@echo "  make logs          - Show logs from all services"
	@echo "  make logs-worker   - Show logs from worker service"
	@echo "  make shell         - Open Django shell"
	@echo "  make migrate       - Run database migrations"
	@echo "  make createsuperuser - Create a superuser"
	@echo "  make clean         - Stop and remove all containers and volumes"
	@echo "  make test          - Run tests"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started! Access at http://localhost:8000"
	@echo "Default credentials: admin / admin123"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-worker:
	docker-compose logs -f worker

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

clean:
	docker-compose down -v
	@echo "All containers and volumes removed!"

test:
	docker-compose exec web python manage.py test

# Local development commands
local-run:
	python manage.py runserver

local-worker:
	python manage.py run_workorders

local-migrate:
	python manage.py migrate

local-requirements:
	pip install -r requirements.txt
