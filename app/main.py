import os
import logging
from fastapi import FastAPI, Request, Header, HTTPException, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from .ollama_client import process_user_query
from .embed import validate_signature, handle_notion_webhook

# загрузка переменных окружения
load_dotenv()

# инициализация FastAPI приложения
app = FastAPI()

@app.post("/api/v1/webhook")
async def notion_webhook(
    request: Request,
    x_notion_signature: str | None = Header(None),
):
    body = await request.body()
    
    # логирование запроса от notion
    print(body.decode("utf-8", errors="ignore"))

    # валидация подписи (вынести)
    if os.getenv("NOTION_VERIFICATION_TOKEN"):
        if not x_notion_signature:
            raise HTTPException(400, "Missing signature")
        if not validate_signature(body, x_notion_signature):
            raise HTTPException(403, "Invalid signature")
    payload = await request.json()
    if "verification_token" in payload:
        return {"verification_token": payload["verification_token"]}
    
    result = handle_notion_webhook(payload)
    # добавить логирование
    return JSONResponse(result)


@app.post("/api/v1/ai")
async def ai_handler(
    request: Request,
    role: str = Query(..., description="student | applicant") # затычка до авторизации
):
    body = await request.json()

    # заменит на нормальную валидацию
    if "message" not in body:
        raise HTTPException(400, "message field required")

    resp = process_user_query(
        text=body["message"],
        role=role
    )

    # добавить проверку ответа

    return {
        "status": "ok",
        "content": resp['message']['content'],
    }

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy"}