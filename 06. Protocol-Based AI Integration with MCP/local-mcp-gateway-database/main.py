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
