
## Memory and State

```
docker compose up --build
```

You'll see the agent start with Redis ready:

```
 => => exporting config sha256:811fa2f874a038286a77c20f5f831da8968b85dc446fe02a8e3dc938c30  0.0s
 => => exporting attestation manifest sha256:5dca18d80903a3bc28c3cd088e85edfa2f2a8b31bc0e7  0.0s
 => => exporting manifest list sha256:c298425c36a5e7823d1b769433961ed6333f744fe5862424d104  0.0s
 => => naming to docker.io/library/memory-state-task-agent:latest                           0.0s
[+] up 12/13king to docker.io/library/memory-state-task-agent:latest                        0.2s
[+] up 16/17is:7-alpine  Pulled                                                             5.9s
 ✔ Image redis:7-alpine                Pulled                                               5.9s
 ✔ Image memory-state-task-agent       Built                                               11.2s
 ⠇ llm                                 Configuring                                          8.8s
 ✔ Network memory-state_default        Created                                              0.0s
 ✔ Volume memory-state_agent-state     Created                                              0.0s
 ✔ Container memory-state-agent-memory-1 Healthy                                            5.8s
 ✔ Container memory-state-task-agent-1 Created
```

### Verify memory persistence:


```
# List all memory keys
docker compose exec agent-memory redis-cli KEYS "agent:*"
```

## Result:


```
1) "agent:task-processor:actions:task-003"
2) "agent:task-processor:actions:task-002"
3) "agent:task-processor:actions:task-004"
4) "agent:task-processor:actions:task-001"
```

### You can also view the specific task history:

```
# View specific task history
docker compose exec agent-memory redis-cli LRANGE agent:task-processor:actions:task-001 0 -1
```

### Result:

```
"{\"action\": \"Identify the source of customer feedback data.\", \"result\": \"Successfully completed: Identify the source of customer feedback data.\", \"success\": true, \"timestamp\": \"2025-12-27T14:13:42.205306\"}"
```

