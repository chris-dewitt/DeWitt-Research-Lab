"""Deterministic pricing and replication oracle for Paper II (CFI-202).

Nothing here is a contribution to finance. Black-Scholes and put-call parity are
used only as a *normative oracle*: a price that is correct under stated
assumptions, against which an elicited valuation can be scored. Representing any
of this as new pricing theory would be a category error, and the novelty review
records it as one.

All assumptions are the textbook ones — a single non-dividend-paying underlying,
constant risk-free rate and volatility, frictionless trading, European exercise.
They are stated rather than satisfied; the oracle is exact for the model, and the
model is an idealisation.
"""

from __future__ import annotations

from math import erf, exp, log, sqrt

from drl_cfi.payoffs import Claim, LegKind

# Volatilities outside this bracket are not economically meaningful for the
# task family and bound the implied-volatility search.
MIN_VOLATILITY = 1e-9
MAX_VOLATILITY = 10.0
IMPLIED_VOLATILITY_TOLERANCE = 1e-10
IMPLIED_VOLATILITY_MAX_STEPS = 200


class PricingError(ValueError):
    """A pricing input was outside the model's stated domain."""


def norm_cdf(value: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + erf(value / sqrt(2.0)))


def discount_factor(rate: float, time_to_expiry: float) -> float:
    """Present value of one currency unit paid at ``time_to_expiry``."""
    if time_to_expiry < 0.0:
        raise PricingError(f"time_to_expiry must be non-negative, got {time_to_expiry}")
    return exp(-rate * time_to_expiry)


def _validate(spot: float, strike: float, time_to_expiry: float, volatility: float) -> None:
    if spot < 0.0:
        raise PricingError(f"spot must be non-negative, got {spot}")
    if strike < 0.0:
        raise PricingError(f"strike must be non-negative, got {strike}")
    if time_to_expiry < 0.0:
        raise PricingError(f"time_to_expiry must be non-negative, got {time_to_expiry}")
    if volatility < 0.0:
        raise PricingError(f"volatility must be non-negative, got {volatility}")


def _degenerate_price(
    spot: float, strike: float, rate: float, time_to_expiry: float, *, is_call: bool
) -> float:
    """Price with zero volatility or zero time: the payoff is already determined."""
    forward = spot * exp(rate * time_to_expiry)
    intrinsic = max(forward - strike, 0.0) if is_call else max(strike - forward, 0.0)
    return discount_factor(rate, time_to_expiry) * intrinsic


def black_scholes(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_expiry: float,
    *,
    is_call: bool,
) -> float:
    """European option value under the stated Black-Scholes assumptions."""
    _validate(spot, strike, time_to_expiry, volatility)
    if time_to_expiry == 0.0 or volatility <= MIN_VOLATILITY or spot == 0.0 or strike == 0.0:
        if spot == 0.0:
            return 0.0 if is_call else discount_factor(rate, time_to_expiry) * strike
        if strike == 0.0:
            return spot if is_call else 0.0
        return _degenerate_price(spot, strike, rate, time_to_expiry, is_call=is_call)

    spread = volatility * sqrt(time_to_expiry)
    d1 = (log(spot / strike) + (rate + 0.5 * volatility * volatility) * time_to_expiry) / spread
    d2 = d1 - spread
    discounted_strike = strike * discount_factor(rate, time_to_expiry)
    if is_call:
        return spot * norm_cdf(d1) - discounted_strike * norm_cdf(d2)
    return discounted_strike * norm_cdf(-d2) - spot * norm_cdf(-d1)


def price_claim(
    claim: Claim, spot: float, rate: float, volatility: float, time_to_expiry: float
) -> float:
    """Model value of a whole claim, summed leg by leg.

    Cash settles at expiry and is therefore discounted; the underlying is held
    outright and is worth spot, there being no dividend in the stated model.
    """
    total = 0.0
    for leg in claim.legs:
        if leg.kind is LegKind.CASH:
            total += leg.quantity * discount_factor(rate, time_to_expiry)
        elif leg.kind is LegKind.UNDERLYING:
            total += leg.quantity * spot
        else:
            strike = leg.strike
            if strike is None:
                raise PricingError(f"{leg.kind.value} leg is missing its strike")
            total += leg.quantity * black_scholes(
                spot, strike, rate, volatility, time_to_expiry, is_call=leg.kind is LegKind.CALL
            )
    return total


def put_call_parity_residual(
    spot: float, strike: float, rate: float, volatility: float, time_to_expiry: float
) -> float:
    """Return ``C - P - (S - K e^{-rT})``, which the model forces to zero.

    This is a replication invariant rather than a fitted relationship, so a
    non-zero residual indicates an implementation defect, not a market effect.
    """
    call = black_scholes(spot, strike, rate, volatility, time_to_expiry, is_call=True)
    put = black_scholes(spot, strike, rate, volatility, time_to_expiry, is_call=False)
    return call - put - (spot - strike * discount_factor(rate, time_to_expiry))


def no_arbitrage_bounds(
    spot: float, strike: float, rate: float, time_to_expiry: float, *, is_call: bool
) -> tuple[float, float]:
    """Return the ``(lower, upper)`` price bounds implied by replication alone.

    These hold for any arbitrage-free model, not only Black-Scholes, and bracket
    the implied-volatility search.
    """
    discounted_strike = strike * discount_factor(rate, time_to_expiry)
    if is_call:
        return max(spot - discounted_strike, 0.0), spot
    return max(discounted_strike - spot, 0.0), discounted_strike


def implied_volatility(
    observed_price: float,
    spot: float,
    strike: float,
    rate: float,
    time_to_expiry: float,
    *,
    is_call: bool,
) -> float | None:
    """Invert Black-Scholes for volatility, or return ``None`` if no root exists.

    Option value is strictly increasing in volatility, so bisection converges
    from the replication bounds without a derivative and without the failure
    modes Newton shows near zero vega. ``None`` means the observed price sits
    outside the no-arbitrage bounds — an incoherent quote rather than a hard
    numerical problem, and the caller should treat it as a finding, not an error.
    """
    _validate(spot, strike, time_to_expiry, 0.0)
    if time_to_expiry == 0.0:
        return None

    lower_bound, upper_bound = no_arbitrage_bounds(
        spot, strike, rate, time_to_expiry, is_call=is_call
    )
    if observed_price < lower_bound - IMPLIED_VOLATILITY_TOLERANCE:
        return None
    if observed_price > upper_bound + IMPLIED_VOLATILITY_TOLERANCE:
        return None

    low, high = MIN_VOLATILITY, MAX_VOLATILITY
    if black_scholes(spot, strike, rate, high, time_to_expiry, is_call=is_call) < observed_price:
        return None

    for _ in range(IMPLIED_VOLATILITY_MAX_STEPS):
        middle = 0.5 * (low + high)
        value = black_scholes(spot, strike, rate, middle, time_to_expiry, is_call=is_call)
        if abs(value - observed_price) <= IMPLIED_VOLATILITY_TOLERANCE:
            return middle
        if value < observed_price:
            low = middle
        else:
            high = middle
        if high - low <= IMPLIED_VOLATILITY_TOLERANCE:
            break
    return 0.5 * (low + high)
