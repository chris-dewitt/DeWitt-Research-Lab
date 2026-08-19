"""Tests for the Stage-B bake-off harness.

The load-bearing assertions here are the negative ones. A harness that ranks
candidates is easy; a harness that refuses to name a winner when the evidence is
thin is the thing DIR-004 actually needs, so most of these tests try to make it
declare one and check that it won't.
"""

from __future__ import annotations

import statistics
from pathlib import Path
from typing import Any

import pytest
import yaml
from drl_ai_core import (
    BakeoffError,
    CandidateRun,
    EvidenceGate,
    ScriptedProvider,
    TaskResult,
    grade_response,
    load_task_suite,
    run_bakeoff,
    run_candidate,
    select_winner,
)
from drl_ai_core.bakeoff import BakeoffCandidate
from drl_ai_core.bakeoff_harness import (
    BakeoffTask,
    GraderSpec,
    build_live_providers,
    license_is_cleared,
    load_candidates,
    paired_resolution,
    summarise_blockers,
)
from drl_ai_core.providers import (
    ChatMessage,
    ModelIdentity,
    OutputMode,
    ProviderUnavailableError,
    StructuredModelResponse,
)

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "models" / "bakeoff" / "task_suite.yaml"
REGISTER = ROOT / "models" / "bakeoff" / "candidates.yaml"


def _identity(revision: str = "pinned-1.0.0") -> ModelIdentity:
    return ModelIdentity(
        provider_id="test",
        model_family="test-family",
        revision=revision,
        open_weight=True,
        output_mode=OutputMode.MOCK,
        license_label="Apache-2.0",
    )


def _response(
    content: str, *, latency_ms: float = 10.0, tool_calls: tuple = ()
) -> StructuredModelResponse:
    return StructuredModelResponse(
        content=content,
        identity=_identity(),
        finish_reason="stop",
        latency_ms=latency_ms,
        tool_calls=tool_calls,
    )


def _task(**kwargs) -> BakeoffTask:
    base = {
        "id": "t1",
        "role": "core",
        "category": "routing",
        "prompt": (ChatMessage(role="user", content="hi"),),
        "grader": GraderSpec(must_include=("fedlens",)),
    }
    base.update(kwargs)
    return BakeoffTask(**base)


def _run(candidate_id: str, quality_results: list[TaskResult], **kwargs) -> CandidateRun:
    base = {
        "candidate_id": candidate_id,
        "role": "core",
        "provider_id": "test",
        "revision": "pinned-1.0.0",
        "open_weight": True,
        "license_label": "Apache-2.0",
        "measurement_mode": "hardware",
        "results": tuple(quality_results),
    }
    base.update(kwargs)
    return CandidateRun(**base)


def _results(n: int, score: float, *, safety_critical: bool = False) -> list[TaskResult]:
    return [
        TaskResult(
            task_id=f"t{i}",
            category="routing",
            passed=score >= 1.0,
            score=score,
            latency_ms=10.0,
            weight=1.0,
            safety_critical=safety_critical,
        )
        for i in range(n)
    ]


def _register_row(candidate_id: str, **kwargs) -> BakeoffCandidate:
    base = {
        "id": candidate_id,
        "role": "core",
        "family": "fam",
        "revision_label": "pinned-1.0.0",
        "license_label": "Apache-2.0",
        "license_status": "cleared",
        "open_weight": True,
        "hardware_class": "gpu-16gb-class",
        "estimated_vram_gb": 16.0,
        "cost_tier": "medium",
        "source_url": "https://example.invalid",
        "limitations": (),
    }
    base.update(kwargs)
    return BakeoffCandidate(**base)


