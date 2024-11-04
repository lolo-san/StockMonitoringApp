# Makefile for StockMonitoringApp

# Variables
ENVIRONMENT ?= local  # Default to 'local' if not specified

# Help target
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  install: Install dependencies"
	@echo "  test: Run tests"
	@echo "  lint: Lint the code"
	@echo "  run-local: Run the app locally"

# Install dependencies
.PHONY: install
install:
	pip install -r requirements.txt

# Run tests
.PHONY: test
test:
	pytest -v

# Lint the code
.PHONY: lint
lint: 
	python3 -m black app
	pylint app --disable=C,R

# Run the app locally
.PHONY: run-local
run-local:
	@echo "Running application locally with environment: $(ENVIRONMENT)"
	ENVIRONMENT=$(ENVIRONMENT) python app/main.py

# Build the Docker image
.PHONY: docker-build
docker-build:
	docker build -t stock-monitoring-app:latest .

# Run the Docker container
.PHONY: docker-run
docker-run:
	docker run --rm -it stock-monitoring-app:latest

# Run the Docker container with volume mount (for development)
.PHONY: docker-run-dev
docker-run-dev:
	docker run --rm -it -e ENVIRONMENT=$(ENVIRONMENT) -v "$(PWD)/data":/data stock-monitoring-app:latest

# Docker clean up
.PHONY: docker-clean
docker-clean:
	docker rmi stock-monitoring-app:latest