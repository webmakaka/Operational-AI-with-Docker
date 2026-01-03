# Container Isolation Tests

These tests verify the container isolation patterns from Chapter 7.

## Test 1: Shared Volumes with Read-Only Access

This test demonstrates how agents can share data safely using volumes.

### Run the test:
```bash
cd test-shared-volumes
docker compose up
```

### Expected output:
- Writer agent creates a file in /workspace
- Reader agent successfully reads the file
- Reader agent FAILS to write (read-only mount)

### Verify:
```bash
docker compose logs writer-agent
docker compose logs reader-agent
```

You should see:
- Writer: "This is shared data from writer"
- Reader: Successfully reads the data
- Reader: "Write blocked - read-only mount working!"

### Cleanup:
```bash
docker compose down -v
```

## Test 2: Redis Message Passing

This test shows agents communicating through Redis pub/sub.

### Run the test:
```bash
cd ../strategy2-redis-pubsub
docker compose up
```

### Expected output:
- Writer publishes metadata to Redis channel
- Reader receives and processes the metadata
- No direct filesystem sharing

### Verify:
```bash
docker compose logs writer
docker compose logs reader
```

### Cleanup:
```bash
docker compose down -v
```

## Test 3: Network Segmentation

This test demonstrates network isolation between agents.

### Run the test:
```bash
cd ../test-network-isolation
docker compose up
```

### Expected output:
- Frontend agent can access the internet
- Backend agent CANNOT access the internet (internal network)
- Agents can only communicate within their network zones

### Verify:
```bash
docker compose logs frontend-agent
docker compose logs backend-agent
```

### Cleanup:
```bash
docker compose down -v
```
