"""Point-in-time public Atlas adapter with cache, validation, and source terms."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, cast

from drl_ai_core import canonical_digest

from .service import MetricObservation


@dataclass(frozen=True, slots=True)
class SourceTerms:
    """Rights and provenance for one public data source."""

    source_id: str
    display_name: str
    data_tier: str
    license_label: str
    terms_url: str
    redistribution: str
    notes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TemporalRecord:
    """Distinct temporal fields required by Atlas retrieval."""

    observation_date: date
    published_date: date
    ingested_at: datetime
    as_of: date | None = None


@dataclass(frozen=True, slots=True)
class CachedObservation:
    observation: MetricObservation
    checksum: str
    source_terms: SourceTerms
    temporal: TemporalRecord
    cache_key: str


class AtlasValidationError(ValueError):
    """Raised when an inbound observation fails deterministic validation."""


FIXTURE_SOURCE_TERMS = SourceTerms(
    source_id="drl-synthetic-public-macro",
    display_name="DRL synthetic public macro fixtures",
    data_tier="public",
    license_label="CC0-1.0-equivalent-fixture",
    terms_url="fixture://atlas/SOURCE_TERMS",
    redistribution="synthetic-demo-only",
    notes=(
        "Not live FRED/Treasury data.",
        "Safe for local/CI demos; do not claim live coverage.",
    ),
)


def validate_observation_payload(payload: dict[str, Any]) -> MetricObservation:
    """Validate and normalize one observation mapping."""

    required = (
        "series_id",
        "title",
        "value",
        "unit",
        "observation_date",
        "published_date",
        "source",
        "citation",
    )
    missing = [key for key in required if key not in payload]
    if missing:
        raise AtlasValidationError(f"missing fields: {missing}")
    try:
        value = Decimal(str(payload["value"]))
    except (InvalidOperation, TypeError) as exc:
        raise AtlasValidationError("value must be a decimal number") from exc
    try:
        observation_date = date.fromisoformat(str(payload["observation_date"]))
        published_date = date.fromisoformat(str(payload["published_date"]))
    except ValueError as exc:
        raise AtlasValidationError("dates must be ISO YYYY-MM-DD") from exc
    if published_date < observation_date:
        raise AtlasValidationError("published_date cannot precede observation_date")
    series_id = str(payload["series_id"]).strip()
    if not series_id:
        raise AtlasValidationError("series_id cannot be blank")
    return MetricObservation(
        series_id=series_id,
        title=str(payload["title"]),
        value=value,
        unit=str(payload["unit"]),
        observation_date=observation_date,
        published_date=published_date,
        source=str(payload["source"]),
        citation=str(payload["citation"]),
    )


class FileObservationCache:
    """Content-addressed on-disk cache for validated observations."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, cache_key: str) -> Path:
        digest = canonical_digest(cache_key)
        return self.root / f"{digest}.json"

    def get(self, cache_key: str) -> dict[str, Any] | None:
        path = self._path(cache_key)
        if not path.exists():
            return None
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise AtlasValidationError(f"corrupt cache entry for {cache_key}")
        return cast(dict[str, Any], loaded)

    def put(self, cache_key: str, payload: dict[str, Any]) -> str:
        body = json.dumps(payload, sort_keys=True, default=str)
        checksum = f"sha256:{canonical_digest(body)}"
        path = self._path(cache_key)
        path.write_text(body + "\n", encoding="utf-8")
        return checksum


class PublicFixtureAdapter:
    """Offline public adapter: fixture payloads → validate → cache → observations."""

    def __init__(
        self,
        *,
        cache: FileObservationCache,
        source_terms: SourceTerms = FIXTURE_SOURCE_TERMS,
        fixture_payloads: list[dict[str, Any]] | None = None,
        ingested_at: datetime | None = None,
    ) -> None:
        if source_terms.data_tier != "public":
            raise ValueError("Atlas public adapter requires data_tier=public")
        self.cache = cache
        self.source_terms = source_terms
        self.fixture_payloads = fixture_payloads or default_fixture_payloads()
        self.ingested_at = ingested_at or datetime.fromisoformat("2026-07-29T00:00:00+00:00")

    def load(self) -> list[CachedObservation]:
        loaded: list[CachedObservation] = []
        for payload in self.fixture_payloads:
            observation = validate_observation_payload(payload)
            cache_key = (
                f"{observation.series_id}:{observation.observation_date.isoformat()}:"
                f"{observation.published_date.isoformat()}"
            )
            cached = self.cache.get(cache_key)
            record = {
                "observation": asdict(observation),
                "source_terms": asdict(self.source_terms),
                "ingested_at": self.ingested_at.isoformat(),
            }
            if cached is None:
                checksum = self.cache.put(cache_key, record)
            else:
                payload = json.dumps(cached, sort_keys=True, default=str)
                checksum = f"sha256:{canonical_digest(payload)}"
            loaded.append(
                CachedObservation(
                    observation=observation,
                    checksum=checksum,
                    source_terms=self.source_terms,
                    temporal=TemporalRecord(
                        observation_date=observation.observation_date,
                        published_date=observation.published_date,
                        ingested_at=self.ingested_at,
                    ),
                    cache_key=cache_key,
                )
            )
        return loaded


def default_fixture_payloads() -> list[dict[str, Any]]:
    return [
        {
            "series_id": "CPI_YOY",
            "title": "Consumer Price Index, year-over-year",
            "value": "3.10",
            "unit": "percent",
            "observation_date": "2026-06-30",
            "published_date": "2026-07-14",
            "source": "DRL synthetic public-data fixture",
            "citation": "fixture://atlas/CPI_YOY/2026-06",
        },
        {
            "series_id": "UST_2Y",
            "title": "US Treasury two-year yield",
            "value": "4.15",
            "unit": "percent",
            "observation_date": "2026-07-24",
            "published_date": "2026-07-24",
            "source": "DRL synthetic market fixture",
            "citation": "fixture://atlas/UST_2Y/2026-07-24",
        },
        {
            "series_id": "UST_10Y",
            "title": "US Treasury ten-year yield",
            "value": "4.48",
            "unit": "percent",
            "observation_date": "2026-07-24",
            "published_date": "2026-07-24",
            "source": "DRL synthetic market fixture",
            "citation": "fixture://atlas/UST_10Y/2026-07-24",
        },
    ]


FAILURE_FIXTURE_PAYLOAD: dict[str, Any] = {
    "series_id": "BAD_SERIES",
    "title": "Invalid future leak candidate",
    "value": "not-a-number",
    "unit": "percent",
    "observation_date": "2026-07-24",
    "published_date": "2026-07-01",
    "source": "failure-fixture",
    "citation": "fixture://atlas/failure",
}
