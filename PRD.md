# PRD — MCP Portfolio Tools Server

> Product Requirements Document
> Owner: Engineering Lead · Status: Draft v1.0 · Last Updated: 2026-09-07

---

## 1. Product Overview

The **MCP Portfolio Tools Server** is a lightweight backend that exposes a small, well-curated set of financial and operational tools to AI assistants (Claude Desktop, Cursor, and other MCP-compatible clients) via the **Model Context Protocol (MCP)**.

It is designed to be:

- **Easy to embed** — zero external services, runs locally from a Python venv.
- **Strictly typed** — every tool argument is validated by Pydantic schemas.
- **Inspectable** — local end-to-end testable through the official MCP Inspector.
- **Deterministic** — tool results are reproducible, with no hidden side effects.

## 2. Target Audience

| Audience | Why they use this server |
| --- | --- |
| **AI assistant power users** | They want their assistant to perform structured math/status queries without granting it full filesystem or shell access. |
| **Independent developers** | They want a reference implementation of a FastMCP server they can clone and extend. |
| **Financial analysts (light use)** | Quick compound-growth projections during conversational sessions. |
| **Internal tooling teams** | A baseline server template to fork into domain-specific tool collections. |

## 3. User Personas

### Persona A — "Maya, the AI power user"
- Uses Claude Desktop as a daily research assistant.
- Wants predictable, schema-validated financial math she can quote in conversations.
- Hates hallucinated numbers; values reproducibility.

### Persona B — "Daniel, the indie dev"
- Building personal MCP toolkits.
- Needs a clean, minimal server he can read in 5 minutes and extend in 30.

### Persona C — "Priya, the analyst"
- Wants fast ballpark compound-growth estimates during meetings.
- Will not install a heavy backend; expects a one-command spin-up.

## 4. Functional Requirements

### FR-1 — Compound Growth Calculator
- **Tool:** `calculate_growth(initial_value, growth_rate, years)`
- **Behavior:** Computes compound growth using the formula `final = initial × (1 + rate/100)^years`.
- **Inputs:** `initial_value: float ≥ 0`, `growth_rate: float` (any real), `years: int ≥ 0`.
- **Output:** `{ initial, years, projected_value }` with `projected_value` rounded to 2 decimals.
- **Errors:** Returns an MCP validation error if inputs violate schema.

### FR-2 — System Status
- **Tool:** `get_system_status()`
- **Behavior:** Reports operational status and the registry of currently active tools.
- **Output:** `{ status: "online", protocol: "MCP v1.0", active_tools: [...] }`.

### FR-3 — MCP Transport
- Server supports stdio transport out of the box (default `mcp.run()`).
- Compatible with the official `@modelcontextprotocol/inspector` for local testing.

### FR-4 — Tool Discoverability
- All tools must expose Python docstrings; they are surfaced as tool descriptions to clients.

## 5. Non-Functional Requirements

| Category | Requirement |
| --- | --- |
| **Performance** | Tool calls return in < 50 ms on a modern laptop. No I/O blocking. |
| **Reliability** | Deterministic outputs for identical inputs (pure functions). |
| **Security** | No filesystem or network egress from tools. No secret material loaded. |
| **Portability** | Runs on Windows / macOS / Linux Python 3.10+ environments. |
| **Maintainability** | New tools can be added by dropping a single annotated function. |
| **Observability** | Tool calls surface via the MCP protocol; no separate logging layer required for v1. |

## 6. Key User Flows

1. **First-time setup**
   User clones repo → creates venv → installs requirements → runs inspector → calls tools.
2. **Daily use (Claude Desktop integration)**
   User adds server to Claude's MCP config → assistant auto-discovers tools → invokes them via natural language.
3. **Local debugging**
   User runs the inspector → selects a tool → enters arguments → reviews JSON response.
4. **Extension**
   User adds a new `@mcp.tool()` function → restarts server → tool appears in client UI automatically.

## 7. Edge-Case Behaviors

| Edge case | Expected behavior |
| --- | --- |
| `initial_value = 0` | Returns `projected_value = 0`. |
| `growth_rate = 0` | Returns `projected_value = initial_value`. |
| `growth_rate = -100` | Returns `projected_value = 0`. |
| `growth_rate < -100` | Pydantic allows but math produces positive value (documented quirk). |
| `years = 0` | Returns `projected_value = initial_value`. |
| Very large `years` (>200) | Math may overflow; v1 accepts and returns `inf` if applicable. |
| Non-numeric input | Rejected by MCP schema before reaching the function. |

## 8. Success Metrics

- **Adoption:** Repo cloned and inspected ≥ 50 times within first quarter.
- **Time-to-first-tool:** < 5 minutes from `git clone` to first successful tool call.
- **Tool-call success rate:** ≥ 99% in inspector sessions (excluding intentionally invalid inputs).
- **Extension friction:** Adding a new tool requires ≤ 1 file edit and 0 new dependencies.

## 9. Out of Scope (v1)

- Persistent storage / database.
- Authentication / multi-user.
- HTTP transport (only stdio in v1).
- Long-running tools, async streaming responses.
- Tool versioning, rate limiting.

## 10. Open Questions

- Should `growth_rate` be expressed as a decimal (0.07) or percent (7.0)? — **v1: percent, locked.**
- Do we want a third tool (`calculate_compound_interest_with_contributions`) in v1.1? — **deferred.**