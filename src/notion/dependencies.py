import logging
from fastapi import Request, HTTPException, Header
from src.notion.service import validate_signature

log = logging.getLogger(__name__)

async def verify_notion_signature(
    request: Request,
    x_notion_signature: str = Header(..., alias="x-notion-signature"),
) -> bool:
    payload = await request.json()
    if "verification_token" in payload:
        log.info(f"Notion Webhook received: {payload.decode('utf-8')}")
        return True
    if not validate_signature(payload, x_notion_signature):
        log.error(f"Invalid Notion signature: {x_notion_signature[:50]}...")
        raise HTTPException(403, "Invalid signature")

    return True