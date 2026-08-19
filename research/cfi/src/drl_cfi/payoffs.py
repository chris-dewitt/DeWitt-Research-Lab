"""Payoff primitives and the deterministic payoff-equivalence oracle (CFI-201/202).

Paper II compares how a subject values the *same* economic payoff under
different descriptions. That design is only valid if "the same payoff" is a
decidable property rather than an author's assertion, so equivalence here is
decided structurally on the payoff function and never on the wording.

Every primitive is continuous and piecewise linear in the terminal price, with
kinks only at strikes. That restriction is deliberate. Two continuous piecewise
linear functions whose kinks lie in a known finite set are identical everywhere
on an interval if and only if they agree at every kink and at one interior point
of each maximal affine piece — a finite, exact check. Digital and barrier
payoffs are excluded precisely because their discontinuities would break that
proof and force equivalence back onto sampling, which can only ever be evidence
of equivalence rather than a decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

# Payoffs are compared in currency units; this tolerance is far below the
# smallest price difference any elicitation could meaningfully report.
PAYOFF_TOLERANCE = 1e-9


class LegKind(Enum):
    """The piecewise-linear primitives a claim may be built from."""

    CASH = "cash"
    UNDERLYING = "underlying"
    CALL = "call"
    PUT = "put"


@dataclass(frozen=True)
class Leg:
    """One primitive position: ``quantity`` units of ``kind`` struck at ``strike``.

    ``strike`` must be ``None`` for cash and the underlying, and a non-negative
    number for options. A negative ``quantity`` is a short position.
    """

    kind: LegKind
    quantity: float = 1.0
    strike: float | None = None

    def __post_init__(self) -> None:
        needs_strike = self.kind in (LegKind.CALL, LegKind.PUT)
        if needs_strike and self.strike is None:
            raise ValueError(f"{self.kind.value} leg requires a strike")
        if not needs_strike and self.strike is not None:
            raise ValueError(f"{self.kind.value} leg must not carry a strike")
        if self.strike is not None and self.strike < 0.0:
            raise ValueError(f"strike must be non-negative, got {self.strike}")

    def payoff_at(self, terminal_price: float) -> float:
        """Value of this leg if the underlying settles at ``terminal_price``."""
        if self.kind is LegKind.CASH:
            return self.quantity
        if self.kind is LegKind.UNDERLYING:
            return self.quantity * terminal_price
        strike = self.strike
        if strike is None:  # unreachable: __post_init__ requires a strike here
            raise ValueError(f"{self.kind.value} leg lost its strike")
        if self.kind is LegKind.CALL:
            return self.quantity * max(terminal_price - strike, 0.0)
        return self.quantity * max(strike - terminal_price, 0.0)

    def terminal_slope(self) -> float:
        """Slope of this leg's payoff for terminal prices above every strike."""
        if self.kind is LegKind.CASH:
            return 0.0
        if self.kind is LegKind.UNDERLYING:
            return self.quantity
        if self.kind is LegKind.CALL:
            return self.quantity
        return 0.0


@dataclass(frozen=True)
class Claim:
    """A portfolio of legs, identified for experimental bookkeeping."""

    claim_id: str
    legs: tuple[Leg, ...]

    def __post_init__(self) -> None:
        if not self.claim_id:
            raise ValueError("claim_id must be non-empty")
        if not self.legs:
            raise ValueError(f"claim {self.claim_id!r} has no legs")

    def payoff_at(self, terminal_price: float) -> float:
        """Total payoff if the underlying settles at ``terminal_price``."""
        return sum(leg.payoff_at(terminal_price) for leg in self.legs)

    def terminal_slope(self) -> float:
        """Asymptotic slope of the payoff as the terminal price grows."""
        return sum(leg.terminal_slope() for leg in self.legs)

    def kinks(self) -> tuple[float, ...]:
        """Sorted distinct strikes, which are the only points where slope changes."""
        return tuple(sorted({leg.strike for leg in self.legs if leg.strike is not None}))


def equivalence_grid(*claims: Claim) -> tuple[float, ...]:
    """Return the finite set of terminal prices that decides equivalence exactly.

    The grid holds zero, every kink of every claim, the midpoint of each pair of
    adjacent kinks, and one point above the largest kink. Agreement on this grid
    plus agreement of terminal slopes is necessary and sufficient for the claims
    to have identical payoffs on ``[0, inf)``.
    """
    if not claims:
        raise ValueError("equivalence_grid requires at least one claim")
    kinks = sorted({kink for claim in claims for kink in claim.kinks()})
    points: list[float] = [0.0]
    points.extend(kinks)
    for lower, upper in zip(kinks, kinks[1:], strict=False):
        points.append((lower + upper) / 2.0)
    highest = kinks[-1] if kinks else 0.0
    points.append(highest + 1.0)
    return tuple(sorted(set(points)))


def payoff_vector(claim: Claim, grid: tuple[float, ...]) -> list[float]:
    """Evaluate ``claim`` at every point of ``grid``."""
    return [claim.payoff_at(price) for price in grid]


def is_payoff_equivalent(left: Claim, right: Claim, *, tolerance: float = PAYOFF_TOLERANCE) -> bool:
    """Decide whether two claims have identical payoffs at every terminal price.

    This is a decision, not a sample: see the module docstring for why the finite
    grid suffices. The terminal slopes are compared separately because the grid
    cannot by itself constrain behaviour above its largest point.
    """
    grid = equivalence_grid(left, right)
    if abs(left.terminal_slope() - right.terminal_slope()) > tolerance:
        return False
    return all(abs(left.payoff_at(price) - right.payoff_at(price)) <= tolerance for price in grid)


def equivalence_failure(
    left: Claim, right: Claim, *, tolerance: float = PAYOFF_TOLERANCE
) -> str | None:
    """Return a human-readable reason the claims differ, or ``None`` if equivalent.

    Used when constructing frame pairs so that a rejected pair explains itself
    rather than surfacing as a bare assertion error.
    """
    slope_gap = left.terminal_slope() - right.terminal_slope()
    if abs(slope_gap) > tolerance:
        return (
            f"terminal slopes differ by {slope_gap:.6g}: "
            f"{left.claim_id}={left.terminal_slope():.6g}, "
            f"{right.claim_id}={right.terminal_slope():.6g}"
        )
    for price in equivalence_grid(left, right):
        gap = left.payoff_at(price) - right.payoff_at(price)
        if abs(gap) > tolerance:
            return (
                f"payoffs differ by {gap:.6g} at terminal price {price:.6g}: "
                f"{left.claim_id}={left.payoff_at(price):.6g}, "
                f"{right.claim_id}={right.payoff_at(price):.6g}"
            )
    return None


def state_grid(*claims: Claim, upper_multiple: float = 2.0) -> tuple[float, ...]:
    """Build the finite state space used for arbitrage and coherence work.

    A portfolio of these claims is affine between adjacent grid points, and an
    affine function attains its extremes at the endpoints of an interval, so
    non-negativity on the grid certifies non-negativity across the whole spanned
    range. Behaviour above the largest grid point is *not* certified by the grid
    alone, which is why callers must also inspect the terminal slope; see
    :func:`drl_cfi.coherence.detect_arbitrage`.
    """
    if upper_multiple <= 1.0:
        raise ValueError("upper_multiple must exceed 1.0 so the grid extends past the largest kink")
    base = list(equivalence_grid(*claims))
    highest = max(base)
    base.append(max(highest * upper_multiple, highest + 1.0))
    return tuple(sorted(set(base)))
