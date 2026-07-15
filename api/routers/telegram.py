import logging
from fastapi import APIRouter, HTTPException
from models import RetellPayload
from utils import format_message, send_telegram_message

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/send_notification")
async def send_notification(payload: RetellPayload):
    call = payload.call
    analysis = call.call_analysis if call else None
    data = analysis.custom_analysis_data if analysis else None

    if data is None:
        logger.warning("Received retell payload data with no custom_analysis_data field")
        raise HTTPException(status_code=422, detail="Missing custom_analysis_data field in the payload")

    message = format_message(data)
    await send_telegram_message(message)

    return {"notification_sent": True}
