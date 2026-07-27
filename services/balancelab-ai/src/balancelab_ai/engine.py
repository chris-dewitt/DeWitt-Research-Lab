"""Deterministic, hand-verifiable rate scenario engine.

All values are synthetic and expressed in millions of dollars unless noted.
This is an educational vertical slice, not a production bank model.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

_CENT = Decimal("0.01")
_BPS = Decimal("10000")


def _money(value: Decimal) -> Decimal:
    return value.quantize(_CENT, rounding=ROUND_HALF_UP)


@dataclass(frozen=True, slots=True)
class BalanceSheet:
    earning_assets: Decimal
    interest_bearing_deposits: Decimal
    wholesale_funding: Decimal
    asset_beta: Decimal = Decimal("0.55")
    deposit_beta: Decimal = Decimal("0.35")
    wholesale_beta: Decimal = Decimal("0.95")

    def validate(self) -> None:
        amounts = (self.earning_assets, self.interest_bearing_deposits, self.wholesale_funding)
        betas = (self.asset_beta, self.deposit_beta, self.wholesale_beta)
        if any(amount < 0 for amount in amounts):
            raise ValueError("Balance-sheet amounts cannot be negative")
        if any(beta < 0 or beta > 1 for beta in betas):
            raise ValueError("Repricing betas must be between zero and one")


@dataclass(frozen=True, slots=True)
class RateScenario:
    name: str
    short_rate_bps: int
    long_rate_bps: int


@dataclass(frozen=True, slots=True)
class ProjectionResult:
    scenario: RateScenario
    asset_income_change: Decimal
    deposit_expense_change: Decimal
    wholesale_expense_change: Decimal
    annual_nii_change: Decimal
    curve_slope_change_bps: int
    calculation_lineage: tuple[str, ...]


class ScenarioEngine:
    """Apply a parallel/curve rate shock using explicit repricing betas."""

    def project(self, balance_sheet: BalanceSheet, scenario: RateScenario) -> ProjectionResult:
        balance_sheet.validate()
        short_change = Decimal(scenario.short_rate_bps) / _BPS
        long_change = Decimal(scenario.long_rate_bps) / _BPS
        blended_asset_change = (short_change + long_change) / Decimal("2")

        asset_income = (
            balance_sheet.earning_assets * blended_asset_change * balance_sheet.asset_beta
        )
        deposit_expense = (
            balance_sheet.interest_bearing_deposits * short_change * balance_sheet.deposit_beta
        )
        wholesale_expense = (
            balance_sheet.wholesale_funding * short_change * balance_sheet.wholesale_beta
        )
        nii_change = asset_income - deposit_expense - wholesale_expense

        return ProjectionResult(
            scenario=scenario,
            asset_income_change=_money(asset_income),
            deposit_expense_change=_money(deposit_expense),
            wholesale_expense_change=_money(wholesale_expense),
            annual_nii_change=_money(nii_change),
            curve_slope_change_bps=scenario.long_rate_bps - scenario.short_rate_bps,
            calculation_lineage=(
                "asset_change = earning_assets × average(short_shock,long_shock) × asset_beta",
                "deposit_change = interest_bearing_deposits × short_shock × deposit_beta",
                "wholesale_change = wholesale_funding × short_shock × wholesale_beta",
                "nii_change = asset_change - deposit_change - wholesale_change",
            ),
        )
