"""Unit tests for the calculate_growth pure function.

These tests import the math directly (bypassing the @mcp.tool decorator) to
keep them fast and free of MCP runtime concerns. To make this work cleanly
in v1.1, factor the math into a non-decorated helper inside tools/finance.py.
"""

import pytest

# TODO(v1.1): import the pure math helper instead of the decorated tool.
pytestmark = pytest.mark.skip(reason="Awaiting v1.1 refactor of tools/finance.py")


def test_calculate_growth_zero_rate_returns_initial() -> None:
    assert False  # placeholder


def test_calculate_growth_zero_years_returns_initial() -> None:
    assert False  # placeholder


def test_calculate_growth_rounds_to_two_decimals() -> None:
    assert False  # placeholder