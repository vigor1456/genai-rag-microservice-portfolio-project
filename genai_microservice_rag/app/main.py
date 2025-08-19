from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models import IngestRequest, QueryRequest, QueryResponse
from app.auth import require_api_key
from app.monitoring import REQUESTS, ERRORS, LATENCY, RETRIEVAL_HITS, ANSWER_LENGTH, metrics_response
from app.chain import RAGService
from app.logging_utils import logger

app = FastAPI(title="GenAI Knowledge Assistant", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = RAGService()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return metrics_response()

@app.post("/ingest")
def ingest(req: IngestRequest, _=Depends(require_api_key)):
    REQUESTS.labels(endpoint="/ingest").inc()
    with LATENCY.labels(endpoint="/ingest").time():
        try:
            count = service.ingest(req.paths, recursive=req.recursive)
            logger.info(f"Ingested {count} chunks from {req.paths}")
            return {"ingested": count}
        except Exception as e:
            ERRORS.labels(endpoint="/ingest").inc()
            logger.error(f"Ingest error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest, _=Depends(require_api_key)):
    REQUESTS.labels(endpoint="/query").inc()
    with LATENCY.labels(endpoint="/query").time():
        try:
            answer, sources = service.query(req.question, req.top_k)
            RETRIEVAL_HITS.set(len(sources))
            ANSWER_LENGTH.set(len(answer or ""))
            logger.info(f"Query ok | q='{req.question[:120]}' | hits={len(sources)}")
            return QueryResponse(answer=answer, sources=[{"source": s["source"], "score": float(s["score"])} for s in sources])
        except Exception as e:
            ERRORS.labels(endpoint="/query").inc()
            logger.error(f"Query error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
