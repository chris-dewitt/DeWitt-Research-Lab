"""Belief-trajectory viewer — the CFI-007 local instrument.

CFI-005 produced estimators and a recovery study, but both speak only in
terminal text. This module renders a belief path and the fits taken from it as
static HTML you can look at.

It exists because of one measurement. Fit the Ornstein-Uhlenbeck estimator to a
pure drifting walk and it reports a resting level of −16.53 log-odds — a
probability of 0.000000066 — for a path that never once dropped below even odds.
The number is not wrong; the model was simply asked a question the data cannot
answer, and nothing in the return value says so. **A viewer that printed that
level beside the others would be the same failure this laboratory has now
recorded twice: an instrument quietly producing a plausible number instead of
refusing.**

So every estimate here travels with diagnostics. A diagnostic is a statement
about *identifiability or resolution* — this output does not carry the
information its name implies — and never about whether a value is good.
``RecoveryReport`` deliberately carries no verdict because G3 has not been
passed, and this renderer inherits that: no page in the generated site contains a
threshold, a pass, or a failure.

The renderer is deliberately **not** re-exported from ``drl_cfi/__init__.py``.
That package's ``__all__`` is a curated numerical API; HTML generation is not
mathematics and does not belong in it.

Everything is stdlib and deterministic. Fixtures are generated from fixed seeds
rather than committed, so the seed *is* the fixture and cannot drift from the
code that produces it.
"""

from __future__ import annotations

import html
import math
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from drl_cfi.baselines import (
    JUMP_THRESHOLD,
    AsymmetricBayesianFit,
    BayesianFit,
    DiffusionFit,
    JumpDiffusionFit,
    OrnsteinUhlenbeckFit,
    fit_asymmetric_bayesian,
    fit_bayesian,
    fit_diffusion,
    fit_jump_diffusion,
    fit_ornstein_uhlenbeck,
    simulate_asymmetric_bayesian,
    simulate_bayesian,
    simulate_diffusion,
    simulate_jump_diffusion,
    simulate_ornstein_uhlenbeck,
)
from drl_cfi.beliefs import BeliefTrajectory


class BeliefSiteError(RuntimeError):
    """The requested site cannot be built."""


__all__ = [
    "BeliefSiteError",
    "ChartGeometry",
    "Diagnostic",
    "FitPanel",
    "TrajectoryCase",
    "build_site",
    "chart_geometry",
    "default_cases",
    "diagnose_asymmetric_bayesian",
    "diagnose_bayesian",
    "diagnose_diffusion",
    "diagnose_jump_diffusion",
    "diagnose_ornstein_uhlenbeck",
    "ordered",
    "render_case_page",
    "render_index",
    "select_cases",
    "site_metadata",
]

#: Rows in the sampled step table. A 401-row table is a data dump, not a data
#: equivalent; the caption states exactly which rows were kept.
TABLE_ROWS = 24

#: Chart viewBox. Rendered at any width; nothing inside carries text, because a
#: label sized for 720 units is illegible once the box scales down to a 320px
#: screen. Every label lives in the HTML around the figure instead, which is
#: simultaneously the small-screen fix and the screen-reader fix.
VIEW_W, VIEW_H = 720.0, 240.0
PAD_X, PAD_Y = 6.0, 10.0

#: A safety valve, not a feature. No shipped fixture reaches it — the longest is
#: 401 points. It exists so a hand-built long path degrades to uniform striding
#: rather than emitting a megabyte of coordinates. Do not delete it as dead code;
#: it is covered by a library test.
MAX_POLYLINE_POINTS = 800

#: Vertical rules are drawn per detected jump. Past this count the chart is a
#: barcode and the table is the better reading, so drawing stops and the caption
#: says how many were omitted.
MAX_JUMP_RULES = 60

#: Residuals at or below this are indistinguishable from exact reproduction.
#: Not decorative: the noiseless asymmetric fit lands at 1.89e-13, so an
#: equality test against zero misses it.
ZERO_SCALE = 1e-12

#: Above this share of increments flagged as jumps, the separation has stopped
#: being a separation. CFI-005 traced this signature to a saturating path
#: collapsing the robust scale until ordinary diffusion was flagged.
JUMP_FRACTION_CEILING = 0.10


@dataclass(frozen=True, slots=True)
class ChartGeometry:
    """Everything needed to draw a belief path, computed without touching HTML.

    Separating the arithmetic from the markup is what lets the geometry be
    tested for correctness — that zero lands on the reference line, that a dense
    path strides without losing its endpoint — rather than by grepping a string
    of SVG for coordinates.
    """

    points: tuple[tuple[float, float], ...]
    zero_y: float
    jump_x: tuple[float, ...]
    y_low: float
    y_high: float
    t_low: float
    t_high: float
    plotted: int
    total: int
    stride: int
    jumps_drawn: int
    jumps_total: int
    x_is_step_index: bool

    @property
    def is_strided(self) -> bool:
        return self.stride > 1


def chart_geometry(
    times: Sequence[float],
    path: Sequence[float],
    *,
    jump_indices: Sequence[int] = (),
) -> ChartGeometry:
    """Map a belief path into view coordinates.

    The vertical domain **always contains zero**, even when the path never
    approaches it. That costs a little resolution on a path living far from even
    odds, and buys three things: the even-odds reference line is always present,
    pages are comparable to each other, and there is no ``zero is off-screen``
    branch to render or to test.
    """
    if len(path) < 2:
        raise ValueError("a chart needs at least two points")
    if len(times) != len(path):
        raise ValueError(f"times and path differ in length: {len(times)} vs {len(path)}")

    low = min(min(path), 0.0)
    high = max(max(path), 0.0)
    if high - low <= 0.0:
        # A path pinned at exactly zero for its whole length. Give it a unit
        # window rather than dividing by a zero span.
        low, high = -1.0, 1.0
    else:
        margin = 0.05 * (high - low)
        low -= margin
        high += margin
    span = high - low

    t_low, t_high = times[0], times[-1]
    # BeliefTrajectory permits equal timestamps (it only forbids *decreasing*
    # ones), so a path recorded without a clock still has to plot.
    x_is_step_index = not (t_high > t_low)
    if x_is_step_index:
        t_low, t_high = 0.0, float(len(path) - 1)

    inner_w = VIEW_W - 2.0 * PAD_X
    inner_h = VIEW_H - 2.0 * PAD_Y

    def x_of(value: float) -> float:
        return PAD_X + inner_w * (value - t_low) / (t_high - t_low)

    def y_of(value: float) -> float:
        return PAD_Y + inner_h * (high - value) / span

    total = len(path)
    stride = 1 if total <= MAX_POLYLINE_POINTS else math.ceil(total / MAX_POLYLINE_POINTS)
    kept = list(range(0, total, stride))
    if kept[-1] != total - 1:
        kept.append(total - 1)

    axis = [float(i) for i in range(total)] if x_is_step_index else list(times)
    points = tuple((x_of(axis[i]), y_of(path[i])) for i in kept)

    drawn: list[float] = []
    for index in sorted(jump_indices)[:MAX_JUMP_RULES]:
        # jump_indices are *increment* indices; the belief lands on the point
        # after the flagged increment.
        landing = index + 1
        if 0 <= landing < total:
            drawn.append(x_of(axis[landing]))

    return ChartGeometry(
        points=points,
        zero_y=y_of(0.0),
        jump_x=tuple(drawn),
        y_low=low,
        y_high=high,
        t_low=t_low,
        t_high=t_high,
        plotted=len(points),
        total=total,
        stride=stride,
        jumps_drawn=len(drawn),
        jumps_total=len(tuple(jump_indices)),
        x_is_step_index=x_is_step_index,
    )


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """One reason an estimate does not carry the information its name implies.

    Never a verdict. ``detail`` explains what the number *is* under the
    circumstances, so a reader can decide for themselves; it does not say whether
    that is acceptable, because acceptability is a protocol question and no
    protocol has passed G3.
    """

    code: str
    label: str
    detail: str


