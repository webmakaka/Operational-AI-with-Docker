# 01: Basic model binding

Demonstrates the minimal Compose `models:` syntax.

When you run `docker compose up`, Docker Model Runner:
1. Pulls `ai/smollm2:360M-Q4_K_M` if not already cached.
2. Starts the model runner backend.
3. Injects `LLM_URL` and `LLM_MODEL` into the `chat-app` container.

Your application reads these environment variables to call the model:

```python
import os, openai
openai.api_base = os.environ["LLM_URL"]
model = os.environ["LLM_MODEL"]
```
