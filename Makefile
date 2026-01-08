.PHONY: setup setup-backend setup-frontend test test-unit test-integration run-backend run-frontend format lint docker-up docker-down clean

# Setup Targets
setup:
	uv run python scripts/dev.py setup

setup-backend:
	uv run python scripts/dev.py setup-backend

setup-frontend:
	uv run python scripts/dev.py setup-frontend

# Testing Targets
test:
	uv run python scripts/dev.py test all

test-unit:
	uv run python scripts/dev.py test unit

test-integration:
	uv run python scripts/dev.py test integration

# Run Targets
run-backend:
	uv run python scripts/dev.py run-backend

run-frontend:
	uv run python scripts/dev.py run-frontend

# Quality Targets
format:
	uv run python scripts/dev.py format

lint:
	uv run python scripts/dev.py lint

# Infra Targets
docker-up:
	uv run python scripts/dev.py docker-up

docker-down:
	uv run python scripts/dev.py docker-down

clean:
	uv run python scripts/dev.py clean

# Git Targets
git-status:
	uv run python scripts/dev.py git-status

git-commit:
	uv run python scripts/dev.py git-commit "$(msg)"

git-push:
	uv run python scripts/dev.py git-push
