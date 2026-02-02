import logging
import asyncio
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.ai.service import process_user_query

log = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat")
async def chat(
    request: Request,
) -> JSONResponse:
    body = await request.json()

    # TODO:: заменить на валидацию pydantic
    if "message" not in body:
        raise HTTPException(400, "message field required")

    resp = await asyncio.to_thread(process_user_query, body["message"])

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "status": "ok",
        "content": resp
    })