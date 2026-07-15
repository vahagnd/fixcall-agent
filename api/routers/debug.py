import logging

from fastapi import APIRouter, Request

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/debug", tags=["debug"])


@router.post("/echo")
async def debug_echo(request: Request) -> dict[str, bool]:
    """Debug route: point Retell's webhook here first to see the real payload shape."""
    payload = await request.json()
    logger.info("Debug echo payload: %s", payload)
    return {"ok": True}
