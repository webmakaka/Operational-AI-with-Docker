# 02: Multiple models per service

Binds two models to one service: a chat LLM and an embedding model.

Compose injects four environment variables:

| Variable               | Value                                           |
|------------------------|-------------------------------------------------|
| `LLM_URL`              | `http://model-runner.docker.internal/engines/v1` |
| `LLM_MODEL`            | `ai/smollm2:360M-Q4_K_M`                       |
| `EMBEDDING_MODEL_URL`  | `http://model-runner.docker.internal/engines/v1` |
| `EMBEDDING_MODEL_MODEL`| `ai/all-minilm`                                 |

The URL is the same Docker Model Runner endpoint for both — the model
identifier in the request body selects which model to use.
