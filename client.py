import asyncio
from fastmcp import Client

# Point the client at your server file — FastMCP infers stdio transport automatically
client = Client("server.py")

async def main():
    async with client:
        # 1. DISCOVERY: ask the server what tools it has
        tools = await client.list_tools()
        print("Discovered tools:")
        for t in tools:
            print(f"  - {t.name}: {t.description}")

        # 2. EXECUTION: call the tool
        result = await client.call_tool("add", {"a": 2, "b": 3})
        print("Tool result:", result.data)

if __name__ == "__main__":
    asyncio.run(main())