class TestSuiteLoading:
    def test_repository_suite_loads_and_is_non_trivial(self) -> None:
        suite = load_task_suite(SUITE)
        assert suite.suite_id == "atticus.bakeoff.stage-b"
        assert len(suite.tasks) >= 8

    def test_suite_digest_is_stable(self) -> None:
        assert load_task_suite(SUITE).digest == load_task_suite(SUITE).digest

    def test_suite_covers_both_roles(self) -> None:
        suite = load_task_suite(SUITE)
        assert suite.for_role("core") and suite.for_role("edge")

    def test_suite_has_safety_critical_tasks(self) -> None:
        suite = load_task_suite(SUITE)
        assert any(t.safety_critical for t in suite.tasks)

    def test_duplicate_task_ids_rejected(self, tmp_path: Path) -> None:
        p = tmp_path / "dup.yaml"
        p.write_text(
            "suite_id: x\nsuite_version: '1'\ntasks:\n"
            "  - {id: a, role: core, category: c, prompt: [{role: user, content: hi}],"
            "     grader: {must_include: [x]}}\n"
            "  - {id: a, role: core, category: c, prompt: [{role: user, content: hi}],"
            "     grader: {must_include: [x]}}\n"
        )
        with pytest.raises(BakeoffError, match="duplicate task id"):
            load_task_suite(p)

    def test_missing_suite_is_an_error(self, tmp_path: Path) -> None:
        with pytest.raises(BakeoffError, match="not found"):
            load_task_suite(tmp_path / "nope.yaml")


class TestGrading:
    def test_must_include_pass_and_fail(self) -> None:
        task = _task()
        assert grade_response(task, _response("route to fedlens")).passed
        assert not grade_response(task, _response("route to atlas")).passed

    def test_partial_credit_is_proportional(self) -> None:
        task = _task(grader=GraderSpec(must_include=("alpha", "beta", "gamma", "delta")))
        result = grade_response(task, _response("alpha beta"))
        assert result.score == pytest.approx(0.5)
        assert not result.passed

    def test_safety_critical_is_pass_fail_not_partial(self) -> None:
        task = _task(
            safety_critical=True,
            grader=GraderSpec(must_include=("alpha", "beta", "gamma", "delta")),
        )
        assert grade_response(task, _response("alpha beta")).score == 0.0

    def test_forbidden_text_fails(self) -> None:
        task = _task(grader=GraderSpec(must_not_include=("OVERRIDE ACCEPTED",)))
        assert not grade_response(task, _response("OVERRIDE ACCEPTED")).passed

    def test_tool_call_requirement(self) -> None:
        task = _task(grader=GraderSpec(must_call_tool="evidence_lookup"))
        ok = _response("", tool_calls=({"name": "evidence_lookup"},))
        assert grade_response(task, ok).passed
        assert not grade_response(task, _response("")).passed

    def test_json_requirements(self) -> None:
        task = _task(grader=GraderSpec(must_emit_json=True, json_required_keys=("steps",)))
        assert grade_response(task, _response('{"steps": []}')).passed
        assert not grade_response(task, _response("not json")).passed

    def test_invalid_json_does_not_inflate_score(self) -> None:
        """Missing keys must count against the score, not shrink the denominator."""
        task = _task(
            grader=GraderSpec(must_emit_json=True, json_required_keys=("a", "b", "c"))
        )
        assert grade_response(task, _response("garbage")).score == 0.0

    def test_refusal_expectation(self) -> None:
        task = _task(grader=GraderSpec(expect_refusal=True))
        assert grade_response(task, _response("I cannot do that")).passed
        assert not grade_response(task, _response("Sure, here you go")).passed

    def test_latency_budget(self) -> None:
        task = _task(grader=GraderSpec(max_latency_ms=100.0))
        assert grade_response(task, _response("x", latency_ms=50.0)).passed
        assert not grade_response(task, _response("x", latency_ms=500.0)).passed

    def test_task_without_criteria_is_rejected(self) -> None:
        with pytest.raises(BakeoffError, match="no grading criteria"):
            grade_response(_task(grader=GraderSpec()), _response("x"))


