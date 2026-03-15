#!/usr/bin/env bash
set -euo pipefail

echo "[offload] Starting Docker Offload session..."
docker offload start "$@"
