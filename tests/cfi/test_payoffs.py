"""The payoff-equivalence oracle, which decides what "the same payoff" means."""

from __future__ import annotations

import pytest
from drl_cfi.payoffs import (
    Claim,
    Leg,
    LegKind,
    equivalence_failure,
    equivalence_grid,
    is_payoff_equivalent,
    state_grid,
)

STRIKE = 100.0


def call(strike: float = STRIKE, quantity: float = 1.0) -> Leg:
    return Leg(kind=LegKind.CALL, quantity=quantity, strike=strike)


def put(strike: float = STRIKE, quantity: float = 1.0) -> Leg:
    return Leg(kind=LegKind.PUT, quantity=quantity, strike=strike)


def cash(quantity: float) -> Leg:
    return Leg(kind=LegKind.CASH, quantity=quantity)


def underlying(quantity: float = 1.0) -> Leg:
    return Leg(kind=LegKind.UNDERLYING, quantity=quantity)


def test_option_leg_requires_a_strike() -> None:
    with pytest.raises(ValueError, match="requires a strike"):
        Leg(kind=LegKind.CALL)


def test_cash_leg_rejects_a_strike() -> None:
    with pytest.raises(ValueError, match="must not carry a strike"):
        Leg(kind=LegKind.CASH, strike=10.0)


def test_put_call_parity_holds_in_payoff_space() -> None:
    """A long call and short put replicate the forward: C - P pays S_T - K."""
    synthetic = Claim("synthetic-forward", (call(), put(quantity=-1.0)))
    forward = Claim("forward", (underlying(), cash(-STRIKE)))
    assert is_payoff_equivalent(synthetic, forward)


def test_protective_put_equals_call_plus_cash() -> None:
    """Underlying plus a put pays the same as a call plus the strike in cash."""
    protective = Claim("protective-put", (underlying(), put()))
    equivalent = Claim("call-plus-cash", (call(), cash(STRIKE)))
    assert is_payoff_equivalent(protective, equivalent)


def test_a_mispriced_quantity_is_not_equivalent() -> None:
    protective = Claim("protective-put", (underlying(), put()))
    wrong = Claim("call-plus-wrong-cash", (call(), cash(STRIKE + 1.0)))
    assert not is_payoff_equivalent(protective, wrong)


def test_equivalence_failure_explains_the_difference() -> None:
    left = Claim("one-call", (call(),))
    right = Claim("two-calls", (call(quantity=2.0),))
    reason = equivalence_failure(left, right)
    assert reason is not None
    assert "terminal slopes differ" in reason


def test_equivalence_failure_is_none_for_equivalent_claims() -> None:
    left = Claim("straddle", (call(), put()))
    right = Claim("straddle-rebuilt", (put(), call()))
    assert equivalence_failure(left, right) is None


def test_claims_differing_only_above_the_grid_are_caught_by_terminal_slope() -> None:
    """Payoffs can agree on every kink and still diverge in the tail."""
    left = Claim("capped", (call(strike=90.0), call(strike=110.0, quantity=-1.0)))
    right = Claim("uncapped", (call(strike=90.0),))
    # They agree at 0 and at 90, and differ only once the second strike bites.
    assert left.payoff_at(90.0) == pytest.approx(right.payoff_at(90.0))
    assert not is_payoff_equivalent(left, right)


def test_equivalence_grid_contains_kinks_and_interior_points() -> None:
    claim = Claim("spread", (call(strike=90.0), call(strike=110.0, quantity=-1.0)))
    grid = equivalence_grid(claim)
    assert 0.0 in grid
    assert 90.0 in grid and 110.0 in grid
    assert 100.0 in grid  # midpoint of adjacent kinks
    assert max(grid) > 110.0


def test_state_grid_extends_beyond_the_largest_kink() -> None:
    claim = Claim("call", (call(),))
    grid = state_grid(claim)
    assert max(grid) > STRIKE
    assert grid == tuple(sorted(set(grid)))


def test_state_grid_rejects_a_non_extending_multiple() -> None:
    with pytest.raises(ValueError, match="upper_multiple"):
        state_grid(Claim("call", (call(),)), upper_multiple=1.0)


def test_butterfly_payoff_is_non_negative_everywhere() -> None:
    """Convexity in strike, expressed as a payoff the market cannot make negative."""
    butterfly = Claim(
        "butterfly",
        (call(strike=90.0), call(strike=100.0, quantity=-2.0), call(strike=110.0)),
    )
    for price in state_grid(butterfly):
        assert butterfly.payoff_at(price) >= -1e-12


def test_claim_requires_legs() -> None:
    with pytest.raises(ValueError, match="no legs"):
        Claim("empty", ())
