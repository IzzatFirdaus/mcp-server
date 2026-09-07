# AGENTS.md — Operational Rules for AI Agents

> Applies to any AI coding agent (Copilot, Claude Code, Cursor, etc.) modifying this repository.
> When in doubt, prefer the stricter rule.

---

## 1. Scope of Authority

- You **may** edit `src/`, `server.py`, tests, and project-internal docs (`PRD.md`, `ARCHITECTURE*.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`).
- You **may** add new dependencies by appending to `requirements.txt`, **but** you must justify the addition in the same commit/PR description.
- You **may not** modify `.gitignore`, license files, CI config, or anything in `venv/` / `.git/`.

## 2. File Modification Safety

| File / dir | Allowed | Notes |
| --- | --- | --- |
| `server.py` | Editable | Treat as the public entrypoint shim; keep import surface stable. |
| `src/mcp_server/**` | Editable | Main work area. |
| `requirements.txt` | Editable | Pin exact versions; no `>=`. |
| `PRD.md` | Editable for product scope only | Do **not** add technical detail. |
| `ARCHITECTURE.md` / `ARCHITECTURE-ESSENTIALS.md` | Editable | Keep in sync with each other. |
| `README.md` | Editable | User-facing; keep concise. |
| `.env`, `venv/`, `__pycache__/` | **Never** | Ignored. |
| `.git/` | **Never** | Read-only. |

Rule of thumb: **don't touch files you don't have a concrete reason to touch.**

## 3. Coding Standards

- **Python ≥ 3.10** syntax. No walrus-heavy tricks, no match/case if a plain `if` is clearer.
- **Type hints on every public function** — FastMCP relies on them.
- **Docstrings on every `@mcp.tool()`** — the docstring becomes the tool description surfaced to clients.
- **Pure functions** for tools. No side effects, no global mutation, no logging inside tool bodies.
- **Imports**: stdlib → third-party → local; one blank line between groups.
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- **No emojis** in code, docstrings, or commit messages.
- **No "AI-slop" comments** (e.g. "this function calculates…" when the name says so). Keep comments for non-obvious *why*.

## 4. Design Patterns

| Pattern | Use for |
| --- | --- |
| Decorator registration (`@mcp.tool()`) | Exposing tools. |
| Pure functions | Tool implementations. |
| TypedDict / Pydantic models | Structured responses. |
| Composition root (`app.py`) | Wiring tools + factory. |
| Constants in `core/config.py` | Strings, magic numbers, version pins. |

**Avoid**: dependency injection frameworks, abstract base classes, repository patterns, premature abstractions. This codebase is intentionally flat.

## 5. Feature Implementation Workflow (Step-by-Step)

When asked to add a tool, follow this order:

1. **Read** `ARCHITECTURE-ESSENTIALS.md` (≤ 1 minute).
2. **Confirm** the tool fits PRD §9 scope. If not, surface a question to the user.
3. **Create / extend** `src/mcp_server/tools/<domain>.py` with a single `@mcp.tool()` function:
   - Type-annotated arguments.
   - One-line docstring.
   - Pure body (or read-only access to `core/config.py`).
4. **Register** the module by importing it from `src/mcp_server/app.py`.
5. **Update** `get_system_status.active_tools` **or** migrate to `core/registry.py` if it now exceeds 3 tools.
6. **Sanity-check**:
   - `python -c "from src.mcp_server.app import mcp"` succeeds.
   - Tool appears in `mcp.list_tools()` if exposed programmatically.
7. **Smoke-test** with `npx @modelcontextprotocol/inspector .\venv\Scripts\python.exe server.py` when possible.
8. **Update docs**: `README.md` tool list, `ARCHITECTURE.md` §5, and `PRD.md` if scope changes.

## 6. Refactor Workflow

1. State the *why* in one sentence before touching code.
2. Make the smallest change that preserves public behavior.
3. Run a manual tool call (via Inspector) before considering the refactor done.
4. If `ARCHITECTURE-ESSENTIALS.md` rules shift, update it in the same commit.

## 7. Tests

- v1 has **no automated tests**. Do not invent a heavy test framework.
- If you add tests, use `pytest` with files named `test_*.py` under `tests/`, and keep them as **pure-function tests** — no MCP runtime required.

## 8. Forbidden Actions

- Adding a database, cache, queue, auth, or external HTTP client.
- Switching transport to HTTP in v1.
- Adding `print()` inside tool functions (use stderr logging only at module level if absolutely needed).
- Introducing `from __future__ import annotations` (already on Python 3.10+).
- Renaming an existing tool or its arguments (breaking change).

## 9. Commit Hygiene

- One logical change per commit.
- Imperative-mood subject, ≤ 72 chars.
- Body explains **why**, not what (the diff shows what).

## 10. When You're Unsure

1. Re-read `ARCHITECTURE-ESSENTIALS.md`.
2. Re-read the relevant PRD requirement.
3. If still unsure, **ask before implementing**. Do not invent scope.