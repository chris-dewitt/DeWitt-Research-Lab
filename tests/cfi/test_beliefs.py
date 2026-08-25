"""Tests for the CFI-004 observable belief-event schema."""

from __future__ import annotations

import math

import pytest
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

LINEAGE = {
    "study_id": "cfi-test",
    "run_id": "run-1",
    "subject_id": "s-1",
    "subject_kind": SubjectKind.SIMULATOR,
    "model_or_cohort_revision": "rev-1",
    "task_id": "t-1",
    "proposition_id": "p-1",
    "action": Action.CONTINUE,
    "source_rights_id": "synthetic",
    "code_revision": "test",
    "config_digest": "digest",
    "seed": 7,
    "maturity": Maturity.SYNTHETIC,
}


def event(step: int, p: float, *, time: float | None = None, **overrides: object) -> BeliefEvent:
    fields = dict(LINEAGE)
    fields.update(overrides)
    return BeliefEvent(
        step_index=step,
        event_time=float(step) if time is None else time,
        reported_probability=p,
        **fields,  # type: ignore[arg-type]
    )


class TestLogOdds:
    def test_roundtrip(self) -> None:
        for p in (0.01, 0.25, 0.5, 0.73, 0.999):
            assert probability(log_odds(p)) == pytest.approx(p, abs=1e-12)

    def test_even_odds_is_zero(self) -> None:
        assert log_odds(0.5) == pytest.approx(0.0)

    @pytest.mark.parametrize("p", [0.0, 1.0, -0.1, 1.5])
    def test_boundary_and_outside_rejected(self, p: float) -> None:
        # Certainty is a real report and an unrepresentable one. It must raise
        # rather than be clipped to an epsilon that reads back as data.
        with pytest.raises(SchemaError, match="strictly inside"):
            log_odds(p)

    def test_nan_rejected(self) -> None:
        with pytest.raises(SchemaError, match="finite"):
            log_odds(math.nan)

    def test_probability_saturates_without_overflow(self) -> None:
        assert probability(-800.0) == pytest.approx(0.0, abs=1e-300)
        assert probability(800.0) == pytest.approx(1.0)


class TestBeliefEvent:
    def test_carries_log_odds(self) -> None:
        assert event(0, 0.75).log_odds == pytest.approx(math.log(3.0))

    def test_synthetic_flag_tracks_maturity(self) -> None:
        assert event(0, 0.5).is_synthetic
        assert not event(0, 0.5, maturity=Maturity.PILOT).is_synthetic

    @pytest.mark.parametrize(
        "field",
        ["study_id", "subject_id", "source_rights_id", "code_revision", "config_digest"],
    )
    def test_lineage_fields_are_required(self, field: str) -> None:
        with pytest.raises(SchemaError, match=field):
            event(0, 0.5, **{field: "  "})

    def test_negative_step_rejected(self) -> None:
        with pytest.raises(SchemaError, match="step_index"):
            event(-1, 0.5)

    def test_negative_action_cost_rejected(self) -> None:
        with pytest.raises(SchemaError, match="action_cost"):
            event(0, 0.5, action_cost=-1.0)

    def test_declared_action_cost_is_kept(self) -> None:
        assert event(0, 0.5, action_cost=2.5).action_cost == 2.5


class TestBeliefTrajectory:
    def test_needs_two_events_for_an_increment(self) -> None:
        with pytest.raises(SchemaError, match="at least two"):
            BeliefTrajectory((event(0, 0.5),))

    def test_increments_and_intervals(self) -> None:
        path = BeliefTrajectory((event(0, 0.5), event(1, 0.75), event(2, 0.9)))
        assert path.increments() == pytest.approx([math.log(3.0), math.log(9.0) - math.log(3.0)])
        assert path.intervals() == pytest.approx([1.0, 1.0])

    def test_out_of_order_steps_rejected(self) -> None:
        with pytest.raises(SchemaError, match="strictly increase"):
            BeliefTrajectory((event(1, 0.5), event(0, 0.6)))

    def test_duplicate_steps_rejected(self) -> None:
        with pytest.raises(SchemaError, match="strictly increase"):
            BeliefTrajectory((event(0, 0.5), event(0, 0.6)))

    def test_backwards_time_rejected(self) -> None:
        with pytest.raises(SchemaError, match="event_time"):
            BeliefTrajectory((event(0, 0.5, time=5.0), event(1, 0.6, time=1.0)))

    def test_mixed_subjects_rejected(self) -> None:
        with pytest.raises(SchemaError, match="subject_id"):
            BeliefTrajectory((event(0, 0.5), event(1, 0.6, subject_id="other")))

    def test_mixed_propositions_rejected(self) -> None:
        with pytest.raises(SchemaError, match="proposition_id"):
            BeliefTrajectory((event(0, 0.5), event(1, 0.6, proposition_id="other")))

    def test_from_events_sorts(self) -> None:
        path = BeliefTrajectory.from_events([event(2, 0.9), event(0, 0.5), event(1, 0.75)])
        assert [e.step_index for e in path] == [0, 1, 2]

    def test_from_events_cannot_repair_duplicates(self) -> None:
        # Which of two records with the same step came first is not recoverable
        # from the data, so sorting must not paper over it.
        with pytest.raises(SchemaError, match="strictly increase"):
            BeliefTrajectory.from_events([event(0, 0.5), event(0, 0.6)])

    def test_zero_time_gap_rejected_at_intervals(self) -> None:
        path = BeliefTrajectory((event(0, 0.5, time=0.0), event(1, 0.6, time=0.0)))
        with pytest.raises(SchemaError, match="separated in time"):
            path.intervals()

    def test_maturity_is_the_weakest_record(self) -> None:
        path = BeliefTrajectory((event(0, 0.5), event(1, 0.6, maturity=Maturity.PILOT)))
        assert path.maturity is Maturity.SYNTHETIC
        assert not path.is_synthetic

    def test_evidence_ids_align_with_increments(self) -> None:
        path = BeliefTrajectory(
            (
                event(0, 0.5, evidence_id="a"),
                event(1, 0.6, evidence_id="b"),
                event(2, 0.7, evidence_id="c"),
            )
        )
        # One label per increment: the evidence shown *before* each move.
        assert path.evidence_ids() == ["a", "b"]
        assert len(path.evidence_ids()) == len(path.increments())
