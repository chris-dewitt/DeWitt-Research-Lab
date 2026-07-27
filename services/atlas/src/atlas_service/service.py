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
        return [self.latest(series_id, as_of=as_of) for series_id in series]
