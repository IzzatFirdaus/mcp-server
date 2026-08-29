from fastmcp import FastMCP

# Initialize MCP Server
mcp = FastMCP("Portfolio Tools Server")

# Tool 1: Mathematical helper tool for AI client
@mcp.tool()
def calculate_growth(initial_value: float, growth_rate: float, years: int) -> dict:
    """Calculates compound growth over a given number of years."""
    final_value = initial_value * ((1 + growth_rate / 100) ** years)
    return {
        "initial": initial_value,
        "years": years,
        "projected_value": round(final_value, 2)
    }

# Tool 2: System info tool
@mcp.tool()
def get_system_status() -> dict:
    """Returns the operational status of the portfolio MCP backend."""
    return {
        "status": "online",
        "protocol": "MCP v1.0",
        "active_tools": ["calculate_growth", "get_system_status"]
    }

if __name__ == "__main__":
    mcp.run()