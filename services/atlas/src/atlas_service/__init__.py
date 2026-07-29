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
from .service import AtlasService, MetricObservation

__all__ = [
    "AtlasService",
    "AtlasValidationError",
    "CachedObservation",
    "FAILURE_FIXTURE_PAYLOAD",
    "FIXTURE_SOURCE_TERMS",
    "FileObservationCache",
    "MetricObservation",
    "PublicFixtureAdapter",
    "SourceTerms",
    "TemporalRecord",
    "validate_observation_payload",
]

__version__ = "0.2.0"
