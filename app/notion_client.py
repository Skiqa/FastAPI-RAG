import os
import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "Authorization": "Bearer " + os.getenv("NOTION_INTEGRATION_SECRET"),
    "Notion-Version": os.getenv("NOTION_VERSION"),
    "Content-Type": "application/json",
}

def fetch_page_blocks(page_id: str) -> list[str]:
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    texts = []
    print(f"GET {url}")
    print("HEADERS:", HEADERS)
    while url:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()

        for block in data["results"]:
            print("BLOCK:", block)
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