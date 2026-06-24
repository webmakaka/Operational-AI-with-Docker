#!/usr/bin/env bash
set -euo pipefail

echo "[offload] Running Docker Offload diagnostics..."
docker offload diagnose
