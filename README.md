# fixcall-agent

A lightweight FastAPI backend that bridges **Retell AI** post-call webhooks with **Telegram** notifications. It is exposed to the internet via an **ngrok** tunnel (for now) so Retell AI can reach it after every call.

## How it works — end to end

1. **Customer calls in.**

    A customer starts a voice chat with [RetellAI agent](https://agent.retellai.com/orb/agent_6dd3a799b432e4cbe22fac3e0f?token=f64102be7473a3dac44ca92bf96c54eb). Agent which conducts the conversation autonomously.

2. **AI agent analyzes the call.**

    After the call, Retell AI classifies the caller and extracts structured information — caller name, callback number, service address, appliance type, brand, issue description, and overall call outcome. Callers are bucketed into one of four categories: standard repair customer, warranty customer, warranty company rep, or spam.

3. **Retell AI fires a post-call webhook.**

    Once the call ends, Retell AI sends an HTTP POST request to the configured webhook URL with the full call analytics payload, including the custom analysis data produced by the agent.

4. **ngrok tunnel receives the request.** (for now)

    Because this backend runs locally (for now), an **ngrok** tunnel forwards the inbound webhook from Retell AI's servers to the local FastAPI process. The public ngrok URL is what is registered as the webhook endpoint inside the Retell AI dashboard.

5. **Backend processes the payload and sends a Telegram message.**

    The `/telegram/send_notification` endpoint parses the Retell payload, pulls out the structured call summary, formats it into a readable message, and delivers it to a configured [Telegram channel](https://t.me/+zJCJEcYkn3YxYjgy) via the Telegram Bot API — giving the business owner an instant notification for every call.

## Environments & deployment

> ⚠️ **Pushing to `master` deploys to production automatically.** Work on `develop`; merge into `master` only when ready to ship.

| Environment | Where | Run | Public URL |
|---|---|---|---|
| dev | local machine | `make start` (api + ngrok) | ngrok URL (`make ngrok-url`) |
| prod | Linode VM, `/opt/fixcall-agent` | `make prod-start` (api + Caddy) | `https://$DOMAIN` |

- On every push to `master`, `.github/workflows/deploy.yml` SSHes into the server and runs `git pull && make prod-start`. A deploy can also be started manually: **Actions → Deploy to prod → Run workflow**.
- Required GitHub secrets: `PROD_HOST` (server IP) and `PROD_SSH_KEY` (private deploy key).
- Prod secrets live only in `/opt/fixcall-agent/.env` on the server (see `.env.example`). They are never committed.
- Retell's webhook URL in prod: `https://$DOMAIN/telegram/send_notification`.
