from typing import List, Tuple
from app.embeddings import Embeddings
from app.vectorstore import VectorStore, chunk_documents
from app.config import settings
from app.llm import LLM

def build_prompt(question: str, contexts: List[Tuple[float, dict]]) -> str:
    context_texts = []
    for score, meta in contexts:
        snippet = meta.get("text","")
        src = meta.get("source","unknown")
        context_texts.append(f"[source: {src} | score: {score:.3f}]\n{snippet}")
    context_block = "\n\n".join(context_texts[:10])
    return (
        "You are an internal assistant. Answer the QUESTION strictly using the CONTEXT. "
        "If the answer isn't in the context, say you don't know. Always cite sources by filename.\n\n"
        f"CONTEXT:\n{context_block}\n\nQUESTION: {question}"
    )

class RAGService:
    def __init__(self):
        self.emb = Embeddings()
        self.store = VectorStore(settings.index_dir, self.emb.name, self.emb.dimension)
        self.llm = LLM()

    def ingest(self, paths: list[str], recursive: bool = True):
        texts, metas = chunk_documents(paths, settings.chunk_size, settings.chunk_overlap, recursive)
        for i, t in enumerate(texts):
            metas[i]["text"] = t
        vecs = self.emb.embed(texts)
        self.store.add(vecs, metas)
        return len(texts)

    def query(self, question: str, top_k: int | None = None):
        k = top_k or settings.top_k
        qv = self.emb.embed([question])[0]
        hits = self.store.search(qv, k)
        prompt = build_prompt(question, hits)
        answer = self.llm.generate(prompt)
        sources = [{"source": h[1].get("source","unknown"), "score": h[0]} for h in hits]
        return answer, sources
