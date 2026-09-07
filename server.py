"""Entrypoint shim.

Keeps the historical `python server.py` workflow alive while delegating
composition to `src/mcp_server/app.py`.
"""

from src.mcp_server.app import run

if __name__ == "__main__":
    run()