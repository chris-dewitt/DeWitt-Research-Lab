"""Deterministic deltas between successive public observations."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from typing import Any


def compute_series_changes(observations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return one change row per series that has at least two dated points."""
    by_series: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in observations:
        series_id = str(item.get("series_id", "")).strip()
        if series_id:
            by_series[series_id].append(item)
    changes: list[dict[str, Any]] = []
    for series_id, rows in sorted(by_series.items()):
        ordered = sorted(rows, key=lambda row: str(row.get("observation_date", "")))
        if len(ordered) < 2:
            continue
        previous, current = ordered[-2], ordered[-1]
        prev_value = Decimal(str(previous["value"]))
        curr_value = Decimal(str(current["value"]))
        changes.append(
            {
                "series_id": series_id,
                "title": current.get("title"),
                "previous_value": format(prev_value, "f"),
                "current_value": format(curr_value, "f"),
                "delta": format(curr_value - prev_value, "f"),
                "previous_date": previous.get("observation_date"),
                "current_date": current.get("observation_date"),
                "source_id": current.get("source_id"),
                "citation": current.get("citation"),
            }
        )
    return changes
