"""The numerical-competence screen that guards Paper II's attribution."""

from __future__ import annotations

import pytest
from drl_cfi.competence import CompetenceProbe, screen
from drl_cfi.frames import PairedValuation


def probe(subject: str, reported: float, oracle: float = 10.0, **kw: float) -> CompetenceProbe:
    return CompetenceProbe(
        subject_id=subject, claim_id="unframed-call", reported_value=reported,
        oracle_price=oracle, **kw,
    )


def test_accurate_pricing_passes_the_screen() -> None:
    assert probe("model-a", 10.5).is_competent
    assert probe("model-a", 10.5).exclusion_reason() is None


def test_pricing_outside_tolerance_fails() -> None:
    """A subject 40% off the oracle cannot be said to have priced the claim."""
    failed = probe("model-b", 14.0)
    assert not failed.is_competent
    reason = failed.exclusion_reason()
    assert reason is not None
    assert "exceeds" in reason and "0.400" in reason


def test_tolerance_boundary_is_inclusive() -> None:
    assert probe("model-c", 11.0, relative_tolerance=0.10).is_competent
    assert not probe("model-c", 11.01, relative_tolerance=0.10).is_competent


def test_zero_oracle_price_cannot_certify_competence() -> None:
    """Relative error is undefined at zero, so the screen refuses rather than divides."""
    edge = probe("model-d", 0.0, oracle=0.0)
    assert edge.relative_error == float("inf")
    assert not edge.is_competent
    reason = edge.exclusion_reason()
    assert reason is not None and "oracle price is zero" in reason


def test_screen_keeps_the_excluded_and_their_reasons() -> None:
    """Reporting only the retained cohort would hide the exclusion rate."""
    cohort = screen((probe("a", 10.1), probe("b", 20.0), probe("c", 9.9)))
    assert cohort.retained == ("a", "c")
    assert [s for s, _ in cohort.excluded] == ["b"]
    assert cohort.retention_rate == pytest.approx(2 / 3)


def test_empty_screen_reports_zero_retention_without_dividing() -> None:
    assert screen(()).retention_rate == 0.0


def test_valuation_without_a_probe_is_not_admissible() -> None:
    """Absent evidence of competence is not evidence of it."""
    v = PairedValuation(
        pair_id="p1", subject_id="model-a", left_value=12.0, right_value=9.5, oracle_price=10.0
    )
    assert not v.is_admissible
    reason = v.inadmissibility_reason()
    assert reason is not None and "no competence probe" in reason


def test_valuation_with_a_passing_probe_is_admissible() -> None:
    v = PairedValuation(
        pair_id="p1", subject_id="model-a", left_value=12.0, right_value=9.5,
        oracle_price=10.0, competence=probe("model-a", 10.2),
    )
    assert v.is_admissible
    assert v.inadmissibility_reason() is None
    assert v.framing_difference == pytest.approx(2.5)


def test_valuation_with_a_failing_probe_is_not_admissible() -> None:
    """The framing difference still computes — it just must not be analysed."""
    v = PairedValuation(
        pair_id="p1", subject_id="model-b", left_value=12.0, right_value=9.5,
        oracle_price=10.0, competence=probe("model-b", 25.0),
    )
    assert not v.is_admissible
    assert v.framing_difference == pytest.approx(2.5)


def test_probe_must_belong_to_the_same_subject() -> None:
    """A probe from another subject would certify the wrong one."""
    with pytest.raises(ValueError, match="competence probe is for"):
        PairedValuation(
            pair_id="p1", subject_id="model-a", left_value=12.0, right_value=9.5,
            oracle_price=10.0, competence=probe("someone-else", 10.0),
        )


def test_probe_rejects_a_non_positive_tolerance() -> None:
    with pytest.raises(ValueError, match="relative_tolerance must be positive"):
        probe("model-a", 10.0, relative_tolerance=0.0)
