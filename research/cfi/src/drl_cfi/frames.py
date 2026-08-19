"""Frame taxonomy and payoff-equivalent frame pairs (CFI-201).

The experimental claim Paper II wants to make is that *wording* moves a
valuation while the *payoff* is held fixed. The threat to that claim is
mundane: an author writes two descriptions, believes they are economically
identical, and is wrong. Every observed difference then measures the author's
error rather than the subject's framing sensitivity.

:class:`FramePair` closes that hole structurally. A pair cannot be constructed
unless the two claims are decided payoff-equivalent by the oracle in
:mod:`drl_cfi.payoffs`, and the text is carried alongside the claim rather than
being able to define it. Wording is therefore incapable of changing the payoff by
construction, which is a stronger guarantee than review.

The taxonomy below is **proposed, not frozen**. Fixing the frame families is a
protocol decision behind the G3 gate, and this module deliberately provides no
inferential statistics for the same reason: paired differences are exposed as
raw observations, and estimands, intervals, and multiplicity corrections belong
to a preregistered plan that does not yet exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from drl_cfi.payoffs import Claim, LegKind, equivalence_failure


class FrameFamily(Enum):
    """Proposed families of payoff-preserving linguistic transformation.

    Each family names a contrast that prior work reports as behaviourally
    active. Membership is a property of the *description*; the payoff is
    identical across a pair by construction.
    """

    GAIN_LOSS = "gain_loss"
    INSURANCE_GAMBLE = "insurance_gamble"
    AGGREGATED_SEGREGATED = "aggregated_segregated"
    NARRATIVE_TECHNICAL = "narrative_technical"


@dataclass(frozen=True)
class Frame:
    """One natural-language rendering of a specific claim."""

    frame_id: str
    family: FrameFamily
    text: str
    claim: Claim

    def __post_init__(self) -> None:
        if not self.frame_id:
            raise ValueError("frame_id must be non-empty")
        if not self.text.strip():
            raise ValueError(f"frame {self.frame_id!r} has empty text")


class FrameEquivalenceError(ValueError):
    """Two frames proposed as a pair do not describe the same payoff."""


@dataclass(frozen=True)
class FramePair:
    """Two descriptions of one payoff, verified equivalent at construction."""

    pair_id: str
    left: Frame
    right: Frame

    def __post_init__(self) -> None:
        if not self.pair_id:
            raise ValueError("pair_id must be non-empty")
        reason = equivalence_failure(self.left.claim, self.right.claim)
        if reason is not None:
            raise FrameEquivalenceError(
                f"frame pair {self.pair_id!r} does not hold payoff fixed: {reason}"
            )
        if self.left.text.strip() == self.right.text.strip():
            raise ValueError(
                f"frame pair {self.pair_id!r} uses identical text, so it varies nothing"
            )

    def families(self) -> tuple[FrameFamily, FrameFamily]:
        """The two frame families being contrasted."""
        return self.left.family, self.right.family


def vanilla_option(claim: Claim) -> tuple[bool, float] | None:
    """Return ``(is_call, strike)`` if ``claim`` is a single unit vanilla option.

    Implied volatility is only defined for a single vanilla option, so callers
    use this to decide whether an implied-volatility comparison is meaningful
    for a given claim rather than assuming it is.
    """
    if len(claim.legs) != 1:
        return None
    leg = claim.legs[0]
    if leg.kind not in (LegKind.CALL, LegKind.PUT) or leg.quantity != 1.0:
        return None
    strike = leg.strike
    if strike is None:
        return None
    return leg.kind is LegKind.CALL, strike


@dataclass(frozen=True)
class PairedValuation:
    """One subject's elicited values for both sides of a frame pair.

    ``oracle_price`` is the model value of the shared payoff. It is recorded on
    the observation rather than recomputed later so that a stored result cannot
    silently change when pricing inputs are edited.
    """

    pair_id: str
    subject_id: str
    left_value: float
    right_value: float
    oracle_price: float

    @property
    def framing_difference(self) -> float:
        """Raw paired difference ``left - right``.

        This is an observation, not an estimate. Aggregating these into an effect
        requires the frozen analysis plan behind G3.
        """
        return self.left_value - self.right_value

    def distortion(self) -> tuple[float, float]:
        """Signed deviation of each side from the oracle price."""
        return self.left_value - self.oracle_price, self.right_value - self.oracle_price