def diagnose_diffusion(fit: DiffusionFit) -> tuple[Diagnostic, ...]:
    """Identifiability notes for a drift-diffusion fit.

    The drift standard error is deliberately *not* a diagnostic. It is reported
    as a row on the page, because comparing it to the point estimate would be an
    inferential threshold.
    """
    found: list[Diagnostic] = []
    if fit.observations < 2:
        found.append(
            Diagnostic(
                code="single-increment",
                label="one increment",
                detail=(
                    "With a single increment the drift is that increment and the "
                    "volatility is exactly zero by construction. Neither is estimated."
                ),
            )
        )
    return tuple(found)


def diagnose_ornstein_uhlenbeck(
    fit: OrnsteinUhlenbeckFit, *, path: Sequence[float]
) -> tuple[Diagnostic, ...]:
    """Identifiability notes for an OU fit, read against the path it came from.

    The path is required because the most dangerous OU failure is only visible
    beside it: a level far outside the range the belief ever visited is an
    extrapolation from a pull too weak to locate one, not an observed resting
    point.
    """
    found: list[Diagnostic] = []
    if fit.observations < 2:
        found.append(
            Diagnostic(
                code="single-increment",
                label="one increment",
                detail="A single increment cannot separate a pull from a step.",
            )
        )
    if fit.reversion_rate < 0.0:
        found.append(
            Diagnostic(
                code="no-reversion",
                label="no reversion detected",
                detail=(
                    "The fitted reversion rate is not positive, so the half-life is "
                    "infinite and the fitted level is not a value the belief is pulled "
                    "toward. The driftless random walk is nested at a reversion rate of "
                    "zero, and this path does not leave it."
                ),
            )
        )
    elif fit.reversion_rate == 0.0:
        found.append(
            Diagnostic(
                code="level-unidentified",
                label="level unidentified",
                detail=(
                    "The estimator detected no pull at all and reported the sample mean. "
                    "The level is unidentified rather than zero."
                ),
            )
        )
    if path:
        low, high = min(path), max(path)
        span = high - low
        if not (low - span <= fit.level <= high + span):
            found.append(
                Diagnostic(
                    code="level-off-path",
                    label="level outside the observed range",
                    detail=(
                        f"The fitted level of {fit.level:+.3f} lies outside the range "
                        f"[{low:+.3f}, {high:+.3f}] the belief actually visited. It is an "
                        "extrapolation from a weak pull, not a resting point the data show."
                    ),
                )
            )
    return tuple(found)


def diagnose_jump_diffusion(fit: JumpDiffusionFit) -> tuple[Diagnostic, ...]:
    """Resolution notes for a jump-diffusion fit."""
    found: list[Diagnostic] = []
    if fit.jump_count == 0:
        found.append(
            Diagnostic(
                code="no-jumps-detected",
                label="no jumps detected",
                detail=(
                    "No increment exceeded the robust threshold, so this reduces to the "
                    "plain diffusion and reports an intensity of zero. That is a "
                    "detection floor, not a measured absence: a jump smaller than the "
                    "diffusion's own noise is not detectable by this or any threshold rule."
                ),
            )
        )
    elif fit.jump_count == 1:
        found.append(
            Diagnostic(
                code="jump-scale-unresolved",
                label="jump scale unresolved",
                detail=(
                    "One flagged jump gives a jump scale of exactly zero. The scale is "
                    "not estimated; it is what a single observation forces."
                ),
            )
        )
    if fit.observations > 0 and fit.jump_count / fit.observations > JUMP_FRACTION_CEILING:
        found.append(
            Diagnostic(
                code="jump-fraction-high",
                label="a large share of increments flagged",
                detail=(
                    f"{fit.jump_count} of {fit.observations} increments were flagged as "
                    "jumps. CFI-005 traced this signature to a saturating path collapsing "
                    "the robust scale until ordinary diffusive movement was flagged."
                ),
            )
        )
    return tuple(found)


def diagnose_bayesian(fit: BayesianFit) -> tuple[Diagnostic, ...]:
    """Identifiability notes for per-evidence log-likelihood ratios.

    The predicate is structural and integer, not a float comparison against the
    residual scale. Measured: with one increment per evidence id the residual
    scale is exactly 0.0 *even under reporting noise*, because each estimate is
    its own single observation. It is repetition, not noise, that makes a
    residual informative.
    """
    found: list[Diagnostic] = []
    distinct = len(fit.llr_by_evidence)
    if distinct and fit.observations <= distinct:
        found.append(
            Diagnostic(
                code="one-increment-per-evidence",
                label="one increment per evidence item",
                detail=(
                    f"{fit.observations} increments across {distinct} evidence ids: each "
                    "id labels at most one increment, so every fitted ratio is that "
                    "increment and every residual is zero by construction. The residual "
                    "scale here measures the parameterisation, not the fit."
                ),
            )
        )
    elif fit.residual_scale <= ZERO_SCALE:
        found.append(
            Diagnostic(
                code="zero-residual",
                label="residuals vanish",
                detail=(
                    "Residuals fall to machine precision: the fitted ratios reproduce the "
                    "increments exactly, so the residual scale carries no information "
                    "about goodness of fit."
                ),
            )
        )
    return tuple(found)


def diagnose_asymmetric_bayesian(fit: AsymmetricBayesianFit) -> tuple[Diagnostic, ...]:
    """Identifiability notes for direction-split updating weights."""
    found: list[Diagnostic] = []
    if fit.observations < 2:
        found.append(
            Diagnostic(
                code="single-increment",
                label="one increment",
                detail="Two weights cannot be separated from a single increment.",
            )
        )
    if fit.residual_scale <= ZERO_SCALE:
        found.append(
            Diagnostic(
                code="zero-residual",
                label="residuals vanish",
                detail=(
                    "Residuals fall to machine precision: the two weights reproduce every "
                    "increment exactly, so the residual scale says nothing about fit."
                ),
            )
        )
    return tuple(found)


