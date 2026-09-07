"""Shared FastMCP instance.

Lives in `core/` to break the import cycle: both `app.py` and every
`tools/*` module import this ``mcp`` symbol without depending on `app.py`.
"""

from fastmcp import FastMCP

from .config import SERVER_NAME

mcp = FastMCP(SERVER_NAME)

__all__ = ["mcp"]