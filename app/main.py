from .embed import handle_notion_webhook, validate_signature
import os
import logging
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s | headers=%(headers)s | body=%(body)s",
)

logger = logging.getLogger("notion_webhook")

app = FastAPI()

@app.post("/api/v1/webhook")
async def notion_webhook(
    request: Request,
    x_notion_signature: str | None = Header(None),
):
    body = await request.body()

    logger.info(
        "Notion webhook received",
        extra={
            "headers": dict(request.headers),
            "body": body.decode("utf-8", errors="ignore"),
        },
    )

    if os.getenv("NOTION_VERIFICATION_TOKEN"):
        if not x_notion_signature:
            raise HTTPException(400, "Missing signature")

        if not validate_signature(body, x_notion_signature):
            raise HTTPException(403, "Invalid signature")

    payload = await request.json()

    # Webhook verification
    if "verification_token" in payload:
        return {"verification_token": payload["verification_token"]}

    result = handle_notion_webhook(payload)
    return JSONResponse(result)

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "message": "Server is running"}