# ---------------------------------------------------------------------------
# Fit panels — an estimator's output, or its refusal, made renderable
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FitPanel:
    """One estimator applied to one trajectory.

    ``error`` holds the estimator's own message when it refused. A refusal is
    reported verbatim and **never** accompanied by a substitute number.
    """

    model: str
    title: str
    rows: tuple[tuple[str, str], ...] = ()
    diagnostics: tuple[Diagnostic, ...] = ()
    notes: tuple[str, ...] = ()
    error: str | None = None
    flagged_rows: tuple[str, ...] = ()

    @property
    def refused(self) -> bool:
        return self.error is not None

    @property
    def degraded(self) -> bool:
        return self.refused or bool(self.diagnostics)


def _fmt(value: float, places: int = 4) -> str:
    """Format a number for a table cell.

    Normalises ``-0.0`` to ``0.0`` — it is the same number and the minus sign
    reads as information — and renders an infinite half-life as words, since a
    bare ``inf`` looks like a bug rather than the statement that there is no
    reversion to have a half-life.
    """
    if math.isinf(value):
        return "∞ — no reversion detected"
    if math.isnan(value):
        return "not a number"
    if value == 0.0:
        value = 0.0
    return f"{value:+.{places}f}"


def diffusion_panel(trajectory: BeliefTrajectory) -> FitPanel:
    """Drift and volatility, with the drift's own precision reported beside it."""
    try:
        fit = fit_diffusion(trajectory)
    except ValueError as exc:  # noqa: BLE001 - see _refused
        return _refused("diffusion", "Drift-diffusion", exc)
    horizon = math.fsum(trajectory.intervals())
    standard_error = fit.volatility / math.sqrt(horizon) if horizon > 0 else math.inf
    return FitPanel(
        model="diffusion",
        title="Drift-diffusion",
        rows=(
            ("drift", _fmt(fit.drift)),
            ("volatility", _fmt(fit.volatility)),
            ("increments", str(fit.observations)),
            ("horizon", _fmt(horizon, 3)),
            ("drift standard error (σ/√T)", _fmt(standard_error)),
        ),
        diagnostics=diagnose_diffusion(fit),
        notes=(
            "The drift standard error is reported, never compared to the drift. "
            "Comparing them would be an inferential threshold, and no protocol has "
            "passed the G3 gate that would fix one.",
        ),
    )


def ornstein_uhlenbeck_panel(trajectory: BeliefTrajectory) -> FitPanel:
    """Mean reversion, checked against the range the belief actually visited."""
    try:
        fit = fit_ornstein_uhlenbeck(trajectory)
    except ValueError as exc:  # noqa: BLE001 - see _refused
        return _refused("ornstein-uhlenbeck", "Ornstein-Uhlenbeck", exc)
    path = trajectory.log_odds_path()
    return FitPanel(
        model="ornstein-uhlenbeck",
        title="Ornstein-Uhlenbeck",
        rows=(
            ("reversion rate", _fmt(fit.reversion_rate)),
            ("level", _fmt(fit.level)),
            ("volatility", _fmt(fit.volatility)),
            ("half-life", _fmt(fit.half_life)),
            ("observed range", f"{_fmt(min(path), 3)} to {_fmt(max(path), 3)}"),
        ),
        diagnostics=diagnose_ornstein_uhlenbeck(fit, path=path),
        notes=(
            "CFI-005 measured this estimator's reversion rate as biased upward by "
            "about 10.7 percent, the classic small-sample bias of the autoregressive "
            "coefficient. It reports belief as more strongly mean-reverting than it is.",
        ),
        flagged_rows=("level", "reversion rate", "half-life"),
    )


def jump_diffusion_panel(
    trajectory: BeliefTrajectory, *, threshold: float = JUMP_THRESHOLD
) -> FitPanel:
    """Diffusion and discrete revisions, separated by a robust threshold."""
    try:
        fit = fit_jump_diffusion(trajectory, threshold=threshold)
    except ValueError as exc:  # noqa: BLE001 - see _refused
        return _refused("jump-diffusion", "Jump-diffusion", exc)
    gaps = trajectory.intervals()
    mean_gap = math.fsum(gaps) / len(gaps)
    # Approximate: the estimator's own robust scale is not exposed on the fit, and
    # recomputing the median absolute deviation here would duplicate estimator
    # logic that could then drift from it. The label says so.
    approx_threshold = threshold * fit.volatility * math.sqrt(mean_gap)
    indices = ", ".join(str(i) for i in fit.jump_indices) if fit.jump_indices else "none"
    return FitPanel(
        model="jump-diffusion",
        title="Jump-diffusion",
        rows=(
            ("drift", _fmt(fit.drift)),
            ("volatility", _fmt(fit.volatility)),
            ("jump intensity", _fmt(fit.jump_intensity)),
            ("jump mean", _fmt(fit.jump_mean)),
            ("jump scale", _fmt(fit.jump_scale)),
            ("jumps detected", f"{fit.jump_count} of {fit.observations} increments"),
            ("flagged increment indices", indices),
            (
                "approximate detection threshold (uses the fitted volatility, "
                "not the estimator's internal robust scale)",
                _fmt(approx_threshold),
            ),
        ),
        diagnostics=diagnose_jump_diffusion(fit),
        notes=(
            "CFI-005 measured this estimator recovering about 66 percent of simulated "
            "jumps in its reference design, because a jump below the detection "
            "threshold is indistinguishable from diffusion. It under-reports rather "
            "than guessing.",
        ),
        flagged_rows=("jump intensity", "jump scale", "jumps detected"),
    )


def bayesian_panel(trajectory: BeliefTrajectory) -> FitPanel:
    """Per-evidence log-likelihood ratios."""
    try:
        fit = fit_bayesian(trajectory)
    except ValueError as exc:  # noqa: BLE001 - see _refused
        return _refused("bayesian", "Exact Bayesian updating", exc)
    ratios = tuple(
        (f"log-likelihood ratio · {name}", _fmt(value))
        # sorted, never set iteration: hash order would break byte-identical output
        for name, value in sorted(fit.llr_by_evidence.items())
    )
    return FitPanel(
        model="bayesian",
        title="Exact Bayesian updating",
        rows=(
            *ratios,
            ("distinct evidence ids", str(len(fit.llr_by_evidence))),
            ("increments", str(fit.observations)),
            ("residual scale", _fmt(fit.residual_scale)),
        ),
        diagnostics=diagnose_bayesian(fit),
        notes=(
            "In log-odds, Bayes' rule is addition: each evidence item contributes its "
            "log-likelihood ratio and nothing else.",
        ),
        flagged_rows=("residual scale",),
    )


