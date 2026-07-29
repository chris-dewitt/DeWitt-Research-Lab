"""Synthetic bank fixtures, scenario catalog, and calculation artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal

from drl_ai_core import canonical_digest

from .engine import BalanceSheet, ProjectionResult, RateScenario, ScenarioEngine


@dataclass(frozen=True, slots=True)
class SyntheticBank:
    bank_id: str
    label: str
    balance_sheet: BalanceSheet


@dataclass(frozen=True, slots=True)
class CalculationArtifact:
    artifact_id: str
    bank_id: str
    scenario_name: str
    digest: str
    result: ProjectionResult


SCENARIO_CATALOG: dict[str, RateScenario] = {
    "parallel-up-100": RateScenario("parallel-up-100", 100, 100),
    "parallel-down-100": RateScenario("parallel-down-100", -100, -100),
    "bear-steepener": RateScenario("bear-steepener", 25, 75),
    "bull-flattener": RateScenario("bull-flattener", -75, -25),
    "basis-short-only": RateScenario("basis-short-only", 50, 0),
    "zero": RateScenario("zero", 0, 0),
}


def sample_regional_bank() -> SyntheticBank:
    """Educational synthetic regional bank used by Atticus demos."""

    return SyntheticBank(
        bank_id="synth-regional-001",
        label="Synthetic regional bank (educational)",
        balance_sheet=BalanceSheet(
            Decimal("8500"),
            Decimal("6200"),
            Decimal("900"),
        ),
    )


def project_named_scenario(
    bank: SyntheticBank,
    scenario_name: str,
    *,
    engine: ScenarioEngine | None = None,
) -> CalculationArtifact:
    if scenario_name not in SCENARIO_CATALOG:
        raise KeyError(f"unknown scenario {scenario_name!r}")
    scenario = SCENARIO_CATALOG[scenario_name]
    engine = engine or ScenarioEngine()
    result = engine.project(bank.balance_sheet, scenario)
    payload = {
        "bank_id": bank.bank_id,
        "scenario": asdict(scenario),
        "annual_nii_change": str(result.annual_nii_change),
        "curve_slope_change_bps": result.curve_slope_change_bps,
        "lineage": list(result.calculation_lineage),
    }
    digest = f"sha256:{canonical_digest(payload)}"
    return CalculationArtifact(
        artifact_id=f"balancelab-{bank.bank_id}-{scenario_name}",
        bank_id=bank.bank_id,
        scenario_name=scenario_name,
        digest=digest,
        result=result,
    )


def assert_projection_invariants(result: ProjectionResult) -> None:
    """Deterministic invariants for educational projections."""

    recomputed = (
        result.asset_income_change - result.deposit_expense_change - result.wholesale_expense_change
    )
    if recomputed != result.annual_nii_change:
        raise AssertionError("NII identity failed")
    if result.curve_slope_change_bps != (
        result.scenario.long_rate_bps - result.scenario.short_rate_bps
    ):
        raise AssertionError("curve slope identity failed")