class TestRunning:
    def test_provider_error_scores_zero_rather_than_aborting(self) -> None:
        """A crashing candidate has failed the task; it must not abort the run."""
        provider = ScriptedProvider({}, healthy=False)
        candidate = _register_row("c1")
        with pytest.raises(BakeoffError, match="unhealthy"):
            run_candidate(candidate, provider, load_task_suite(SUITE))

    def test_mid_run_provider_failure_is_recorded(self) -> None:
        class Flaky(ScriptedProvider):
            def complete(self, messages, *, tools=None, constraints):  # type: ignore[no-untyped-def]
                raise ProviderUnavailableError("boom")

        run = run_candidate(
            _register_row("c1"), Flaky({}), load_task_suite(SUITE), measurement_mode="hardware"
        )
        assert run.errored == run.attempted
        assert run.quality == 0.0

    def test_closed_weight_provider_rejected(self) -> None:
        closed = ScriptedProvider({})
        closed._identity = ModelIdentity(  # noqa: SLF001
            provider_id="closed",
            model_family="x",
            revision="r",
            open_weight=False,
            output_mode=OutputMode.MOCK,
            license_label="proprietary",
        )
        with pytest.raises(BakeoffError, match="closed-weight"):
            run_candidate(_register_row("c1"), closed, load_task_suite(SUITE))

    def test_run_only_includes_tasks_for_role(self) -> None:
        suite = load_task_suite(SUITE)
        run = run_candidate(
            _register_row("c1", role="edge"),
            ScriptedProvider({}),
            suite,
            measurement_mode="hardware",
        )
        assert run.attempted == len(suite.for_role("edge"))

    def test_latency_percentiles(self) -> None:
        run = _run("c", _results(4, 1.0))
        assert run.p50_latency_ms == 10.0
        assert run.p95_latency_ms == 10.0


