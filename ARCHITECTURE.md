# ARCHITECTURE.md — MCP Portfolio Tools Server

> Technical source of truth. Translation of `PRD.md` into implementation-grade specs.
> Version: 1.0 · Date: 2026-09-07

---

## 1. Tech Stack

| Layer | Choice | Rationale |
| --- | --- | --- |
| Language | Python 3.10+ | Matches FastMCP minimum; broad AI client support. |
| MCP framework | `fastmcp==3.4.7` | High-level, decorator-based tool registration. |
| Underlying MCP | `mcp==1.29.1` | Protocol primitives. |
| Schema / validation | `pydantic==2.13.5` (via FastMCP) | Type-annotated tool args = auto JSON-schema. |
| ASGI runtime | `uvicorn==0.52.4` + `starlette==1.6.0` | Implicit; pulled by FastMCP if HTTP transport used. |
| Packaging | `requirements.txt` (pinned) | Reproducible venv. |
| Inspector | `@modelcontextprotocol/inspector` (npm) | Local UI testing, no test code needed. |

No DB, no cache, no broker, no auth — by design (see PRD §9).

---

## 2. Runtime Topology

```
┌────────────────────────┐         stdio (JSON-RPC)         ┌────────────────────────┐
│  MCP Client (Claude /  │  ─────────────────────────────►  │   FastMCP Server       │
│  Cursor / Inspector)   │  ◄─────────────────────────────  │   (server.py)          │
└────────────────────────┘                                  └────────────┬───────────┘
                                                                          │
                                              in-process @mcp.tool() registry
                                                                          │
                                                              ┌───────────▼────────────┐
                                                              │  calculate_growth      │
                                                              │  get_system_status     │
                                                              │  (future tools…)       │
                                                              └────────────────────────┘
```

- **Transport:** stdio (default `mcp.run()`).
- **Process model:** single-process, synchronous handlers.
- **State:** none. Tools are pure functions or constants.

---

## 3. Module & File Layout (target)

```
mcp-server/
├── README.md                # human-facing quickstart
├── PRD.md                   # product requirements
├── ARCHITECTURE.md          # this file
├── ARCHITECTURE-ESSENTIALS.md
├── AGENTS.md                # AI-agent operational rules
├── CLAUDE.md                # CLI quickstart for LLM tools
├── requirements.txt
├── .gitignore
├── server.py                # entrypoint (composition root)
└── src/
    └── mcp_server/
        ├── __init__.py
        ├── app.py           # FastMCP() factory + run()
        ├── tools/
        │   ├── __init__.py
        │   ├── finance.py   # calculate_growth
        │   └── system.py    # get_system_status
        ├── core/
        │   ├── __init__.py
        │   ├── config.py    # env / constants
        │   └── registry.py  # active-tool enumeration helper
        └── schemas/
            ├── __init__.py
            └── responses.py # TypedDicts / Pydantic models
```

The flat `server.py` currently used becomes a thin shim that re-exports `app.mcp` so existing workflows (`.\venv\Scripts\python.exe server.py`) keep working.

---

## 4. Data Models

### 4.1 Tool argument schemas (inferred from type hints)

```python
# tools/finance.py
initial_value: float  # validated: must be numeric; semantic check (>=0) deferred
growth_rate:   float  # any real number (percent, not decimal)
years:         int    # >=0
```

### 4.2 Tool response schemas

```python
# schemas/responses.py
from typing import TypedDict

class GrowthResult(TypedDict):
    initial: float
    years: int
    projected_value: float  # rounded to 2 decimals

class SystemStatus(TypedDict):
    status: str           # "online"
    protocol: str         # "MCP v1.0"
    active_tools: list[str]
```

> Note: FastMCP converts `TypedDict` and Pydantic models into JSON-schema for the wire format automatically.

### 4.3 Configuration constants

```python
# core/config.py
SERVER_NAME   = "Portfolio Tools Server"
PROTOCOL_VER  = "MCP v1.0"
STATUS_ONLINE = "online"
ROUND_DIGITS  = 2
```

---

## 5. API Surface (MCP Tools)

