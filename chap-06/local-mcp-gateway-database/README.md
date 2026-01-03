# Run a PostgreSQL database and connect it to the MCP Gateway

This example shows how to query a PostgreSQL database through a PostgreSQL MCP Server,
through the MCP Gateway, from a python client:

+ Configure MCP Gateway with Compose Secrets.
+ Use Health Check to wait for PostgreSQL before starting the MCP Gateway.

## How to run

```console
docker compose up --build
```

## Test the connection using curl

```console
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool": "query", "arguments": {"sql": "SELECT datname FROM pg_database;"}}'
```

