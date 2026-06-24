# Research Assistant Multi-Agent System

A hierarchical multi-agent system that coordinates specialized AI agents to answer research questions.

## Architecture

```
┌─────────────────────────────────────────┐
│         Coordinator Agent               │
│    (Plans & orchestrates workflow)      │
│         Model: qwen3 (8B)              │
└──────────┬──────────────────────────────┘
           │
    ┌──────┴──────┬──────────────┐
    ▼             ▼              ▼
┌─────────┐  ┌─────────┐  ┌──────────┐
│Searcher │  │Analyzer │  │  Writer  │
│  Agent  │  │  Agent  │  │  Agent   │
│nano(1.6B)│ │micro(3B)│  │micro(3B) │
└─────────┘  └─────────┘  └──────────┘
     │
     ▼
┌──────────────┐
│ MCP Gateway  │
│ (Web Search) │
└──────────────┘
```

## Agents

- **Coordinator** (qwen3): Plans research strategy and orchestrates agents
- **Searcher** (granite-nano): Executes web searches via MCP Gateway
- **Analyzer** (granite-micro): Extracts insights from search results
- **Writer** (granite-micro): Synthesizes final research report

## Requirements

- Docker Desktop 4.42.0+
- Docker Model Runner enabled
- 16GB RAM minimum

## Usage

```bash
# Start the system
docker compose up --build

# Wait for all agents to start (check logs for "healthy")

# Submit a research question
curl -X POST http://localhost:8080/api/research \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the latest developments in Docker AI?"}'

# Response includes:
# - search queries used
# - key findings
# - final research report
```

## How It Works

1. Coordinator receives question and generates research plan
2. Searcher executes web searches via MCP Gateway
3. Analyzer extracts key insights from search results
4. Writer synthesizes findings into final report
5. All state stored in Redis for tracking

## Model Selection

| Agent | Model | Why? |
|-------|-------|------|
| Coordinator | qwen3 (8B) | Complex planning & orchestration |
| Searcher | granite-nano (1.6B) | Simple query formatting |
| Analyzer | granite-micro (3B) | Medium complexity summarization |
| Writer | granite-micro (3B) | Structured report writing |

## Shared State

Redis stores:
- Research plan
- Search results
- Extracted insights
- Final report

This allows agents to remain stateless and enables async processing.
