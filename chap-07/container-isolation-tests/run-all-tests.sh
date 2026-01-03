#!/bin/bash

echo "======================================"
echo "Container Isolation Tests"
echo "======================================"
echo ""

# Test 1: Shared Volumes
echo "Test 1: Shared Volumes with Read-Only Access"
echo "--------------------------------------"
cd test-shared-volumes
docker compose up -d
sleep 10
echo ""
echo "Writer Agent Output:"
docker compose logs writer-agent | tail -5
echo ""
echo "Reader Agent Output:"
docker compose logs reader-agent | tail -8
echo ""
read -p "Press Enter to cleanup and continue..."
docker compose down -v
cd ..
echo ""

# Test 2: Redis Pub/Sub
echo "Test 2: Redis Message Passing"
echo "--------------------------------------"
cd strategy2-redis-pubsub
docker compose up -d
sleep 15
echo ""
echo "Writer Output:"
docker compose logs writer | grep -A 5 "Publishing"
echo ""
echo "Reader Output:"
docker compose logs reader | grep -A 10 "Received"
echo ""
read -p "Press Enter to cleanup and continue..."
docker compose down -v
cd ..
echo ""

# Test 3: Network Isolation
echo "Test 3: Network Segmentation"
echo "--------------------------------------"
cd test-network-isolation
docker compose up -d
sleep 10
echo ""
echo "Frontend Agent Output:"
docker compose logs frontend-agent | tail -5
echo ""
echo "Backend Agent Output:"
docker compose logs backend-agent | tail -5
echo ""
read -p "Press Enter to cleanup..."
docker compose down -v
cd ..
echo ""

echo "======================================"
echo "All tests complete!"
echo "======================================"
