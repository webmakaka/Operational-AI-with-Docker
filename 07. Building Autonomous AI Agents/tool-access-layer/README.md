## Tool Access Layer


```
docker compose up -build
```

## Result:

The gateway launches each MCP server as an isolated Docker container with security constraints. The --security-opt no-new-privileges flag prevents privilege escalation. 

```
- github-official: time=2025-12-27T13:37:26.229Z level=INFO msg="starting server" 
  version=v0.26.3
- github-official: GitHub MCP Server running on stdio
- github-official: time=2025-12-27T13:37:26.241Z level=INFO msg="session initialized"
  > github-official: (40 tools) (2 prompts) (5 resourceTemplates)
  
  > firecrawl: (6 tools)
  
> 46 tools listed in 6.29s
> Initialized in 16.93s
> Start stdio server
```

## Test the gateway with a simple tool call:


### List available tools

```
curl http://localhost:8811/tools
```

### Search GitHub repositories (read-only, safe to test)

```
curl -X POST http://localhost:8811/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "search_repositories",
    "arguments": {
      "query": "docker language:go stars:>1000"
    }
  }'
```
