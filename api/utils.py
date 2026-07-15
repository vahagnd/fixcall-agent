import httpx
from models import CallSummary
from settings import telegram_settings

LABELS = {
    "standard_customer": "Standard Repair Call",
    "warranty_customer": "Warranty Call",
    "warranty_rep": "Warranty Company Rep",
    "spam": "Spam / Irrelevant",
}


def format_message(data: CallSummary) -> str:
    label = LABELS.get(data.caller_type, f"Call ({data.caller_type})")

    lines = [f"*{label}*"]

    if data.caller_name:
        lines.append(f"Name: {data.caller_name}")
    if data.callback_phone:
        lines.append(f"Phone: {data.callback_phone}")
    if data.company_name:
        lines.append(f"Company: {data.company_name}")
    if data.service_address:
        lines.append(f"Address: {data.service_address}")
    if data.appliance_type:
        lines.append(f"Appliance: {data.appliance_type}")
    if data.appliance_brand:
        lines.append(f"Brand: {data.appliance_brand}")
    if data.appliance_issue:
        lines.append(f"Issue: {data.appliance_issue}")
    if data.call_outcome:
        lines.append(f"Outcome: {data.call_outcome}")

    return "\n".join(lines)


async def send_telegram_message(text: str) -> None:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://api.telegram.org/bot{telegram_settings.bot_token}/sendMessage",
            json={
                "chat_id": telegram_settings.chat_id,
                "text": text,
                "parse_mode": "Markdown",
            },
        )
        resp.raise_for_status()
