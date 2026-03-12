#!/usr/bin/env python3
"""
python_sdk.py — Call Docker Model Runner using the OpenAI Python SDK.

Install: pip install openai
Run:     python python_sdk.py

Docker Model Runner exposes an OpenAI-compatible API at:
  http://localhost:12434/engines/v1          (from host)
  http://model-runner.docker.internal/engines/v1  (from inside a container)
"""

import openai

# Point the SDK at the local Docker Model Runner.
# No API key is required — DMR's local API has no authentication by default.
client = openai.OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="not-required",  # SDK requires a value; DMR ignores it
)

response = client.chat.completions.create(
    model="ai/smollm2:360M-Q4_K_M",
    messages=[
        {"role": "user", "content": "What is Docker Compose?"}
    ],
)

print(response.choices[0].message.content)
print(f"\nTokens used: {response.usage.total_tokens}")
