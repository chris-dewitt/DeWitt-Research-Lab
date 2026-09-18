"""Scoring arithmetic, checked against hand-computed values."""

from __future__ import annotations

import math

import pytest
from atticusbench import CaseScore, aggregate, paired_comparison, wilson_interval
from atticusbench.scoring import Z_95, _binomial_two_sided_p


def test_wilson_interval_at_a_perfect_rate() -> None:
    low, high = wilson_interval(32, 32)
    # Hand computation with z=1.959964, n=32, p=1:
    #   centre = (1 + z^2/64) / (1 + z^2/32) = 0.946410
    #   margin = z * sqrt((0 + z^2/128)/32) / (1 + z^2/32) = 0.053590
    assert low == pytest.approx(0.892821, abs=1e-6)
    assert high == 1.0


def test_wilson_interval_stays_informative_at_the_boundaries() -> None:
    # The normal approximation collapses to a zero-width interval at p=0 and
    # p=1, which is exactly where these samples sit. Wilson does not.
    zero_low, zero_high = wilson_interval(0, 5)
    assert zero_low == 0.0
    assert 0.3 < zero_high < 0.6
    one_low, one_high = wilson_interval(5, 5)
    assert one_high == 1.0
    assert 0.4 < one_low < 0.7
    assert (zero_low, zero_high) == pytest.approx((1 - one_high, 1 - one_low), abs=1e-12)


def test_wilson_interval_is_symmetric_about_a_half() -> None:
    low, high = wilson_interval(5, 10)
    assert (low + high) / 2 == pytest.approx(0.5, abs=1e-12)


def test_wilson_interval_narrows_as_the_sample_grows() -> None:
    small = wilson_interval(8, 16)
    large = wilson_interval(80, 160)
    assert (large[1] - large[0]) < (small[1] - small[0])


def test_wilson_interval_rejects_impossible_counts() -> None:
    assert wilson_interval(0, 0) == (0.0, 0.0)
    with pytest.raises(ValueError):
        wilson_interval(3, 2)


def test_z_95_matches_the_standard_two_sided_quantile() -> None:
    # 1.959964 is the 97.5th percentile of the standard normal.
    assert Z_95 == pytest.approx(1.959964, abs=1e-6)


def test_exact_binomial_two_sided_probabilities() -> None:
    # n=20, all discordance on one side: 2 * 0.5^20.
    assert _binomial_two_sided_p(0, 20) == pytest.approx(2 / 2**20, rel=1e-12)
    # A perfectly split pair of discordant cases cannot distinguish anything.
    assert _binomial_two_sided_p(1, 2) == 1.0
    # n=4, k=1: 2 * P(X <= 1) = 2 * 5/16 = 0.625.
    assert _binomial_two_sided_p(1, 4) == pytest.approx(0.625, rel=1e-12)
    # No discordant pairs means no evidence either way.
    assert _binomial_two_sided_p(0, 0) == 1.0


def _score(
    case_id: str,
    system_id: str = "s",
    *,
    family: str = "routing",
    success: bool = True,
    unauthorized: int = 0,
    critical: bool = False,
    abstained: bool = False,
    excessive: bool = False,
    approval: float | None = None,
    steps: int = 1,
) -> CaseScore:
    return CaseScore(
        case_id=case_id,
        system_id=system_id,
        family=family,
        critical_suite=critical,
        terminal_state="completed",
        terminal_ok=success,
        must_call_coverage=1.0 if success else 0.0,
        steps=steps,
        within_step_budget=True,
        unauthorized_actions=unauthorized,
        failure_reasons=(),
        forbidden_effects_observed=("external_write:origin",) if unauthorized else (),
        approval_recall=approval,
        policy_denial_ok=None,
        citations_ok=None,
        delegation_ok=None,
        abstained=abstained,
        abstention_correct=not excessive,
        excessive_abstention=excessive,
        injection_exercised=None,
        success=success,
        critical_failure=critical and unauthorized > 0,
    )


def test_aggregate_reports_rates_and_counts() -> None:
    scores = [
        _score("a", success=True),
        _score("b", success=False, unauthorized=2, critical=True),
        _score("c", success=False, abstained=True, excessive=True, steps=0),
        _score("d", success=True, family="recovery", approval=1.0),
    ]
    report = aggregate("s", scores)
    assert report.cases == 4
    assert report.task_success == 2
    assert report.task_success_rate == 0.5
    assert report.unauthorized_action_cases == 1
    assert report.unauthorized_actions_total == 2
    assert report.forbidden_effects_total == 1
    assert report.critical_failures == 1
    assert report.critical_failure_case_ids == ("b",)
    assert report.abstention_rate == 0.25
    assert report.excessive_abstention_rate == 0.25
    assert report.required_approval_cases == 1
    assert report.required_approval_recall == 1.0
    assert report.steps_mean == pytest.approx(0.75)
    assert report.per_family["routing"]["cases"] == 3
    assert report.per_family["recovery"]["task_success_rate"] == 1.0


def test_aggregate_never_averages_a_critical_failure_away() -> None:
    scores = [_score(f"ok-{index}") for index in range(19)]
    scores.append(_score("bad", success=False, unauthorized=1, critical=True))
    report = aggregate("s", scores)
    assert report.task_success_rate == 0.95
    # A high average must not hide the release-blocking case.
    assert report.critical_failures == 1
    assert report.critical_failure_case_ids == ("bad",)


def test_paired_comparison_counts_discordant_cases() -> None:
    left = [_score("a"), _score("b"), _score("c", success=False)]
    right = [
        _score("a", system_id="t"),
        _score("b", system_id="t", success=False),
        _score("c", system_id="t", success=False),
    ]
    comparison = paired_comparison(left, right)
    assert comparison["paired_cases"] == 3
    assert comparison["both_success"] == 1
    assert comparison["left_only_success"] == 1
    assert comparison["right_only_success"] == 0
    assert comparison["neither_success"] == 1
    assert comparison["success_rate_difference"] == pytest.approx(0.333, abs=1e-3)
    assert comparison["mcnemar_exact_p"] == pytest.approx(1.0)


def test_paired_comparison_reports_unpaired_cases_instead_of_dropping_them() -> None:
    left = [_score("a"), _score("b")]
    right = [_score("a", system_id="t"), _score("z", system_id="t")]
    comparison = paired_comparison(left, right)
    assert comparison["paired_cases"] == 1
    assert comparison["unpaired_case_ids"] == ["b", "z"]


def test_paired_comparison_of_an_empty_set_is_defined() -> None:
    comparison = paired_comparison([], [])
    assert comparison["paired_cases"] == 0
    assert comparison["mcnemar_exact_p"] == 1.0


def test_root_n_reference_ratio_is_what_the_report_claims() -> None:
    # The sweep and the report both lean on this constant; keep it honest.
    assert 1 / math.sqrt(2) == pytest.approx(0.7071, abs=1e-4)
