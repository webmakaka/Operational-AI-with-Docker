#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-onnx-export:offload}"

echo "[build] Building image: ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" .
