.PHONY: help setup setup-backend setup-frontend test test-unit test-integration test-mutation test-hypothesis lint format run-backend docker-up docker-down clean

# Variables
BACKEND_DIR = backend
# VENV is the absolute path-like string from root
VENV = $(BACKEND_DIR)/.venv
# Binaries (referenced from root)
PYTHON = $(VENV)/bin/python
PYTEST = $(VENV)/bin/pytest
UVICORN = $(VENV)/bin/uvicorn
# Binaries (referenced relative to BACKEND_DIR for targets that 'cd' in)
REL_VENV_BIN = .venv/bin

help: ## Show this help message
	@echo "VibeFinance Development Makefile"
	@echo "Usage: make [target]"
	@echo ""
	@echo "Setup Targets:"
	@echo "  setup                Full project setup (Backend + Frontend stub)"
	@echo "  setup-backend        Create venv and install backend deps (uv)"
	@echo "  setup-frontend       Install frontend deps (Stub)"
	@echo ""
	@echo "Development Targets:"
	@echo "  run-backend          Start FastAPI server with hot-reload"
	@echo "  format               Auto-format backend code with ruff"
	@echo "  lint                 Run ruff and mypy checks"
	@echo "  clean                Remove cache and temporary files"
	@echo ""
	@echo "Testing Targets:"
	@echo "  test                 Run default unit tests"
	@echo "  test-unit            Run unit tests specifically"
	@echo "  test-integration     Run integration tests"
	@echo "  test-mutation        Run mutmut mutation tests"
	@echo "  test-hypothesis      Run property-based hypothesis tests"
	@echo "  gen-test-docs        Generate test case documentation from @TESTCASE annotations"
	@echo ""
	@echo "Infrastructure Targets:"
	@echo "  docker-up            Start all services in Docker"
	@echo "  docker-down          Stop all Docker services"

setup: setup-backend setup-frontend ## Full project setup

setup-backend: ## Install backend dependencies with uv
	@command -v uv >/dev/null 2>&1 || { echo "Error: uv is not installed. Please install it: https://github.com/astral-sh/uv"; exit 1; }
	@echo "Installing Backend dependencies with uv..."
	uv venv $(VENV)
	uv pip install --python $(PYTHON) -r $(BACKEND_DIR)/pyproject.toml
	@echo "Backend dependencies installed."

setup-frontend: ## Install frontend dependencies (Stub)
	@echo "Frontend setup is currently a stub. Skipping npm install."

test: test-unit ## Run all tests

test-unit: gen-test-docs ## Run unit tests
	# Running from root is fine for pytest as it handles discovery well,
	# but we point to the dir to be safe.
	$(PYTEST) $(BACKEND_DIR)/tests/unit

test-integration: gen-test-docs ## Run integration tests
	$(PYTEST) $(BACKEND_DIR)/tests/integration

test-mutation: gen-test-docs ## Run mutation tests
	# mutmut must run from backend dir to find pyproject.toml config automatically
	cd $(BACKEND_DIR) && $(REL_VENV_BIN)/mutmut run --paths-to-mutate=services

test-hypothesis: gen-test-docs ## Run property-based tests
	$(PYTEST) -m hypothesis $(BACKEND_DIR)/tests

lint: ## Run code quality tools (ruff, mypy)
	# Run from backend dir so tools find pyproject.toml config automatically
	cd $(BACKEND_DIR) && $(REL_VENV_BIN)/ruff check .
	cd $(BACKEND_DIR) && $(REL_VENV_BIN)/mypy .

format: ## Format code (ruff)
	cd $(BACKEND_DIR) && $(REL_VENV_BIN)/ruff format .

run-backend: ## Run the backend server locally
	# Uvicorn needs to find the app module.
	$(UVICORN) main:app --app-dir $(BACKEND_DIR) --reload

docker-up: ## Start services with Docker Compose
	docker compose up -d

docker-down: ## Stop Docker Compose services
	docker compose down

clean: ## Clean up temporary files
	@echo "Cleaning up..."
	@find $(BACKEND_DIR) -type d -name "__pycache__" -exec rm -rf {} +
	@find $(BACKEND_DIR) -type f -name "*.pyc" -delete
	@find $(BACKEND_DIR) -type f -name "*.pyo" -delete
	@find $(BACKEND_DIR) -type f -name ".coverage" -delete
	@find $(BACKEND_DIR) -type d -name ".pytest_cache" -exec rm -rf {} +
	@find $(BACKEND_DIR) -type d -name ".mypy_cache" -exec rm -rf {} +
	@find $(BACKEND_DIR) -type d -name ".ruff_cache" -exec rm -rf {} +

gen-test-docs: ## Generate test documentation
	python3 scripts/generate_test_docs.py
