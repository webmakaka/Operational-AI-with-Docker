#!/bin/bash
# Setup script for Chapter 9: Advanced Agent Orchestration
# Creates all example files and directories referenced in the chapter.
# Run: bash setup-chap-09.sh

set -e

BASE="chap-09"
rm -rf "$BASE"
mkdir -p "$BASE"

# ───── README ─────
cat > "$BASE/README.md" << 'EOF'
# Chapter 9: Advanced Agent Orchestration

Code for Chapter 9 of *Operational AI with Docker*.

Three tools covered: Docker Sandboxes, cagent, and kagent.

## What you need

- Docker Desktop 4.58+ (for Sandboxes)
- cagent CLI - `brew install docker/tap/cagent`
- For kagent stuff: kubectl, kind, Helm 3
- At least one API key (OpenAI, Anthropic, or Gemini)

## Layout

```
sandboxes/     Docker Sandboxes commands (run interactively)
cagent/        cagent YAML configs (run with: cagent run <file>)
kagent/        Kubernetes manifests for kagent
```

## Quick start

```bash
# Spin up a sandbox
docker sandbox run claude ~/my-project

# Run a cagent example
cd cagent/01-pirate-assistant
cagent run agents.yaml

# Deploy kagent on a local cluster
cd kagent
kind create cluster --config kind-cluster.yaml
bash install-kagent.sh
kubectl apply -f 03-devops-assistant/
```
EOF

# ───── SANDBOXES ─────
mkdir -p "$BASE/sandboxes"

cat > "$BASE/sandboxes/commands.sh" << 'EOF'
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
EOF
chmod +x "$BASE/sandboxes/commands.sh"

# ───── CAGENT EXAMPLES ─────

# 01 - Pirate assistant (minimal config)
mkdir -p "$BASE/cagent/01-pirate-assistant"
cat > "$BASE/cagent/01-pirate-assistant/agents.yaml" << 'EOF'
name: pirate-assistant
model: openai/gpt-4.1-mini
description: A helpful assistant that talks like a pirate
instructions: |
  You are a helpful assistant who speaks like a pirate.
  Always use pirate vocabulary and expressions.
EOF

# 02 - Code reviewer (multi-tool agent)
mkdir -p "$BASE/cagent/02-code-reviewer"
cat > "$BASE/cagent/02-code-reviewer/agents.yaml" << 'EOF'
name: code-reviewer
model: anthropic/claude-sonnet-4-20250514
description: Reviews code and suggests improvements
instructions: |
  You are an expert code reviewer. When given a codebase:
  1. Use filesystem to read the project structure
  2. Create a todo list of files to review
  3. Use think to analyze patterns and issues
  4. Write a review summary using filesystem
  5. Use memory to track which files you've reviewed
tools:
  - filesystem
  - shell
  - memory
  - think
  - todo
EOF

# 03 - Multi-model classifier + analyzer
mkdir -p "$BASE/cagent/03-multi-model"
cat > "$BASE/cagent/03-multi-model/agents.yaml" << 'EOF'
agents:
  quick-classifier:
    model: openai/gpt-4.1-mini
    description: Fast triage of incoming requests
    instructions: |
      Classify incoming requests as: bug, feature, question, or other.
      Be fast and concise.

  deep-analyzer:
    model: anthropic/claude-sonnet-4-20250514
    description: Deep analysis of complex issues
    instructions: |
      Perform thorough analysis of technical issues.
      Consider edge cases, security implications, and performance.
    tools:
      - think
      - filesystem
EOF

# 04 - Local model with Docker Model Runner
mkdir -p "$BASE/cagent/04-local-model"
cat > "$BASE/cagent/04-local-model/agents.yaml" << 'EOF'
models:
  local-llm:
    provider: docker
    model: ai/llama3.2:3B-Q8_0

agents:
  local-agent:
    model: local-llm
    description: Runs entirely on local hardware
    instructions: Analyze files in the current directory.
    tools:
      - filesystem
EOF

