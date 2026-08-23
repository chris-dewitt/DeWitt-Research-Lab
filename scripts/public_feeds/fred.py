"""FRED series observations. Key is required; never logged."""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any
from urllib.parse import urlencode

FRED_API = "https://api.stlouisfed.org/fred/series/observations"

# Atlas series_id → FRED series + transform.
FRED_SERIES: dict[str, dict[str, str]] = {
    "CPI_YOY": {
        "fred_id": "CPIAUCSL",
        "units": "pc1",
        "title": "Consumer Price Index, year-over-year",
        "citation_base": "https://fred.stlouisfed.org/series/CPIAUCSL",
    },
    "UST_2Y": {
        "fred_id": "DGS2",
        "units": "lin",
        "title": "US Treasury two-year yield",
        "citation_base": "https://fred.stlouisfed.org/series/DGS2",
    },
    "UST_10Y": {
        "fred_id": "DGS10",
        "units": "lin",
        "title": "US Treasury ten-year yield",
        "citation_base": "https://fred.stlouisfed.org/series/DGS10",
    },
}


def fred_observations_url(series_id: str, api_key: str, *, limit: int = 36) -> str:
    spec = FRED_SERIES[series_id]
    query = urlencode(
        {
            "series_id": spec["fred_id"],
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": str(limit),
            "units": spec["units"],
        }
    )
    return f"{FRED_API}?{query}"


def parse_fred_observations(series_id: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    spec = FRED_SERIES[series_id]
    rows = payload.get("observations")
    if not isinstance(rows, list):
        raise ValueError("FRED payload missing observations list")
    items: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        raw = str(row.get("value", "")).strip()
        if raw in {"", "."}:
            continue
        try:
            value = Decimal(raw)
        except InvalidOperation:
            continue
        observed = date.fromisoformat(str(row["date"]))
        items.append(
            {
                "series_id": series_id,
                "title": spec["title"],
                "value": format(value, "f"),
                "unit": "percent",
                "observation_date": observed.isoformat(),
                "published_date": observed.isoformat(),
                "source": "FRED, Federal Reserve Bank of St. Louis",
                "citation": f"{spec['citation_base']}#{observed.isoformat()}",
                "source_id": "fred-stlouisfed",
                "upstream_series": spec["fred_id"],
            }
        )
    items.sort(key=lambda item: item["observation_date"])
    return items
