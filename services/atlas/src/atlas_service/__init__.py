"""Point-in-time evidence service for the runnable DRL foundation."""

from .adapter import (
    FAILURE_FIXTURE_PAYLOAD,
    FIXTURE_SOURCE_TERMS,
    AtlasValidationError,
    CachedObservation,
    FileObservationCache,
    PublicFixtureAdapter,
    SourceTerms,
    TemporalRecord,
    validate_observation_payload,
)
from .live_store import LIVE_SOURCE_TERMS, PublicFeedStoreAdapter
from .service import AtlasService, MetricObservation

__all__ = [
    "AtlasService",
    "AtlasValidationError",
    "CachedObservation",
    "FAILURE_FIXTURE_PAYLOAD",
    "FIXTURE_SOURCE_TERMS",
    "FileObservationCache",
    "LIVE_SOURCE_TERMS",
    "MetricObservation",
    "PublicFeedStoreAdapter",
    "PublicFixtureAdapter",
    "SourceTerms",
    "TemporalRecord",
    "validate_observation_payload",
]

__version__ = "0.2.0"
