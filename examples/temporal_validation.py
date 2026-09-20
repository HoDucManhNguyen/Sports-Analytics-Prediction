"""Small, standalone illustration of time-aware race evaluation.

The rows used with this module are invented. This is not the production model
and cannot reproduce the aggregate findings in the case study.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class RaceKey:
    season: int
    round: int


@dataclass(frozen=True)
class Result:
    race: RaceKey
    driver: str
    grid_position: int
    actual_position: int
    classified: bool = True


def prior_results(rows: list[Result], target: RaceKey) -> list[Result]:
    """Return completed races strictly before the target race."""
    return [row for row in rows if row.race < target]


def spearman_order(predicted: list[str], actual: list[str]) -> float:
    """Spearman correlation for two complete, tie-free driver orders."""
    if len(predicted) != len(actual) or len(predicted) < 2:
        raise ValueError("Orders must have equal lengths of at least two")
    if len(set(predicted)) != len(predicted) or set(predicted) != set(actual):
        raise ValueError("Orders must contain each driver exactly once")

    actual_rank = {driver: index for index, driver in enumerate(actual)}
    squared_error = sum(
        (index - actual_rank[driver]) ** 2
        for index, driver in enumerate(predicted)
    )
    n = len(predicted)
    return 1 - 6 * squared_error / (n * (n * n - 1))


def grid_baseline(rows: list[Result], race: RaceKey) -> list[str]:
    """Rank a race's classified drivers by their starting-grid positions."""
    selected = [row for row in rows if row.race == race and row.classified]
    if len(selected) < 2:
        raise ValueError("A race needs at least two classified drivers")
    return [row.driver for row in sorted(selected, key=lambda row: row.grid_position)]


def actual_order(rows: list[Result], race: RaceKey) -> list[str]:
    """Return the classified finishing order for a race."""
    selected = [row for row in rows if row.race == race and row.classified]
    if len(selected) < 2:
        raise ValueError("A race needs at least two classified drivers")
    return [row.driver for row in sorted(selected, key=lambda row: row.actual_position)]
