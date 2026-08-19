"""Computational Finance of Intelligence — shared research instrumentation.

This package is the machine-side instrument for the CFI program's Paper II
track. It contains no experiment, no dataset, and no result: it is the
apparatus that a preregistered protocol would later drive.

Nothing here has passed the G3 protocol gate, so no estimand, threshold, or
inferential procedure is frozen in this code by design.
"""

from __future__ import annotations

from drl_cfi.coherence import (
    COHERENCE_TOLERANCE,
    CoherenceReport,
    audit_prices,
    payoff_matrix,
    portfolio_cost,
    portfolio_payoffs,
)
from drl_cfi.frames import (
    Frame,
    FrameEquivalenceError,
    FrameFamily,
    FramePair,
    PairedValuation,
    vanilla_option,
)
from drl_cfi.linalg import nnls, solve_least_squares
from drl_cfi.payoffs import (
    Claim,
    Leg,
    LegKind,
    equivalence_failure,
    equivalence_grid,
    is_payoff_equivalent,
    payoff_vector,
    state_grid,
)
from drl_cfi.pricing import (
    black_scholes,
    discount_factor,
    implied_volatility,
    no_arbitrage_bounds,
    price_claim,
    put_call_parity_residual,
)

__all__ = [
    "COHERENCE_TOLERANCE",
    "Claim",
    "CoherenceReport",
    "Frame",
    "FrameEquivalenceError",
    "FrameFamily",
    "FramePair",
    "Leg",
    "LegKind",
    "PairedValuation",
    "audit_prices",
    "black_scholes",
    "discount_factor",
    "equivalence_failure",
    "equivalence_grid",
    "implied_volatility",
    "is_payoff_equivalent",
    "nnls",
    "no_arbitrage_bounds",
    "payoff_matrix",
    "payoff_vector",
    "portfolio_cost",
    "portfolio_payoffs",
    "price_claim",
    "put_call_parity_residual",
    "solve_least_squares",
    "state_grid",
    "vanilla_option",
]