### 5.1 `calculate_growth`
| Field | Value |
| --- | --- |
| **Signature** | `calculate_growth(initial_value: float, growth_rate: float, years: int) -> dict` |
| **Decorator** | `@mcp.tool()` |
| **Docstring** | "Calculates compound growth over a given number of years." |
| **Algorithm** | `final = initial × (1 + rate/100)^years`; `round(final, 2)` |
| **Returns** | `{ "initial": float, "years": int, "projected_value": float }` |
| **Failure modes** | Overflow → `inf` (acceptable v1); negative `initial_value` allowed but undefined financially — accepted at boundary, documented in PRD §7. |

### 5.2 `get_system_status`
| Field | Value |
| --- | --- |
| **Signature** | `get_system_status() -> dict` |
| **Decorator** | `@mcp.tool()` |
| **Returns** | `{ "status": "online", "protocol": "MCP v1.0", "active_tools": [ ... ] }` |
| **Source of truth for `active_tools`** | Enumerate functions in `tools/` whose `__mcp_tool__` attribute is set, **or** a static registry populated at startup. v1 uses a hardcoded list; v1.1 will switch to dynamic enumeration via `registry.py`. |

### 5.3 Future tool template
```python
@mcp.tool()
def tool_name(arg_a: SomeType, arg_b: AnotherType) -> SomeReturn:
    """One-line description shown to clients."""
    ...
```

---

## 6. Composition Root

`server.py`:
```python
from src.mcp_server.app import mcp, run

if __name__ == "__main__":
    run()
```

`src/mcp_server/app.py`:
```python
from fastmcp import FastMCP
from .core.config import SERVER_NAME
from .tools import finance, system  # registers @mcp.tool functions

mcp = FastMCP(SERVER_NAME)

def run() -> None:
    mcp.run()
```

Importing each `tools/*` module triggers decorator registration as a side effect — explicit and idiomatic.

---

## 7. Environment Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `MCP_TRANSPORT` | `stdio` | Future: switch to `http` (FastMCP supports it). |
| `MCP_HOST` | `127.0.0.1` | Future HTTP transport. |
| `MCP_PORT` | `8000` | Future HTTP transport. |
| `PYTHONHASHSEED` | unset | Determinism for tests (set in test harness). |

Loaded via `python-dotenv` if a `.env` is present; ignored otherwise.

---

## 8. Third-Party Integrations

| Integration | Purpose | Notes |
| --- | --- | --- |
| `@modelcontextprotocol/inspector` (npm) | Local UI testing | Spawned via `npx`, no project dep. |
| Claude Desktop (out-of-scope install) | Consumer client | Configured by user, not by this repo. |

No SaaS, no telemetry, no auth provider.

---

## 9. Build, Test, Run

```powershell
# Build / install
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run (stdio, for clients)
.\venv\Scripts\python.exe server.py

# Inspect (local UI)
npx @modelcontextprotocol/inspector .\venv\Scripts\python.exe server.py
```

### Test strategy (v1)
- **Manual:** MCP Inspector covers happy-path and input-validation cases.
- **Unit (future):** `pytest` against pure functions in `tools/` (no MCP runtime needed).
- **No contract test in v1:** tool schemas are pinned by Python type hints; FastMCP surfaces them.

---

## 10. Error & Boundary Semantics

| Layer | Behavior |
| --- | --- |
| **Schema violation** (e.g. `years="abc"`) | FastMCP rejects before invoking tool; returns MCP `InvalidRequest`. |
| **Math overflow** | Python `float` overflow → `inf` returned as-is. |
| **Tool raises** | Bubbles to MCP as `InternalError`; v1 keeps simple. |
| **Process death** | Client (e.g. Claude Desktop) restarts server automatically. |

---

## 11. Versioning & Compatibility

- Tools addressed by **name** in MCP wire format — renaming a function is a breaking change.
- Tool **arguments** are matched by name and validated by JSON-schema; adding optional args is backward compatible, removing/renaming is not.
- `server.py` shim guarantees the historical entrypoint keeps working across refactors.

---

## 12. Open Technical Questions

1. Should `calculate_growth` use `Decimal` for precision? — **No** for v1 (matches PRD: 2-decimal rounding).
2. Should `get_system_status.active_tools` be auto-derived? — **Yes**, tracked as v1.1 in `core/registry.py`.
3. HTTP transport behind feature flag? — **Deferred** to v1.2.