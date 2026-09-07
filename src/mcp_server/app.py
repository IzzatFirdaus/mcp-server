"""FastMCP composition root.

Importing each `tools/*` module triggers `@mcp.tool()` registration as a
side effect. Keep imports explicit; do not use wildcard imports.
"""

from .core.config import SERVER_NAME
from .core.mcp_instance import mcp
from .tools import finance, system


def run() -> None:
    """Start the MCP server on stdio."""
    mcp.run()


__all__ = ["mcp", "run", "SERVER_NAME"]