def asymmetric_bayesian_panel(
    trajectory: BeliefTrajectory, nominal_llrs: Sequence[float]
) -> FitPanel:
    """Separate weights on confirming and disconfirming evidence."""
    try:
        fit = fit_asymmetric_bayesian(trajectory, nominal_llrs)
    except ValueError as exc:  # noqa: BLE001 - see _refused
        return _refused("asymmetric-bayesian", "Asymmetric Bayesian updating", exc)
    return FitPanel(
        model="asymmetric-bayesian",
        title="Asymmetric Bayesian updating",
        rows=(
            ("confirming weight", _fmt(fit.confirming_weight)),
            ("disconfirming weight", _fmt(fit.disconfirming_weight)),
            ("asymmetry", _fmt(fit.asymmetry)),
            ("increments", str(fit.observations)),
            ("residual scale", _fmt(fit.residual_scale)),
        ),
        diagnostics=diagnose_asymmetric_bayesian(fit),
        notes=(
            "Exact Bayesian updating is nested here at weights of one and one, so the "
            "asymmetry is the signed distance from exact updating.",
        ),
        flagged_rows=("residual scale",),
    )


def _refused(model: str, title: str, exc: ValueError) -> FitPanel:
    """Render an estimator's own refusal, verbatim and without a substitute.

    Only ``ValueError`` reaches here. ``SchemaError``, ``SaturatedBeliefError``
    and ``LinearAlgebraError`` are all subclasses of it, so one clause covers
    every documented refusal. Catching ``Exception`` instead would render a bug
    in this module as an estimator refusal — which is exactly the failure this
    laboratory has recorded twice, an instrument quietly producing a plausible
    output instead of stopping.
    """
    return FitPanel(model=model, title=title, error=str(exc))


# ---------------------------------------------------------------------------
# Cases — the synthetic fixtures, defined by seed rather than committed
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TrajectoryCase:
    """One page's worth of subject: a path, the fits taken from it, or a refusal."""

    name: str
    title: str
    blurb: str
    generator: str
    trajectory: BeliefTrajectory | None = None
    fits: tuple[FitPanel, ...] = ()
    error: str | None = None

    @property
    def failed(self) -> bool:
        return self.trajectory is None

    @property
    def degraded(self) -> bool:
        return not self.failed and any(panel.degraded for panel in self.fits)

    @property
    def state(self) -> str:
        if self.failed:
            return "error"
        return "degraded" if self.degraded else "clean"


_ALTERNATING: tuple[float, ...] = (0.6, -0.5, 0.7, -0.4, 0.55, -0.65, 0.45, -0.35) * 4
_SEED = 20260825


def default_cases() -> tuple[TrajectoryCase, ...]:
    """Build every shipped fixture from its seed.

    Generated rather than committed on purpose. A committed JSON path would be a
    second copy of information that already lives in ``baselines.py``, free to
    drift from it silently; and the error case cannot be committed at all,
    because that state *is* the simulator refusing to record. There is no
    artifact, only a refusal.
    """
    cases: list[TrajectoryCase] = []

    walk = simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, seed=_SEED)
    cases.append(
        TrajectoryCase(
            name="diffusion",
            title="Drifting belief",
            blurb="A belief that drifts steadily upward under constant volatility.",
            generator=(
                f"simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, seed={_SEED})"
            ),
            trajectory=walk,
            fits=(diffusion_panel(walk),),
        )
    )

    reverting = simulate_ornstein_uhlenbeck(
        reversion_rate=1.5, level=0.7, volatility=0.6, steps=400, dt=0.05, seed=_SEED
    )
    cases.append(
        TrajectoryCase(
            name="ornstein-uhlenbeck",
            title="Reverting belief",
            blurb="A belief pulled back toward a resting level whenever it wanders.",
            generator=(
                "simulate_ornstein_uhlenbeck(reversion_rate=1.5, level=0.7, "
                f"volatility=0.6, steps=400, dt=0.05, seed={_SEED})"
            ),
            trajectory=reverting,
            fits=(ornstein_uhlenbeck_panel(reverting), diffusion_panel(reverting)),
        )
    )

    jumpy = simulate_jump_diffusion(
        drift=0.0,
        volatility=0.5,
        jump_intensity=0.8,
        jump_mean=0.0,
        jump_scale=1.2,
        steps=400,
        dt=0.05,
        seed=_SEED,
    )
    cases.append(
        TrajectoryCase(
            name="jump-diffusion",
            title="Belief with discrete revisions",
            blurb=(
                "A diffusing belief interrupted by occasional jumps. The plain "
                "diffusion fit is shown alongside, because ignoring the jumps nearly "
                "doubles the volatility it reports."
            ),
            generator=(
                "simulate_jump_diffusion(drift=0.0, volatility=0.5, jump_intensity=0.8, "
                f"jump_mean=0.0, jump_scale=1.2, steps=400, dt=0.05, seed={_SEED})"
            ),
            trajectory=jumpy,
            fits=(jump_diffusion_panel(jumpy), diffusion_panel(jumpy)),
        )
    )

    repeated = simulate_bayesian(
        list(_ALTERNATING),
        seed=_SEED,
        report_noise=0.2,
        evidence_ids=["e-confirm", "e-disconfirm"] * 16,
    )
    cases.append(
        TrajectoryCase(
            name="bayesian-repeated-evidence",
            title="Bayesian updating, evidence repeated",
            blurb=(
                "Two evidence items shown sixteen times each. Because each ratio is "
                "estimated from many increments, the residual scale carries real "
                "information about fit."
            ),
            generator=(
                f"simulate_bayesian(ALTERNATING, seed={_SEED}, report_noise=0.2, "
                'evidence_ids=["e-confirm", "e-disconfirm"] * 16)'
            ),
            trajectory=repeated,
            fits=(bayesian_panel(repeated), asymmetric_bayesian_panel(repeated, _ALTERNATING)),
        )
    )

    one_shot = simulate_asymmetric_bayesian(
        list(_ALTERNATING),
        confirming_weight=1.4,
        disconfirming_weight=0.6,
        seed=_SEED,
        report_noise=0.25,
    )
    cases.append(
        TrajectoryCase(
            name="bayesian-one-shot-evidence",
            title="Bayesian updating, evidence never repeated",
            blurb=(
                "The same subject, with every evidence item unique. The asymmetric fit "
                "recovers both weights; the per-evidence fit cannot, and says so."
            ),
            generator=(
                "simulate_asymmetric_bayesian(ALTERNATING, confirming_weight=1.4, "
                f"disconfirming_weight=0.6, seed={_SEED}, report_noise=0.25)"
            ),
            trajectory=one_shot,
            fits=(
                asymmetric_bayesian_panel(one_shot, _ALTERNATING),
                bayesian_panel(one_shot),
            ),
        )
    )

    cases.append(
        TrajectoryCase(
            name="walk-fitted-as-reverting",
            title="A walk, asked the wrong questions",
            blurb=(
                "The same path as the drifting belief, handed to three more estimators. "
                "Each answers. Only one of the answers means anything."
            ),
            generator=(
                "simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, "
                f"seed={_SEED})  # the same trajectory as 'diffusion'"
            ),
            trajectory=walk,
            fits=(
                diffusion_panel(walk),
                ornstein_uhlenbeck_panel(walk),
                jump_diffusion_panel(walk),
                bayesian_panel(walk),
            ),
        )
    )

    try:
        simulate_diffusion(drift=50.0, volatility=0.1, steps=200, dt=0.1, seed=3)
    except ValueError as exc:
        cases.append(
            TrajectoryCase(
                name="saturated-belief",
                title="A belief the schema cannot record",
                blurb=(
                    "A drift strong enough to carry the belief past the representable "
                    "range. The simulator refuses rather than pinning the report at the "
                    "boundary and emitting zeros the estimators would read as data."
                ),
                generator=(
                    "simulate_diffusion(drift=50.0, volatility=0.1, steps=200, dt=0.1, seed=3)"
                ),
                error=str(exc),
            )
        )
    else:  # pragma: no cover - reachable only if the saturation guard is removed
        raise BeliefSiteError(
            "the saturated-belief fixture no longer raises; the guard that makes "
            "unrepresentable beliefs loud has regressed"
        )

    return tuple(cases)


