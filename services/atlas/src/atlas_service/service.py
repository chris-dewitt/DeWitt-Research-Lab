"""Small point-in-time macro evidence store used by the local demo."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class MetricObservation:
    series_id: str
    title: str
    value: Decimal
    unit: str
    observation_date: date
    published_date: date
    source: str
    citation: str


class AtlasService:
    """Query public macro observations without violating as-of time."""

    def __init__(self, observations: list[MetricObservation] | None = None) -> None:
        self._observations = observations or self.fixture_observations()

    @classmethod
    def from_public_adapter(cls, adapter: object) -> AtlasService:
        """Build a service from any adapter that exposes ``load()``."""

        load = getattr(adapter, "load", None)
        if not callable(load):
            raise TypeError("adapter must provide load()")
        loaded = load()
        return cls([item.observation for item in loaded])

    @classmethod
    def from_feed_store(cls, root: object) -> AtlasService:
        from pathlib import Path

        from .live_store import PublicFeedStoreAdapter

        return cls.from_public_adapter(PublicFeedStoreAdapter(Path(str(root))))

    @staticmethod
    def fixture_observations() -> list[MetricObservation]:
        """Return explicitly synthetic/public-demo observations."""

        return [
            MetricObservation(
                "CPI_YOY",
                "Consumer Price Index, year-over-year",
                Decimal("3.10"),
                "percent",
                date(2026, 6, 30),
                date(2026, 7, 14),
                "DRL synthetic public-data fixture",
                "fixture://atlas/CPI_YOY/2026-06",
            ),
            MetricObservation(
                "UST_2Y",
                "US Treasury two-year yield",
                Decimal("4.15"),
                "percent",
                date(2026, 7, 24),
                date(2026, 7, 24),
                "DRL synthetic market fixture",
                "fixture://atlas/UST_2Y/2026-07-24",
            ),
            MetricObservation(
                "UST_10Y",
                "US Treasury ten-year yield",
                Decimal("4.48"),
                "percent",
                date(2026, 7, 24),
                date(2026, 7, 24),
                "DRL synthetic market fixture",
                "fixture://atlas/UST_10Y/2026-07-24",
            ),
        ]

    def latest(self, series_id: str, *, as_of: date) -> MetricObservation:
        """Return the latest item published on or before ``as_of``."""

        eligible = [
            item
            for item in self._observations
            if item.series_id == series_id and item.published_date <= as_of
        ]
        if not eligible:
            raise LookupError(f"No {series_id!r} observation was public by {as_of.isoformat()}")
        return max(eligible, key=lambda item: (item.published_date, item.observation_date))

    def research_snapshot(
        self,
        *,
        as_of: date,
        series: tuple[str, ...] = ("CPI_YOY", "UST_2Y", "UST_10Y"),
    ) -> list[MetricObservation]:
        items: list[MetricObservation] = []
        for series_id in series:
            try:
                items.append(self.latest(series_id, as_of=as_of))
            except LookupError:
                continue
        if not items:
            raise LookupError(f"No requested series were public by {as_of.isoformat()}")
        return items

    def series_changes(
        self,
        *,
        as_of: date,
        series: tuple[str, ...] = ("CPI_YOY", "UST_2Y", "UST_10Y"),
    ) -> list[dict[str, str]]:
        """Latest minus previous public print for each series."""
        changes: list[dict[str, str]] = []
        for series_id in series:
            eligible = [
                item
                for item in self._observations
                if item.series_id == series_id and item.published_date <= as_of
            ]
            eligible.sort(key=lambda item: (item.published_date, item.observation_date))
            if len(eligible) < 2:
                continue
            previous, current = eligible[-2], eligible[-1]
            delta = Decimal(current.value) - Decimal(previous.value)
            changes.append(
                {
                    "series_id": series_id,
                    "previous_value": format(previous.value, "f"),
                    "current_value": format(current.value, "f"),
                    "delta": format(delta, "f"),
                    "previous_date": previous.observation_date.isoformat(),
                    "current_date": current.observation_date.isoformat(),
                    "citation": current.citation,
                }
            )
        return changes
