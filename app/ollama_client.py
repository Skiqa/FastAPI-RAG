import requests
import os
from sentence_transformers import SentenceTransformer, util
from .chroma_client import client as chroma, get_collection
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

def ask_ollama(prompt: str, model: str) -> str:
    response: ChatResponse = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response['message']['content']

def process_user_query(text: str, role: str) -> dict:
    if role == "student":
        collection = get_collection("applicant_data")
    else:
        collection = get_collection("applicant_data")

    results = collection.query(
        query_texts=[text],
        n_results=5
    )

    context = "\n".join(results["documents"][0]) if results["documents"] else ""

    final_prompt = f"""
                {COLLEGE_PROMPT}

                Контекст:
                {context}

                Вопрос:
                {text}
                """
    print("Final prompt for Ollama:", final_prompt)
    response: ChatResponse = ollama.chat(
        model="qwen3:4b",
        messages=[{"role": "user", "content": final_prompt}],
    )
    return response['message']['content']