# 05 - Named model configurations
mkdir -p "$BASE/cagent/05-named-models"
cat > "$BASE/cagent/05-named-models/agents.yaml" << 'EOF'
models:
  creative-writer:
    provider: openai
    model: gpt-4.1-mini
    temperature: 0.9

  precise-coder:
    provider: anthropic
    model: claude-sonnet-4-20250514
    temperature: 0.1

  deep-thinker:
    provider: anthropic
    model: claude-sonnet-4-20250514
    thinking_budget: high
EOF

# 06 - Bug investigation team (multi-agent)
mkdir -p "$BASE/cagent/06-bug-investigation-team/agents"
cat > "$BASE/cagent/06-bug-investigation-team/bug-investigator.yaml" << 'EOF'
name: bug-investigator
model: anthropic/claude-sonnet-4-20250514
description: Lead investigator that coordinates bug fixes
instructions: |
  You lead bug investigations. When a bug is reported:
  1. Analyze the bug report
  2. Delegate code investigation to the code-analyst
  3. Delegate fix implementation to the fixer
  4. Review the fix and provide final assessment
tools:
  - think
  - todo
sub_agents:
  - agents/code-analyst.yaml
  - agents/fixer.yaml
EOF

cat > "$BASE/cagent/06-bug-investigation-team/agents/code-analyst.yaml" << 'EOF'
name: code-analyst
model: openai/gpt-4.1-mini
description: Analyzes code to identify bug locations
instructions: |
  Read the codebase and identify the root cause of bugs.
  Report file names, line numbers, and explanations.
tools:
  - filesystem
  - shell
EOF

cat > "$BASE/cagent/06-bug-investigation-team/agents/fixer.yaml" << 'EOF'
name: fixer
model: anthropic/claude-sonnet-4-20250514
description: Implements bug fixes
instructions: |
  Implement fixes for identified bugs.
  Write tests to verify the fix.
  Run tests to confirm they pass.
tools:
  - filesystem
  - shell
EOF

# 07 - Research assistant with MCP tools
mkdir -p "$BASE/cagent/07-research-assistant"
cat > "$BASE/cagent/07-research-assistant/agents.yaml" << 'EOF'
name: research-assistant
model: openai/gpt-4.1-mini
description: Researches topics using web search and GitHub
instructions: |
  Research the given topic thoroughly.
  Search the web for recent information.
  Check GitHub for relevant repositories and code.
tools:
  - think
  - memory
toolsets:
  - docker:duckduckgo
  - docker:github-official
EOF

# 08 - MCP with restricted tools
mkdir -p "$BASE/cagent/08-restricted-mcp"
cat > "$BASE/cagent/08-restricted-mcp/agents.yaml" << 'EOF'
name: readonly-github-agent
model: openai/gpt-4.1-mini
description: Read-only GitHub researcher
instructions: |
  Search GitHub for repositories, read files, and list issues.
  You cannot create, modify, or delete anything.
tools:
  - think
toolsets:
  - name: docker:github-official
    tools:
      - search_repositories
      - get_file_contents
      - list_issues
EOF

# ───── KAGENT EXAMPLES ─────
mkdir -p "$BASE/kagent"

# kind cluster config
cat > "$BASE/kagent/kind-cluster.yaml" << 'EOF'
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
EOF

# install script
cat > "$BASE/kagent/install-kagent.sh" << 'EOF'
#!/bin/bash
# Install kagent on a kind cluster
set -e

echo "Creating kind cluster..."
kind create cluster --config kind-cluster.yaml 2>/dev/null || echo "Cluster already exists"

echo "Adding kagent Helm repo..."
helm repo add kagent https://kagent-ai.github.io/kagent/
helm repo update

echo "Installing kagent..."
helm install kagent kagent/kagent \
  --set apiKey="${OPENAI_API_KEY}" \
  --namespace kagent \
  --create-namespace

echo "Waiting for controller..."
kubectl wait --for=condition=ready pod -l app=kagent -n kagent --timeout=120s

echo "Done. Verify with: kubectl get pods -n kagent"
EOF
chmod +x "$BASE/kagent/install-kagent.sh"

