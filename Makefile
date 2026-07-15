# ===================================================================
# Docker
# ===================================================================

start:
	docker compose up --build --remove-orphans

stop:
	docker compose down

restart: stop start

# ===================================================================
# Development
# ===================================================================

project-init-dev: --install-packages-dev --tools-install

project-init-run:
	uv sync --all-packages --no-dev

--install-packages-dev:
	uv sync --all-packages --all-groups

--tools-install:
	uv run pre-commit install --hook-type pre-commit

# ===================================================================
# Linting
# ===================================================================
lint:
	uv run pre-commit run --all-files

ruff-fix:
	uv run ruff check --fix

ruff-check:
	uv run ruff check .
