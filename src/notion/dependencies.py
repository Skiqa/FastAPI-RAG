# src/notion/dependencies.py (или переименуйте middleware.py)
import logging
from fastapi import Request, HTTPException, Header, Depends
from src.notion.service import validate_signature

log = logging.getLogger(__name__)

async def verify_notion_signature(
    request: Request,
    x_notion_signature: str = Header(..., alias="x-notion-signature"),
):
    body = await request.body()

    payload = await request.json()
    if "verification_token" in payload:
        log.info(f"Notion Webhook received: {body.decode('utf-8')}")
        return True
    if not validate_signature(body, x_notion_signature):
        log.error(f"Invalid Notion signature: {x_notion_signature[:50]}...")
        raise HTTPException(403, "Invalid signature")

    return True