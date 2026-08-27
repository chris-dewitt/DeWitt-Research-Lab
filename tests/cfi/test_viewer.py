"""Tests for the CFI-007 belief-trajectory viewer."""

from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
from pathlib import Path

import pytest
from drl_cfi.baselines import (
    MAX_REPRESENTABLE_LOG_ODDS,
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
from drl_cfi.viewer import (
    MAX_POLYLINE_POINTS,
    PAD_X,
    PAD_Y,
    VIEW_H,
    VIEW_W,
    ZERO_SCALE,
    BeliefSiteError,
    TrajectoryCase,
    build_site,
    chart_geometry,
    default_cases,
    diagnose_asymmetric_bayesian,
    diagnose_bayesian,
    diagnose_diffusion,
    diagnose_jump_diffusion,
    diagnose_ornstein_uhlenbeck,
    ordered,
    render_case_page,
    render_index,
    select_cases,
    site_metadata,
)

# The CLI lives in scripts/, which is not a package, so it is loaded by path.
# Testing it at all is the point: the replay-site script cannot be tested,
# because its main() takes no argv.
_CLI_PATH = Path(__file__).resolve().parents[2] / "scripts" / "build_belief_site.py"
_spec = importlib.util.spec_from_file_location("build_belief_site", _CLI_PATH)
assert _spec is not None and _spec.loader is not None
build_belief_site = importlib.util.module_from_spec(_spec)
sys.modules["build_belief_site"] = build_belief_site
_spec.loader.exec_module(build_belief_site)

SEED = 20260825
ALTERNATING = [0.6, -0.5, 0.7, -0.4, 0.55, -0.65, 0.45, -0.35] * 4


def codes(diagnostics: tuple[object, ...]) -> set[str]:
    return {d.code for d in diagnostics}  # type: ignore[attr-defined]


class TestOrnsteinUhlenbeckDiagnostics:
    def test_a_walk_fitted_as_reverting_is_caught(self) -> None:
        # The measurement this whole module exists for: OU on a pure drifting
        # walk reports a resting level of about -16.5 log-odds (p = 6.6e-8) for
        # a path that never went below even odds.
        walk = simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, seed=SEED)
        found = diagnose_ornstein_uhlenbeck(fit_ornstein_uhlenbeck(walk), path=walk.log_odds_path())
        assert "no-reversion" in codes(found)
        assert "level-off-path" in codes(found)

    def test_the_off_path_detail_names_both_ranges(self) -> None:
        walk = simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, seed=SEED)
        path = walk.log_odds_path()
        found = diagnose_ornstein_uhlenbeck(fit_ornstein_uhlenbeck(walk), path=path)
        detail = next(d.detail for d in found if d.code == "level-off-path")
        assert f"{max(path):+.3f}" in detail

    def test_a_genuinely_reverting_path_is_clean(self) -> None:
        path = simulate_ornstein_uhlenbeck(
            reversion_rate=1.5, level=0.7, volatility=0.6, steps=400, dt=0.05, seed=SEED
        )
        assert (
            diagnose_ornstein_uhlenbeck(fit_ornstein_uhlenbeck(path), path=path.log_odds_path())
            == ()
        )

    def test_no_reversion_and_level_unidentified_are_disjoint(self) -> None:
        walk = simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, seed=SEED)
        found = codes(
            diagnose_ornstein_uhlenbeck(fit_ornstein_uhlenbeck(walk), path=walk.log_odds_path())
        )
        assert not ({"no-reversion", "level-unidentified"} <= found)


