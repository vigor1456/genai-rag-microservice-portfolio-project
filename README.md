# GenAI Knowledge Assistant – Portfolio Project

A **demo enterprise-style microservice** that combines Generative AI with modern observability practices.  
The goal: practice building and deploying a realistic system that goes beyond “toy notebooks,” with monitoring, alerting, and containerized deployment.  

⚠️ **Note:** This is a **learning project**, not production-ready software. It’s meant to show how enterprise systems *could* be structured.  

---

## 🚀 Features
- **GenAI Retrieval-Augmented Generation (RAG)**
  - Ingests documents into a vector store (FAISS)  
  - Query interface via FastAPI (`/query`)  
  - Demo dataset: fictional company policy documents  

- **API Service**
  - FastAPI with OpenAPI docs at `/docs`  
  - Endpoints: `/ingest`, `/query`, `/healthz`, `/metrics`  

- **Observability**
  - **Prometheus** scrapes service metrics (`/metrics`)  
  - **Grafana** dashboard for request rate, errors, latency  
  - **Alertmanager** triggers alerts if the service is down  

- **Deployment**
  - Fully containerized with Docker Compose  
  - Modular code layout (`app/`, `src/`)  
  - Config via `.env` (example included)  

---

## Tech Stack
- **Python** (FastAPI, LangChain, FAISS)  
- **Prometheus** (metrics collection)  
- **Grafana** (dashboards)  
- **Alertmanager** (alert routing)  
- **Docker Compose** (orchestration)  

---

## Quickstart

1. Clone the repo and `cd` into it
   ```bash
   git clone https://github.com/yourusername/genai-rag-microservice.git
   cd genai-rag-microservice
   ```

2. Copy environment example
   ```bash
   cp .env.example .env
   ```

3. Start the stack
   ```bash
   docker compose up --build
   ```

4. Access services:
   - API: [http://localhost:8000/docs](http://localhost:8000/docs)  
   - Metrics: [http://localhost:8000/metrics](http://localhost:8000/metrics)  
   - Prometheus: [http://localhost:9090](http://localhost:9090)  
   - Grafana: [http://localhost:3000](http://localhost:3000) (admin / admin)  
   - Alertmanager: [http://localhost:9093](http://localhost:9093)  

---

## Project Structure
```
.
├── app/                 # FastAPI app (endpoints, monitoring, RAG logic)
├── grafana_dashboards/  # Pre-provisioned Grafana dashboards
├── grafana_provisioning # Datasource + dashboard provisioning
├── prometheus.yml       # Prometheus config + scrape targets
├── alertmanager.yml     # Alert rules
├── docker-compose.yml   # Multi-service deployment
├── .env.example         # Example config
└── README.md
```

---

## Why this project
I wanted to build something closer to how **real enterprise software runs**:  
- Containerized, observable, alert-driven  
- Modular codebase instead of a single script  
- Clear separation between **app logic** and **infrastructure**  

It’s not production-grade, but it demonstrates awareness of the tools and practices companies use to run critical systems.

---

## License
MIT License  