_STATE_RANK = {"clean": 0, "degraded": 1, "error": 2}


def ordered(cases: Sequence[TrajectoryCase]) -> list[TrajectoryCase]:
    """Clean first, then degraded, then error.

    Shared by the index and the metadata so the two cannot disagree about order.
    Alphabetical would open the site on a diagnosed page, and a reader has to see
    what a recovered fit looks like before a diagnosed one means anything.
    """
    return sorted(cases, key=lambda case: (_STATE_RANK[case.state], case.name))


def select_cases(
    cases: Sequence[TrajectoryCase],
    *,
    only: Sequence[str] | None = None,
    empty: bool = False,
) -> tuple[TrajectoryCase, ...]:
    """Choose which cases to build.

    An empty result is reachable only through ``empty=True``. A misspelled
    ``only`` raises instead, so the empty state can never be arrived at by
    accident and then read as "there was nothing to show".
    """
    if empty:
        return ()
    if only is None:
        return tuple(cases)
    known = {case.name: case for case in cases}
    unknown = [name for name in only if name not in known]
    if unknown:
        raise BeliefSiteError(
            f"unknown fixture(s): {', '.join(sorted(unknown))}; known: {', '.join(sorted(known))}"
        )
    return tuple(known[name] for name in only)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

_STYLE = """
:root {
  --canvas: #0b0b0c;
  --panel: #141416;
  --ink: #ede6d6;
  --muted: #9a948a;
  --line: #2a2a2e;
  --accent: #e0a94e;
  --ok: #7fb069;
  --bad: #d9694f;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --sans: "IBM Plex Sans", system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0;
  background: var(--canvas); color: var(--ink);
  font-family: var(--sans); line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 62rem; margin: 0 auto; padding: 2rem 1.25rem 5rem; }
a { color: var(--accent); text-underline-offset: 2px; }
a:focus-visible, button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
main:focus { outline: none; }
/* The skip link is the first focusable element and must be reachable, so it is
   moved off-screen rather than hidden — display:none would remove it from the
   tab order entirely, which is the bug this element exists to prevent. */
.skip {
  position: absolute; left: -9999px; top: 0;
  background: var(--panel); color: var(--ink);
  padding: .6rem .9rem; border: 1px solid var(--accent); border-radius: 2px;
  font-family: var(--mono); font-size: .8rem; z-index: 10;
}
.skip:focus { left: .5rem; top: .5rem; }
h1, h2, h3 { line-height: 1.2; font-weight: 600; }
h1 { font-size: clamp(1.5rem, 4vw, 2.1rem); margin: 0 0 .35rem; }
h2 { font-size: 1.15rem; margin: 2.5rem 0 .75rem; border-bottom: 1px solid var(--line);
     padding-bottom: .4rem; }
h3 { font-size: 1rem; margin: 0 0 .5rem; }
.kicker { font-family: var(--mono); font-size: .74rem; letter-spacing: .08em;
          text-transform: uppercase; color: var(--muted); margin: 0 0 1rem; }
nav { margin: 0 0 1.5rem; font-family: var(--mono); font-size: .78rem; }
.lede { color: var(--muted); max-width: 44rem; }
.meta { display: flex; flex-wrap: wrap; gap: .5rem; margin: 1rem 0 0; padding: 0;
        list-style: none; }
.meta li { font-family: var(--mono); font-size: .72rem; border: 1px solid var(--line);
           padding: .25rem .55rem; border-radius: 2px; color: var(--muted); }
/* These must outspecify `.meta li`, which sets colour and border on every tag. */
.meta li.tag-ok { color: var(--ok);
                  border-color: color-mix(in srgb, var(--ok) 45%, var(--line)); }
.meta li.tag-bad { color: var(--bad);
                   border-color: color-mix(in srgb, var(--bad) 45%, var(--line)); }
.meta li.tag-accent { color: var(--accent);
                      border-color: color-mix(in srgb, var(--accent) 45%, var(--line)); }
ul.cards { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
           margin: 1.5rem 0 0; padding: 0; list-style: none; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 3px;
        padding: 1.1rem 1.15rem; }
.card p { margin: 0 0 .8rem; color: var(--muted); font-size: .9rem; }
.chart-svg { display: block; width: 100%; height: auto; background: var(--panel);
             border: 1px solid var(--line); border-radius: 3px; }
.c-bg { fill: var(--panel); }
.c-zero { stroke: var(--muted); stroke-width: 1; stroke-dasharray: 6 5;
          vector-effect: non-scaling-stroke; }
.c-jump { stroke: var(--bad); stroke-width: 1; stroke-dasharray: 2 4;
          vector-effect: non-scaling-stroke; }
.c-path { fill: none; stroke: var(--accent); stroke-width: 1.5; stroke-linejoin: round;
          stroke-linecap: round; vector-effect: non-scaling-stroke; }
figure { margin: 1.5rem 0 0; }
figcaption { color: var(--muted); font-size: .85rem; margin-top: .6rem; max-width: 44rem; }
table { width: 100%; border-collapse: collapse; font-size: .88rem; }
caption { text-align: left; font-family: var(--mono); font-size: .72rem;
          text-transform: uppercase; letter-spacing: .06em; color: var(--muted);
          padding-bottom: .5rem; }
th, td { text-align: left; padding: .5rem .6rem; border-bottom: 1px solid var(--line);
         vertical-align: top; }
th { font-family: var(--mono); font-size: .7rem; text-transform: uppercase;
     letter-spacing: .06em; color: var(--muted); font-weight: 500; }
tbody th[scope="row"] { text-transform: none; letter-spacing: 0; font-size: .78rem; }
tr.is-flagged td, tr.is-flagged th { color: var(--bad); }
code { font-family: var(--mono); font-size: .78rem; color: var(--muted);
       word-break: break-all; }
.scroll { overflow-x: auto; }
/* Negative offset so the ring is not clipped by the scroll container itself. */
.scroll:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: 3px;
         padding: 1.1rem 1.15rem; margin: 1.25rem 0 0; }
.panel.is-degraded { border-color: color-mix(in srgb, var(--bad) 45%, var(--line)); }
.panel.is-refused { border-color: color-mix(in srgb, var(--bad) 60%, var(--line)); }
.diagnostics { margin: 1rem 0 0; padding: 0; list-style: none; }
.diagnostics li { border-left: 2px solid var(--bad); padding: .5rem .8rem;
                  margin-bottom: .6rem; font-size: .88rem; color: var(--muted); }
.diagnostics strong { color: var(--bad); font-family: var(--mono); font-size: .78rem;
                      display: block; margin-bottom: .2rem; }
.verbatim { white-space: pre-wrap; margin: .6rem 0 0; }
.note { background: var(--panel); border-left: 2px solid var(--accent);
        padding: .9rem 1.1rem; margin: 1.5rem 0; font-size: .9rem; color: var(--muted); }
.note.note-bad { border-left-color: var(--bad); }
.note strong { color: var(--ink); }
ul.plain { padding-left: 1.1rem; color: var(--muted); font-size: .9rem; }
footer { margin-top: 4rem; padding-top: 1.25rem; border-top: 1px solid var(--line);
         font-family: var(--mono); font-size: .72rem; color: var(--muted); }
@media (prefers-reduced-motion: no-preference) {
  .card { transition: border-color .15s ease; }
  .card:hover { border-color: var(--accent); }
}
"""


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _page(title: str, body: str) -> str:
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{_esc(title)}</title>\n"
        f"<style>{_STYLE}</style>\n"
        "</head>\n<body>\n"
        '<a class="skip" href="#main">Skip to content</a>\n'
        f'<div class="wrap">\n{body}\n</div>\n'
        "</body>\n</html>\n"
    )


