"""The normative pricing oracle and its replication invariants."""

from __future__ import annotations

from math import exp

import pytest
from drl_cfi.payoffs import Claim, Leg, LegKind
from drl_cfi.pricing import (
    PricingError,
    black_scholes,
    discount_factor,
    implied_volatility,
    no_arbitrage_bounds,
    norm_cdf,
    price_claim,
    put_call_parity_residual,
)

SPOT = 100.0
RATE = 0.03
VOLATILITY = 0.25
EXPIRY = 0.75


def test_norm_cdf_matches_known_values() -> None:
    assert norm_cdf(0.0) == pytest.approx(0.5, abs=1e-12)
    assert norm_cdf(-8.0) == pytest.approx(0.0, abs=1e-12)
    assert norm_cdf(8.0) == pytest.approx(1.0, abs=1e-12)


@pytest.mark.parametrize("strike", [50.0, 90.0, 100.0, 110.0, 200.0])
def test_put_call_parity_residual_is_zero(strike: float) -> None:
    """Parity is a replication identity, so a residual would be an implementation bug."""
    residual = put_call_parity_residual(SPOT, strike, RATE, VOLATILITY, EXPIRY)
    assert residual == pytest.approx(0.0, abs=1e-10)


@pytest.mark.parametrize("is_call", [True, False])
def test_prices_respect_the_replication_bounds(is_call: bool) -> None:
    for strike in (60.0, 100.0, 150.0):
        price = black_scholes(SPOT, strike, RATE, VOLATILITY, EXPIRY, is_call=is_call)
        lower, upper = no_arbitrage_bounds(SPOT, strike, RATE, EXPIRY, is_call=is_call)
        assert lower - 1e-12 <= price <= upper + 1e-12


def test_call_value_decreases_with_strike() -> None:
    strikes = [80.0, 90.0, 100.0, 110.0, 120.0]
    values = [black_scholes(SPOT, k, RATE, VOLATILITY, EXPIRY, is_call=True) for k in strikes]
    assert all(earlier > later for earlier, later in zip(values, values[1:], strict=False))


def test_call_value_is_convex_in_strike() -> None:
    """Convexity is what makes a butterfly spread non-negative in price as well as payoff."""
    low, middle, high = 90.0, 100.0, 110.0
    butterfly = (
        black_scholes(SPOT, low, RATE, VOLATILITY, EXPIRY, is_call=True)
        - 2.0 * black_scholes(SPOT, middle, RATE, VOLATILITY, EXPIRY, is_call=True)
        + black_scholes(SPOT, high, RATE, VOLATILITY, EXPIRY, is_call=True)
    )
    assert butterfly >= -1e-12


def test_call_value_increases_with_volatility() -> None:
    values = [
        black_scholes(SPOT, SPOT, RATE, sigma, EXPIRY, is_call=True)
        for sigma in (0.05, 0.15, 0.30, 0.60)
    ]
    assert all(earlier < later for earlier, later in zip(values, values[1:], strict=False))


def test_zero_time_collapses_to_intrinsic_value() -> None:
    assert black_scholes(120.0, 100.0, RATE, VOLATILITY, 0.0, is_call=True) == pytest.approx(20.0)
    assert black_scholes(80.0, 100.0, RATE, VOLATILITY, 0.0, is_call=True) == pytest.approx(0.0)
    assert black_scholes(80.0, 100.0, RATE, VOLATILITY, 0.0, is_call=False) == pytest.approx(20.0)


def test_zero_volatility_prices_the_discounted_forward() -> None:
    """With no volatility the payoff is already determined by the forward."""
    forward = SPOT * exp(RATE * EXPIRY)
    expected = discount_factor(RATE, EXPIRY) * max(forward - 90.0, 0.0)
    assert black_scholes(SPOT, 90.0, RATE, 0.0, EXPIRY, is_call=True) == pytest.approx(expected)


def test_negative_inputs_are_rejected() -> None:
    with pytest.raises(PricingError):
        black_scholes(-1.0, 100.0, RATE, VOLATILITY, EXPIRY, is_call=True)
    with pytest.raises(PricingError):
        black_scholes(SPOT, 100.0, RATE, VOLATILITY, -1.0, is_call=True)


def test_price_claim_sums_legs_and_discounts_cash() -> None:
    claim = Claim(
        "call-plus-cash",
        (
            Leg(kind=LegKind.CALL, strike=100.0),
            Leg(kind=LegKind.CASH, quantity=100.0),
        ),
    )
    expected = black_scholes(
        SPOT, 100.0, RATE, VOLATILITY, EXPIRY, is_call=True
    ) + 100.0 * discount_factor(RATE, EXPIRY)
    assert price_claim(claim, SPOT, RATE, VOLATILITY, EXPIRY) == pytest.approx(expected)


def test_price_claim_agrees_with_parity_on_equivalent_portfolios() -> None:
    """Protective put and call-plus-cash are payoff-equivalent, so they must price alike."""
    protective = Claim(
        "protective-put",
        (Leg(kind=LegKind.UNDERLYING), Leg(kind=LegKind.PUT, strike=100.0)),
    )
    equivalent = Claim(
        "call-plus-cash",
        (Leg(kind=LegKind.CALL, strike=100.0), Leg(kind=LegKind.CASH, quantity=100.0)),
    )
    left = price_claim(protective, SPOT, RATE, VOLATILITY, EXPIRY)
    right = price_claim(equivalent, SPOT, RATE, VOLATILITY, EXPIRY)
    assert left == pytest.approx(right, abs=1e-10)


@pytest.mark.parametrize("is_call", [True, False])
@pytest.mark.parametrize("target_volatility", [0.08, 0.25, 0.75])
def test_implied_volatility_round_trips(is_call: bool, target_volatility: float) -> None:
    price = black_scholes(SPOT, 105.0, RATE, target_volatility, EXPIRY, is_call=is_call)
    recovered = implied_volatility(price, SPOT, 105.0, RATE, EXPIRY, is_call=is_call)
    assert recovered is not None
    assert recovered == pytest.approx(target_volatility, abs=1e-6)


def test_implied_volatility_returns_none_outside_the_bounds() -> None:
    """A quote below intrinsic is an incoherent price, reported rather than raised."""
    _, upper = no_arbitrage_bounds(SPOT, 100.0, RATE, EXPIRY, is_call=True)
    assert implied_volatility(upper + 5.0, SPOT, 100.0, RATE, EXPIRY, is_call=True) is None
    assert implied_volatility(-1.0, SPOT, 100.0, RATE, EXPIRY, is_call=True) is None


def test_implied_volatility_is_undefined_at_expiry() -> None:
    assert implied_volatility(5.0, SPOT, 100.0, RATE, 0.0, is_call=True) is None
