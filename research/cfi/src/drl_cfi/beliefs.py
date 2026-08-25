"""Observable belief-event records and trajectories — the CFI-004 schema.

This is the common data contract from `COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md`
§4, made executable. One `BeliefEvent` is one observation of one subject's
reported belief about one proposition at one step; a `BeliefTrajectory` is the
ordered sequence of those observations that the bridge's baselines consume.

Three constraints are enforced here rather than left to the analyst, because
each one silently corrupts an estimate rather than raising:

*Probabilities strictly inside the unit interval.* The bridge models belief in
log-odds, and `log(p / (1 - p))` is undefined at both ends. A subject who
reports certainty is a real and interesting event, but it is not representable
in this parameterisation, so it is rejected at the boundary rather than clipped
to an arbitrary epsilon that would then be read back as data.

*Monotone step index and non-decreasing event time.* Every estimator in
`baselines` reads consecutive differences. An out-of-order record does not fail
loudly there; it contributes a spurious increment of the wrong sign.

*Lineage on every record.* `source_rights_id`, `code_revision`, `config_digest`,
and `seed` are required, not optional, so that a trajectory cannot reach an
estimator without carrying the means to reproduce and to check its rights
provenance. Synthetic data carries them too — `maturity` says which it is.

Nothing here has passed G2. `SubjectKind.HUMAN` exists because the schema must
be able to describe human records; constructing one is not authorisation to
collect any.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from enum import StrEnum

__all__ = [
    "Action",
    "BeliefEvent",
    "BeliefTrajectory",
    "Maturity",
    "SchemaError",
    "SubjectKind",
    "log_odds",
    "probability",
]


class SchemaError(ValueError):
    """A record or trajectory violates the observable data contract."""


class SubjectKind(StrEnum):
    """What produced the report. §4 `subject_kind`."""

    HUMAN = "human"
    MODEL = "model"
    POLICY = "policy"
    MARKET = "market"
    SIMULATOR = "simulator"


class Action(StrEnum):
    """What the subject did at this step. §4 `action`."""

    CONTINUE = "continue"
    STOP = "stop"
    ACQUIRE = "acquire"
    PRICE = "price"
    TRADE = "trade"
    DEFER = "defer"
    ABSTAIN = "abstain"


class Maturity(StrEnum):
    """How far through the lifecycle this record's study is. §4 `maturity`.

    The ordering is deliberate and is not a quality ranking: `SYNTHETIC` is the
    only value the bridge's own recovery studies may carry, because no gate has
    cleared anything else.
    """

    SYNTHETIC = "synthetic"
    PILOT = "pilot"
    FROZEN = "frozen"
    CONFIRMATORY = "confirmatory"
    REPLICATION = "replication"


def log_odds(p: float) -> float:
    """Convert a reported probability to log-odds.

    Raises rather than clipping at the boundary. See the module docstring.
    """
    if not math.isfinite(p):
        raise SchemaError(f"reported_probability must be finite, got {p!r}")
    if not 0.0 < p < 1.0:
        raise SchemaError(
            f"reported_probability must lie strictly inside (0, 1) to be "
            f"representable in log-odds, got {p!r}"
        )
    return math.log(p / (1.0 - p))


def probability(ell: float) -> float:
    """Invert :func:`log_odds`. Saturates gracefully for large magnitudes."""
    if not math.isfinite(ell):
        raise SchemaError(f"log-odds must be finite, got {ell!r}")
    if ell >= 0.0:
        return 1.0 / (1.0 + math.exp(-ell))
    scaled = math.exp(ell)
    return scaled / (1.0 + scaled)


@dataclass(frozen=True, slots=True)
class BeliefEvent:
    """One observation of one subject's belief about one proposition.

    Field names track §4 exactly so that a record can be read against the
    written contract without a translation table.
    """

    study_id: str
    run_id: str
    subject_id: str
    subject_kind: SubjectKind
    model_or_cohort_revision: str
    task_id: str
    proposition_id: str
    step_index: int
    event_time: float
    reported_probability: float
    action: Action
    source_rights_id: str
    code_revision: str
    config_digest: str
    seed: int
    maturity: Maturity
    evidence_id: str | None = None
    frame_id: str | None = None
    action_cost: float | None = None
    outcome: bool | None = None

    def __post_init__(self) -> None:
        for name in (
            "study_id",
            "run_id",
            "subject_id",
            "task_id",
            "proposition_id",
            "model_or_cohort_revision",
            "source_rights_id",
            "code_revision",
            "config_digest",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise SchemaError(f"{name} is required and must be a non-empty string")
        if self.step_index < 0:
            raise SchemaError(f"step_index must be non-negative, got {self.step_index}")
        if not math.isfinite(self.event_time):
            raise SchemaError(f"event_time must be finite, got {self.event_time!r}")
        if self.action_cost is not None:
            if not math.isfinite(self.action_cost) or self.action_cost < 0.0:
                raise SchemaError(
                    f"action_cost must be a finite non-negative number when declared, "
                    f"got {self.action_cost!r}"
                )
        # Validates the probability and, as a side effect, proves the record can
        # be projected into the space the baselines actually work in.
        log_odds(self.reported_probability)

    @property
    def log_odds(self) -> float:
        """This record's belief in the bridge's parameterisation."""
        return log_odds(self.reported_probability)

    @property
    def is_synthetic(self) -> bool:
        """True when no gate is implicated by using this record."""
        return self.maturity is Maturity.SYNTHETIC


@dataclass(frozen=True, slots=True)
class BeliefTrajectory:
    """One subject's ordered belief path over one proposition.

    Construction enforces that the events belong together and are in order.
    Estimators may then read consecutive differences without re-checking.
    """

    events: tuple[BeliefEvent, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if len(self.events) < 2:
            raise SchemaError(
                f"a trajectory needs at least two events to carry an increment, "
                f"got {len(self.events)}"
            )
        first = self.events[0]
        for event in self.events[1:]:
            for name in ("study_id", "run_id", "subject_id", "proposition_id"):
                if getattr(event, name) != getattr(first, name):
                    raise SchemaError(
                        f"a trajectory is one subject on one proposition; {name} "
                        f"differs: {getattr(first, name)!r} vs {getattr(event, name)!r}"
                    )
        for earlier, later in zip(self.events, self.events[1:], strict=False):
            if later.step_index <= earlier.step_index:
                raise SchemaError(
                    f"step_index must strictly increase, got {earlier.step_index} "
                    f"then {later.step_index}"
                )
            if later.event_time < earlier.event_time:
                raise SchemaError(
                    f"event_time must not decrease, got {earlier.event_time} "
                    f"then {later.event_time}"
                )

    @classmethod
    def from_events(cls, events: Iterable[BeliefEvent]) -> BeliefTrajectory:
        """Build a trajectory, sorting by step index first.

        Sorting is a convenience for assembling records that arrived out of
        order. It cannot repair a genuine ordering conflict: duplicate step
        indices still raise, because which of two records came first is not
        recoverable from the data.
        """
        return cls(tuple(sorted(events, key=lambda e: e.step_index)))

    def __len__(self) -> int:
        return len(self.events)

    def __iter__(self) -> Iterator[BeliefEvent]:
        return iter(self.events)

    @property
    def subject_kind(self) -> SubjectKind:
        return self.events[0].subject_kind

    @property
    def maturity(self) -> Maturity:
        """The least-mature record in the path.

        A trajectory is only as clearable as its weakest record, so mixing a
        pilot observation into a frozen path makes the whole path pilot.
        """
        order = list(Maturity)
        return min((e.maturity for e in self.events), key=order.index)

    @property
    def is_synthetic(self) -> bool:
        return all(event.is_synthetic for event in self.events)

    def log_odds_path(self) -> list[float]:
        """The belief path in log-odds, in step order."""
        return [event.log_odds for event in self.events]

    def times(self) -> list[float]:
        return [event.event_time for event in self.events]

    def increments(self) -> list[float]:
        """Consecutive log-odds differences."""
        path = self.log_odds_path()
        return [later - earlier for earlier, later in zip(path, path[1:], strict=False)]

    def intervals(self) -> list[float]:
        """Consecutive time gaps.

        Zero-length gaps are rejected here rather than in each estimator: every
        baseline divides by dt, and a zero gap is a data defect, not a limit.
        """
        stamps = self.times()
        gaps = [later - earlier for earlier, later in zip(stamps, stamps[1:], strict=False)]
        for gap in gaps:
            if gap <= 0.0:
                raise SchemaError(
                    "consecutive events must be separated in time to support a rate; "
                    f"found a gap of {gap}"
                )
        return gaps

    def evidence_ids(self) -> list[str | None]:
        """The evidence presented *before* each increment."""
        return [event.evidence_id for event in self.events[:-1]]
