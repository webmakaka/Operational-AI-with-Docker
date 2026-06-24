#!/usr/bin/env bash
# curl_examples.sh — Direct HTTP examples for Docker Model Runner.
#
# Run Docker Model Runner first:
#   docker model run ai/smollm2:360M-Q4_K_M "warmup"
#
# Then run this script:
#   chmod +x curl_examples.sh && ./curl_examples.sh

set -euo pipefail

BASE="http://localhost:12434/engines/v1"
MODEL="ai/smollm2:360M-Q4_K_M"

echo "=== 1. Chat completions ==="
curl -s "$BASE/chat/completions" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [
      {\"role\": \"user\", \"content\": \"Explain Docker in simple terms.\"}
    ]
  }" | python3 -m json.tool

echo ""
echo "=== 2. List available models ==="
curl -s "$BASE/models" | python3 -m json.tool

echo ""
echo "=== 3. Streaming response ==="
curl -s "$BASE/chat/completions" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"stream\": true,
    \"messages\": [
      {\"role\": \"user\", \"content\": \"Count from 1 to 5.\"}
    ]
  }"
