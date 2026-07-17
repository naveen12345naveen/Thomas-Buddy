.PHONY: help install setup run test lint format clean docker-build docker-run

help:
	@echo "Thomas Buddy - AI Agent"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make setup        - Setup environment (.env file)"
	@echo "  make run          - Run the agent"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Lint code"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean temporary files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env file created. Please update it with your credentials."; \
	else \
		echo ".env file already exists."; \
	fi
	mkdir -p logs

run: setup
	python main.py

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src tests main.py

format:
	black src tests main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

ldocker-build:
	docker-compose build

docker-run: setup
	docker-compose up
