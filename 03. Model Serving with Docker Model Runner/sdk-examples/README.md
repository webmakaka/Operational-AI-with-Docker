# SDK examples

Direct API and SDK examples for Docker Model Runner.

## Prerequisites

```bash
# Pull the model
docker model pull ai/smollm2:360M-Q4_K_M

# Warm it up (starts the inference engine)
docker model run ai/smollm2:360M-Q4_K_M "hello"
```

## Python

```bash
pip install openai
python python_sdk.py
```

## Node.js

```bash
npm install openai
node nodejs_sdk.js
```

## curl

```bash
chmod +x curl_examples.sh
./curl_examples.sh
```

## Base URL reference

| Context                          | Base URL                                               |
|----------------------------------|--------------------------------------------------------|
| From host machine                | `http://localhost:12434/engines/v1`                    |
| From Docker container (Compose)  | `http://model-runner.docker.internal/engines/v1`       |
| Alternative (engines path)       | `http://localhost:12434/engines/llama.cpp/v1`          |

No `Authorization` header is required — DMR's local API has no authentication.
