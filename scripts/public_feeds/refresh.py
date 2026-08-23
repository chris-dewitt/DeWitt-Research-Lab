"""Refresh official public feeds into the local store."""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .changes import compute_series_changes
from .fed_rss import FED_MONETARY_RSS, parse_fed_monetary_rss
from .fred import FRED_SERIES, fred_observations_url, parse_fred_observations
from .http import fetch_text
from .store import (
    CHANGES_NAME,
    DOCUMENTS_NAME,
    OBSERVATIONS_NAME,
    STATUS_NAME,
    FeedStore,
)
from .treasury import TREASURY_CSV, parse_treasury_csv

Fetcher = Callable[[str], str]


def _dedupe_observations(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[tuple[str, str], dict[str, Any]] = {}
    for item in items:
        key = (str(item["series_id"]), str(item["observation_date"]))
        seen[key] = item
    return [seen[key] for key in sorted(seen)]


def refresh_public_feeds(
    *,
    root: Path | None = None,
    fred_api_key: str | None = None,
    fetch: Fetcher | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Fetch allowlisted official sources and write the local store.

    ``fetch`` is injected in tests. The default talks to the network.
    """
    store = FeedStore(root)
    getter = fetch or fetch_text
    key = (fred_api_key if fred_api_key is not None else os.environ.get("FRED_API_KEY", "")).strip()
    stamped = now or datetime.now(UTC)
    observations: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    errors: list[str] = []
    used: list[str] = []

    if key:
        for series_id in FRED_SERIES:
            try:
                body = getter(fred_observations_url(series_id, key))
                payload = json.loads(body)
                if not isinstance(payload, dict):
                    raise ValueError("FRED response is not an object")
                observations.extend(parse_fred_observations(series_id, payload))
                used.append(f"fred:{series_id}")
            except (OSError, ValueError, KeyError) as exc:
                errors.append(f"fred:{series_id}: {exc.__class__.__name__}")
    else:
        errors.append("fred:skipped:no FRED_API_KEY")

    have_yields = any(item["series_id"] in {"UST_2Y", "UST_10Y"} for item in observations)
    if not have_yields:
        try:
            csv_text = getter(TREASURY_CSV)
            observations.extend(parse_treasury_csv(csv_text))
            used.append("treasury:yield-curve")
        except (OSError, ValueError) as exc:
            errors.append(f"treasury: {exc.__class__.__name__}")

    try:
        rss = getter(FED_MONETARY_RSS)
        documents.extend(parse_fed_monetary_rss(rss))
        used.append("fed:press-monetary")
    except (OSError, ValueError) as exc:
        errors.append(f"fed: {exc.__class__.__name__}")

    observations = _dedupe_observations(observations)
    changes = compute_series_changes(observations)
    store.write_json(
        OBSERVATIONS_NAME,
        {
            "schema": "drl-public-feed-observations/v1",
            "refreshed_at": stamped.isoformat(),
            "items": observations,
        },
    )
    store.write_json(
        DOCUMENTS_NAME,
        {
            "schema": "drl-public-feed-documents/v1",
            "refreshed_at": stamped.isoformat(),
            "items": documents,
        },
    )
    store.write_json(
        CHANGES_NAME,
        {
            "schema": "drl-public-feed-changes/v1",
            "refreshed_at": stamped.isoformat(),
            "items": changes,
        },
    )
    status = {
        "schema": "drl-public-feed-refresh/v1",
        "refreshed_at": stamped.isoformat(),
        "sources_used": used,
        "observation_count": len(observations),
        "document_count": len(documents),
        "change_count": len(changes),
        "errors": errors,
        "yahoo_finance": "rejected:terms-of-use",
    }
    store.write_json(STATUS_NAME, status)
    return status
