import chromadb
from chromadb.config import Settings

from src.config import CHROMA_HOST, CHROMA_PORT


client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
    settings=Settings(
        anonymized_telemetry=False
    )
)


def query_by_collection(query: str, collection_name: str) -> dict:
    collection = client.get_collection(name=collection_name)

    return collection.query(
        query_texts=[query],
        n_results=5,
    )
