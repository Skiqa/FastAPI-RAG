from ollama import Client, ChatResponse, ResponseError
from src.config import OLLAMA_HOST, OLLAMA_PORT
from src.ai.constants import OLLAMA_TIMEOUT
from src.config import OLLAMA_MODEL

client = Client(
    host=f"{OLLAMA_HOST}:{OLLAMA_PORT}",
    timeout=OLLAMA_TIMEOUT,
)

def chat(message: str) -> ChatResponse:
    try:
        return client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "user", "content": message}
            ],
        )
    except ResponseError as e:
        raise Exception(f"Ollama error: {e}")