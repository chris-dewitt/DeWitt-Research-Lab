"""Tests for Atlas public point-in-time adapter (DRL-014)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from atlas_service import (
    FAILURE_FIXTURE_PAYLOAD,
    FIXTURE_SOURCE_TERMS,
    AtlasService,
    AtlasValidationError,
    FileObservationCache,
    PublicFixtureAdapter,
    validate_observation_payload,
)


def test_source_terms_are_public_and_documented() -> None:
    assert FIXTURE_SOURCE_TERMS.data_tier == "public"
    assert FIXTURE_SOURCE_TERMS.license_label
    assert FIXTURE_SOURCE_TERMS.terms_url.startswith("fixture://")
    assert FIXTURE_SOURCE_TERMS.redistribution


def test_temporal_fields_and_as_of_filtering(tmp_path: Path) -> None:
    adapter = PublicFixtureAdapter(cache=FileObservationCache(tmp_path / "cache"))
    service = AtlasService.from_public_adapter(adapter)
    item = service.latest("CPI_YOY", as_of=date(2026, 7, 14))
    assert item.published_date == date(2026, 7, 14)
    assert item.observation_date == date(2026, 6, 30)
    with pytest.raises(LookupError):
        service.latest("CPI_YOY", as_of=date(2026, 7, 1))


def test_cache_round_trip_is_idempotent(tmp_path: Path) -> None:
    cache = FileObservationCache(tmp_path / "cache")
    adapter = PublicFixtureAdapter(cache=cache)
    first = adapter.load()
    second = adapter.load()
    assert len(first) == len(second) == 3
    assert {item.cache_key for item in first} == {item.cache_key for item in second}
    assert all(item.checksum.startswith("sha256:") for item in first)
    assert all(item.temporal.published_date >= item.temporal.observation_date for item in first)


def test_validation_failure_fixture() -> None:
    with pytest.raises(AtlasValidationError):
        validate_observation_payload(FAILURE_FIXTURE_PAYLOAD)


def test_published_before_observation_rejected() -> None:
    payload = {
        "series_id": "X",
        "title": "x",
        "value": "1.0",
        "unit": "percent",
        "observation_date": "2026-07-10",
        "published_date": "2026-07-01",
        "source": "t",
        "citation": "c",
    }
    with pytest.raises(AtlasValidationError, match="published_date"):
        validate_observation_payload(payload)
