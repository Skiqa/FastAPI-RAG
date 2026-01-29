import logging
from fastapi import APIRouter, Depends, Request, BackgroundTasks, status
from fastapi.responses import JSONResponse
from src.notion.service import validate_signature, handle_notion_webhook
from src.notion.dependencies import verify_notion_signature
from src.config import APP_ENV

router = APIRouter()

log = logging.getLogger(__name__)

@router.post("/webhook", dependencies=[Depends(verify_notion_signature)])
async def notion_webhook(
    request: Request,
    background_tasks: BackgroundTasks
) -> JSONResponse:
    payload = await request.json()

    # логирование запроса от notion
    if APP_ENV == "development":
        log.warning( f"Notion Webhook received: {payload.decode('utf-8')}")

    background_tasks.add_task(handle_notion_webhook, payload)

    return JSONResponse(status_code=status.HTTP_200_OK)