import hmac
import hashlib
import logging

from src.config import NOTION_VERIFICATION_TOKEN
from src.notion.client import fetch_page_blocks
from src.chroma.client import client as chroma
from src.notion.schemas import NotionEventType

log = logging.getLogger(__name__)

def validate_signature(body: bytes, signature: str) -> bool:
    mac = hmac.new(
        NOTION_VERIFICATION_TOKEN.encode(),
        body,
        hashlib.sha256,
    )
    expected = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected, signature)

# TODO:: разделить логику по событиям
def handle_notion_webhook(payload: dict)-> None:
    event = payload.get("type")
    page_id = payload.get("entity", {}).get("id")

    if not page_id:
        log.warning("No page_id found in payload")
        return None

    collection = chroma.get_or_create_collection("student_data")

    if event == NotionEventType.PAGE_DELETED:
        collection.delete(ids=[page_id])

        log.info(f"Deleted page_id: {page_id}")
        return None

    if event in (NotionEventType.PAGE_CREATED, NotionEventType.PAGE_CONTENT_UPDATED):
        blocks = fetch_page_blocks(page_id)
        text = "\n".join(blocks)

        if not text.strip():
            return None

        collection.upsert(
            ids=[page_id],
            documents=[text],
            metadatas=[{"source": "notion"}],
        )

        log.info(f"Upserting text for page_id: {page_id}")
        return None

    return None