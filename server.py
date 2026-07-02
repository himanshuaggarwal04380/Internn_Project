from fastmcp import FastMCP

# Create the server — this name shows up when a client connects
mcp = FastMCP(name = "HelloWorldServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport