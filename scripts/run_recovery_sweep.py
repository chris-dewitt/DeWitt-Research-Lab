#!/usr/bin/env python
"""Sweep the CFI-005 parameter-recovery study along two axes.

CFI-005 is the parameter-recovery work item of the Computational Finance of
Intelligence research program. The single-point study in
`scripts/run_belief_recovery.py` reports how far each estimate sits from its
truth at one design. One number cannot separate three different situations: an
estimator that converges, an estimator that never will, and Monte Carlo noise in
the measurement of the bias itself. This sweep separates them.

Axis 1, grid refinement. Calendar time is held fixed while the observation grid
is refined, so a longer series means finer sampling of the same interval rather
than a longer interval. Holding calendar time fixed is not a convenience: with
drift held constant, extending the interval drives the simulated belief past the
representable log-odds bound and the simulator refuses the path outright.

Axis 2, Monte Carlo precision. The design is held fixed while the number of
replications grows, which shrinks the standard error of the measured bias
without changing the estimator at all. A bias worth discussing has to be large
relative to that standard error.

    uv run python scripts/run_recovery_sweep.py
    uv run python scripts/run_recovery_sweep.py --json
    uv run python scripts/run_recovery_sweep.py --check   # fail if results drift

Every number is reproducible from `--seed`. The sweep asserts nothing about
whether a given bias is tolerable: that is a protocol question, and no protocol
has passed the program's G3 gate.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
# The repository root carries `scripts` as a namespace package, so the single
# point study's designs are reused here rather than duplicated.
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "research" / "cfi" / "src"))

from drl_cfi.baselines import RecoveryReport, recovery_study  # noqa: E402
from drl_cfi.linalg import solve_least_squares  # noqa: E402

from scripts.run_belief_recovery import DESIGNS  # noqa: E402

RESULTS_DIR = REPO_ROOT / "research" / "cfi" / "results"
RESULTS_PATH = RESULTS_DIR / "recovery-sweep.json"
CSV_PATH = RESULTS_DIR / "recovery-sweep.csv"

#: Doubling sequence of observation counts for the grid-refinement axis.
DEFAULT_STEP_COUNTS: tuple[int, ...] = (100, 200, 400, 800, 1600, 3200)

#: Calendar length of the observation interval, in the same time units as dt.
#: Ten units keeps every design's paths well inside the representable belief
#: range at the drifts under study.
DEFAULT_HORIZON_TIME = 10.0

#: Doubling sequence of replication counts for the Monte Carlo precision axis.
DEFAULT_REPLICATION_COUNTS: tuple[int, ...] = (50, 100, 200, 400, 800)

STUDY_VERSION = "1.0.0"

#: Error ratio expected from one doubling under root-n convergence.
ROOT_N_DOUBLING_RATIO = round(1.0 / math.sqrt(2.0), 4)


def log_log_fit(xs: list[int], errors: list[float]) -> dict[str, float | None]:
    """Fit log(error) = intercept + slope * log(x) by least squares.

    Returns ``None`` values for a degenerate design or a non-positive error,
    rather than reporting a slope that came from the logarithm of zero.
    """

    if len(xs) < 3 or any(error <= 0.0 for error in errors):
        return {"slope": None, "intercept": None, "r_squared": None}
    design = [[1.0, math.log(float(value))] for value in xs]
    observed = [math.log(error) for error in errors]
    intercept, slope = solve_least_squares(design, observed)
    mean = sum(observed) / len(observed)
    total = sum((value - mean) ** 2 for value in observed)
    residual = sum(
        (value - (intercept + slope * row[1])) ** 2
        for value, row in zip(observed, design, strict=True)
    )
    r_squared = 1.0 - residual / total if total > 0 else None
    return {
        "slope": round(slope, 4),
        "intercept": round(intercept, 4),
        "r_squared": round(r_squared, 4) if r_squared is not None else None,
    }


def ratios(errors: list[float]) -> list[float | None]:
    """Error ratio between consecutive points in a doubling sequence."""

    return [
        round(current / previous, 4) if previous > 0 else None
        for previous, current in zip(errors[:-1], errors[1:], strict=True)
    ]


def parameter_rows(report: RecoveryReport) -> list[dict[str, Any]]:
    """Per-parameter measurements, including the bias's own standard error."""

    rows: list[dict[str, Any]] = []
    for parameter in report.parameters:
        standard_error = parameter.spread / math.sqrt(report.replications)
        # Relative bias is undefined at a truth of zero, and JSON has no
        # infinity. The jump design's drift truth is exactly zero, so this is a
        # live case rather than a hypothetical one.
        relative = parameter.relative_bias
        rows.append(
            {
                "name": parameter.name,
                "truth": parameter.truth,
                "mean_estimate": round(parameter.mean_estimate, 6),
                "bias": round(parameter.bias, 6),
                "relative_bias": round(relative, 6) if math.isfinite(relative) else None,
                "spread": round(parameter.spread, 6),
                "root_mean_square_error": round(parameter.root_mean_square_error, 6),
                "bias_standard_error": round(standard_error, 6),
                "bias_in_standard_errors": (
                    round(parameter.bias / standard_error, 3) if standard_error > 0 else None
                ),
            }
        )
    return rows


def _series(points: list[dict[str, Any]], name: str) -> list[dict[str, Any]]:
    return [next(row for row in point["parameters"] if row["name"] == name) for point in points]


def grid_refinement(
    *,
    step_counts: tuple[int, ...],
    horizon_time: float,
    replications: int,
    seed: int,
) -> list[dict[str, Any]]:
    """Refine the observation grid over a fixed calendar interval."""

    studies: list[dict[str, Any]] = []
    for model, truth in DESIGNS:
        points: list[dict[str, Any]] = []
        for steps in step_counts:
            dt = horizon_time / steps
            report = recovery_study(
                model,
                replications=replications,
                steps=steps,
                dt=dt,
                seed=seed,
                **truth,
            )
            points.append(
                {
                    "steps": steps,
                    "dt": round(dt, 8),
                    "horizon_time": horizon_time,
                    "parameters": parameter_rows(report),
                }
            )

        convergence: list[dict[str, Any]] = []
        for name in [row["name"] for row in points[0]["parameters"]]:
            series = _series(points, name)
            rmse = [float(row["root_mean_square_error"]) for row in series]
            absolute_bias = [abs(float(row["bias"])) for row in series]
            convergence.append(
                {
                    "name": name,
                    "truth": series[0]["truth"],
                    "rmse_by_steps": rmse,
                    "absolute_bias_by_steps": absolute_bias,
                    "rmse_ratios": ratios(rmse),
                    "rmse_log_log_fit": log_log_fit(list(step_counts), rmse),
                    "bias_log_log_fit": log_log_fit(list(step_counts), absolute_bias),
                    "coarsest_relative_bias": series[0]["relative_bias"],
                    "finest_relative_bias": series[-1]["relative_bias"],
                }
            )
        studies.append(
            {
                "model": model,
                "truth": dict(truth),
                "by_steps": points,
                "convergence": convergence,
            }
        )
    return studies


def replication_precision(
    *,
    replication_counts: tuple[int, ...],
    steps: int,
    dt: float,
    seed: int,
) -> list[dict[str, Any]]:
    """Grow the replication count at a fixed design."""

    studies: list[dict[str, Any]] = []
    for model, truth in DESIGNS:
        points: list[dict[str, Any]] = []
        for replications in replication_counts:
            report = recovery_study(
                model,
                replications=replications,
                steps=steps,
                dt=dt,
                seed=seed,
                **truth,
            )
            points.append(
                {
                    "replications": replications,
                    "steps": steps,
                    "dt": dt,
                    "parameters": parameter_rows(report),
                }
            )

        resolution: list[dict[str, Any]] = []
        for name in [row["name"] for row in points[0]["parameters"]]:
            series = _series(points, name)
            standard_errors = [float(row["bias_standard_error"]) for row in series]
            largest = series[-1]
            in_errors = largest["bias_in_standard_errors"]
            resolution.append(
                {
                    "name": name,
                    "truth": series[0]["truth"],
                    "bias_by_replications": [float(row["bias"]) for row in series],
                    "bias_standard_error_by_replications": standard_errors,
                    "standard_error_ratios": ratios(standard_errors),
                    "standard_error_log_log_fit": log_log_fit(
                        list(replication_counts), standard_errors
                    ),
                    "bias_in_standard_errors_at_largest": in_errors,
                    # Two standard errors is the conventional line for "not noise".
                    # This is a statement about the measurement, not about whether
                    # the bias is acceptable.
                    "bias_resolved_from_noise": (
                        bool(abs(in_errors) >= 2.0) if in_errors is not None else None
                    ),
                }
            )
        studies.append(
            {
                "model": model,
                "truth": dict(truth),
                "by_replications": points,
                "resolution": resolution,
            }
        )
    return studies


