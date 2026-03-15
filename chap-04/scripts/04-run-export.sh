#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-onnx-export:offload}"
MODEL_ID="${MODEL_ID:-distilbert/distilbert-base-uncased-distilled-squad}"
TASK="${TASK:-question-answering}"
OUTPUT_DIR="${OUTPUT_DIR:-$PWD/out}"

mkdir -p "${OUTPUT_DIR}"

echo "[run] Running export job with image: ${IMAGE_NAME}"
echo "[run] MODEL_ID=${MODEL_ID}"
echo "[run] TASK=${TASK}"
echo "[run] OUTPUT_DIR=${OUTPUT_DIR}"

docker run --rm \
  -e MODEL_ID="${MODEL_ID}" \
  -e TASK="${TASK}" \
  -e OUT_DIR="/out" \
  -v "${OUTPUT_DIR}:/out" \
  "${IMAGE_NAME}"
