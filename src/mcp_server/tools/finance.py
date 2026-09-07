"""Financial tools."""

from src.mcp_server.core.config import ROUND_DIGITS
from src.mcp_server.core.mcp_instance import mcp


@mcp.tool()
def calculate_growth(initial_value: float, growth_rate: float, years: int) -> dict:
    """Calculates compound growth over a given number of years.

    Args:
        initial_value: Starting value (in the same units as the result).
        growth_rate: Annual growth rate as a percentage (e.g. 7 means 7%).
        years: Number of compounding periods.

    Returns:
        Dict with ``initial``, ``years``, and ``projected_value`` (rounded).
    """
    # TODO(v1.1): add input bounds (>=0) and NaN guard.
    final_value = initial_value * ((1 + growth_rate / 100) ** years)
    return {
        "initial": initial_value,
        "years": years,
        "projected_value": round(final_value, ROUND_DIGITS),
    }


__all__ = ["calculate_growth"]