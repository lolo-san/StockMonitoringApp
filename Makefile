# Makefile for StockMonitoringApp

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
	python -m app.main

# Build the Docker image
.PHONY: docker-build
docker-build:
	docker build -t stock-monitoring-app:latest .

# Run the Docker container
.PHONY: docker-run
docker-run:
	docker run --rm -it stock-monitoring-app:latest

# Docker clean up
.PHONY: docker-clean
docker-clean:
	docker rmi stock-monitoring-app:latest

# Build the Docker image to google artifact registry
.PHONY: docker-build-gar
docker-build-gar:
	docker build -t europe-west9-docker.pkg.dev/stock-monitoring-project/stock-monitoring-app/stock-monitoring-app:latest .

# Push the Docker image to google artifact registry
.PHONY: docker-push-gar
docker-push-gar:
	docker push europe-west9-docker.pkg.dev/stock-monitoring-project/stock-monitoring-app/stock-monitoring-app:latest
