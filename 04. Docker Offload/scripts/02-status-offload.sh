#!/usr/bin/env bash
set -euo pipefail

echo "[offload] Checking Docker Offload status..."
docker offload status
