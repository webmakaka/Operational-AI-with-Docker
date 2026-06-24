# Chapter 3: Model Serving with Docker Model Runner

Code examples for Chapter 3 

## Structure

```
chap-03/
├── 01-basic-model/           # Basic model binding in Compose
├── 02-multiple-models/       # Multiple models per service
├── 03-long-syntax/           # Custom endpoint/model env var names
├── 04-model-config/          # context_size and runtime_flags
├── 05-chatbot/               # React + Go chatbot wired to DMR
├── 06-observability/         # Prometheus + Grafana + Jaeger stack
└── sdk-examples/             # Python and Node.js OpenAI SDK examples
```

## Prerequisites

- Docker Desktop 4.41 or later with Docker Model Runner enabled
- Docker Model Runner enabled: Settings → AI → Enable Docker Model Runner
- 8 GB RAM minimum (16 GB recommended)

## Quick start

```bash
# Pull the model used in most examples
docker model pull ai/smollm2:360M-Q4_K_M
```

See the chapter for full walkthrough.
