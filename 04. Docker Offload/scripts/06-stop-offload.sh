#!/usr/bin/env bash
set -euo pipefail

echo "[offload] Stopping Docker Offload session..."
docker offload stop -f
