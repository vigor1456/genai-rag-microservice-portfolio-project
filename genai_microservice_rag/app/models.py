from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    paths: List[str]
    recursive: bool = True

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = None

class QuerySource(BaseModel):
    source: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[QuerySource]
