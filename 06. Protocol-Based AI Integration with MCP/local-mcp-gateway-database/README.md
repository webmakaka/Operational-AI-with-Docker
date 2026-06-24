# MCP Gateway SQLite Integration Example

This example demonstrates how to connect an AI application to a SQLite database through the Docker MCP Gateway using the streaming transport protocol.

## Overview

The example consists of three services:

- **gateway** — Docker MCP Gateway that exposes the SQLite MCP server to AI clients
- **client** — Python application that connects to the Gateway and performs database operations
- **db-init** — Initialises the SQLite database file before the gateway starts

## Prerequisites

- Docker Desktop 4.42.0 or later with MCP Toolkit enabled
- Docker Compose v2 or later

## Project structure

```
.
├── compose.yaml       # Docker Compose configuration
├── Dockerfile         # Python client image
├── main.py            # Python client that calls SQLite MCP tools
└── README.md          # This file
```

## Quick start

Start the stack:

```bash
docker compose up -d
```

Wait for the gateway to initialise the SQLite server (approximately 10 seconds), then view the client output:

```bash
sleep 10 && docker compose logs client
```

You should see:

```
client-1  | Table created
client-1  | Data inserted
client-1  | Query result:
client-1  | [{'id': 1, 'name': 'Widget', 'price': 9.99}, {'id': 2, 'name': 'Gadget', 'price': 24.99}, {'id': 3, 'name': 'Doohickey', 'price': 4.99}]
```

Stop the stack:

```bash
docker compose down
```

## How it works

The Python client connects to the Gateway's streaming endpoint at `http://gateway:8811/mcp` and uses three SQLite MCP tools:

- `create_table` — Creates a `products` table with `id`, `name`, and `price` columns
- `write_query` — Inserts three product records
- `read_query` — Retrieves all records and prints the results

The Gateway forwards each tool call to the SQLite MCP server container, which executes the operation against the SQLite database file and returns results. Your application never accesses the database directly — all interactions go through the Gateway.

## Available SQLite tools

The SQLite MCP server exposes six tools:

| Tool | Description |
|------|-------------|
| `create_table` | Create a new table in the SQLite database |
| `list_tables` | List all tables in the SQLite database |
| `describe_table` | Get the schema information for a specific table |
| `read_query` | Execute a SELECT query on the SQLite database |
| `write_query` | Execute an INSERT, UPDATE, or DELETE query on the SQLite database |
| `append_insight` | Add a business insight to the memo |

## Transport protocol

This example uses the **streaming** transport protocol, which is suitable for programmatic AI agent access. The Gateway exposes the endpoint at `http://gateway:8811/mcp`.

## Key files

### compose.yaml

```yaml
services:
  client:
    build: .
    environment:
      - MCP_HOST=http://gateway:8811/mcp
    depends_on:
      - gateway
    restart: on-failure

  gateway:
    image: docker/mcp-gateway
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command:
      - --transport=streaming
      - --servers=SQLite
      - --port=8811
      - --verbose=false

  db-init:
    image: mcp/sqlite@sha256:efbc05ccace18df122f26b674bd1730c76ece716551df2b3961d519909c34696
    volumes:
      - ./data:/mcp
    entrypoint: ["sh", "-c", "exit 0"]
```

### main.py

```python
import os
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    async with streamablehttp_client(os.getenv("MCP_HOST")) as (
        read_stream, write_stream, _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Create a table
            await session.call_tool("create_table", {
                "query": "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)"
            })
            print("Table created")

            # Insert data
            await session.call_tool("write_query", {
                "query": "INSERT INTO products (name, price) VALUES ('Widget', 9.99), ('Gadget', 24.99), ('Doohickey', 4.99)"
            })
            print("Data inserted")

            # Query the data
            result = await session.call_tool("read_query", {
                "query": "SELECT * FROM products"
            })
            print("Query result:")
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
```

### Dockerfile

```dockerfile
FROM python:3.13-alpine
RUN pip install mcp[cli]
WORKDIR /app
COPY main.py ./
CMD ["python", "main.py"]
```

## Notes

- The `restart: on-failure` policy on the client service handles the case where the client starts before the gateway is fully ready. Docker automatically retries until the gateway is available.
- The SQLite database file is stored in a Docker volume (`mcp-sqlite`) managed by the Gateway.
- No credentials or secrets are required — SQLite is a file-based database with no authentication.
- This example has been verified on Apple Silicon (ARM64) and AMD64.
