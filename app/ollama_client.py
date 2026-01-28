import requests
import os
from sentence_transformers import SentenceTransformer
from .chroma_client import client as chroma
from ollama import Client as ollama, ChatResponse
from .utils import load_file

host = os.getenv("OLLAMA_HOST", "http://localhost")
port = os.getenv("OLLAMA_PORT", "11434")

ollama = ollama(
    host=f"{host}:{port}",
    timeout=60,
)

model = SentenceTransformer("all-MiniLM-L6-v2")

COLLEGE_PROMPT = load_file("prompts/rag.txt")

college_emb = model.encode(COLLEGE_PROMPT, convert_to_tensor=True)

def process_user_query(query: str, role: str) -> dict:
    # Заменить на нормальную логику выбора коллекции
    if role == "student":
        collection = chroma.get_collection("applicant_data")
    else:
        collection = chroma.get_collection("applicant_data")

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    context = "\n".join(results["documents"][0]) if results["documents"] else ""

    final_prompt = f"""
                {COLLEGE_PROMPT}

                Контекст:
                {context}

                Вопрос:
                {query}
                """
    
    print("Final prompt for Ollama:", final_prompt)

    response: ChatResponse = ollama.chat(
        model="qwen3:4b", # заменить на динамичную
        messages=[{"role": "user", "content": final_prompt}],
    )

    return response
