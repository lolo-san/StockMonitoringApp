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
	python app/main.py
