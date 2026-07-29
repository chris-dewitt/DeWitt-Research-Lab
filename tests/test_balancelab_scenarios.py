"""BalanceLab scenario catalog and invariant tests (DRL-017)."""

from __future__ import annotations

from decimal import Decimal

import pytest
from balancelab_ai import (
    SCENARIO_CATALOG,
    BalanceSheet,
    ScenarioEngine,
    assert_projection_invariants,
    project_named_scenario,
    sample_regional_bank,
)


def test_bear_steepener_hand_calculation_regression() -> None:
    artifact = project_named_scenario(sample_regional_bank(), "bear-steepener")
    result = artifact.result
    assert result.annual_nii_change == Decimal("15.81")
    assert result.curve_slope_change_bps == 50
    assert_projection_invariants(result)
    assert artifact.digest.startswith("sha256:")


def test_zero_shock_identity() -> None:
    result = project_named_scenario(sample_regional_bank(), "zero").result
    assert result.annual_nii_change == Decimal("0.00")
    assert result.curve_slope_change_bps == 0
    assert_projection_invariants(result)


def test_scenario_catalog_covers_curve_shapes() -> None:
    names = set(SCENARIO_CATALOG)
    assert {"parallel-up-100", "bear-steepener", "bull-flattener", "basis-short-only"} <= names
    bank = sample_regional_bank()
    for name in ("parallel-up-100", "bull-flattener", "basis-short-only"):
        artifact = project_named_scenario(bank, name)
        assert_projection_invariants(artifact.result)


def test_boundary_rejects_negative_amounts_and_invalid_betas() -> None:
    with pytest.raises(ValueError, match="negative"):
        BalanceSheet(Decimal("-1"), Decimal("1"), Decimal("1")).validate()
    with pytest.raises(ValueError, match="betas"):
        BalanceSheet(
            Decimal("1"),
            Decimal("1"),
            Decimal("1"),
            asset_beta=Decimal("1.5"),
        ).validate()


def test_unknown_scenario_fails() -> None:
    with pytest.raises(KeyError):
        project_named_scenario(sample_regional_bank(), "does-not-exist")


def test_lineage_present_for_all_catalog_scenarios() -> None:
    engine = ScenarioEngine()
    bank = sample_regional_bank()
    for name in SCENARIO_CATALOG:
        result = engine.project(bank.balance_sheet, SCENARIO_CATALOG[name])
        assert len(result.calculation_lineage) == 4
        assert_projection_invariants(result)
