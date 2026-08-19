"""Arbitrage detection and coherence repair.

The substantive assertions are the certificate properties: an exploiting
portfolio must cost a negative amount and pay non-negatively in every state.
Those are what make a reported violation a violation rather than a number.
"""

from __future__ import annotations

import pytest
from drl_cfi.coherence import (
    COHERENCE_TOLERANCE,
    audit_prices,
    payoff_matrix,
    portfolio_cost,
    portfolio_payoffs,
)
from drl_cfi.linalg import mat_vec
from drl_cfi.payoffs import Claim, Leg, LegKind, state_grid


def cash_claim(name: str, quantity: float) -> Claim:
    return Claim(name, (Leg(kind=LegKind.CASH, quantity=quantity),))


def call_claim(name: str, strike: float) -> Claim:
    return Claim(name, (Leg(kind=LegKind.CALL, strike=strike),))


def test_prices_built_from_state_prices_are_coherent() -> None:
    """Any non-negatively weighted combination of state payoffs admits no arbitrage."""
    claims = (
        cash_claim("cash", 1.0),
        call_claim("call-90", 90.0),
        call_claim("call-110", 110.0),
    )
    grid = state_grid(*claims)
    matrix = payoff_matrix(claims, grid)
    weights = [0.05 * (index + 1) for index in range(len(grid))]
    quoted = mat_vec(matrix, weights)

    report = audit_prices(claims, quoted, grid=grid)
    assert report.is_coherent
    assert report.repair_distance == pytest.approx(0.0, abs=1e-9)
    assert report.repaired_prices == pytest.approx(quoted, abs=1e-8)


def test_dominated_claim_priced_above_its_dominator_is_arbitrage() -> None:
    """A 90-strike call dominates a 110-strike call, so it cannot be cheaper."""
    claims = (call_claim("call-90", 90.0), call_claim("call-110", 110.0))
    report = audit_prices(claims, [5.0, 8.0])

    assert not report.is_coherent
    assert report.repair_distance > COHERENCE_TOLERANCE

    cost = portfolio_cost(report.quoted_prices, report.exploiting_portfolio)
    payoffs = portfolio_payoffs(claims, report.exploiting_portfolio, report.grid)
    assert cost < 0.0  # the portfolio pays the holder to enter it
    assert all(value >= -1e-9 for value in payoffs)  # and never owes anything back


def test_exploiting_portfolio_profit_equals_the_squared_repair_distance() -> None:
    """The projection geometry fixes the relationship; it is not an independent quantity."""
    claims = (cash_claim("cash-1", 1.0), cash_claim("cash-2", 2.0))
    report = audit_prices(claims, [1.0, 0.5])

    cost = portfolio_cost(report.quoted_prices, report.exploiting_portfolio)
    assert report.arbitrage_profit == pytest.approx(report.repair_distance**2, abs=1e-12)
    assert cost == pytest.approx(-report.arbitrage_profit, abs=1e-12)


def test_repair_of_a_hand_computable_case_matches_the_closed_form() -> None:
    """Two pure-cash claims reduce the coherent set to a ray, so the projection is exact.

    With payoffs 1 and 2 in every state the coherent set is ``{(t, 2t) : t >= 0}``.
    Projecting ``(1.0, 0.5)`` gives ``t = 0.4``.
    """
    claims = (cash_claim("cash-1", 1.0), cash_claim("cash-2", 2.0))
    report = audit_prices(claims, [1.0, 0.5])

    assert report.repaired_prices == pytest.approx([0.4, 0.8], abs=1e-9)
    assert report.repair_distance == pytest.approx(0.45**0.5, abs=1e-9)
    assert report.exploiting_portfolio == pytest.approx([-0.6, 0.3], abs=1e-9)


def test_repaired_prices_are_themselves_coherent() -> None:
    """Repair must land inside the coherent set, not merely closer to it."""
    claims = (call_claim("call-90", 90.0), call_claim("call-110", 110.0))
    report = audit_prices(claims, [5.0, 8.0])
    second_pass = audit_prices(claims, report.repaired_prices, grid=report.grid)
    assert second_pass.is_coherent


def test_repair_is_minimal_against_nearby_coherent_points() -> None:
    """No coherent point sampled from the cone beats the projection."""
    claims = (call_claim("call-90", 90.0), call_claim("call-110", 110.0))
    grid = state_grid(*claims)
    matrix = payoff_matrix(claims, grid)
    quoted = [5.0, 8.0]
    report = audit_prices(claims, quoted, grid=grid)

    for scale in (0.1, 0.5, 1.0, 2.0):
        for index in range(len(grid)):
            weights = [0.0] * len(grid)
            weights[index] = scale
            candidate = mat_vec(matrix, weights)
            distance = sum((q - c) ** 2 for q, c in zip(quoted, candidate, strict=True)) ** 0.5
            assert distance >= report.repair_distance - 1e-9


def test_implied_distribution_is_a_probability_vector() -> None:
    claims = (
        cash_claim("cash", 1.0),
        call_claim("call-90", 90.0),
        call_claim("call-110", 110.0),
    )
    grid = state_grid(*claims)
    matrix = payoff_matrix(claims, grid)
    quoted = mat_vec(matrix, [0.2] * len(grid))

    distribution = audit_prices(claims, quoted, grid=grid).implied_distribution()
    assert distribution is not None
    assert sum(distribution) == pytest.approx(1.0, abs=1e-9)
    assert all(value >= -1e-12 for value in distribution)


def test_coherent_prices_are_not_flagged_as_grid_bounded() -> None:
    claims = (cash_claim("cash-1", 1.0), cash_claim("cash-2", 2.0))
    report = audit_prices(claims, [1.0, 2.0])
    assert report.is_coherent
    assert not report.certificate_is_grid_bounded


def test_audit_rejects_a_price_count_mismatch() -> None:
    claims = (cash_claim("cash", 1.0),)
    with pytest.raises(ValueError, match="one price per claim"):
        audit_prices(claims, [1.0, 2.0])


def test_audit_requires_at_least_one_claim() -> None:
    with pytest.raises(ValueError, match="at least one claim"):
        audit_prices((), [])
