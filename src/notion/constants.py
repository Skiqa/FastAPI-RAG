from src.config import NOTION_INTEGRATION_SECRET
from enum import Enum

NOTION_VERSION="2025-09-03"
NOTION_API_URL="https://api.notion.com/v1"

HEADERS = {
    "Authorization": NOTION_INTEGRATION_SECRET,
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

class NotionEventType(str, Enum):
    PAGE_CREATED = "page.created"
    PAGE_CONTENT_UPDATED = "page.content_updated"
    PAGE_DELETED = "page.deleted"