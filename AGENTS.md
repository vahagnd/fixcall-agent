# AGENTS.md

## Project
FastAPI service: Retell AI post-call webhook → Telegram notification.
Endpoint: `POST /telegram/send_notification` (payload: `call.call_analysis.custom_analysis_data`).
`CallerType` values must match the Retell agent's post-call analysis fields.

## Tooling
- Python 3.13, **uv only** (never pip / bare python).
- Lint: `make lint` (pre-commit, ruff with ALL rules, line length 120).
- `api/` uses flat imports (`from models import ...`): the Dockerfile copies `api/*.py` into `/app`.

## Git
- Work on `develop`. **Pushing `master` auto-deploys to prod** (`.github/workflows/deploy.yml`).
- Never push, and never touch `master`, unless explicitly asked. Merge `develop` → `master` fast-forward only.
- Commit messages: short, lowercase, no prefixes (e.g. `add prod make commands`).

## Environments
- dev: local, `make start` (api + ngrok).
- prod: Linode VM, `/opt/fixcall-agent`, `make prod-start` (api + Caddy, HTTPS via `DOMAIN`).
- `.env` is never committed. Keys: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `NGROK_AUTHTOKEN` (dev), `DOMAIN`, `PROD_HOST`.
- Helpers: `make prod-ssh`, `make prod-test-echo`.