def _footer() -> str:
    return (
        "<footer>\n"
        "<p>Christopher Noxon DeWitt · Charlotte, North Carolina · Status: Prototype</p>\n"
        "<p>Independent student research artifact. UNC-Chapel Hill is identified "
        "for educational context and does not endorse this project.</p>\n"
        '<p><a href="https://www.dewitt-labs.com">Return to academic portfolio →</a></p>\n'
        "</footer>"
    )


def _caveat() -> str:
    """The standing disclosure, on every page without exception."""
    return (
        '<div class="note">\n'
        "<p><strong>Every path here is synthetic.</strong> These trajectories were "
        "generated by <code>drl_cfi.baselines</code> from a fixed seed. No human and no "
        "model was observed, no dataset is implicated, and each record says so in its "
        "own <code>source_rights_id</code>.</p>\n"
        "<p>The fits are reported <strong>without a verdict</strong>. Whether a given "
        "estimate is fit for a purpose depends on an estimand and a tolerance that a "
        "preregistered protocol fixes, and no protocol has passed the G3 gate. This "
        "viewer reports and stops.</p>\n"
        "</div>"
    )


def _scroll_table(caption: str, caption_id: str, inner: str) -> str:
    """Wrap a table so a keyboard user can actually scroll it.

    The region takes its accessible name from the caption, so a screen-reader
    user reaching it by tab knows which table they are in rather than hearing an
    unnamed scrollable region.
    """
    return (
        f'<div class="scroll" tabindex="0" role="region" aria-labelledby="{_esc(caption_id)}">\n'
        f'<table>\n<caption id="{_esc(caption_id)}">{_esc(caption)}</caption>\n'
        f"{inner}\n</table>\n</div>"
    )


def _render_chart(geometry: ChartGeometry, *, ident: str, title: str, description: str) -> str:
    """One belief path as inline SVG, labelled entirely from outside itself."""
    points = " ".join(f"{x:.2f},{y:.2f}" for x, y in geometry.points)
    rules = "\n".join(
        f'<line class="c-jump" x1="{x:.2f}" y1="{PAD_Y:.2f}" '
        f'x2="{x:.2f}" y2="{VIEW_H - PAD_Y:.2f}"></line>'
        for x in geometry.jump_x
    )
    return (
        f'<svg class="chart-svg" viewBox="0 0 {VIEW_W:.0f} {VIEW_H:.0f}" role="img" '
        f'aria-labelledby="cv-{_esc(ident)}-t cv-{_esc(ident)}-d" focusable="false" '
        'preserveAspectRatio="xMidYMid meet">\n'
        f'<title id="cv-{_esc(ident)}-t">{_esc(title)}</title>\n'
        f'<desc id="cv-{_esc(ident)}-d">{_esc(description)}</desc>\n'
        f'<rect class="c-bg" x="0" y="0" width="{VIEW_W:.0f}" height="{VIEW_H:.0f}"></rect>\n'
        f'<line class="c-zero" x1="{PAD_X:.2f}" y1="{geometry.zero_y:.2f}" '
        f'x2="{VIEW_W - PAD_X:.2f}" y2="{geometry.zero_y:.2f}"></line>\n'
        f"{rules}\n"
        f'<polyline class="c-path" fill="none" points="{points}"></polyline>\n'
        "</svg>"
    )


def _describe(case: TrajectoryCase, geometry: ChartGeometry, jumps: Sequence[int]) -> str:
    """The chart's text equivalent, and the promise that the tables repeat it."""
    trajectory = case.trajectory
    assert trajectory is not None  # noqa: S101 - callers gate on case.failed
    path = trajectory.log_odds_path()
    times = trajectory.times()
    low_i = min(range(len(path)), key=lambda i: path[i])
    high_i = max(range(len(path)), key=lambda i: path[i])
    axis = "step index" if geometry.x_is_step_index else "time"
    jump_sentence = (
        "No increments are marked as jumps."
        if not jumps
        else f"{len(jumps)} increments are marked as jumps by vertical dashed rules."
    )
    return (
        f"Line chart. Log-odds belief runs from {path[0]:+.2f} to {path[-1]:+.2f} over "
        f"{len(path)} recorded steps, plotted against {axis}. The lowest point is "
        f"{path[low_i]:+.2f} at {axis} {times[low_i]:.2f} and the highest is "
        f"{path[high_i]:+.2f} at {axis} {times[high_i]:.2f}. A dashed horizontal rule "
        f"marks log-odds 0, even odds. {jump_sentence} "
        "The same numbers are in the tables below this chart."
    )


