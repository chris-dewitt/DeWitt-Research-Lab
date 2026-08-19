"""Arbitrage detection and coherence repair for elicited prices (CFI-204).

The novelty review is explicit that Dutch-book auditing and projection repair are
**baselines** here, not the contribution, and that prior work already separates
coherence from calibration. This module therefore aims at being a correct,
inspectable reimplementation with an exact certificate — not at novelty.

Formally: with a finite state space, a price vector admits no arbitrage exactly
when it is a non-negatively weighted combination of the claims' state payoffs.
Writing ``A`` for the claims-by-states payoff matrix, the coherent set is the
closed convex cone ``C = {A q : q >= 0}``. Deciding membership, repairing a
violation, measuring the repair distance, and extracting the exploiting
portfolio are then all consequences of one projection, which is a non-negative
least-squares problem.

Two deliberate choices are worth stating because they bound what the certificate
means:

* The cone uses ``q >= 0`` rather than ``q > 0``. The strictly-positive set is
  not closed, so projection onto it is not well defined; the closure is the
  right object. The cost is that a *weak* arbitrage — zero cost, non-negative
  payoff, strictly positive somewhere — sits on the boundary and reports as
  coherent. That is a real limitation, not a rounding artifact.
* Non-negativity is certified on the state grid. A portfolio of piecewise-linear
  claims is affine between adjacent grid points and an affine function attains
  its extremes at the endpoints, so grid non-negativity does certify
  non-negativity across the spanned range. Above the largest grid point nothing
  is certified by the grid, so the terminal slope is reported separately.
"""

from __future__ import annotations

from dataclasses import dataclass

from drl_cfi.linalg import Matrix, Vector, mat_t_vec, mat_vec, nnls, norm
from drl_cfi.payoffs import Claim, payoff_vector, state_grid

# Residuals below this are treated as coherent. Set well above the accumulated
# floating-point error of the projection at the problem sizes used here.
COHERENCE_TOLERANCE = 1e-8


@dataclass(frozen=True)
class CoherenceReport:
    """The outcome of auditing one set of quoted prices against one claim set."""

    claim_ids: tuple[str, ...]
    grid: tuple[float, ...]
    quoted_prices: Vector
    repaired_prices: Vector
    state_prices: Vector
    repair_distance: float
    exploiting_portfolio: Vector
    arbitrage_profit: float
    terminal_slope: float

    @property
    def is_coherent(self) -> bool:
        """True when the quoted prices already admit no arbitrage on the grid."""
        return self.repair_distance <= COHERENCE_TOLERANCE

    @property
    def certificate_is_grid_bounded(self) -> bool:
        """True when the exploiting portfolio's payoff is not certified past the grid.

        A negative terminal slope means the portfolio's payoff eventually falls
        below zero above the largest grid point, so the arbitrage is only
        certified across the spanned range and the grid should be widened before
        the finding is reported as unconditional.
        """
        return not self.is_coherent and self.terminal_slope < -COHERENCE_TOLERANCE

    def implied_distribution(self) -> Vector | None:
        """Normalise the state prices into a risk-neutral distribution.

        Returns ``None`` when the state prices sum to zero, which happens only if
        every quoted price projects to zero and there is no distribution to read.
        """
        total = sum(self.state_prices)
        if total <= COHERENCE_TOLERANCE:
            return None
        return [price / total for price in self.state_prices]


def payoff_matrix(claims: tuple[Claim, ...], grid: tuple[float, ...]) -> Matrix:
    """Build the claims-by-states payoff matrix."""
    return [payoff_vector(claim, grid) for claim in claims]


def audit_prices(
    claims: tuple[Claim, ...],
    quoted_prices: Vector,
    *,
    grid: tuple[float, ...] | None = None,
) -> CoherenceReport:
    """Audit ``quoted_prices`` for arbitrage and compute the minimal repair.

    The repair is the Euclidean projection onto the coherent cone, so it is the
    smallest price change that removes the violation. The exploiting portfolio is
    the negated residual: it costs a negative amount, meaning it pays the holder
    up front, and its payoff is non-negative in every state on the grid.
    """
    if not claims:
        raise ValueError("audit_prices requires at least one claim")
    if len(quoted_prices) != len(claims):
        raise ValueError(
            f"expected one price per claim: {len(claims)} claims, {len(quoted_prices)} prices"
        )

    resolved_grid = grid if grid is not None else state_grid(*claims)
    matrix = payoff_matrix(claims, resolved_grid)

    state_prices = nnls(matrix, quoted_prices)
    repaired = mat_vec(matrix, state_prices)
    residual = [
        quoted - repaired_price
        for quoted, repaired_price in zip(quoted_prices, repaired, strict=True)
    ]
    distance = norm(residual)

    # x = -residual costs -||residual||^2 (it pays the holder) and, because the
    # residual lies in the polar cone, pays >= 0 in every state on the grid.
    exploiting = [-value for value in residual]
    profit = distance * distance
    slope = sum(
        weight * claim.terminal_slope() for weight, claim in zip(exploiting, claims, strict=True)
    )

    return CoherenceReport(
        claim_ids=tuple(claim.claim_id for claim in claims),
        grid=resolved_grid,
        quoted_prices=list(quoted_prices),
        repaired_prices=repaired,
        state_prices=state_prices,
        repair_distance=distance,
        exploiting_portfolio=exploiting,
        arbitrage_profit=profit,
        terminal_slope=slope,
    )


def portfolio_payoffs(
    claims: tuple[Claim, ...], portfolio: Vector, grid: tuple[float, ...]
) -> Vector:
    """Payoff of ``portfolio`` in every state of ``grid``."""
    return mat_t_vec(payoff_matrix(claims, grid), portfolio)


def portfolio_cost(prices: Vector, portfolio: Vector) -> float:
    """Cost of entering ``portfolio`` at ``prices``; negative means cash received."""
    return sum(price * weight for price, weight in zip(prices, portfolio, strict=True))