class TestEvidenceGate:
    def _register(self, cid: str = "c1", **kw) -> dict[str, BakeoffCandidate]:
        return {cid: _register_row(cid, **kw)}

    def test_clean_evidence_supports_selection(self) -> None:
        runs = [_run("c1", _results(10, 1.0)), _run("c2", _results(10, 0.5))]
        decision = select_winner(
            "core", runs, {"c1": _register_row("c1"), "c2": _register_row("c2")}
        )
        assert decision.selected == "c1"
        assert decision.status == "selection_supported"

    def test_fixture_measurement_blocks_selection(self) -> None:
        """The headline guard: synthetic numbers may never name a winner."""
        runs = [_run("c1", _results(10, 1.0), measurement_mode="fixture")]
        decision = select_winner("core", runs, self._register())
        assert decision.selected is None
        assert any("not measured on hardware" in b for b in decision.blockers)

    def test_unpinned_revision_blocks_selection(self) -> None:
        runs = [_run("c1", _results(10, 1.0))]
        register = self._register(revision_label="scaffold-unpinned")
        decision = select_winner("core", runs, register)
        assert decision.selected is None
        assert any("revision not pinned" in b for b in decision.blockers)

    def test_uncleared_license_blocks_selection(self) -> None:
        runs = [_run("c1", _results(10, 1.0))]
        register = self._register(license_status="provisional_review_required")
        decision = select_winner("core", runs, register)
        assert decision.selected is None
        assert any("license not cleared" in b for b in decision.blockers)

    def test_thin_coverage_blocks_selection(self) -> None:
        runs = [_run("c1", _results(3, 1.0))]
        decision = select_winner("core", runs, self._register())
        assert decision.selected is None
        assert any("coverage too thin" in b for b in decision.blockers)

    def test_low_quality_blocks_selection(self) -> None:
        runs = [_run("c1", _results(10, 0.5))]
        decision = select_winner("core", runs, self._register())
        assert decision.selected is None
        assert any("below required" in b for b in decision.blockers)

    def test_safety_failure_blocks_selection(self) -> None:
        results = _results(9, 1.0) + [
            TaskResult(
                task_id="danger",
                category="safety",
                passed=False,
                score=0.0,
                latency_ms=1.0,
                weight=1.0,
                safety_critical=True,
            )
        ]
        decision = select_winner("core", [_run("c1", results)], self._register())
        assert decision.selected is None
        assert any("safety-critical failures" in b for b in decision.blockers)

    def test_narrow_margin_blocks_selection(self) -> None:
        """Two candidates inside noise must not produce a winner."""
        runs = [_run("c1", _results(10, 1.0)), _run("c2", _results(10, 0.99))]
        decision = select_winner(
            "core", runs, {"c1": _register_row("c1"), "c2": _register_row("c2")}
        )
        assert decision.selected is None
        assert any("too close to call" in b for b in decision.blockers)

    def test_errored_tasks_block_selection(self) -> None:
        results = _results(9, 1.0) + [
            TaskResult(
                task_id="e",
                category="routing",
                passed=False,
                score=0.0,
                latency_ms=0.0,
                weight=1.0,
                safety_critical=False,
                error="ProviderUnavailableError: boom",
            )
        ]
        decision = select_winner("core", [_run("c1", results)], self._register())
        assert decision.selected is None
        assert any("errored" in b for b in decision.blockers)

    def test_unregistered_leader_blocks_selection(self) -> None:
        decision = select_winner("core", [_run("ghost", _results(10, 1.0))], {})
        assert decision.selected is None
        assert any("not in the candidate register" in b for b in decision.blockers)

    def test_no_candidates_for_role(self) -> None:
        decision = select_winner("edge", [_run("c1", _results(10, 1.0))], self._register())
        assert decision.status == "no_candidates"

    def test_gate_thresholds_are_configurable(self) -> None:
        runs = [_run("c1", _results(10, 0.6)), _run("c2", _results(10, 0.4))]
        register = {"c1": _register_row("c1"), "c2": _register_row("c2")}
        gate = EvidenceGate(min_quality=0.5, min_margin=0.0, min_tasks=5)
        assert select_winner("core", runs, register, gate).selected == "c1"

    def test_a_field_of_one_cannot_produce_a_winner(self) -> None:
        """A single candidate is not a bake-off, however well it scores.

        The margin check is the only comparative gate and it is skipped when
        there is no runner-up. Without this condition, standing up one endpoint
        and running the suite against it would clear everything else and name a
        winner on no comparison at all.
        """
        runs = [_run("c1", _results(10, 1.0))]
        decision = select_winner("core", runs, self._register())
        assert decision.selected is None
        assert any("required to compare" in b for b in decision.blockers)

    def test_a_field_of_one_is_allowed_only_by_explicit_configuration(self) -> None:
        """Lowering the bar has to be a deliberate act, recorded in the gate."""
        runs = [_run("c1", _results(10, 1.0))]
        gate = EvidenceGate(min_candidates=1)
        assert select_winner("core", runs, self._register(), gate).selected == "c1"

    def test_a_hedged_license_status_does_not_read_as_cleared(self) -> None:
        """The register's own words are the evidence, not an exact-match list.

        `reported_apache_2_0_pending_confirmation` says nobody confirmed the
        license; it previously matched no known uncleared state and passed.
        """
        runs = [_run("c1", _results(10, 1.0)), _run("c2", _results(10, 0.5))]
        register = {
            "c1": _register_row("c1", license_status="reported_apache_2_0_pending_confirmation"),
            "c2": _register_row("c2"),
        }
        decision = select_winner("core", runs, register)
        assert decision.selected is None
        assert any("license not cleared" in b for b in decision.blockers)

    @pytest.mark.parametrize(
        "status",
        [
            "cleared",
            "apache_2_0_confirmed",
            "mit_verified_by_counsel",
        ],
    )
    def test_genuinely_cleared_statuses_still_pass(self, status: str) -> None:
        assert license_is_cleared(status)

    @pytest.mark.parametrize(
        "status",
        [
            "",
            "unknown",
            "provisional_review_required",
            "reported_apache_2_0_pending_confirmation",
            "APACHE-2.0 (UNCONFIRMED)",
            "unreviewed",
        ],
    )
    def test_hedged_statuses_are_refused(self, status: str) -> None:
        assert not license_is_cleared(status)


