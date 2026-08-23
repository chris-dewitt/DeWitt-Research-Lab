"""Load Atlas observations from the opt-in official feed store."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .adapter import (
    CachedObservation,
    SourceTerms,
    TemporalRecord,
    validate_observation_payload,
)
from .service import MetricObservation

LIVE_SOURCE_TERMS = SourceTerms(
    source_id="drl-official-public-feeds",
    display_name="Official public feed store (FRED / Treasury)",
    data_tier="public",
    license_label="per-source; see configs/public-feed-sources.yaml",
    terms_url="https://fred.stlouisfed.org/docs/api/terms_of_use.html",
    redistribution="link-and-transform",
    notes=(
        "Operator-refreshed official public data. Not a Yahoo Finance scrape.",
        "Not a fixture. Do not treat as a DRL forecast.",
    ),
)


class PublicFeedStoreAdapter:
    """Read validated observations written by scripts/refresh_public_feeds.py."""

    def __init__(self, root: Path, *, ingested_at: datetime | None = None) -> None:
        self.root = root
        self.ingested_at = ingested_at or datetime.now(UTC)

    def load(self) -> list[CachedObservation]:
        path = self.root / "observations.json"
        if not path.is_file():
            raise FileNotFoundError(
                f"no live Atlas store at {path}; run scripts/refresh_public_feeds.py"
            )
        payload = json.loads(path.read_text(encoding="utf-8"))
        items = payload.get("items") if isinstance(payload, dict) else None
        if not isinstance(items, list) or not items:
            raise ValueError("live Atlas store has no observations")
        loaded: list[CachedObservation] = []
        for raw in items:
            if not isinstance(raw, dict):
                continue
            observation = validate_observation_payload(_observation_fields(raw))
            cache_key = (
                f"{observation.series_id}:{observation.observation_date.isoformat()}:"
                f"{observation.published_date.isoformat()}"
            )
            loaded.append(
                CachedObservation(
                    observation=observation,
                    checksum="store",
                    source_terms=LIVE_SOURCE_TERMS,
                    temporal=TemporalRecord(
                        observation_date=observation.observation_date,
                        published_date=observation.published_date,
                        ingested_at=self.ingested_at,
                    ),
                    cache_key=cache_key,
                )
            )
        return loaded


def _observation_fields(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "series_id": raw["series_id"],
        "title": raw["title"],
        "value": raw["value"],
        "unit": raw["unit"],
        "observation_date": raw["observation_date"],
        "published_date": raw["published_date"],
        "source": raw["source"],
        "citation": raw["citation"],
    }


def observations_from_store(root: Path) -> list[MetricObservation]:
    return [item.observation for item in PublicFeedStoreAdapter(root).load()]
