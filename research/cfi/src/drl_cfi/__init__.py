"""Computational Finance of Intelligence — shared research instrumentation.

This package is the machine-side instrument for the CFI program's Paper II
track. It contains no experiment, no dataset, and no result: it is the
apparatus that a preregistered protocol would later drive.

Nothing here has passed the G3 protocol gate, so no estimand, threshold, or
inferential procedure is frozen in this code by design.
"""

from __future__ import annotations

from drl_cfi.baselines import (
    MAX_REPRESENTABLE_LOG_ODDS,
    AsymmetricBayesianFit,
    BayesianFit,
    DiffusionFit,
    JumpDiffusionFit,
    OrnsteinUhlenbeckFit,
    ParameterRecovery,
    RecoveryReport,
    SaturatedBeliefError,
    fit_asymmetric_bayesian,
    fit_bayesian,
    fit_diffusion,
    fit_jump_diffusion,
    fit_ornstein_uhlenbeck,
    recovery_study,
    simulate_asymmetric_bayesian,
    simulate_bayesian,
    simulate_diffusion,
    simulate_jump_diffusion,
    simulate_ornstein_uhlenbeck,
)
from drl_cfi.beliefs import (
    Action,
    BeliefEvent,
    BeliefTrajectory,
    Maturity,
    SchemaError,
    SubjectKind,
    log_odds,
    probability,
)
from drl_cfi.coherence import (
    COHERENCE_TOLERANCE,
    CoherenceReport,
    audit_prices,
    payoff_matrix,
    portfolio_cost,
    portfolio_payoffs,
)
from drl_cfi.competence import (
    DEFAULT_RELATIVE_TOLERANCE,
    CompetenceProbe,
    ScreenedCohort,
    screen,
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
    "Action",
    "AsymmetricBayesianFit",
    "BayesianFit",
    "BeliefEvent",
    "BeliefTrajectory",
    "COHERENCE_TOLERANCE",
    "Claim",
    "CoherenceReport",
    "CompetenceProbe",
    "DEFAULT_RELATIVE_TOLERANCE",
    "DiffusionFit",
    "Frame",
    "FrameEquivalenceError",
    "FrameFamily",
    "FramePair",
    "JumpDiffusionFit",
    "Leg",
    "LegKind",
    "MAX_REPRESENTABLE_LOG_ODDS",
    "Maturity",
    "OrnsteinUhlenbeckFit",
    "PairedValuation",
    "ParameterRecovery",
    "RecoveryReport",
    "SaturatedBeliefError",
    "SchemaError",
    "ScreenedCohort",
    "SubjectKind",
    "audit_prices",
    "black_scholes",
    "discount_factor",
    "equivalence_failure",
    "equivalence_grid",
    "fit_asymmetric_bayesian",
    "fit_bayesian",
    "fit_diffusion",
    "fit_jump_diffusion",
    "fit_ornstein_uhlenbeck",
    "implied_volatility",
    "is_payoff_equivalent",
    "log_odds",
    "nnls",
    "no_arbitrage_bounds",
    "payoff_matrix",
    "payoff_vector",
    "portfolio_cost",
    "portfolio_payoffs",
    "price_claim",
    "probability",
    "put_call_parity_residual",
    "recovery_study",
    "screen",
    "simulate_asymmetric_bayesian",
    "simulate_bayesian",
    "simulate_diffusion",
    "simulate_jump_diffusion",
    "simulate_ornstein_uhlenbeck",
    "solve_least_squares",
    "state_grid",
    "vanilla_option",
]