# 01 - DevOps assistant (single agent)
mkdir -p "$BASE/kagent/01-devops-assistant"
cat > "$BASE/kagent/01-devops-assistant/devops-assistant.yaml" << 'EOF'
apiVersion: kagent.ai/v1
kind: Agent
metadata:
  name: devops-assistant
  namespace: kagent
spec:
  description: "Kubernetes DevOps assistant"
  systemPrompt: |
    You are a DevOps expert. Help with Kubernetes
    troubleshooting, deployment issues, and infrastructure
    questions. Be concise and practical.
  modelConfigRef:
    name: gpt4-config
---
apiVersion: kagent.ai/v1
kind: ModelConfig
metadata:
  name: gpt4-config
  namespace: kagent
spec:
  provider: openai
  model: gpt-4.1-mini
  apiKeySecretRef:
    name: openai-secret
    key: api-key
EOF

# 02 - Ops troubleshooting team (multi-agent)
mkdir -p "$BASE/kagent/02-ops-team"
cat > "$BASE/kagent/02-ops-team/ops-team.yaml" << 'EOF'
apiVersion: kagent.ai/v1
kind: Agent
metadata:
  name: ops-coordinator
spec:
  description: "Coordinates DevOps troubleshooting"
  systemPrompt: |
    You coordinate troubleshooting across specialized agents.
    Delegate log analysis to log-analyzer.
    Delegate metrics investigation to metrics-checker.
    Synthesize findings into actionable recommendations.
  modelConfigRef:
    name: claude-sonnet-config
  subAgents:
    - name: log-analyzer
    - name: metrics-checker
---
apiVersion: kagent.ai/v1
kind: Agent
metadata:
  name: log-analyzer
spec:
  description: "Analyzes Kubernetes logs for issues"
  systemPrompt: |
    Analyze Kubernetes pod logs to identify errors,
    warnings, and anomalies. Report findings concisely.
  modelConfigRef:
    name: gpt4-mini-config
  tools:
    - name: k8s-logs
---
apiVersion: kagent.ai/v1
kind: Agent
metadata:
  name: metrics-checker
spec:
  description: "Checks cluster metrics and resource usage"
  systemPrompt: |
    Monitor Kubernetes cluster metrics including CPU,
    memory, and network usage. Identify resource bottlenecks.
  modelConfigRef:
    name: gpt4-mini-config
  tools:
    - name: prometheus-query
EOF

# 03 - Autoscaling config
mkdir -p "$BASE/kagent/03-autoscaling"
cat > "$BASE/kagent/03-autoscaling/hpa.yaml" << 'EOF'
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: log-analyzer-hpa
spec:
  scaleTargetRef:
    apiVersion: kagent.ai/v1
    kind: Agent
    name: log-analyzer
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
EOF

cat > "$BASE/kagent/03-autoscaling/resource-limits.yaml" << 'EOF'
apiVersion: kagent.ai/v1
kind: Agent
metadata:
  name: log-analyzer
spec:
  resources:
    requests:
      cpu: "500m"
      memory: "512Mi"
    limits:
      cpu: "2"
      memory: "2Gi"
EOF

# 04 - Network policy
mkdir -p "$BASE/kagent/04-network-policy"
cat > "$BASE/kagent/04-network-policy/agent-isolation.yaml" << 'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: agent-isolation
spec:
  podSelector:
    matchLabels:
      kagent.ai/role: agent
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              kagent.ai/role: coordinator
  egress:
    - to:
        - podSelector:
            matchLabels:
              kagent.ai/role: mcp-server
    - to:
        - namespaceSelector:
            matchLabels:
              name: kagent
EOF

# ───── .gitignore ─────
cat > "$BASE/.gitignore" << 'EOF'
.env
*.key
*.secret
EOF

# ───── Done ─────
echo ""
echo "Created $(find "$BASE" -type f | wc -l | tr -d ' ') files in $BASE/"
echo ""
find "$BASE" -type f | sort | sed 's/^/  /'
