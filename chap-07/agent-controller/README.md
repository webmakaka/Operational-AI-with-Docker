# Agent Controller - Multi-Agent Orchestration System

A complete working example of an **Agent Controller** that manages multiple autonomous agents, coordinates tasks, and provides real-time monitoring.

## What This Demonstrates

**Agent Registration** - Agents self-register with the controller  
**Task Queue Management** - Centralized task distribution  
**Agent Monitoring** - Real-time health checks and status tracking  
**Load Balancing** - Tasks automatically distributed to available agents  
**Failure Recovery** - Automatic agent restarts on failure  
**Web Dashboard** - Visual monitoring of entire system  
**REST API** - Programmatic control of agents and tasks  

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Agent Controller                        │
│  - REST API (port 8000)                             │
│  - Web Dashboard                                     │
│  - Task Queue Management                            │
│  - Agent Health Monitoring                          │
└──────────────┬──────────────────────────────────────┘
               │
       ┌───────┴──────────┬─────────────┐
       │                  │             │
   ┌───▼───┐          ┌───▼───┐    ┌───▼───┐
   │Worker │          │Worker │    │Worker │
   │  #1   │          │  #2   │    │  #3   │
   │(Data) │          │(Analyst)   │  ...  │
   └───┬───┘          └───┬───┘    └───┬───┘
       │                  │             │
       └───────┬──────────┴─────────────┘
               │
        ┌──────▼───────┐
        │    Redis     │
        │  (Memory)    │
        └──────────────┘
```

## Quick Start

```bash
# Start the entire system
docker compose up --build

# Access the dashboard
open http://localhost:8000
```

**You should see:**
- Controller starts and creates demo tasks
- Worker agents register themselves
- Agents pull and process tasks
- Dashboard shows real-time status

## Dashboard Features

The web dashboard at `http://localhost:8001` shows:

1. **System Stats**
   - Total Agents
   - Active Agents
   - Pending Tasks
   - Success Rate

2. **Agent List**
   - Agent name and type
   - Active/Inactive status
   - Tasks completed/failed
   - Last heartbeat time

3. **Task Queue**
   - Pending tasks
   - Task descriptions
   - Assigned types

**Auto-refreshes every 5 seconds!**

## REST API

### Agent Management

```bash
# Get all agents
curl http://localhost:8000/api/agents

# Register a new agent
curl -X POST http://localhost:8000/api/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "worker-3", "type": "specialist"}'

# Send heartbeat
curl -X POST http://localhost:8000/api/agents/worker-1/heartbeat
```

### Task Management

```bash
# Get task queue
curl http://localhost:8001/api/tasks

# Assign a new task
curl -X POST http://localhost:8001/api/tasks/assign \
  -H "Content-Type: application/json" \
  -d '{"id": "task-123", "description": "Analyze data", "type": "analyst"}'

# Agent requests next task
curl -X POST http://localhost:8001/api/tasks/dequeue \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "worker-1"}'

# Mark task complete
curl -X POST http://localhost:8001/api/tasks/task-123/complete \
  -H "Content-Type: application/json" \
  -d '{"success": true, "result": "Analysis complete"}'
```

### System Stats

```bash
# Get system statistics
curl http://localhost:8000/api/stats
```

## Testing the System

### Test 1: Verify Agents Register

```bash
# Start system
docker compose up -d

# Wait a few seconds, then check
curl http://localhost:8000/api/agents | jq

# Expected: 2 agents (worker-1, worker-2)
```

### Test 2: Add Tasks Dynamically

```bash
# Add a new task
curl -X POST http://localhost:8001/api/tasks/assign \
  -H "Content-Type: application/json" \
  -d '{"id": "manual-001", "description": "Process urgent data", "type": "data-processor"}'

# Watch logs to see which agent picks it up
docker compose logs -f worker-1 worker-2
```

### Test 3: Agent Failure Recovery

```bash
# Kill an agent
docker compose kill worker-1

# Watch dashboard - agent goes inactive
# Docker restarts it automatically (restart: on-failure)
# Agent re-registers with controller
docker compose logs -f worker-1
```

### Test 4: Scale Agents

```bash
# Add more workers
docker compose up -d --scale worker-2=3

# Check dashboard - 4 agents total now
```

## 📁 File Structure

```
agent-controller/
├── docker-compose.yml      # Defines all services
├── controller.py           # Controller with REST API
├── agent.py               # Worker agent logic
├── Dockerfile.controller   # Controller container
├── Dockerfile.agent        # Agent container
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔄 Agent Lifecycle

### 1. Startup
```
Agent starts → Waits for controller → Registers → Sends heartbeat
```

### 2. Task Processing Loop
```
Request task → Process with LLM → Report result → Repeat
```

### 3. Heartbeat
```
Every 10 iterations → Send heartbeat → Controller marks as active
```

### 4. Failure
```
Agent crashes → Docker restarts → Re-register → Resume work
```

