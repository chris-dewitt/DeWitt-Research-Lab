"""U.S. Treasury daily par yield curve (no API key)."""

from __future__ import annotations

import csv
import io
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

TREASURY_CSV = (
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
    "daily-treasury-rates.csv/all?type=daily_treasury_yield_curve"
    "&field_tdr_date_value=all&page&_format=csv"
)

_COLUMN_TO_SERIES = {
    "2 Yr": "UST_2Y",
    "2-Yr": "UST_2Y",
    "2 Year": "UST_2Y",
    "10 Yr": "UST_10Y",
    "10-Yr": "UST_10Y",
    "10 Year": "UST_10Y",
}

_TITLES = {
    "UST_2Y": "US Treasury two-year yield",
    "UST_10Y": "US Treasury ten-year yield",
}


def _parse_date(raw: str) -> date:
    text = raw.strip()
    if "-" in text:
        return date.fromisoformat(text[:10])
    if "/" in text:
        month, day, year = text.split("/")
        return date(int(year), int(month), int(day))
    raise ValueError(f"unrecognized Treasury date {raw!r}")


def parse_treasury_csv(text: str, *, limit_rows: int = 40) -> list[dict[str, Any]]:
    """Parse Daily Treasury Par Yield Curve CSV into Atlas observation dicts."""
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise ValueError("Treasury CSV has no header")
    items: list[dict[str, Any]] = []
    for index, row in enumerate(reader):
        if index >= limit_rows:
            break
        date_raw = row.get("Date") or row.get("date")
        if not date_raw:
            continue
        try:
            observed = _parse_date(str(date_raw))
        except ValueError:
            continue
        for column, series_id in _COLUMN_TO_SERIES.items():
            raw = (row.get(column) or "").strip()
            if not raw or raw == "N/A":
                continue
            try:
                value = Decimal(raw)
            except InvalidOperation:
                continue
            items.append(
                {
                    "series_id": series_id,
                    "title": _TITLES[series_id],
                    "value": format(value, "f"),
                    "unit": "percent",
                    "observation_date": observed.isoformat(),
                    "published_date": observed.isoformat(),
                    "source": "U.S. Department of the Treasury",
                    "citation": (
                        "https://home.treasury.gov/resource-center/data-chart-center/"
                        f"interest-rates#{observed.isoformat()}-{series_id}"
                    ),
                    "source_id": "us-treasury-yield-curve",
                    "upstream_series": column,
                }
            )
    items.sort(key=lambda item: (item["series_id"], item["observation_date"]))
    return items
