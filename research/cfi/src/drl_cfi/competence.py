"""Numerical-competence screening for valuation subjects (Paper II).

Paper II attributes a difference between two payoff-equivalent descriptions to
the *wording*. That attribution only holds if the subject could price the claim
at all. If a subject cannot value the plain, unframed claim to within a stated
tolerance, a difference between its two framed answers is not evidence of
framing sensitivity — it is arithmetic noise wearing a framing costume.

The threat is documented rather than hypothetical. Levy (2026), *Caution Ahead:
Numerical Reasoning and Look-Ahead Bias in AI Models*, Journal of Accounting
Research 64(3):1139-1188, finds that language models "exhibit extremely poor
numerical reasoning" on accounting and finance tasks and concludes that
"application in these settings should proceed with caution." A framing study
that skips this check inherits that failure mode silently.

So competence is a **screen, not a covariate**: a subject that fails it is
excluded before its framed answers are counted, and the exclusion is recorded.
Screening after seeing the framed results would be an exclusion rule chosen with
knowledge of the outcome, which the research plan forbids.

Nothing here sets a threshold. The tolerance is an argument with a documented
default, and the value that governs a real study belongs to a preregistered
protocol that does not yet exist.
"""

from __future__ import annotations

from dataclasses import dataclass

# Default relative tolerance for the unframed control. Asserted from judgment as
# a starting value, exactly as the bake-off's thresholds were, and carrying the
# same caveat: it should be replaced by a value derived from observed spread
# once a pilot establishes what that spread is.
DEFAULT_RELATIVE_TOLERANCE = 0.10


@dataclass(frozen=True)
class CompetenceProbe:
    """A subject's attempt to price the unframed claim it will later see framed.

    ``oracle_price`` is the model value of the same claim. Both are recorded on
    the observation so a stored screen cannot change when pricing inputs are
    edited later.
    """

    subject_id: str
    claim_id: str
    reported_value: float
    oracle_price: float
    relative_tolerance: float = DEFAULT_RELATIVE_TOLERANCE

    def __post_init__(self) -> None:
        if not self.subject_id:
            raise ValueError("subject_id must be non-empty")
        if not self.claim_id:
            raise ValueError("claim_id must be non-empty")
        if self.relative_tolerance <= 0.0:
            raise ValueError(f"relative_tolerance must be positive, got {self.relative_tolerance}")

    @property
    def absolute_error(self) -> float:
        """Unsigned distance between the reported value and the oracle price."""
        return abs(self.reported_value - self.oracle_price)

    @property
    def relative_error(self) -> float:
        """Absolute error as a fraction of the oracle price.

        A zero-priced claim has no meaningful relative error, so it reports
        infinity rather than dividing by zero — a subject cannot be shown
        competent on a claim worth nothing.
        """
        if self.oracle_price == 0.0:
            return float("inf")
        return self.absolute_error / abs(self.oracle_price)

    @property
    def is_competent(self) -> bool:
        """True when the subject priced the unframed claim within tolerance."""
        return self.relative_error <= self.relative_tolerance

    def exclusion_reason(self) -> str | None:
        """Why this subject is excluded, or ``None`` if it is retained.

        The reason is recorded rather than reduced to a boolean so an excluded
        subject can be audited without rerunning the screen.
        """
        if self.is_competent:
            return None
        if self.oracle_price == 0.0:
            return (
                f"{self.subject_id} cannot be screened on {self.claim_id}: "
                "the oracle price is zero, so relative error is undefined"
            )
        return (
            f"{self.subject_id} priced {self.claim_id} at {self.reported_value:.4f} "
            f"against an oracle price of {self.oracle_price:.4f} — relative error "
            f"{self.relative_error:.3f} exceeds the {self.relative_tolerance:.3f} tolerance"
        )


@dataclass(frozen=True)
class ScreenedCohort:
    """The outcome of screening a set of subjects, retaining both sides."""

    retained: tuple[str, ...]
    excluded: tuple[tuple[str, str], ...]

    @property
    def retention_rate(self) -> float:
        """Fraction of screened subjects retained; 0.0 when none were screened."""
        total = len(self.retained) + len(self.excluded)
        if total == 0:
            return 0.0
        return len(self.retained) / total


def screen(probes: tuple[CompetenceProbe, ...]) -> ScreenedCohort:
    """Partition subjects into retained and excluded, keeping the reasons.

    Excluded subjects are returned rather than discarded. A study that reports
    only its retained cohort has hidden its exclusion rate, and the exclusion
    rate is itself a finding — a screen that removes most subjects says
    something about the instrument, not only about the subjects.
    """
    retained: list[str] = []
    excluded: list[tuple[str, str]] = []
    for probe in probes:
        reason = probe.exclusion_reason()
        if reason is None:
            retained.append(probe.subject_id)
        else:
            excluded.append((probe.subject_id, reason))
    return ScreenedCohort(retained=tuple(retained), excluded=tuple(excluded))
