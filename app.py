import os
import httpx
from fastapi import FastAPI, Request

app = FastAPI()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

LABELS = {
    "standard_customer": "Standard Repair Call",
    "warranty_customer": "Warranty Call",
    "warranty_rep": "Warranty Company Rep",
    "spam": "Spam / Irrelevant",
}

def format_message(data: dict) -> str:
    call_type = data.get("caller_type", "unknown")
    label = LABELS.get(call_type, f"Call ({call_type})")

    lines = [f"*{label}*"]

    if data.get("customer_name"):
        lines.append(f"Name: {data['customer_name']}")
    if data.get("phone_number"):
        lines.append(f"Phone: {data['phone_number']}")
    if data.get("warranty_company"):
        lines.append(f"Company: {data['warranty_company']}")
    if data.get("service_address"):
        lines.append(f"Address: {data['service_address']}")
    if data.get("appliance_type"):
        lines.append(f"Appliance: {data['appliance_type']}")
    if data.get("brand"):
        lines.append(f"Brand: {data['brand']}")
    if data.get("issue_description"):
        lines.append(f"Issue: {data['issue_description']}")
    if data.get("fee_status"):
        lines.append(f"Fee status: {data['fee_status']}")
    if data.get("outcome"):
        lines.append(f"Outcome: {data['outcome']}")

    return "\n".join(lines)


@app.post("/webhooks/call_ended")
async def call_ended(request: Request):
    payload = await request.json()

    # Retell nests extracted fields under call.call_analysis.custom_analysis_data
    # adjust this path once you see a real payload — log first, trust second
    call = payload.get("call", payload)
    analysis = call.get("call_analysis", {})
    data = analysis.get("custom_analysis_data", analysis)

    message = format_message(data)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown",
            },
        )
        resp.raise_for_status()

    return {"ok": True}


@app.post("/debug/echo")
async def debug_echo(request: Request):
    """Temporary route: point Retell's webhook here first to see the real payload shape."""
    payload = await request.json()
    print(payload)
    return {"ok": True}
