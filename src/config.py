from starlette.config import Config

config = Config(".env")

APP_ENV: str = config("APP_ENV", default="development")

CHROMA_HOST: str = config("CHROMA_HOST", default="chromadb")
CHROMA_PORT: int = config("CHROMA_PORT", cast=int, default=8000)

NOTION_INTEGRATION_SECRET: str = config("NOTION_INTEGRATION_SECRET")
NOTION_VERIFICATION_TOKEN: str = config("NOTION_VERIFICATION_TOKEN")

OLLAMA_HOST: str = config("OLLAMA_HOST", default="http://localhost")
OLLAMA_PORT: int = config("OLLAMA_PORT", cast=int, default=11434)
