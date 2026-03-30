# Chapter 9: Advanced Agent Orchestration


## What you need

- Docker Desktop 4.58+ (for Sandboxes)
- cagent CLI - `brew install docker/tap/docker-agent`
- For kagent stuff: kubectl, kind, Helm 3
- At least one API key (OpenAI, Anthropic, or Gemini)

## Layout

```
sandboxes/     Docker Sandboxes commands (run interactively)
docker-agent/  Docker Agent YAML configs (run with: cagent run <file>)
kagent/        Kubernetes manifests for kagent
```

## Quick start

```bash
# Spin up a sandbox
docker sandbox run claude ~/my-project

# Run a cagent example
cd docker-agent/01-pirate-assistant
docker agent run agents.yaml

# Deploy kagent on a local cluster
cd kagent
kind create cluster --config kind-cluster.yaml
bash install-kagent.sh
kubectl apply -f 03-devops-assistant/
```
