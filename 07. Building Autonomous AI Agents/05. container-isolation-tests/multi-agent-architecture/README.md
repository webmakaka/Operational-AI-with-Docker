# Multi-Container Agent Architecture Test

This demonstrates the key benefits of multi-container agent architectures:

## Architecture Benefits

1. **Shared Model**: Multiple agents use one LLM instance (cost optimization)
2. **Isolated State**: Each agent has dedicated volumes for persistence
3. **Shared Memory**: Redis provides centralized coordination
4. **Auto-recovery**: `restart: unless-stopped` recovers crashed agents
5. **Named Volumes**: State persists across container restarts

## Run the Test

```bash
docker compose up --build
```

## What You'll See

- Two agents start: `bug-tracker` and `status-reporter`
- Each agent writes to its own state key: `agent:bug-tracker:state`
- Agents can read each other's state (shared memory)
- Each agent has isolated filesystem: `/data` volume

## Verify Isolation

### Check volumes (isolated state):
```bash
docker volume ls
```

You should see:
- `multi-agent-architecture_bug-tracker-state`
- `multi-agent-architecture_reporter-state`
- `multi-agent-architecture_shared-memory`

### Check Redis (shared coordination):
```bash
docker compose exec agent-memory redis-cli KEYS "agent:*"
```

You should see:
- `agent:bug-tracker:state`
- `agent:status-reporter:state`

### View agent states:
```bash
docker compose exec agent-memory redis-cli GET "agent:bug-tracker:state"
docker compose exec agent-memory redis-cli GET "agent:status-reporter:state"
```

## Test Auto-Recovery

Kill an agent and watch it restart:
```bash
docker compose kill bug-tracker
docker compose ps
# Wait 5-10 seconds
docker compose ps
# bug-tracker should be back up
```

## Test State Persistence and Resumption

The agents resume from their last state after restarts. Let's test this:

### Check current state:
```bash
docker compose exec agent-memory redis-cli GET "agent:bug-tracker:state"
docker compose exec agent-memory redis-cli GET "agent:status-reporter:state"
```

Note the iteration numbers (e.g., iteration 50).

### Restart one agent:
```bash
docker compose restart bug-tracker
```

### Watch it resume:
```bash
docker compose logs bug-tracker --tail 20 -f
```

You should see:
```
🤖 Starting bug-tracker (monitoring)
📥 Resuming from iteration 51
✅ bug-tracker iteration 51 - state saved
```

The agent picked up where it left off!

### Test full restart:
```bash
# Stop everything
docker compose down

# Volumes persist (check)
docker volume ls | grep multi-agent

# Restart everything
docker compose up -d

# Both agents resume from their last iteration
docker compose logs bug-tracker --tail 10
docker compose logs status-reporter --tail 10
```

Both agents should show "📥 Resuming from iteration X" messages.

## Cleanup

```bash
docker compose down -v
```
