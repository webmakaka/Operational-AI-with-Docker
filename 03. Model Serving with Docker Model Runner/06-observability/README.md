# 06: Observability: Prometheus + Grafana + Jaeger

Extends the Chapter 3 chatbot with a full observability stack.

## Services

| Service    | URL                         | Purpose                         |
|------------|-----------------------------|---------------------------------|
| backend    | http://localhost:8080       | Go backend (app + /metrics)     |
| Prometheus | http://localhost:9090       | Metrics scraping and storage    |
| Grafana    | http://localhost:3001       | Dashboards (admin/admin)        |
| Jaeger     | http://localhost:16686      | Distributed tracing UI          |

## Key metrics exposed by the backend

| Metric                              | Type      | Description                  |
|-------------------------------------|-----------|------------------------------|
| `genai_app_http_requests_total`     | counter   | Total HTTP requests          |
| `genai_app_model_latency_seconds`   | histogram | DMR response latency         |
| `genai_app_tokens_per_second`       | gauge     | Current inference throughput |
| `genai_app_llamacpp_context_size`   | gauge     | Context window in use        |
| `genai_app_chat_tokens_total`       | counter   | Total tokens processed       |

## Running

```bash
cd chap-03/06-observability
docker compose up --build

# Watch metrics
open http://localhost:9090      # Prometheus — query genai_app_*
open http://localhost:3001      # Grafana — admin/admin
open http://localhost:16686     # Jaeger — search for service "chatbot"
```
