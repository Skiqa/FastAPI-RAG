from fastapi import FastAPI
from src.api import api_router

# инициализация FastAPI приложения
app = FastAPI(title="RAG API", version="0.1.0")

# включение роутеров api
app.include_router(api_router, prefix="/api/v1")