def run_sweep(
    *,
    step_counts: tuple[int, ...],
    horizon_time: float,
    replications: int,
    replication_counts: tuple[int, ...],
    fixed_steps: int,
    fixed_dt: float,
    seed: int,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "study": "cfi-005-parameter-recovery-sweep",
        "study_version": STUDY_VERSION,
        "seed": seed,
        "reference_rate_exponent": -0.5,
        "root_n_doubling_ratio": ROOT_N_DOUBLING_RATIO,
        "grid_refinement": {
            "description": (
                "Calendar time fixed, observation grid refined. Tests whether each "
                "parameter's error falls as the same interval is sampled more finely."
            ),
            "horizon_time": horizon_time,
            "replications": replications,
            "step_counts": list(step_counts),
            "studies": grid_refinement(
                step_counts=step_counts,
                horizon_time=horizon_time,
                replications=replications,
                seed=seed,
            ),
        },
        "replication_precision": {
            "description": (
                "Design fixed, replications grown. Tests how precisely the bias "
                "itself is measured, which is a property of this study rather than "
                "of the estimator."
            ),
            "steps": fixed_steps,
            "dt": fixed_dt,
            "replication_counts": list(replication_counts),
            "studies": replication_precision(
                replication_counts=replication_counts,
                steps=fixed_steps,
                dt=fixed_dt,
                seed=seed,
            ),
        },
        "interpretation_rules": [
            (
                "A log-log slope near -0.5 with high r-squared is consistent with "
                "root-n convergence of that quantity."
            ),
            (
                "A slope near zero on the grid-refinement axis says finer sampling of "
                "the same interval did not reduce the error. For a drift parameter that "
                "is the expected result, not a defect: over a fixed interval the drift "
                "is identified by the endpoints, so more interior points add little."
            ),
            (
                "On the replication axis the standard error must fall near -0.5 by "
                "construction. A bias that stays many standard errors from zero as that "
                "error shrinks is a real bias rather than Monte Carlo noise."
            ),
        ],
        "limitations": [
            (
                "Simulated data from the same model family that is then fitted. This "
                "measures recovery under correct specification only; it says nothing "
                "about misspecification or about real belief data."
            ),
            (
                "Calendar time is fixed at one value, so nothing here describes what "
                "happens as the observation interval lengthens. Extending the interval "
                "at these drifts saturates the belief representation, which is the "
                "reason for the constraint."
            ),
            (
                "Each replication count is a fresh study from the same base seed, so "
                "the replication axis is nested: larger counts contain the smaller "
                "ones. The standard errors are therefore not independent across points."
            ),
            (
                "No protocol has passed the program's G3 gate, so no threshold here "
                "constitutes a pass or fail of anything."
            ),
        ],
    }


