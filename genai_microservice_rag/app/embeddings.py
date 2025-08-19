import hashlib, math
from typing import List
from app.config import settings

def _openai_embed(texts: List[str]) -> List[List[float]]:
    from openai import OpenAI
    client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else OpenAI()
    model = settings.openai_embedding_model
    resp = client.embeddings.create(model=model, input=texts)
    return [d.embedding for d in resp.data]

def _hash_embed(texts: List[str], dim: int = 384) -> List[List[float]]:
    out = []
    for t in texts:
        vec = [0.0]*dim
        for tok in t.split():
            h = int(hashlib.sha256(tok.encode("utf-8")).hexdigest(), 16)
            idx = h % dim
            vec[idx] += 1.0
        norm = math.sqrt(sum(v*v for v in vec)) or 1.0
        vec = [v/norm for v in vec]
        out.append(vec)
    return out

class Embeddings:
    def __init__(self):
        self.provider = settings.embeddings_provider.lower()

    @property
    def name(self) -> str:
        if self.provider == "openai":
            return f"openai_{settings.openai_embedding_model.replace('-','_')}"
        return "hash_384"

    @property
    def dimension(self) -> int:
        if self.provider == "openai":
            return 1536 if "small" in settings.openai_embedding_model else 3072
        return 384

    def embed(self, texts: List[str]) -> List[List[float]]:
        if self.provider == "openai":
            return _openai_embed(texts)
        return _hash_embed(texts, dim=self.dimension)
