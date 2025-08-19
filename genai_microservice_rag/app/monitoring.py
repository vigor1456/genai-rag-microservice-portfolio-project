from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

REQUESTS = Counter("requests_total", "Total requests", ["endpoint"])
ERRORS = Counter("errors_total", "Total errors", ["endpoint"])
LATENCY = Histogram("request_latency_seconds", "Request latency", ["endpoint"])
RETRIEVAL_HITS = Gauge("retrieval_hits", "Retrieved documents count")
ANSWER_LENGTH = Gauge("answer_length_chars", "Answer length in characters")

def metrics_response():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