def _landmark_table(case: TrajectoryCase, jumps: Sequence[int]) -> str:
    trajectory = case.trajectory
    assert trajectory is not None  # noqa: S101 - callers gate on case.failed
    path = trajectory.log_odds_path()
    times = trajectory.times()
    increments = trajectory.increments()
    biggest = max(range(len(increments)), key=lambda i: abs(increments[i]))
    low_i = min(range(len(path)), key=lambda i: path[i])
    high_i = max(range(len(path)), key=lambda i: path[i])
    rows = [
        ("first belief", _fmt(path[0], 3)),
        ("last belief", _fmt(path[-1], 3)),
        ("net change", _fmt(path[-1] - path[0], 3)),
        ("lowest", f"{_fmt(path[low_i], 3)} at time {times[low_i]:.2f}"),
        ("highest", f"{_fmt(path[high_i], 3)} at time {times[high_i]:.2f}"),
        (
            "largest single increment",
            f"{_fmt(increments[biggest], 3)} at increment {biggest}",
        ),
        ("recorded steps", str(len(path))),
        ("horizon", f"{times[-1] - times[0]:.2f}"),
        (
            "increments flagged as jumps",
            ", ".join(str(i) for i in jumps) if jumps else "none",
        ),
    ]
    body = "\n".join(
        f'<tr><th scope="row">{_esc(name)}</th><td>{_esc(value)}</td></tr>' for name, value in rows
    )
    return _scroll_table(
        "Landmarks of the belief path",
        f"lm-{case.name}",
        f'<thead><tr><th scope="col">landmark</th><th scope="col">value</th></tr></thead>\n'
        f"<tbody>\n{body}\n</tbody>",
    )


def _step_table(case: TrajectoryCase) -> str:
    trajectory = case.trajectory
    assert trajectory is not None  # noqa: S101 - callers gate on case.failed
    path = trajectory.log_odds_path()
    times = trajectory.times()
    events = list(trajectory)
    total = len(path)
    stride = 1 if total <= TABLE_ROWS else math.ceil(total / TABLE_ROWS)
    kept = list(range(0, total, stride))
    if kept[-1] != total - 1:
        kept.append(total - 1)
    body = "\n".join(
        f'<tr><th scope="row">{index}</th>'
        f"<td>{times[index]:.2f}</td>"
        f"<td>{_fmt(path[index], 3)}</td>"
        f"<td>{events[index].reported_probability:.6f}</td>"
        f"<td>{_esc(events[index].evidence_id or '—')}</td></tr>"
        for index in kept
    )
    caption = (
        f"Belief path — all {total} recorded steps"
        if stride == 1
        else (
            f"Belief path — {len(kept)} of the {total} recorded steps "
            f"(every {stride}th, plus the first and the last)"
        )
    )
    return _scroll_table(
        caption,
        f"st-{case.name}",
        '<thead><tr><th scope="col">step</th><th scope="col">time</th>'
        '<th scope="col">log-odds</th><th scope="col">probability</th>'
        '<th scope="col">evidence</th></tr></thead>\n'
        f"<tbody>\n{body}\n</tbody>",
    )


def _render_panel(case: TrajectoryCase, panel: FitPanel) -> str:
    classes = ["panel"]
    if panel.refused:
        classes.append("is-refused")
    elif panel.diagnostics:
        classes.append("is-degraded")
    parts = [f'<section class="{" ".join(classes)}">', f"<h3>{_esc(panel.title)}</h3>"]

    if panel.refused:
        parts.append(
            '<p class="lede">This estimator refused. Its own message is reproduced '
            "below, and no substitute number is shown in its place.</p>"
        )
        parts.append(f'<p class="verbatim"><code>{_esc(panel.error)}</code></p>')
    else:
        flagged = set(panel.flagged_rows) if panel.diagnostics else set()
        rows = "\n".join(
            f"<tr{' class="is-flagged"' if name in flagged else ''}>"
            f'<th scope="row">{_esc(name)}</th><td>{_esc(value)}</td></tr>'
            for name, value in panel.rows
        )
        parts.append(
            _scroll_table(
                f"{panel.title} — fitted values",
                f"fp-{case.name}-{panel.model}",
                '<thead><tr><th scope="col">parameter</th>'
                '<th scope="col">value</th></tr></thead>\n'
                f"<tbody>\n{rows}\n</tbody>",
            )
        )

    if panel.diagnostics:
        items = "\n".join(
            f"<li><strong>{_esc(d.label)}</strong>{_esc(d.detail)}</li>" for d in panel.diagnostics
        )
        parts.append(f'<ul class="diagnostics">\n{items}\n</ul>')

    for note in panel.notes:
        parts.append(f'<p class="lede">{_esc(note)}</p>')
    parts.append("</section>")
    return "\n".join(parts)


