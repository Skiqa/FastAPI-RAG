import logging

from src.chroma.client import query_by_collection
from src.ai.client import chat
from src.utils import load_file
from src.config import APP_ENV

log = logging.getLogger(__name__)

COLLEGE_PROMPT = load_file("prompts/rag.txt")

def process_user_query(query: str) -> dict:
    results = query_by_collection(query, collection_name="student_data")
    
    context = ""
    if results.get("documents"):
        context = "\n".join(results["documents"][0])

    prompt = f"""
{COLLEGE_PROMPT}

Контекст:
{context}

Вопрос:
{query}
"""

    if APP_ENV == "development":
        log.debug("Full prompt: {}".format(prompt))

    response = chat(prompt)

    try:
        return response["message"]["content"]
    except Exception:
        raise Exception("Некорректный ответ от модели")