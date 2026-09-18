"""The CFI-005 recovery sweep: its arithmetic, and the artifact it committed."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest
from drl_cfi.baselines import recovery_study

from scripts.run_recovery_sweep import (
    CSV_PATH,
    DEFAULT_REPLICATION_COUNTS,
    DEFAULT_STEP_COUNTS,
    RESULTS_PATH,
    ROOT_N_DOUBLING_RATIO,
    build_csv,
    grid_refinement,
    log_log_fit,
    parameter_rows,
    ratios,
    replication_precision,
    run_sweep,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_log_log_fit_recovers_a_known_exponent() -> None:
    xs = [100, 200, 400, 800, 1600]
    errors = [3.0 * value**-0.5 for value in xs]
    fit = log_log_fit(xs, errors)
    # The fit rounds to four decimals, so the tolerance is the rounding step.
    assert fit["slope"] == pytest.approx(-0.5, abs=1e-4)
    assert fit["intercept"] == pytest.approx(math.log(3.0), abs=1e-4)
    assert fit["r_squared"] == pytest.approx(1.0, abs=1e-4)


def test_log_log_fit_reports_a_flat_series_as_no_convergence() -> None:
    xs = [100, 200, 400, 800]
    fit = log_log_fit(xs, [0.25] * len(xs))
    assert fit["slope"] == pytest.approx(0.0, abs=1e-9)


def test_log_log_fit_declines_degenerate_input() -> None:
    assert log_log_fit([100, 200], [1.0, 0.5])["slope"] is None
    assert log_log_fit([100, 200, 400], [1.0, 0.0, 0.5])["slope"] is None
    assert log_log_fit([100, 200, 400], [1.0, -1.0, 0.5])["slope"] is None


def test_root_n_doubling_ratio_is_the_advertised_constant() -> None:
    assert ROOT_N_DOUBLING_RATIO == pytest.approx(0.7071, abs=1e-4)
    xs = [100, 200, 400, 800]
    errors = [value**-0.5 for value in xs]
    for ratio in ratios(errors):
        assert ratio == pytest.approx(ROOT_N_DOUBLING_RATIO, abs=1e-3)


def test_ratios_guard_a_zero_denominator() -> None:
    assert ratios([0.0, 1.0]) == [None]
    assert ratios([2.0, 1.0, 0.5]) == [0.5, 0.5]


def test_parameter_rows_report_the_standard_error_of_the_bias() -> None:
    report = recovery_study(
        "diffusion",
        replications=64,
        steps=200,
        dt=0.05,
        seed=7,
        drift=0.4,
        volatility=0.8,
    )
    rows = parameter_rows(report)
    assert {row["name"] for row in rows} == {"drift", "volatility"}
    for row, parameter in zip(rows, report.parameters, strict=True):
        expected = parameter.spread / math.sqrt(64)
        assert row["bias_standard_error"] == pytest.approx(expected, abs=1e-6)
        assert row["bias_in_standard_errors"] == pytest.approx(parameter.bias / expected, abs=1e-3)


def test_relative_bias_is_null_rather_than_infinite_at_a_zero_truth() -> None:
    # The jump design's drift truth is exactly zero, and JSON has no infinity.
    report = recovery_study(
        "jump_diffusion",
        replications=8,
        steps=100,
        dt=0.05,
        seed=11,
        drift=0.0,
        volatility=0.5,
        jump_intensity=0.8,
        jump_mean=0.0,
        jump_scale=1.2,
    )
    rows = {row["name"]: row for row in parameter_rows(report)}
    assert rows["drift"]["relative_bias"] is None
    assert rows["volatility"]["relative_bias"] is not None


def test_a_small_sweep_runs_end_to_end() -> None:
    payload = run_sweep(
        step_counts=(50, 100, 200),
        horizon_time=5.0,
        replications=6,
        replication_counts=(4, 8),
        fixed_steps=100,
        fixed_dt=0.05,
        seed=3,
    )
    assert payload["grid_refinement"]["step_counts"] == [50, 100, 200]
    assert len(payload["grid_refinement"]["studies"]) == 3
    assert len(payload["replication_precision"]["studies"]) == 3
    # The payload must survive a strict JSON round trip: no infinity, no NaN.
    reloaded = json.loads(json.dumps(payload, allow_nan=False))
    assert reloaded == payload
    assert build_csv(payload).startswith("axis,model,steps,dt,replications,parameter")


def test_grid_refinement_holds_calendar_time_fixed() -> None:
    studies = grid_refinement(
        step_counts=(50, 100),
        horizon_time=5.0,
        replications=4,
        seed=5,
    )
    for study in studies:
        for point in study["by_steps"]:
            assert point["steps"] * point["dt"] == pytest.approx(5.0, abs=1e-6)


def test_replication_axis_shrinks_the_standard_error() -> None:
    studies = replication_precision(
        replication_counts=(25, 100, 400),
        steps=200,
        dt=0.05,
        seed=9,
    )
    for study in studies:
        for parameter in study["resolution"]:
            errors = parameter["bias_standard_error_by_replications"]
            assert errors[0] > errors[-1]
            fit = parameter["standard_error_log_log_fit"]
            # Quadrupling the replications roughly halves the standard error,
            # so the slope sits near -0.5. It is not exactly -0.5: the spread it
            # is built from is itself an estimate, and this run is deliberately
            # tiny. The committed sweep is checked to a tighter tolerance below.
            assert fit["slope"] == pytest.approx(-0.5, abs=0.2)


@pytest.fixture(scope="module")
def committed() -> dict:
    return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))


def test_committed_sweep_is_strict_json(committed) -> None:
    raw = RESULTS_PATH.read_text(encoding="utf-8")
    assert "Infinity" not in raw
    assert "NaN" not in raw
    assert json.loads(raw) == committed


def test_committed_sweep_covers_both_axes_and_every_design(committed) -> None:
    assert committed["study"] == "cfi-005-parameter-recovery-sweep"
    grid = committed["grid_refinement"]
    precision = committed["replication_precision"]
    assert grid["step_counts"] == list(DEFAULT_STEP_COUNTS)
    assert precision["replication_counts"] == list(DEFAULT_REPLICATION_COUNTS)
    models = {study["model"] for study in grid["studies"]}
    assert models == {"diffusion", "ornstein_uhlenbeck", "jump_diffusion"}
    assert models == {study["model"] for study in precision["studies"]}


def test_committed_sweep_states_its_limitations(committed) -> None:
    text = " ".join(committed["limitations"]).lower()
    assert "correct specification" in text
    assert "g3" in text


def _convergence(committed: dict, model: str, parameter: str) -> dict:
    study = next(s for s in committed["grid_refinement"]["studies"] if s["model"] == model)
    return next(p for p in study["convergence"] if p["name"] == parameter)


def _resolution(committed: dict, model: str, parameter: str) -> dict:
    study = next(s for s in committed["replication_precision"]["studies"] if s["model"] == model)
    return next(p for p in study["resolution"] if p["name"] == parameter)


def test_volatility_converges_under_grid_refinement(committed) -> None:
    # The report's headline claim. Pin it so a code change cannot quietly
    # invalidate the prose.
    for model in ("diffusion", "ornstein_uhlenbeck", "jump_diffusion"):
        fit = _convergence(committed, model, "volatility")["rmse_log_log_fit"]
        assert fit["slope"] < -0.4, model
        assert fit["r_squared"] > 0.9, model


def test_drift_and_level_do_not_converge_under_grid_refinement(committed) -> None:
    # Over a fixed interval these parameters are identified by the endpoints,
    # so sampling the interior more finely cannot help.
    drift = _convergence(committed, "diffusion", "drift")["rmse_log_log_fit"]
    level = _convergence(committed, "ornstein_uhlenbeck", "level")["rmse_log_log_fit"]
    assert abs(drift["slope"]) < 0.1
    assert abs(level["slope"]) < 0.1


def test_reversion_rate_bias_is_resolved_from_monte_carlo_noise(committed) -> None:
    resolution = _resolution(committed, "ornstein_uhlenbeck", "reversion_rate")
    assert resolution["bias_resolved_from_noise"] is True
    assert abs(resolution["bias_in_standard_errors_at_largest"]) > 5.0


def test_committed_replication_axis_tracks_the_root_n_line(committed) -> None:
    for study in committed["replication_precision"]["studies"]:
        for parameter in study["resolution"]:
            fit = parameter["standard_error_log_log_fit"]
            assert fit["slope"] == pytest.approx(-0.5, abs=0.12), (
                study["model"],
                parameter["name"],
            )
            assert fit["r_squared"] > 0.99


def test_committed_csv_matches_the_committed_json(committed) -> None:
    assert CSV_PATH.read_text(encoding="utf-8") == build_csv(committed)