def render_case_page(case: TrajectoryCase) -> str:
    """One trajectory as a page — clean, degraded, or error."""
    parts = [
        "<header>",
        '<p class="kicker">Belief-trajectory viewer · CFI-007</p>',
        '<nav aria-label="Viewer"><a href="index.html">← all trajectories</a></nav>',
        "</header>",
        '<main id="main" tabindex="-1">',
        f"<h1>{_esc(case.title)}</h1>",
        f'<p class="lede">{_esc(case.blurb)}</p>',
    ]

    if case.failed:
        parts.append('<ul class="meta"><li class="tag-bad">not recorded</li></ul>')
        parts.append(
            '<div class="note note-bad">\n'
            "<p><strong>No trajectory was recorded.</strong> The simulator refused, and "
            "its message is reproduced verbatim below. There is no chart, no table and "
            "no fitted value on this page, because there is no path to describe.</p>\n"
            f'<p class="verbatim"><code>{_esc(case.error)}</code></p>\n'
            "<p>This is the behaviour the CFI-005 recovery study was rewritten to "
            "produce. An earlier version pinned an unrepresentable belief at the "
            "boundary instead, which emitted a run of identical records that the "
            "estimators read as a subject who had stopped updating.</p>\n"
            "</div>"
        )
        parts.append("<h2>Reproduction</h2>")
        parts.append(f"<p><code>{_esc(case.generator)}</code></p>")
        parts.append(_caveat())
        parts.append("</main>")
        parts.append(_footer())
        return _page(f"{case.title} — belief-trajectory viewer", "\n".join(parts))

    trajectory = case.trajectory
    assert trajectory is not None  # noqa: S101 - guarded by case.failed above
    jumps: tuple[int, ...] = ()
    for panel in case.fits:
        if panel.model == "jump-diffusion" and not panel.refused:
            for name, value in panel.rows:
                if name == "flagged increment indices" and value != "none":
                    jumps = tuple(int(part) for part in value.split(", "))

    state_chip = (
        '<li class="tag-bad">degraded</li>'
        if case.degraded
        else '<li class="tag-ok">recovered</li>'
    )
    first = next(iter(trajectory))
    chips = [
        state_chip,
        f'<li class="tag-accent">maturity: {_esc(trajectory.maturity.value)}</li>',
        f"<li>subject: {_esc(trajectory.subject_kind.value)}</li>",
        f"<li>{len(trajectory)} events</li>",
        f"<li>seed {_esc(first.seed)}</li>",
        f"<li>study {_esc(first.study_id)}</li>",
    ]
    parts.append(f'<ul class="meta">{"".join(chips)}</ul>')

    if case.degraded:
        labels = sorted({d.label for panel in case.fits for d in panel.diagnostics})
        refused = sorted(p.title for p in case.fits if p.refused)
        sentences = []
        if labels:
            sentences.append("Diagnostics on this page: " + "; ".join(labels) + ".")
        if refused:
            sentences.append("Refused outright: " + ", ".join(refused) + ".")
        parts.append(
            '<div class="note note-bad">\n'
            "<p><strong>This page reports numbers the estimators cannot vouch for.</strong> "
            "Each flagged value is still shown, because hiding it would be its own kind of "
            "dishonesty. What follows every flagged panel is a statement of what the number "
            "is under the circumstances — not a judgement of whether it is good.</p>\n"
            f"<p>{_esc(' '.join(sentences))}</p>\n"
            "</div>"
        )

    geometry = chart_geometry(trajectory.times(), trajectory.log_odds_path(), jump_indices=jumps)
    description = _describe(case, geometry, jumps)
    caption_bits = [
        f"Log-odds from {_fmt(geometry.y_low, 2)} to {_fmt(geometry.y_high, 2)}",
        f"{geometry.total} recorded steps",
    ]
    if geometry.is_strided:
        caption_bits.append(f"showing every {geometry.stride}th point")
    if geometry.jumps_total > geometry.jumps_drawn:
        caption_bits.append(f"{geometry.jumps_drawn} of {geometry.jumps_total} jump rules drawn")
    parts.append("<h2>Belief path</h2>")
    parts.append(
        "<figure>\n"
        + _render_chart(
            geometry,
            ident=case.name,
            title=f"Belief path in log-odds for {case.title}",
            description=description,
        )
        + f"\n<figcaption>{_esc('. '.join(caption_bits))}. "
        "The dashed horizontal rule is log-odds 0, even odds. "
        "Every value in this chart also appears in the tables below.</figcaption>\n"
        "</figure>"
    )

    parts.append("<h2>Landmarks</h2>")
    parts.append(_landmark_table(case, jumps))
    parts.append("<h2>Recorded steps</h2>")
    parts.append(_step_table(case))

    parts.append("<h2>Fits</h2>")
    for panel in case.fits:
        parts.append(_render_panel(case, panel))

    labelled = [e for e in trajectory if e.evidence_id]
    parts.append("<h2>Evidence</h2>")
    if labelled:
        names = sorted({e.evidence_id for e in labelled if e.evidence_id})
        items = "".join(f"<li><code>{_esc(name)}</code></li>" for name in names)
        parts.append(f'<ul class="plain">{items}</ul>')
    else:
        parts.append(
            '<p class="lede">This trajectory carries no evidence labels. It records how a '
            "belief moved, not what moved it, so no per-evidence ratio can be attributed "
            "to it.</p>"
        )

    parts.append("<h2>Reproduction</h2>")
    parts.append(f"<p><code>{_esc(case.generator)}</code></p>")
    parts.append(
        "<p><code>uv run python scripts/build_belief_site.py --out site/beliefs "
        "--metadata</code></p>"
    )

    provenance = [
        ("study", first.study_id),
        ("run", first.run_id),
        ("subject", f"{first.subject_id} ({first.subject_kind.value})"),
        ("model or cohort revision", first.model_or_cohort_revision),
        ("code revision", first.code_revision),
        ("configuration digest", first.config_digest),
        ("seed", str(first.seed)),
        ("maturity", trajectory.maturity.value),
        ("rights record", first.source_rights_id),
    ]
    rows = "\n".join(
        f'<tr><th scope="row">{_esc(name)}</th><td><code>{_esc(value)}</code></td></tr>'
        for name, value in provenance
    )
    parts.append("<h2>Provenance</h2>")
    parts.append(
        _scroll_table(
            "Where this trajectory came from",
            f"pv-{case.name}",
            '<thead><tr><th scope="col">field</th><th scope="col">value</th></tr></thead>\n'
            f"<tbody>\n{rows}\n</tbody>",
        )
    )

    parts.append(_caveat())
    parts.append("</main>")
    parts.append(_footer())
    return _page(f"{case.title} — belief-trajectory viewer", "\n".join(parts))


def render_index(cases: Sequence[TrajectoryCase]) -> str:
    """The index, including the deliberate empty state."""
    parts = [
        "<header>",
        '<p class="kicker">Belief-trajectory viewer · CFI-007</p>',
        "</header>",
        '<main id="main" tabindex="-1">',
        "<h1>Synthetic belief trajectories</h1>",
        '<p class="lede">Belief in a binary proposition, in log-odds, moving under the '
        "model families the Computational Finance of Intelligence bridge starts from. "
        "Each page shows one path, the estimators applied to it, and — where an estimator "
        "returned a number it cannot vouch for — what that number actually is.</p>",
    ]

    if not cases:
        parts.append(
            '<p class="lede">No trajectories were selected, so there is nothing to show. '
            "This is the viewer's empty state, rendered deliberately: a build that "
            "produces no pages says so, rather than producing a page that looks like a "
            "result.</p>"
        )
        parts.append(
            "<p><code>uv run python scripts/build_belief_site.py --out site/beliefs</code></p>"
        )
    else:
        items = []
        for case in ordered(cases):
            chip = {
                "clean": '<li class="tag-ok">recovered</li>',
                "degraded": '<li class="tag-bad">degraded</li>',
                "error": '<li class="tag-bad">not recorded</li>',
            }[case.state]
            count = f"<li>{len(case.fits)} fits</li>" if case.fits else "<li>no fits</li>"
            items.append(
                '<li class="card">\n'
                f"<h3>{_esc(case.title)}</h3>\n"
                f"<p>{_esc(case.blurb)}</p>\n"
                f'<ul class="meta">{chip}{count}</ul>\n'
                f'<p style="margin-top:.9rem"><a href="{_esc(case.name)}.html">'
                f"Open the {_esc(case.title.lower())} trajectory →</a></p>\n"
                "</li>"
            )
        parts.append(f'<ul class="cards">\n{"".join(items)}\n</ul>')

    parts.append(_caveat())
    parts.append("</main>")
    parts.append(_footer())
    return _page("Synthetic belief trajectories — belief-trajectory viewer", "\n".join(parts))


def build_site(cases: Sequence[TrajectoryCase], output_dir: Path) -> list[Path]:
    """Write the index and one page per case. Returns what was written, in order."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    index = output_dir / "index.html"
    index.write_text(render_index(cases), encoding="utf-8")
    written.append(index)
    for case in ordered(cases):
        page = output_dir / f"{case.name}.html"
        page.write_text(render_case_page(case), encoding="utf-8")
        written.append(page)
    return written


def site_metadata(cases: Sequence[TrajectoryCase]) -> dict[str, Any]:
    """Describe what was published.

    Deliberately carries no ``generated_at``. The whole output is byte-identical
    across builds, and a timestamp would be the one field that is not.
    """
    return {
        "case_count": len(cases),
        "cases": [
            {
                "name": case.name,
                "title": case.title,
                "state": case.state,
                "generator": case.generator,
                "fits": [
                    {
                        "model": panel.model,
                        "refused": panel.refused,
                        "diagnostics": [d.code for d in panel.diagnostics],
                    }
                    for panel in case.fits
                ],
            }
            for case in ordered(cases)
        ],
    }