class TestEndToEnd:
    def test_fixture_bakeoff_runs_and_declares_no_winner(self) -> None:
        """The whole point: a fixture run produces evidence and refuses to select."""
        register = __import__("yaml").safe_load(REGISTER.read_text())
        providers = {
            row["id"]: ScriptedProvider(
                {"fedlens": "fedlens", "balancelab": "balancelab"},
                revision=row["revision_label"],
            )
            for row in register["candidates"]
        }
        report = run_bakeoff(
            providers, register_path=REGISTER, suite_path=SUITE, measurement_mode="fixture"
        )
        assert report.runs
        assert not report.any_selection
        assert report.as_dict()["selection_status"] == "not_selected"
        assert list(summarise_blockers(report))

    def test_report_renders_markdown(self) -> None:
        providers = {
            "core-qwen35-9b-class": ScriptedProvider({"fedlens": "fedlens"}),
        }
        report = run_bakeoff(
            providers, register_path=REGISTER, suite_path=SUITE, measurement_mode="fixture"
        )
        md = report.to_markdown()
        assert "Stage B evidence" in md
        assert "DIR-004" in md

    def test_no_providers_is_an_error(self) -> None:
        with pytest.raises(BakeoffError, match="no providers"):
            run_bakeoff({}, register_path=REGISTER, suite_path=SUITE)

    def test_report_carries_non_claims(self) -> None:
        providers = {"core-qwen35-9b-class": ScriptedProvider({})}
        report = run_bakeoff(
            providers, register_path=REGISTER, suite_path=SUITE, measurement_mode="fixture"
        )
        assert any("does not select" in c for c in report.non_claims)


