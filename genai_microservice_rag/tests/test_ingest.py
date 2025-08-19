from app.chain import RAGService

def test_ingest_and_query_dummy(tmp_path, monkeypatch):
    p = tmp_path / "docs"
    p.mkdir()
    (p / "policy.txt").write_text("Passwords must be at least 12 characters. Two-factor auth is required for remote access.")
    monkeypatch.setenv("EMBEDDINGS_PROVIDER", "hash")
    monkeypatch.setenv("LLM_PROVIDER", "dummy")
    monkeypatch.setenv("INDEX_DIR", str(tmp_path / "index"))
    svc = RAGService()
    svc.ingest([str(p)], recursive=True)
    ans, sources = svc.query("What are the password rules?")
    assert "demo response" in ans.lower()
    assert len(sources) > 0
