## Agent Discovery


```
docker compose up --build
```

Watch the coordinator discover and call the worker:


```
worker-1      | 🔧 Worker 640d12fed193 starting...
worker-1      |    Hostname: 640d12fed193
coordinator-1 | 🎯 Coordinator Agent Starting...
coordinator-1 |    Worker URL: http://worker:8000
coordinator-1 | 
coordinator-1 | 📤 Sending task #1 to worker...
coordinator-1 | ✅ Task completed by: 640d12fed193
coordinator-1 |    Hostname: 640d12fed193
coordinator-1 |    Message: Task processed by 640d12fed193
```

### Testing dynamic scaling and load balancing

```
docker compose up -d --scale worker=3
```

Docker spins up two more workers:

```
✔ Container agent-discovery-worker-1      Running
✔ Container agent-discovery-worker-2      Created
✔ Container agent-discovery-worker-3      Created
✔ Container agent-discovery-coordinator-1 Running
```

Watch the coordinator logs to see load balancing in action:

```
docker compose logs coordinator -f
```

At first, all tasks still go to the first worker:

```
coordinator-1 | ✅ Task completed by: 640d12fed193
coordinator-1 | ✅ Task completed by: 640d12fed193
coordinator-1 | ✅ Task completed by: 640d12fed193
```

But once the new workers finish starting up, Docker begins distributing tasks across all three:

```
coordinator-1 | 📤 Sending task #18 to worker...
coordinator-1 | ✅ Task completed by: ebfa6cf86754
coordinator-1 | 
coordinator-1 | 📤 Sending task #19 to worker...
coordinator-1 | ✅ Task completed by: ebfa6cf86754
coordinator-1 | 
coordinator-1 | 📤 Sending task #20 to worker...
coordinator-1 | ✅ Task completed by: fafe4d7988aa
coordinator-1 | 
coordinator-1 | 📤 Sending task #21 to worker...
coordinator-1 | ✅ Task completed by: 640d12fed193
```

```
NAME                            CONTAINER ID
agent-discovery-coordinator-1   627b453bf8f5
agent-discovery-worker-1        640d12fed193
agent-discovery-worker-2        ebfa6cf86754
agent-discovery-worker-3        fafe4d7988aa
```


