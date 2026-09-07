# CLAUDE.md — CLI Quickstart for LLM Tools

> Direct commands an LLM-driven CLI (Claude Code, Codex CLI, etc.) can run against this repo.

---

## 1. Path Aliases

| Alias | Real path |
| --- | --- |
| `@root` | repository root (`d:/Projects/mcp-server` on this machine) |
| `@entry` | `@root/server.py` |
| `@src` | `@root/src/mcp_server` |
| `@tools` | `@root/src/mcp_server/tools` |
| `@core` | `@root/src/mcp_server/core` |
| `@schemas` | `@root/src/mcp_server/schemas` |
| `@venv-py` | `@root/venv/Scripts/python.exe` (Windows) |

> On macOS/Linux, `@venv-py` is `@root/venv/bin/python`.

---

## 2. Environment Setup

### Windows (PowerShell)
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux (bash)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 3. Build / Install

There is no build step. `pip install -r requirements.txt` *is* the install.

```powershell
pip install -r requirements.txt
```

To add a dependency:
```powershell
pip install <pkg>
# then pin it:
pip freeze | Select-String -Pattern "^<pkg>==" >> requirements.txt
```

---

## 4. Run the Server

stdio transport (for MCP clients):
```powershell
.\venv\Scripts\python.exe server.py
```

---

## 5. Test / Inspect

No automated test suite in v1. Use the MCP Inspector:

```powershell
npx @modelcontextprotocol/inspector .\venv\Scripts\python.exe server.py
```
Then open <http://localhost:5173>.

### Quick CLI sanity check (no inspector)
```powershell
.\venv\Scripts\python.exe -c "from src.mcp_server.app import mcp; print(mcp.list_tools())"
```

---

## 6. Lint / Format

No linter is configured in v1. If you need one:
```powershell
pip install ruff
ruff check src
ruff format src
```

---

## 7. Repository Map (files you'd touch)

```
README.md                    # user-facing quickstart
PRD.md                       # product scope
ARCHITECTURE.md              # full technical spec
ARCHITECTURE-ESSENTIALS.md   # load this first
AGENTS.md                    # rules for AI agents
CLAUDE.md                    # this file
requirements.txt             # pinned deps
server.py                    # entrypoint shim (DO NOT remove)
src/
  mcp_server/
    app.py                   # FastMCP factory + run()
    tools/
      finance.py             # calculate_growth
      system.py              # get_system_status
    core/
      config.py              # constants
      registry.py            # tool enumeration (planned v1.1)
    schemas/
      responses.py           # TypedDicts (planned v1.1)
```

---

## 8. Common Tasks

### Add a new tool
1. Edit `src/mcp_server/tools/<domain>.py` — add `@mcp.tool()` function.
2. Edit `src/mcp_server/app.py` — `from .tools import <domain>`.
3. Edit `src/mcp_server/tools/system.py` — add the name to `active_tools`.
4. Edit `README.md` — append to the tool list.

### Update a pinned dependency
```powershell
pip install --upgrade <pkg>==<new-version>
pip freeze | Select-String -Pattern "^(fastmcp|mcp|pydantic)==" 
```
Then hand-edit `requirements.txt` to reflect the chosen version.

### Regenerate `requirements.txt` from scratch
```powershell
.\venv\Scripts\python.exe -m pip freeze > requirements.txt
```
Review the diff — drop dev-only entries (pytest, ruff, etc.) unless they belong.

---

## 9. Troubleshooting

| Symptom | Fix |
| --- | --- |
| `ModuleNotFoundError: fastmcp` | `pip install -r requirements.txt` |
| Inspector can't reach server | Confirm full path to `venv\Scripts\python.exe server.py` |
| `python` not found | Use `py` (Windows) or `python3` (macOS/Linux) |
| Tool not visible to client | Confirm the tool module is imported in `app.py` |
| Stale cached bytecode | Delete `__pycache__/` and restart |

---

## 10. Don't

- Don't run the server as a background daemon in dev — Inspector spawns it.
- Don't commit `venv/`, `__pycache__/`, `.env` (already git-ignored).
- Don't run `pip freeze > requirements.txt` blindly — it captures the whole venv.