#!/bin/bash

# Test script to demonstrate agent memory persistence

set -e

echo "🧪 Testing Agent Memory Persistence"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Clean up any existing containers
echo -e "${BLUE}📦 Cleaning up existing containers...${NC}"
docker compose down -v 2>/dev/null || true
echo ""

# Start services
echo -e "${BLUE}🚀 Starting agent and Redis...${NC}"
docker compose up -d agent-memory
sleep 5
echo ""

# Run agent first time
echo -e "${GREEN}✨ FIRST RUN: Agent will process all tasks${NC}"
echo "=============================================="
docker compose run --rm task-agent &
AGENT_PID=$!

# Wait for agent to process tasks
sleep 30

# Stop the agent
docker compose stop task-agent
echo ""

# Check Redis memory
echo -e "${YELLOW}📊 Checking Redis memory state...${NC}"
docker compose exec agent-memory redis-cli KEYS "agent:*"
echo ""

# Restart agent
echo -e "${GREEN}🔄 SECOND RUN: Agent should skip completed tasks${NC}"
echo "================================================="
docker compose run --rm task-agent &
AGENT_PID=$!

# Wait for agent
sleep 30

# Stop everything
echo ""
echo -e "${BLUE}🛑 Stopping services...${NC}"
docker compose stop

echo ""
echo -e "${GREEN}✅ Test completed!${NC}"
echo ""
echo "What you should observe:"
echo "1. First run: Agent processes all tasks"
echo "2. Second run: Agent skips already completed tasks"
echo "3. Redis persists memory across restarts"
echo ""
echo "To manually inspect Redis:"
echo "  docker compose exec agent-memory redis-cli"
echo "  > KEYS agent:*"
echo "  > LRANGE agent:task-processor:actions:task-001 0 -1"
