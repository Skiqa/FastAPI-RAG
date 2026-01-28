import os
import hmac
import hashlib
from .chroma_client import client as chroma
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
        # логировать
        return {"status": "ignored"}
    
    # проверяем в зависимости от parent_id в какую коллекцию сохранять данные
    # TODO:: выглядит костыльно, переделать потом
    collection_name = "student_data" if parent_id == "2ed95e3f-0bdf-80bf-b508-f5e4ec96544f" else "applicant_data" 
    collection = chroma.get_or_create_collection(collection_name)

    print(f"Handling Notion event: {event} for page_id: {page_id} in collection: {collection_name}")

    if event == "page.deleted":
        collection.delete(ids=[page_id])
        # логировать
        return {"status": "deleted", "id": page_id}

    if event in ("page.created", "page.content_updated"):
        print(f"Fetching blocks for page_id: {page_id}")
        blocks = fetch_page_blocks(page_id)
        text = "\n".join(blocks)
        print(f"Upserting text for page_id: {page_id}, text length: {len(text)}")
        if not text.strip():
            return {"status": "empty"}

        collection.upsert(
            ids=[page_id],
            documents=[text],
            metadatas=[{"source": "notion"}],
        )

        # логировать
        return {"status": "upserted", "id": page_id}

    return {"status": "ignored", "event": event}