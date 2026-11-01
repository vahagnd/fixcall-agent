# ===================================================================
# Docker
# ===================================================================

start:
	docker compose up --build --remove-orphans

stop:
	docker compose down

restart: stop start

# ===================================================================
# Production (Caddy, no ngrok)
# ===================================================================

PROD_COMPOSE = docker compose -f docker-compose.prod.yml
PROD_DIR = /opt/fixcall-agent
PROD_SSH = ssh -t root@$(call env,PROD_HOST)

# Read a variable from .env, fail if missing: $(call env,NAME)
env = $(or $(shell grep '^$(1)=' .env 2>/dev/null | cut -d= -f2-),$(error $(1) is not set in .env))

prod-ssh:
	@$(PROD_SSH)

prod-start:
	$(PROD_COMPOSE) up -d --build --remove-orphans

prod-stop:
	$(PROD_COMPOSE) down

prod-logs:
	$(PROD_COMPOSE) logs -f

prod-test-echo:
	@DOMAIN=$(call env,DOMAIN); \
	echo "Testing https://$$DOMAIN/debug/echo"; \
	curl -fsS -X POST https://$$DOMAIN/debug/echo -H "Content-Type: application/json" -d '{"test":"hi"}'; echo

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
