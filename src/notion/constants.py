from src.config import NOTION_INTEGRATION_SECRET

NOTION_VERSION="2025-09-03"
NOTION_API_URL="https://api.notion.com/v1"

HEADERS = {
    "Authorization": NOTION_INTEGRATION_SECRET,
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}