from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    api_key: str = Field(default=os.getenv("API_KEY", ""))
    llm_provider: str = Field(default=os.getenv("LLM_PROVIDER", "dummy"))
    openai_api_key: str = Field(default=os.getenv("OPENAI_API_KEY", ""))
    openai_model: str = Field(default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    azure_openai_api_key: str = Field(default=os.getenv("AZURE_OPENAI_API_KEY", ""))
    azure_openai_endpoint: str = Field(default=os.getenv("AZURE_OPENAI_ENDPOINT", ""))
    azure_openai_deployment: str = Field(default=os.getenv("AZURE_OPENAI_DEPLOYMENT", ""))
    embeddings_provider: str = Field(default=os.getenv("EMBEDDINGS_PROVIDER", "hash"))
    openai_embedding_model: str = Field(default=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    index_dir: str = Field(default=os.getenv("INDEX_DIR", "data/index"))
    redis_url: str = Field(default=os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    chunk_size: int = Field(default=int(os.getenv("CHUNK_SIZE", 800)))
    chunk_overlap: int = Field(default=int(os.getenv("CHUNK_OVERLAP", 120)))
    top_k: int = Field(default=int(os.getenv("TOP_K", 4)))

settings = Settings()
