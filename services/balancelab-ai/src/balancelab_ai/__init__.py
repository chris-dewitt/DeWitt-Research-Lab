"""Deterministic synthetic balance-sheet calculations for DRL."""

from .engine import BalanceSheet, ProjectionResult, RateScenario, ScenarioEngine
from .scenarios import (
    SCENARIO_CATALOG,
    CalculationArtifact,
    SyntheticBank,
    assert_projection_invariants,
    project_named_scenario,
    sample_regional_bank,
)

__all__ = [
    "BalanceSheet",
    "CalculationArtifact",
    "ProjectionResult",
    "RateScenario",
    "SCENARIO_CATALOG",
    "ScenarioEngine",
    "SyntheticBank",
    "assert_projection_invariants",
    "project_named_scenario",
    "sample_regional_bank",
]

__version__ = "0.2.0"
