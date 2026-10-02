## Agent Security

```
docker compose up --build
```

Watch the agent test security boundaries:

```
{"timestamp": "2025-12-29 13:54:09,336", "level": "INFO", "message": "🔒 Secure Agent Starting...", "agent_id": "506278d768cc"}
{"timestamp": "2025-12-29 13:54:09,337", "level": "INFO", "message": "   Running as: 1000:1000", "agent_id": "506278d768cc"}
{"timestamp": "2025-12-29 13:54:09,337", "level": "WARNING", "message": "⚠️  Filesystem is read-only: [Errno 30] Read-only file system: '/test-write.txt'", "agent_id": "506278d768cc"}
{"timestamp": "2025-12-29 13:54:09,337", "level": "INFO", "message": "✅ /tmp is writable (tmpfs)", "agent_id": "506278d768cc"}
{"timestamp": "2025-12-29 13:54:09,337", "level": "INFO", "message": "Starting task", "agent_id": "506278d768cc", "task_id": "task-001"}
{"timestamp": "2025-12-29 13:54:10,342", "level": "INFO", "message": "Task completed", "agent_id": "506278d768cc", "task_id": "task-001", "duration": 1.0}
```

### Verifying security constraints

```
# Test read-only filesystem
docker compose exec secure-agent touch /test.txt
```

The filesystem blocks it:

```
touch: cannot touch '/test.txt': Read-only file system
```

 Now test that tmpfs actually works:

```
docker compose exec secure-agent touch /tmp/test.txt && echo "✅ tmpfs write succeeded"
```

This succeeds:

```
✅ tmpfs write succeeded
```

### Parsing structured logs

```
# Get all completed tasks with metrics
docker compose logs secure-agent | grep -o '{.*}' | jq 'select(.message == "Task completed") | {task_id, duration}'
```

This returns clean task metrics:

```
{
  "task_id": "task-001",
  "duration": 1.0
}
{
  "task_id": "task-002",
  "duration": 1.01
}
{
  "task_id": "task-003",
  "duration": 1.01
}
```