class TestBayesianDiagnostics:
    def test_one_id_per_increment_is_flagged(self) -> None:
        path = simulate_bayesian(ALTERNATING, seed=SEED)
        fit = fit_bayesian(path)
        assert fit.observations == len(fit.llr_by_evidence)
        assert "one-increment-per-evidence" in codes(diagnose_bayesian(fit))

    def test_reporting_noise_does_not_clear_the_flag(self) -> None:
        # Counter-intuitive and measured: with one id per increment the residual
        # scale is exactly 0.0 even under noise, because each estimate is its own
        # single observation. A float test against the residual would call this
        # clean for the wrong reason.
        path = simulate_bayesian(ALTERNATING, seed=SEED, report_noise=0.2)
        fit = fit_bayesian(path)
        assert fit.residual_scale == 0.0
        assert "one-increment-per-evidence" in codes(diagnose_bayesian(fit))

    def test_repeated_evidence_under_noise_is_clean(self) -> None:
        path = simulate_bayesian(
            ALTERNATING,
            seed=SEED,
            report_noise=0.2,
            evidence_ids=["e-confirm", "e-disconfirm"] * 16,
        )
        fit = fit_bayesian(path)
        assert fit.observations > len(fit.llr_by_evidence)
        assert fit.residual_scale > ZERO_SCALE
        assert diagnose_bayesian(fit) == ()


class TestAsymmetricDiagnostics:
    def test_noiseless_residual_is_below_epsilon_not_equal_to_zero(self) -> None:
        # Pins the reason ZERO_SCALE exists: this lands near 1.9e-13, so an
        # equality test against 0.0 would miss it entirely.
        path = simulate_asymmetric_bayesian(
            ALTERNATING, confirming_weight=1.4, disconfirming_weight=0.6, seed=SEED
        )
        fit = fit_asymmetric_bayesian(path, ALTERNATING)
        assert fit.residual_scale != 0.0
        assert fit.residual_scale <= ZERO_SCALE
        assert "zero-residual" in codes(diagnose_asymmetric_bayesian(fit))

    def test_noise_makes_the_residual_informative(self) -> None:
        path = simulate_asymmetric_bayesian(
            ALTERNATING,
            confirming_weight=1.4,
            disconfirming_weight=0.6,
            seed=SEED,
            report_noise=0.25,
        )
        assert diagnose_asymmetric_bayesian(fit_asymmetric_bayesian(path, ALTERNATING)) == ()


class TestJumpDiagnostics:
    def test_no_jumps_reports_a_detection_floor(self) -> None:
        walk = simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, seed=SEED)
        found = diagnose_jump_diffusion(fit_jump_diffusion(walk))
        assert "no-jumps-detected" in codes(found)
        detail = next(d.detail for d in found if d.code == "no-jumps-detected")
        assert "detection floor" in detail

    def test_a_normal_jump_path_is_clean(self) -> None:
        path = simulate_jump_diffusion(
            drift=0.0,
            volatility=0.5,
            jump_intensity=0.8,
            jump_mean=0.0,
            jump_scale=1.2,
            steps=400,
            dt=0.05,
            seed=SEED,
        )
        assert diagnose_jump_diffusion(fit_jump_diffusion(path)) == ()


class TestDiffusionDiagnostics:
    def test_an_ordinary_path_is_clean(self) -> None:
        path = simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, seed=SEED)
        assert diagnose_diffusion(fit_diffusion(path)) == ()


class TestDiagnosticsCarryNoVerdict:
    def test_no_label_or_detail_uses_verdict_language(self) -> None:
        # G3 has not been passed. A diagnostic says a number is not identified;
        # it must never say the number is bad, or that anything passed or failed.
        walk = simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, seed=SEED)
        collected = (
            diagnose_ornstein_uhlenbeck(fit_ornstein_uhlenbeck(walk), path=walk.log_odds_path())
            + diagnose_jump_diffusion(fit_jump_diffusion(walk))
            + diagnose_bayesian(fit_bayesian(simulate_bayesian(ALTERNATING, seed=SEED)))
        )
        assert collected
        banned = ("pass", "fail", "good", "acceptable", "significant", "invalid", "wrong")
        for diagnostic in collected:
            text = f"{diagnostic.label} {diagnostic.detail}".lower()
            for word in banned:
                assert word not in text, f"{diagnostic.code} uses verdict word {word!r}"


