import asyncio
from ollama import chat
from fastmcp import Client

mcp_client = Client("server.py")

async def main():
    async with mcp_client:
        # 1. DISCOVERY: get tools from the MCP server
        mcp_tools = await mcp_client.list_tools()

        # 2. Convert MCP tool definitions into the format Ollama expects
        ollama_tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                },
            }
            for t in mcp_tools
        ]

        print("Tools available to the LLM:", [t.name for t in mcp_tools])

        # 3. Give Llama a natural-language prompt
        user_prompt = "What is 12 plus 7?"
        messages = [{"role": "user", "content": user_prompt}]

        response = chat(
            model="llama3.1",
            messages=messages,
            tools=ollama_tools,
        )

        # 4. Check if the model decided to call a tool
        if response.message.tool_calls:
            for call in response.message.tool_calls:
                print(f"LLM wants to call: {call.function.name}({call.function.arguments})")

                # 5. EXECUTION: run the actual tool via the MCP server
                result = await mcp_client.call_tool(
                    call.function.name, call.function.arguments
                )
                print("MCP server returned:", result.data)

                # 6. (Optional) feed the result back so the LLM can phrase a final answer
                messages.append(response.message)
                messages.append(
                    {
                        "role": "tool",
                        "tool_name": call.function.name,
                        "content": str(result.data),
                    }
                )
                final = chat(model="llama3.1", messages=messages, tools=ollama_tools)
                print("Final answer:", final.message.content)
        else:
            print("LLM answered directly without a tool call:", response.message.content)

if __name__ == "__main__":
    asyncio.run(main())