# ARCHITECTURE-ESSENTIALS.md

> Lightweight, fast-loading summary of [ARCHITECTURE.md](ARCHITECTURE.md).
> Read this first. Drop into context when picking up a new task.

---

## Non-Negotiable Rules

1. **Tool = pure or constant.** No I/O, no network, no filesystem writes from inside `@mcp.tool()` functions.
2. **All tools are type-annotated.** Python type hints drive the wire-format JSON-schema; do not hand-roll schemas.
3. **One entrypoint.** `server.py` re-exports from `src/mcp_server/app.py`. Never instantiate `FastMCP(...)` outside `app.py`.
4. **Stdio is the only supported transport in v1.** No HTTP server, no auth, no DB.
5. **Pinned dependencies.** Modify `requirements.txt` only with intentional, version-justified changes.
6. **Deterministic outputs.** Same inputs → identical outputs. No `datetime.now()`, no `uuid`, no RNG inside tools.
7. **Tools are addressed by name.** Renaming a tool = breaking change.

---

## Core Data Structures

```python
# Tool argument shape
calculate_growth(initial_value: float, growth_rate: float, years: int) -> dict
get_system_status() -> dict

# Response TypedDicts (schemas/responses.py)
GrowthResult  = TypedDict("GrowthResult", {"initial": float, "years": int, "projected_value": float})
SystemStatus  = TypedDict("SystemStatus", {"status": str, "protocol": str, "active_tools": list[str]})
```

Constants live in `core/config.py`: `SERVER_NAME`, `PROTOCOL_VER`, `STATUS_ONLINE`, `ROUND_DIGITS`.

---

## Primary Routes / Tools

| Tool | Purpose | File |
| --- | --- | --- |
| `calculate_growth` | Compound-growth math | `src/mcp_server/tools/finance.py` |
| `get_system_status` | Liveness + tool registry | `src/mcp_server/tools/system.py` |

To add a tool: create `src/mcp_server/tools/<domain>.py`, decorate a function with `@mcp.tool()`, and import it from `app.py`.

---

## Composition

```
server.py  →  src/mcp_server/app.py  →  src/mcp_server/tools/{finance,system}.py
                          └─→  src/mcp_server/core/{config,registry}.py
                          └─→  src/mcp_server/schemas/responses.py
```

---

## Quick Commands

```powershell
# Run
.\venv\Scripts\python.exe server.py

# Inspect
npx @modelcontextprotocol/inspector .\venv\Scripts\python.exe server.py
```

---

## Stress-Test Self-Audit

### What will break first under load or edge cases?
- **`calculate_growth` math overflow** with `years` > ~1023 and a positive `growth_rate` — Python `float` overflows to `inf`. Acceptable v1 (documented in PRD §7), but a `Decimal`-based path should be considered if we ever loosen input ranges.
- **Dynamic tool registry** in `get_system_status.active_tools` is still a **hardcoded list** — if a new tool is added but the list isn't updated, status will lie. Single point of human error.

### What failure modes or edge cases are currently unaccounted for?
- **NaN / Infinity inputs** are not rejected by Pydantic at the tool boundary. Passing `float('nan')` will produce `nan` outputs and corrupt client UX. *Fix:* add a pre-check in `finance.py` or a `BeforeValidator`.
- **Negative `years`** — schema allows `int` but PRD §4 FR-1 says `≥ 0`. Pydantic `Field(ge=0)` is not currently applied.
- **Negative `initial_value`** — same issue: schema accepts what PRD says it shouldn't.
- **Server crashes silently** in stdio mode — there is no health endpoint or log sink to detect hangs.
- **Concurrent calls** — not exercised; FastMCP's stdio runner is synchronous, so this is fine but undocumented as a contract.

### Which parts of this design are over-engineered and can be simplified?
- **`schemas/responses.py` with `TypedDict`** is currently unused — FastMCP infers return types from type hints on the function itself. Can drop the file until v1.1 if we want to tighten the design.
- **`core/registry.py`** is planned but the v1 hardcoded list inside `get_system_status` works fine for 2 tools. Defer the registry until tool count > 3.
- **HTTP transport scaffolding** in env-config (§7 of ARCHITECTURE.md) is speculative — drop until v1.2 demand is real.

### Net call
The current scope is appropriately minimal. The audit reveals **three concrete gaps to close before v1.1**: (1) Pydantic bounds on `calculate_growth` inputs, (2) NaN guard, (3) auto-derived `active_tools` registry.