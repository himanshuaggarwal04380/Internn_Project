import asyncio
from fastmcp import Client

# Point the client at your server file — FastMCP infers stdio transport automatically
client = Client("server.py")

async def main():
    async with client:
        # ask the server for all the tools it have
        tools = await client.list_tools() # it ruturns add
        print("Discovered tools:")
        for t in tools:
            print(f" {t.name}: {t.description}")

        # Execution : call the tool
        result = await client.call_tool("add", {"a": 2, "b": 3})
        print("Tool result:", result.data)
        
        #list all resource
        resources = await client.list_resources()

        for r in resources:
            print(r.name)
            print(r.uri)
            print(r.description)
        
        resource = await client.read_resource("greeting://message")

        print(resource[0].text)
        

if __name__ == "__main__":
    asyncio.run(main())