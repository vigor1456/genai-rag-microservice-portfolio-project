import os, json
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
import numpy as np

class VectorStore:
    def __init__(self, index_dir: str, embedding_name: str, dim: int):
        self.index_dir = os.path.join(index_dir, embedding_name)
        self.dim = dim
        os.makedirs(self.index_dir, exist_ok=True)
        self.index_path = os.path.join(self.index_dir, "faiss.index")
        self.meta_path = os.path.join(self.index_dir, "meta.json")
        self.map_path = os.path.join(self.index_dir, "docmap.json")
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.map_path, "r") as f:
                self.docmap = json.load(f)
        else:
            self.index = faiss.IndexFlatIP(dim)
            self.docmap = []

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.map_path, "w") as f:
            json.dump(self.docmap, f)

    def add(self, embeddings: List[List[float]], metadatas: List[dict]):
        vecs = np.array(embeddings, dtype="float32")
        norms = np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12
        vecs = vecs / norms
        self.index.add(vecs)
        for m in metadatas:
            self.docmap.append(m)
        self.save()

    def search(self, query: List[float], k: int) -> List[Tuple[float, dict]]:
        q = np.array([query], dtype="float32")
        q = q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-12)
        D, I = self.index.search(q, k)
        results = []
        for score, idx in zip(D[0].tolist(), I[0].tolist()):
            if idx == -1 or idx >= len(self.docmap):
                continue
            results.append((float(score), self.docmap[idx]))
        return results

def chunk_documents(paths: list[str], chunk_size: int, chunk_overlap: int, recursive: bool = True):
    from pathlib import Path
    from langchain_community.document_loaders import TextLoader, DirectoryLoader
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = []
    for p in paths:
        pth = Path(p)
        if pth.is_dir():
            loader = DirectoryLoader(str(pth), glob="**/*.txt" if recursive else "*.txt", loader_cls=TextLoader, show_progress=True)
            docs += loader.load()
        else:
            docs += TextLoader(str(pth)).load()
    chunks = splitter.split_documents(docs)
    texts = [c.page_content for c in chunks]
    metas = [c.metadata | {"source": c.metadata.get("source","") or c.metadata.get("file_path","")} for c in chunks]
    return texts, metas
