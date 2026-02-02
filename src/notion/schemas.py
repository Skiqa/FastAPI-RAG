from enum import Enum

class NotionEventType(str, Enum):
    PAGE_CREATED = "page.created"
    PAGE_CONTENT_UPDATED = "page.content_updated"
    PAGE_DELETED = "page.deleted"