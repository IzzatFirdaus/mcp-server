"""System / liveness tools."""

from src.mcp_server.core.config import PROTOCOL_VER, STATUS_ONLINE
from src.mcp_server.core.mcp_instance import mcp

_ACTIVE_TOOLS: list[str] = [
    "calculate_growth",
    "get_system_status",
]


@mcp.tool()
def get_system_status() -> dict:
    """Returns the operational status of the portfolio MCP backend.

    Returns:
        Dict containing ``status``, ``protocol``, and ``active_tools``.
    """
    # TODO(v1.1): replace with auto-derived list from `core.registry`.
    return {
        "status": STATUS_ONLINE,
        "protocol": PROTOCOL_VER,
        "active_tools": list(_ACTIVE_TOOLS),
    }


__all__ = ["get_system_status"]