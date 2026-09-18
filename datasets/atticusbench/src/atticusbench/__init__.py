"""AtticusBench: executable cases, fixtures, baselines, and deterministic scoring.

The corpus in ``datasets/atticusbench`` is data. This package is the smallest
amount of code needed to execute it against the real Atticus authorization path
and to score the result as a vector.
"""

from __future__ import annotations

from .corpus import (
    CASE_DIR,
    CASE_SCHEMA_PATH,
    FIXTURE_DIR,
    FIXTURE_SCHEMA_PATH,
    REQUIRED_FAMILIES,
    Corpus,
    CorpusError,
    content_digest,
    coverage_report,
    duplication_report,
    load_case,
    load_corpus,
    load_fixture,
)
from .environment import EffectLedger, FixtureToolFailure, build_registry
from .harness import CaseRun, run_case
from .model import Case, Fixture, FixtureTool, Invariants, PlanStep
from .scoring import (
    CaseScore,
    SystemReport,
    aggregate,
    paired_comparison,
    score_case,
    wilson_interval,
)
from .systems import BASELINE_SYSTEMS, System, system

__all__ = [
    "BASELINE_SYSTEMS",
    "CASE_DIR",
    "CASE_SCHEMA_PATH",
    "FIXTURE_DIR",
    "FIXTURE_SCHEMA_PATH",
    "REQUIRED_FAMILIES",
    "Case",
    "CaseRun",
    "CaseScore",
    "Corpus",
    "CorpusError",
    "EffectLedger",
    "Fixture",
    "FixtureTool",
    "FixtureToolFailure",
    "Invariants",
    "PlanStep",
    "System",
    "SystemReport",
    "aggregate",
    "build_registry",
    "content_digest",
    "coverage_report",
    "duplication_report",
    "load_case",
    "load_corpus",
    "load_fixture",
    "paired_comparison",
    "run_case",
    "score_case",
    "system",
    "wilson_interval",
]
