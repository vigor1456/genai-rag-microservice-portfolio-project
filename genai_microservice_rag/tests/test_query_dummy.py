from fastapi.testclient import TestClient
from app.main import app

def test_query_endpoint_dummy(monkeypatch):
    monkeypatch.setenv("EMBEDDINGS_PROVIDER", "hash")
    monkeypatch.setenv("LLM_PROVIDER", "dummy")
    client = TestClient(app)
    r = client.post("/query", json={"question":"How long should passwords be?"})
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data and "sources" in data
