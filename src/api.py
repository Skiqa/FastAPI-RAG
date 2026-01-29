from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.ai.router import router as chat
from src.notion.router import router as notion_webhook

api_router = APIRouter(
    default_response_class=JSONResponse,
)

api_router.include_router(chat, prefix="/ai", tags=["ai"])
api_router.include_router(notion_webhook, prefix="/notion", tags=["notion"])