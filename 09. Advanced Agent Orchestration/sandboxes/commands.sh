#!/bin/bash
# Docker Sandboxes - interactive command reference.
# Don't run this as a script. Copy-paste the commands you need.

# ── Prerequisites ──
# Set your API key GLOBALLY (sandbox daemon can't see inline exports):
#   echo 'export ANTHROPIC_API_KEY=sk-ant-your-key' >> ~/.zshrc
#   source ~/.zshrc
#   # Restart Docker Desktop after this

# ── Create & Run ──
docker sandbox run claude ~/my-project
docker sandbox run claude ~/my-project ~/docs:ro   # read-only mount
docker sandbox run gemini ~/my-project
docker sandbox run codex ~/my-project

# ── Manage ──
docker sandbox ls
docker sandbox exec claude-my-project -- ls -la
docker sandbox exec -it claude-my-project -- bash
docker sandbox stop claude-my-project
docker sandbox run claude-my-project              # reconnect
docker sandbox rm claude-my-project

# ── Network Isolation ──
docker sandbox network proxy claude-my-project --policy deny
docker sandbox network proxy claude-my-project \
  --allow api.anthropic.com \
  --allow github.com \
  --allow registry.npmjs.org \
  --allow pypi.org

# ── Inside the Sandbox (agent runs these, not you) ──
# docker build -t my-app .
# docker run -d -p 8080:8080 my-app
# docker compose up --build