def build_csv(payload: dict[str, Any]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(
        [
            "axis",
            "model",
            "steps",
            "dt",
            "replications",
            "parameter",
            "truth",
            "mean_estimate",
            "bias",
            "relative_bias",
            "spread",
            "root_mean_square_error",
            "bias_standard_error",
            "bias_in_standard_errors",
        ]
    )
    grid = payload["grid_refinement"]
    for study in grid["studies"]:
        for point in study["by_steps"]:
            for row in point["parameters"]:
                writer.writerow(
                    [
                        "grid_refinement",
                        study["model"],
                        point["steps"],
                        point["dt"],
                        grid["replications"],
                        row["name"],
                        row["truth"],
                        row["mean_estimate"],
                        row["bias"],
                        row["relative_bias"],
                        row["spread"],
                        row["root_mean_square_error"],
                        row["bias_standard_error"],
                        row["bias_in_standard_errors"],
                    ]
                )
    for study in payload["replication_precision"]["studies"]:
        for point in study["by_replications"]:
            for row in point["parameters"]:
                writer.writerow(
                    [
                        "replication_precision",
                        study["model"],
                        point["steps"],
                        point["dt"],
                        point["replications"],
                        row["name"],
                        row["truth"],
                        row["mean_estimate"],
                        row["bias"],
                        row["relative_bias"],
                        row["spread"],
                        row["root_mean_square_error"],
                        row["bias_standard_error"],
                        row["bias_in_standard_errors"],
                    ]
                )
    return buffer.getvalue()


def _relative(value: float | None) -> str:
    """Render a relative bias, which is undefined when the truth is zero."""

    return "n/a" if value is None else f"{value:+.4f}"


def render(payload: dict[str, Any]) -> str:
    grid = payload["grid_refinement"]
    precision = payload["replication_precision"]
    lines = [
        f"CFI-005 parameter-recovery sweep (seed {payload['seed']})",
        "",
        f"Axis 1: grid refinement over a fixed interval of {grid['horizon_time']} time units, "
        f"{grid['replications']} replications per point",
        f"  observation counts: {', '.join(str(step) for step in grid['step_counts'])}",
    ]
    for study in grid["studies"]:
        lines.append("")
        lines.append(f"  model: {study['model']}")
        lines.append(
            f"    {'parameter':>16}  {'truth':>9}  {'rmse@100':>9}  {'rmse@3200':>10}  "
            f"{'slope':>7}  {'r2':>6}  {'relbias@fine':>12}"
        )
        for parameter in study["convergence"]:
            fit = parameter["rmse_log_log_fit"]
            slope = "n/a" if fit["slope"] is None else f"{fit['slope']:+.3f}"
            r_squared = "n/a" if fit["r_squared"] is None else f"{fit['r_squared']:.3f}"
            lines.append(
                f"    {parameter['name']:>16}  {parameter['truth']:>+9.4f}  "
                f"{parameter['rmse_by_steps'][0]:>9.4f}  "
                f"{parameter['rmse_by_steps'][-1]:>10.4f}  "
                f"{slope:>7}  {r_squared:>6}  "
                f"{_relative(parameter['finest_relative_bias']):>12}"
            )
    lines.append("")
    lines.append(
        f"Axis 2: Monte Carlo precision at {precision['steps']} observations, dt={precision['dt']}"
    )
    counts = ", ".join(str(count) for count in precision["replication_counts"])
    lines.append(f"  replication counts: {counts}")
    for study in precision["studies"]:
        lines.append("")
        lines.append(f"  model: {study['model']}")
        lines.append(
            f"    {'parameter':>16}  {'bias':>9}  {'se':>8}  {'bias/se':>8}  {'resolved':>9}"
        )
        for parameter in study["resolution"]:
            errors = parameter["bias_standard_error_by_replications"]
            biases = parameter["bias_by_replications"]
            in_errors = parameter["bias_in_standard_errors_at_largest"]
            resolved = (
                "n/a"
                if parameter["bias_resolved_from_noise"] is None
                else ("yes" if parameter["bias_resolved_from_noise"] else "no")
            )
            lines.append(
                f"    {parameter['name']:>16}  {biases[-1]:>+9.4f}  {errors[-1]:>8.4f}  "
                f"{'n/a' if in_errors is None else f'{in_errors:+.2f}':>8}  {resolved:>9}"
            )
    lines.append("")
    lines.append(
        "A slope near -0.5 is root-n convergence; near 0.0 means the error did not shrink. "
        f"One doubling under root-n multiplies error by {payload['root_n_doubling_ratio']}."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replications", type=int, default=400)
    parser.add_argument("--horizon-time", type=float, default=DEFAULT_HORIZON_TIME)
    parser.add_argument("--fixed-steps", type=int, default=400)
    parser.add_argument("--fixed-dt", type=float, default=0.025)
    parser.add_argument("--seed", type=int, default=20260825)
    parser.add_argument(
        "--steps",
        action="append",
        type=int,
        dest="step_counts",
        help="observation count for the grid axis (repeatable)",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare a fresh sweep against the committed results instead of writing them",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=RESULTS_PATH,
        help="results path (default research/cfi/results/recovery-sweep.json)",
    )
    args = parser.parse_args(argv)

    step_counts = tuple(sorted(args.step_counts)) if args.step_counts else DEFAULT_STEP_COUNTS
    payload = run_sweep(
        step_counts=step_counts,
        horizon_time=args.horizon_time,
        replications=args.replications,
        replication_counts=DEFAULT_REPLICATION_COUNTS,
        fixed_steps=args.fixed_steps,
        fixed_dt=args.fixed_dt,
        seed=args.seed,
    )

    print(json.dumps(payload, indent=2) if args.json else render(payload))

    serialized = json.dumps(payload, indent=2) + "\n"
    table = build_csv(payload)
    if args.check:
        problems: list[str] = []
        if not args.out.exists():
            problems.append(f"missing {args.out}")
        elif args.out.read_text(encoding="utf-8") != serialized:
            problems.append(f"{args.out.name} drifted")
        if not CSV_PATH.exists():
            problems.append(f"missing {CSV_PATH}")
        elif CSV_PATH.read_text(encoding="utf-8") != table:
            problems.append(f"{CSV_PATH.name} drifted")
        for problem in problems:
            print(f"drift: {problem}", file=sys.stderr)
        if problems:
            return 1
        print("\nCommitted sweep results match this run.")
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(serialized, encoding="utf-8")
    CSV_PATH.write_text(table, encoding="utf-8")
    print(f"\nwrote {args.out.relative_to(REPO_ROOT)} and {CSV_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
