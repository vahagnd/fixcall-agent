import logging
from fastapi import APIRouter, HTTPException
from models import RetellPayload
from utils import format_message, send_telegram_message

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/call_ended")
async def call_ended(payload: RetellPayload):
    call = payload.call
    analysis = call.call_analysis if call else None
    data = analysis.custom_analysis_data if analysis else None

    if data is None:
        logger.warning("Received call_ended webhook with no custom_analysis_data")
        raise HTTPException(status_code=422, detail="Missing custom_analysis_data")

    message = format_message(data)
    await send_telegram_message(message)

    return {"ok": True}
