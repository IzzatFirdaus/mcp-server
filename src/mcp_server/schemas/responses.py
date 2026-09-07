"""Typed response shapes for tool return values.

Stubbed for v1.1; not currently imported.
"""

from typing import TypedDict


class GrowthResult(TypedDict):
    initial: float
    years: int
    projected_value: float


class SystemStatus(TypedDict):
    status: str
    protocol: str
    active_tools: list[str]


__all__ = ["GrowthResult", "SystemStatus"]