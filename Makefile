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

# ===================================================================
# ngrok
# ===================================================================
ngrok-url:
	@curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"

test-echo:
	@URL=$$($(MAKE) -s ngrok-url); \
	echo "Testing $$URL/debug/echo"; \
	curl -X POST $$URL/debug/echo -H "Content-Type: application/json" -d '{"test":"hi"}'
