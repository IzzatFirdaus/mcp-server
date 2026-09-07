"""Tool registry — auto-enumerates `@mcp.tool()` functions.

Stubbed for v1.1. Replace the hardcoded list in `tools/system.py` with a
call to ``list_active_tools()`` once implemented.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp import FastMCP


def list_active_tools(mcp_instance: "FastMCP") -> list[str]:
    """Return the names of all registered tools on ``mcp_instance``."""
    # TODO(v1.1): implement using FastMCP's introspection API.
    raise NotImplementedError("Tool registry is planned for v1.1.")


__all__ = ["list_active_tools"]