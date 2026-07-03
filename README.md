# Week 1: MCP Orientation & Environment Setup

A local agent pipeline built with the Model Context Protocol (MCP) — a tool-capable LLM (Llama 3.1 via Ollama) discovers and executes a tool exposed by a custom MCP server, over stdio transport.

**Deliverable:** Confirm discovery and tool execution works end-to-end. ✅ Achieved — verified via MCP Inspector, a custom Python client, a live LLM agent loop, and Claude Desktop.

## Architecture

```
User prompt → Llama 3.1 (Ollama) → decides to call a tool
                                          ↓
                        MCP Client (Python / Claude Desktop)
                                          ↓  stdio
                            MCP Server (FastMCP, server.py)
                                          ↓
                                  add(a, b) → result
```

## Tech Stack

| Component | Tool |
|---|---|
| Language / env | Python 3.13, [uv](https://docs.astral.sh/uv/) |
| MCP framework | [FastMCP](https://gofastmcp.com) (`pip install fastmcp`) |
| Local LLM | [Ollama](https://ollama.com) running `llama3.1` (8B, tool-calling capable) |
| IDE | VS Code + Python extension |
| MCP debugging | [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) |
| MCP client (host) | Custom Python script + Claude Desktop |

## Project Structure

```
Week1/
├── .venv/              # uv-managed virtual environment
├── pyproject.toml
├── server.py           # FastMCP server — exposes the `add` tool over stdio
├── client.py            # Custom MCP client — discovery + execution proof
├── llm_agent.py          # Full loop: Llama 3.1 decides + calls the tool via MCP
└── README.md
```

## Setup

```powershell
# 1. Toolchain
uv init
uv add fastmcp ollama

# 2. Local LLM
ollama pull llama3.1
ollama list          # confirm it's installed

# 3. Run the server (sanity check only — client scripts spawn it automatically)
uv run server.py
```

## `server.py` — the MCP server

```python
from fastmcp import FastMCP

mcp = FastMCP("HelloWorldServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    mcp.run()  # stdio transport
```

`@mcp.tool` registers the function for discovery. The docstring becomes the tool's description (what the LLM reads to decide when to use it). Type hints auto-generate the JSON Schema — no manual schema writing.

## Running & Verifying

### Option A — MCP Inspector (visual)
```powershell
npx @modelcontextprotocol/inspector uv run server.py
```
Connect → **Tools** tab lists `add` (discovery) → run with `a=2, b=3` → returns `5` (execution).

### Option B — Custom Python client (programmatic)
```powershell
uv run client.py
```
```
Discovered tools:
  - add: Add two numbers together.
Tool result: data=5, is_error=False
```

### Option C — Full LLM agent loop
```powershell
uv run llm_agent.py
```
```
Tools available to the LLM: ['add']
LLM wants to call: add({'a': 12, 'b': 7})
MCP server returned: 19
Final answer: The answer to '12 + 7' is 19.
```
Llama 3.1 reads the tool schema, decides on its own to call `add`, and the result is routed through MCP — nothing hardcoded.

### Option D — Claude Desktop
Add to `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "hello-world": {
      "command": "C:\\path\\to\\Week1\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\Week1\\server.py"]
    }
  }
}
```
Fully quit and relaunch Claude Desktop, then check **"+" → Connectors** for `hello-world` and the `add` tool.

> ⚠️ Point `command` directly at the venv's `python.exe` and keep each argument as its own array entry — `uv run` / `uvx` inside this config causes build and argument-parsing errors.

## Core MCP Concepts

| Concept | Description |
|---|---|
| **Tools** | Functions the LLM can call to *do* something (like a POST endpoint) |
| **Resources** | Data the client can read into context (like a GET endpoint) |
| **Prompts** | Reusable, parameterized prompt templates the server offers |
| **Transport** | Wire protocol — `stdio` (local, used here) or HTTP (remote) |

Everything runs on JSON-RPC 2.0. A client always **discovers** (`list_tools`) before it **executes** (`call_tool`) — that pattern is the core of this deliverable.

## Deliverables Checklist

- [x] Read MCP docs — tools, resources, prompts, transport
- [x] Toolchain set up — Python, uv, VS Code, Git
- [x] Local LLM running — Ollama + Llama 3.1, tool-calling verified
- [x] MCP client set up — custom Python client + MCP Inspector + Claude Desktop
- [x] Hello-world server built — FastMCP, one tool, stdio transport
- [x] Client connects to server
- [x] Discovery confirmed end-to-end
- [x] Execution confirmed end-to-end
- [x] Bonus: full LLM → MCP agent loop working live

## Next Steps (Week 2)

- Add more tools and multi-tool servers
- Expose resources, not just callable tools
- Try HTTP transport for a remotely-runnable server
- Push to GitHub for team review