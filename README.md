# MCP Server

A lightweight Model Context Protocol (MCP) server built with Python and FastMCP. This project exposes custom structured tools designed for native integration with AI assistants (such as Claude Desktop, Cursor, or local LLM clients).

## Features
- **FastMCP SDK:** High-level Python framework for building MCP servers.
- **Custom Tools:** Exposes mathematical calculation tools and real-time backend status checks.
- **Strict Type Safety:** Type-annotated arguments enforcing schema validation.
- **Local Testing:** Compatible with the interactive @modelcontextprotocol/inspector.

## Available Tools

- \calculate_growth(initial_value, growth_rate, years)\: Calculates compound financial growth over a specified period.
- \get_system_status()\: Returns the operational status and list of active tools.

## Setup & Running

### 1. Clone & Setup Environment
```powershell
git clone https://github.com/IzzatFirdaus/mcp-server.git
cd mcp-server

# Create virtual environment
py -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Inspector for Testing
To test the tools locally using the interactive web Inspector, run:

```powershell
npx @modelcontextprotocol/inspector .\venv\Scripts\python.exe server.py
```

Open \http://localhost:5173\ in your browser to interact with the endpoints.
