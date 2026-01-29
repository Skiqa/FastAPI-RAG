import requests
from src.config import NOTION_INTEGRATION_SECRET
from src.notion.constants import NOTION_API_URL, NOTION_VERSION

HEADERS = {
    "Authorization": NOTION_INTEGRATION_SECRET,
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

def fetch_page_blocks(page_id: str) -> list[str]:
    url = f"{NOTION_API_URL}/blocks/{page_id}/children"
    texts = []
    while url:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()

        for block in data["results"]:
            text = extract_text(block)
            if text:
                texts.append(text)

        url = data.get("next_cursor")

    return texts

def extract_text(block: dict) -> str | None:
    block_type = block.get("type")
    data = block.get(block_type, {})

    if "rich_text" in data:
        return "".join(t["plain_text"] for t in data["rich_text"])

    return None