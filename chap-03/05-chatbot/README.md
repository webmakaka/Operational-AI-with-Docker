# 05: Chatbot: React + Go + Docker Model Runner

The primary application built in Chapter 3. A full-stack chatbot where:

- **React frontend** sends user messages to the Go backend.
- **Go backend** calls Docker Model Runner via the OpenAI-compatible API.
- **Docker Model Runner** serves `ai/smollm2` locally — no cloud API needed.

## Running

```bash
# From chap-03/05-chatbot/
docker compose up --build
```

Open http://localhost:3000 in your browser.

## How it works

Compose injects two environment variables into the Go backend container:

| Variable  | Value                                                         |
|-----------|---------------------------------------------------------------|
| `LLM_URL` | `http://model-runner.docker.internal/engines/v1`              |
| `LLM_MODEL`| `ai/smollm2`                                                 |

The backend uses these to call DMR's OpenAI-compatible endpoint:

```
POST http://model-runner.docker.internal/engines/v1/chat/completions
```

`model-runner.docker.internal` is the DNS name Docker Desktop provides
for containers to reach the Model Runner on the host — equivalent to
`localhost:12434` from outside a container.

## Chapter 5 connection

This same application is migrated to Kubernetes in Chapter 5. The same
Docker images, the same API endpoint — just deployed as Deployments and
Services on a kind cluster instead of via Compose.