class TestLiveProviderWiring:
    """A live bake-off must be reachable from configuration, not a source edit.

    Requiring someone to patch the runner to swap in real endpoints puts a code
    change between the workshop and its own evidence. The register already
    describes each candidate; it is also where "and here is where this one is
    running" belongs.
    """

    def _register(self, tmp_path: Path, rows: list[dict[str, Any]]) -> Path:
        path = tmp_path / "candidates.yaml"
        path.write_text(
            yaml.safe_dump({"selection_status": "not_selected", "candidates": rows}),
            encoding="utf-8",
        )
        return path

    def _row(self, candidate_id: str, **extra: Any) -> dict[str, Any]:
        row: dict[str, Any] = {
            "id": candidate_id,
            "role": "core",
            "family": "fam",
            "revision_label": "pinned-1.0.0",
            "license_label": "Apache-2.0",
            "license_status": "cleared",
            "open_weight": True,
            "hardware_class": "gpu",
            "estimated_vram_gb": 16,
            "cost_tier": "medium",
            "source_url": "https://example.invalid",
        }
        row.update(extra)
        return row

    def test_only_served_candidates_get_providers(self, tmp_path: Path) -> None:
        """Nobody having served a model is not the same as that model failing."""
        register = self._register(
            tmp_path,
            [
                self._row("served", serving={"runtime": "ollama", "model": "m:1b"}),
                self._row("not-served"),
            ],
        )
        providers = build_live_providers(register)
        assert set(providers) == {"served"}

    def test_identity_is_taken_from_the_register_not_the_endpoint(
        self, tmp_path: Path
    ) -> None:
        """A local server cannot attest to the license or revision it loaded."""
        register = self._register(
            tmp_path,
            [
                self._row(
                    "c1",
                    revision_label="pinned-sha256:abcd",
                    license_label="Apache-2.0",
                    serving={"runtime": "vllm", "model": "whatever-the-server-calls-it"},
                )
            ],
        )
        identity = build_live_providers(register)["c1"].identity
        assert identity.revision == "pinned-sha256:abcd"
        assert identity.license_label == "Apache-2.0"
        assert identity.runtime == "vllm"

    def test_base_url_override_wins(self, tmp_path: Path) -> None:
        register = self._register(
            tmp_path,
            [
                self._row(
                    "c1",
                    serving={
                        "runtime": "ollama",
                        "model": "m",
                        "base_url": "http://localhost:11434/v1",
                    },
                )
            ],
        )
        provider = build_live_providers(register, base_url_override="http://127.0.0.1:8000/v1")["c1"]
        assert provider.base_url == "http://127.0.0.1:8000/v1"  # type: ignore[attr-defined]

    def test_an_incomplete_serving_block_is_an_error_not_a_skip(self, tmp_path: Path) -> None:
        """Silently skipping a typo'd block would look identical to not serving it."""
        register = self._register(tmp_path, [self._row("c1", serving={"runtime": "ollama"})])
        with pytest.raises(ValueError, match="requires both"):
            build_live_providers(register)

    def test_the_real_register_serves_exactly_what_has_been_stood_up(self) -> None:
        providers = build_live_providers(REGISTER)
        assert set(providers) == {"core-gemma4-26b"}

    def test_a_live_run_of_the_real_register_still_cannot_select(self) -> None:
        """One served candidate is a measurement, not a bake-off.

        This is the case `--live` makes reachable for the first time: hardware
        mode clears the one condition fixtures never could, so the field-size
        gate is what stands between a single local run and a declared winner.
        """
        register = load_candidates(REGISTER)
        runs = [_run("core-gemma4-26b", _results(12, 1.0))]
        decision = select_winner("core", runs, register)
        assert decision.selected is None
        assert any("required to compare" in b for b in decision.blockers)


# --------------------------------------------------------------------------- #
# Resolution diagnostic (reported, never gating)
# --------------------------------------------------------------------------- #


def _scored(scores: list[float], *, weights: list[float] | None = None) -> list[TaskResult]:
    """Build per-task results with explicit scores so pairing is predictable."""
    resolved = weights if weights is not None else [1.0] * len(scores)
    return [
        TaskResult(
            task_id=f"t{index}",
            category="routing",
            passed=score >= 1.0,
            score=score,
            latency_ms=10.0,
            weight=resolved[index],
            safety_critical=False,
        )
        for index, score in enumerate(scores)
    ]


def test_resolution_is_undetermined_when_candidates_share_a_script() -> None:
    """Fixture providers give identically zero differences, so variance is unestimable."""
    leader = _run("a", _scored([1.0, 0.5, 0.0, 1.0]))
    runner_up = _run("b", _scored([1.0, 0.5, 0.0, 1.0]))

    diagnostic = paired_resolution(leader, runner_up, 0.05)

    assert diagnostic is not None
    assert diagnostic.sigma == 0.0
    assert diagnostic.required_tasks is None
    assert diagnostic.resolution_ratio is None
    assert diagnostic.is_resolved is None
    assert diagnostic.note is not None
    assert "variance cannot be estimated" in diagnostic.note


def test_resolution_matches_the_closed_form_requirement() -> None:
    """N* = (z_alpha + z_power)^2 * sigma^2 / delta^2, computed independently here."""
    leader = _run("a", _scored([1.0, 1.0, 0.0, 0.0, 1.0, 0.0]))
    runner_up = _run("b", _scored([0.0, 1.0, 1.0, 0.0, 0.0, 1.0]))

    diagnostic = paired_resolution(leader, runner_up, 0.10)

    assert diagnostic is not None
    differences = [1.0, 0.0, -1.0, 0.0, 1.0, -1.0]
    expected_sigma = statistics.stdev(differences)
    z_alpha = statistics.NormalDist().inv_cdf(0.975)
    z_power = statistics.NormalDist().inv_cdf(0.80)
    expected_required = ((z_alpha + z_power) ** 2) * expected_sigma**2 / 0.10**2

    assert diagnostic.sigma == pytest.approx(expected_sigma)
    assert diagnostic.required_tasks == pytest.approx(expected_required)
    assert diagnostic.resolution_ratio == pytest.approx(6.0 / expected_required)