@pytest.mark.parametrize(
    "diagnose",
    [diagnose_diffusion, diagnose_jump_diffusion, diagnose_bayesian, diagnose_asymmetric_bayesian],
)
def test_every_diagnoser_returns_a_tuple(diagnose: object) -> None:
    assert callable(diagnose)


class TestChartGeometry:
    def test_zero_lands_on_the_reference_line(self) -> None:
        geometry = chart_geometry([0.0, 1.0, 2.0], [-1.0, 0.0, 1.0])
        middle_y = geometry.points[1][1]
        assert geometry.zero_y == pytest.approx(middle_y)

    def test_the_domain_always_contains_zero(self) -> None:
        # A path living entirely above even odds still gets its reference line.
        geometry = chart_geometry([0.0, 1.0, 2.0], [4.0, 6.0, 9.0])
        assert geometry.y_low <= 0.0 <= geometry.y_high
        assert PAD_Y <= geometry.zero_y <= VIEW_H - PAD_Y

    def test_endpoints_sit_on_the_padded_edges(self) -> None:
        geometry = chart_geometry([0.0, 1.0, 2.0, 3.0], [0.0, 1.0, -1.0, 2.0])
        assert geometry.points[0][0] == pytest.approx(PAD_X)
        assert geometry.points[-1][0] == pytest.approx(VIEW_W - PAD_X)

    def test_a_flat_path_does_not_divide_by_zero(self) -> None:
        geometry = chart_geometry([0.0, 1.0, 2.0], [0.0, 0.0, 0.0])
        assert geometry.y_low < 0.0 < geometry.y_high
        assert all(math.isfinite(y) for _, y in geometry.points)

    def test_equal_timestamps_fall_back_to_step_index(self) -> None:
        geometry = chart_geometry([5.0, 5.0, 5.0], [0.0, 1.0, 2.0])
        assert geometry.x_is_step_index
        assert geometry.points[0][0] == pytest.approx(PAD_X)
        assert geometry.points[-1][0] == pytest.approx(VIEW_W - PAD_X)

    def test_a_dense_path_is_strided_and_keeps_its_last_point(self) -> None:
        n = 2000
        geometry = chart_geometry([float(i) for i in range(n)], [float(i % 7) for i in range(n)])
        assert geometry.is_strided
        assert geometry.plotted <= MAX_POLYLINE_POINTS + 1
        assert geometry.total == n
        assert geometry.points[-1][0] == pytest.approx(VIEW_W - PAD_X)

    def test_a_shipped_length_path_is_not_strided(self) -> None:
        path = simulate_diffusion(drift=0.4, volatility=0.8, steps=400, dt=0.05, seed=SEED)
        geometry = chart_geometry(path.times(), path.log_odds_path())
        assert not geometry.is_strided
        assert geometry.plotted == geometry.total == 401

    def test_jump_rules_mark_the_landing_point(self) -> None:
        geometry = chart_geometry([0.0, 1.0, 2.0, 3.0], [0.0, 0.0, 5.0, 5.0], jump_indices=[1])
        # increment 1 runs from index 1 to index 2, so the rule sits at index 2.
        assert geometry.jump_x == pytest.approx((geometry.points[2][0],))

    def test_an_out_of_range_jump_index_is_dropped(self) -> None:
        geometry = chart_geometry([0.0, 1.0], [0.0, 1.0], jump_indices=[99])
        assert geometry.jump_x == ()
        assert geometry.jumps_total == 1
        assert geometry.jumps_drawn == 0

    def test_too_short_a_path_is_refused(self) -> None:
        with pytest.raises(ValueError, match="at least two points"):
            chart_geometry([0.0], [0.0])

    def test_mismatched_lengths_are_refused(self) -> None:
        with pytest.raises(ValueError, match="differ in length"):
            chart_geometry([0.0, 1.0, 2.0], [0.0, 1.0])


@pytest.fixture(scope="module")
def cases() -> tuple[TrajectoryCase, ...]:
    return default_cases()


def by_name(cases: tuple[TrajectoryCase, ...], name: str) -> TrajectoryCase:
    return next(case for case in cases if case.name == name)


