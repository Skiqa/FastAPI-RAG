import os
import hmac
import hashlib
from .chroma_client import get_collection
from .notion_client import fetch_page_blocks
from dotenv import load_dotenv
load_dotenv()

NOTION_VERIFICATION_TOKEN = os.getenv("NOTION_VERIFICATION_TOKEN")


def validate_signature(body: bytes, signature: str) -> bool:
    mac = hmac.new(
        NOTION_VERIFICATION_TOKEN.encode(),
        body,
        hashlib.sha256,
    )
    expected = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected, signature)


def handle_notion_webhook(payload: dict):
    event = payload.get("type")
    page_id = payload.get("entity", {}).get("id")
    parent_id = payload.get("data", {}).get("parent", {}).get("page_id")
    if not page_id:
        return {"status": "ignored"}
    
    # проверяем в зависимости от parent_id в какую коллекцию сохранять данные
    collection_name = "student_data" if parent_id == "2ed95e3f-0bdf-801c-85ab-f425ca0d43bc" else "applicant_data"
    collection = get_collection(collection_name)

    if event == "page.deleted":
        collection.delete(ids=[page_id])
        return {"status": "deleted", "id": page_id}

    if event in ("page.created", "page.content_updated"):
        blocks = fetch_page_blocks(page_id)
        text = "\n".join(blocks)

        if not text.strip():
            return {"status": "empty"}

        collection.upsert(
            ids=[page_id],
            documents=[text],
            metadatas=[{"source": "notion"}],
        )

        return {"status": "upserted", "id": page_id}

    return {"status": "ignored", "event": event}