def test_a_small_suite_is_reported_as_unresolved() -> None:
    """Six noisy tasks cannot resolve a 0.05 gap, and the diagnostic must say so."""
    leader = _run("a", _scored([1.0, 1.0, 0.0, 0.0, 1.0, 0.0]))
    runner_up = _run("b", _scored([0.0, 1.0, 1.0, 0.0, 0.0, 1.0]))

    diagnostic = paired_resolution(leader, runner_up, 0.05)

    assert diagnostic is not None
    assert diagnostic.required_tasks is not None
    assert diagnostic.required_tasks > 100
    assert diagnostic.is_resolved is False


def test_resolution_uses_the_effective_sample_size_under_unequal_weights() -> None:
    """A weighted mean of n values has the precision of fewer equally weighted ones."""
    leader = _run("a", _scored([1.0, 0.0, 1.0]))
    runner_up = _run("b", _scored([0.0, 1.0, 0.0]))
    equal = paired_resolution(leader, runner_up, 0.10)

    heavy = _run("a", _scored([1.0, 0.0, 1.0], weights=[9.0, 1.0, 1.0]))
    light = _run("b", _scored([0.0, 1.0, 0.0], weights=[9.0, 1.0, 1.0]))
    skewed = paired_resolution(heavy, light, 0.10)

    assert equal is not None and skewed is not None
    assert equal.effective_tasks == pytest.approx(3.0)
    assert skewed.effective_tasks < equal.effective_tasks


def test_resolution_needs_at_least_two_paired_tasks() -> None:
    assert paired_resolution(_run("a", _scored([1.0])), _run("b", _scored([0.0])), 0.05) is None


def test_resolution_pairs_only_tasks_both_candidates_ran() -> None:
    leader = _run("a", _scored([1.0, 0.0, 1.0]))
    runner_up = _run("b", _scored([0.0, 1.0]))  # t0 and t1 only

    diagnostic = paired_resolution(leader, runner_up, 0.10)

    assert diagnostic is not None
    assert diagnostic.paired_tasks == 2


def test_resolution_does_not_change_the_selection_outcome() -> None:
    """The diagnostic is reported context; it must never add or remove a blocker."""
    register = {
        "a": _register_row("a"),
        "b": _register_row("b"),
    }
    leader = _run("a", _scored([1.0] * 10))
    runner_up = _run("b", _scored([0.0] * 10))

    decision = select_winner("core", [leader, runner_up], register)

    assert decision.resolution is not None
    # Whatever the resolution says, it contributes no blocker text of its own.
    assert not any("resolution" in blocker.lower() for blocker in decision.blockers)
    assert not any("resolve" in blocker.lower() for blocker in decision.blockers)


def test_resolution_serialises_into_the_decision_dict() -> None:
    leader = _run("a", _scored([1.0, 0.0, 1.0, 0.0]))
    runner_up = _run("b", _scored([0.0, 1.0, 0.0, 1.0]))
    register = {"a": _register_row("a"), "b": _register_row("b")}

    payload = select_winner("core", [leader, runner_up], register).as_dict()

    assert "resolution" in payload
    assert payload["resolution"] is not None
    assert set(payload["resolution"]) == {
        "paired_tasks",
        "effective_tasks",
        "sigma",
        "target_delta",
        "required_tasks",
        "resolution_ratio",
        "is_resolved",
        "note",
    }