class TestCases:
    def test_every_state_is_represented(self, cases: tuple[TrajectoryCase, ...]) -> None:
        assert {case.state for case in cases} == {"clean", "degraded", "error"}

    def test_the_headline_case_shows_all_four_panel_states(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        # One trajectory, four estimators: recovered, diagnosed, diagnosed, refused.
        case = by_name(cases, "walk-fitted-as-reverting")
        assert case.state == "degraded"
        assert any(not p.degraded for p in case.fits)
        assert sum(1 for p in case.fits if p.diagnostics and not p.refused) == 2
        assert sum(1 for p in case.fits if p.refused) == 1

    def test_ordering_puts_clean_first_and_error_last(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        states = [case.state for case in ordered(cases)]
        assert states == sorted(states, key=["clean", "degraded", "error"].index)
        assert states[0] == "clean"
        assert states[-1] == "error"


class TestRendering:
    def test_pages_are_self_contained(self, cases: tuple[TrajectoryCase, ...]) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        assert "<style>" in page
        for marker in ("http://", "src=", "cdn", "<script"):
            assert marker not in page.lower()

    def test_landmarks_and_skip_link_are_present(self, cases: tuple[TrajectoryCase, ...]) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        assert '<a class="skip" href="#main">' in page
        assert '<main id="main" tabindex="-1">' in page
        assert "<header>" in page
        assert '<nav aria-label="Viewer">' in page

    def test_the_chart_has_a_text_equivalent(self, cases: tuple[TrajectoryCase, ...]) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        assert 'role="img"' in page
        assert "aria-labelledby=" in page
        assert "<title id=" in page and "<desc id=" in page
        assert 'focusable="false"' in page
        # The description promises the tables repeat it; that promise must hold.
        assert "The same numbers are in the tables below this chart." in page
        assert "<caption" in page

    def test_every_table_has_a_caption(self, cases: tuple[TrajectoryCase, ...]) -> None:
        page = render_case_page(by_name(cases, "walk-fitted-as-reverting"))
        assert page.count("<caption") == page.count("<table")

    def test_every_table_header_is_scoped(self, cases: tuple[TrajectoryCase, ...]) -> None:
        page = render_case_page(by_name(cases, "walk-fitted-as-reverting"))
        unscoped = [tag for tag in re.findall(r"<th\b[^>]*>", page) if "scope=" not in tag]
        assert unscoped == []

    def test_scroll_regions_are_focusable_and_named(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        assert page.count('<div class="scroll"') == page.count('tabindex="0" role="region"')
        assert 'aria-labelledby="lm-diffusion"' in page

    def test_no_information_is_carried_by_colour_alone(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        page = render_case_page(by_name(cases, "jump-diffusion"))
        # zero rule and jump rules are distinguished by dash pattern, not hue,
        # and every flagged increment is also listed by index in a table.
        assert "stroke-dasharray: 6 5" in page
        assert "stroke-dasharray: 2 4" in page
        assert "flagged increment indices" in page

    def test_reduced_motion_stays_opt_in(self, cases: tuple[TrajectoryCase, ...]) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        assert "prefers-reduced-motion: no-preference" in page
        assert "prefers-reduced-motion: reduce" not in page

    def test_house_palette_is_used(self, cases: tuple[TrajectoryCase, ...]) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        for hex_value in ("#0b0b0c", "#141416", "#ede6d6", "#9a948a", "#e0a94e", "#d9694f"):
            assert hex_value in page

    def test_a_clean_page_is_not_marked_degraded(self, cases: tuple[TrajectoryCase, ...]) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        # The chip elements, not the stylesheet — every page carries every rule.
        assert '<li class="tag-ok">recovered</li>' in page
        assert '<li class="tag-bad">' not in page
        assert '<section class="panel is-degraded">' not in page
        assert 'class="is-flagged"' not in page

    def test_a_degraded_page_carries_four_redundant_markers(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        case = by_name(cases, "walk-fitted-as-reverting")
        page = render_case_page(case)
        assert case.degraded  # 1. derived boolean
        assert '<li class="tag-bad">degraded</li>' in page  # 2. chip, literal word
        assert "cannot vouch for" in page  # 3. prose callout
        assert "is-degraded" in page and "is-flagged" in page  # 4. per-panel/row class

    def test_a_refused_panel_shows_the_estimator_message_and_no_substitute(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        page = render_case_page(by_name(cases, "walk-fitted-as-reverting"))
        assert "no evidence-labelled increments" in page
        assert "is-refused" in page
        assert "no substitute number is shown" in page

    def test_the_error_page_refuses_rather_than_substituting(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        page = render_case_page(by_name(cases, "saturated-belief"))
        assert "<svg" not in page
        assert "No trajectory was recorded." in page
        assert f"{MAX_REPRESENTABLE_LOG_ODDS:.3f}" in page

    def test_the_evidence_empty_state_explains_the_absence(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        assert "carries no evidence labels" in page

    def test_the_empty_index_renders_rather_than_raising(self) -> None:
        page = render_index(())
        assert "<h1>" in page
        assert 'class="cards"' not in page
        assert "empty state, rendered deliberately" in page

    def test_the_synthetic_caveat_is_on_every_page(self, cases: tuple[TrajectoryCase, ...]) -> None:
        for case in cases:
            assert "Every path here is synthetic" in render_case_page(case)
        assert "Every path here is synthetic" in render_index(cases)
        assert "Every path here is synthetic" in render_index(())

    def test_no_page_delivers_a_verdict(self, cases: tuple[TrajectoryCase, ...]) -> None:
        # G3 has not been passed, so nothing rendered may read as a threshold
        # result. The bare word "passed" is fine and in fact required — the
        # standing caveat says no protocol has passed G3 — so this looks for
        # verdict *constructions* rather than words.
        verdicts = (
            "is acceptable",
            "is unacceptable",
            "within tolerance",
            "out of tolerance",
            "statistically significant",
            "test passed",
            "test failed",
            "good fit",
            "poor fit",
            "fails the",
            "passes the",
        )
        for case in cases:
            lowered = render_case_page(case).lower()
            for phrase in verdicts:
                assert phrase not in lowered, f"{case.name} says {phrase!r}"

    def test_the_caveat_states_the_absence_of_a_verdict(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        assert "without a verdict" in page
        assert "no protocol has passed the G3 gate" in page

    def test_the_portfolio_disclosure_is_on_every_page(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        page = render_case_page(by_name(cases, "diffusion"))
        assert "Christopher Noxon DeWitt" in page
        assert "does not endorse this project" in page
        assert "www.dewitt-labs.com" in page

    def test_html_is_escaped_in_both_directions(self) -> None:
        hostile = TrajectoryCase(
            name="hostile",
            title="<script>bad()</script>",
            blurb="also <script>bad()</script>",
            generator="x",
            error="<script>bad()</script>",
        )
        page = render_case_page(hostile)
        assert "<script>bad()" not in page
        assert "&lt;script&gt;bad()&lt;/script&gt;" in page

    def test_attribute_injection_is_escaped(self) -> None:
        hostile = TrajectoryCase(
            name="hostile",
            title='" onload="steal()',
            blurb="ok",
            generator="x",
            error="ok",
        )
        page = render_case_page(hostile)
        assert '" onload="steal()' not in page
        assert "&quot;" in page

    def test_rendering_is_deterministic(self, cases: tuple[TrajectoryCase, ...]) -> None:
        case = by_name(cases, "bayesian-repeated-evidence")
        assert render_case_page(case) == render_case_page(case)


class TestBuild:
    def test_writes_an_index_and_a_page_per_case(
        self, cases: tuple[TrajectoryCase, ...], tmp_path: Path
    ) -> None:
        written = build_site(cases, tmp_path)
        assert {path.name for path in written} == {"index.html"} | {
            f"{case.name}.html" for case in cases
        }
        assert all(path.stat().st_size > 0 for path in written)

    def test_the_index_links_every_page(
        self, cases: tuple[TrajectoryCase, ...], tmp_path: Path
    ) -> None:
        build_site(cases, tmp_path)
        index = (tmp_path / "index.html").read_text(encoding="utf-8")
        for case in cases:
            assert f'href="{case.name}.html"' in index

    def test_card_links_are_individually_named(self, cases: tuple[TrajectoryCase, ...]) -> None:
        # Repeated "read more" link text is unusable from a link list.
        index = render_index(cases)
        labels = re.findall(r"<a href=\"[^\"]+\.html\">([^<]+)</a>", index)
        assert len(labels) == len(set(labels)) == len(cases)

    def test_clean_sorts_before_degraded_before_error(
        self, cases: tuple[TrajectoryCase, ...], tmp_path: Path
    ) -> None:
        build_site(cases, tmp_path)
        text = (tmp_path / "index.html").read_text(encoding="utf-8")
        assert text.index("diffusion.html") < text.index("walk-fitted-as-reverting.html")
        assert text.index("walk-fitted-as-reverting.html") < text.index("saturated-belief.html")

    def test_the_build_is_reproducible(
        self, cases: tuple[TrajectoryCase, ...], tmp_path: Path
    ) -> None:
        # Byte-identity transitively proves no timestamp, no id(), no repr of an
        # object and no set-iteration order reached the HTML.
        first = build_site(cases, tmp_path / "a")
        second = build_site(cases, tmp_path / "b")
        assert [p.name for p in first] == [p.name for p in second]
        for left, right in zip(first, second, strict=True):
            assert left.read_text(encoding="utf-8") == right.read_text(encoding="utf-8")

    def test_metadata_order_matches_the_index(self, cases: tuple[TrajectoryCase, ...]) -> None:
        meta = site_metadata(cases)
        assert [entry["name"] for entry in meta["cases"]] == [c.name for c in ordered(cases)]

    def test_metadata_carries_no_timestamp(self, cases: tuple[TrajectoryCase, ...]) -> None:
        assert "generated_at" not in json.dumps(site_metadata(cases))

    def test_an_empty_build_writes_only_the_index(self, tmp_path: Path) -> None:
        written = build_site((), tmp_path)
        assert [path.name for path in written] == ["index.html"]


class TestSelection:
    def test_an_unknown_fixture_is_named(self, cases: tuple[TrajectoryCase, ...]) -> None:
        with pytest.raises(BeliefSiteError, match="unknown fixture"):
            select_cases(cases, only=["nope"])

    def test_the_error_lists_what_is_known(self, cases: tuple[TrajectoryCase, ...]) -> None:
        with pytest.raises(BeliefSiteError, match="diffusion"):
            select_cases(cases, only=["nope"])

    def test_the_empty_state_is_only_reachable_deliberately(
        self, cases: tuple[TrajectoryCase, ...]
    ) -> None:
        assert select_cases(cases, empty=True) == ()
        assert len(select_cases(cases)) == len(cases)


class TestCli:
    def test_listing_exits_zero(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert build_belief_site.main(["--list"]) == 0
        assert "walk-fitted-as-reverting" in capsys.readouterr().out

    def test_an_unknown_fixture_exits_one(
        self, capsys: pytest.CaptureFixture[str], tmp_path: Path
    ) -> None:
        code = build_belief_site.main(["--only", "nope", "--out", str(tmp_path)])
        assert code == 1
        assert "unknown fixture" in capsys.readouterr().err

    def test_a_full_build_exits_zero(self, tmp_path: Path) -> None:
        assert build_belief_site.main(["--out", str(tmp_path), "--metadata"]) == 0
        assert (tmp_path / "site.json").exists()
        assert (tmp_path / "index.html").exists()

    def test_the_empty_state_builds(self, tmp_path: Path) -> None:
        assert build_belief_site.main(["--empty-state", "--out", str(tmp_path)]) == 0
        assert [p.name for p in tmp_path.iterdir()] == ["index.html"]
