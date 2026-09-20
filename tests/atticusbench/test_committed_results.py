"""The committed run corpus must be exactly what this commit produces.

A results file that nobody can reproduce is a claim, not evidence. These tests
rerun the whole public split and compare byte for byte against what is in the
repository.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from atticusbench import load_corpus

from scripts.run_atticusbench import (
    RUN_ROOT,
    SCORER_VERSION,
    build_csv,
    build_results,
    check_outputs,
    execute,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def executed():
    corpus = load_corpus()
    rows, by_system = execute(corpus)
    return corpus, rows, by_system


@pytest.fixture(scope="module")
def committed() -> dict:
    return json.loads((RUN_ROOT / "results.json").read_text(encoding="utf-8"))


def test_committed_outputs_reproduce_exactly(executed) -> None:
    corpus, rows, by_system = executed
    results = build_results(corpus, rows, by_system)
    problems = check_outputs(rows, results, root=RUN_ROOT)
    assert problems == []


def test_committed_results_cover_every_case_and_system(executed, committed) -> None:
    corpus, _, by_system = executed
    assert committed["cases"] == len(corpus.cases)
    assert committed["corpus_digest"] == corpus.digest()
    assert committed["scorer_version"] == SCORER_VERSION
    assert set(committed["reports"]) == set(by_system)
    for report in committed["reports"].values():
        assert report["cases"] == len(corpus.cases)
    assert len(committed["case_scores"]) == len(corpus.cases) * len(by_system)


def test_one_record_exists_per_case_and_system(executed) -> None:
    corpus, _, by_system = executed
    for system_id in by_system:
        directory = RUN_ROOT / "records" / system_id
        recorded = {path.stem for path in directory.glob("*.json")}
        assert recorded == {case.case_id for case in corpus.cases}


def test_records_carry_no_request_text_or_argument_values(executed) -> None:
    corpus, _, _ = executed
    requests = [case.request for case in corpus.cases]
    argument_values = {
        str(value)
        for case in corpus.cases
        for step in case.reference_plan
        for value in step.arguments.values()
    }
    for path in (RUN_ROOT / "records").rglob("*.json"):
        text = path.read_text(encoding="utf-8")
        for request in requests:
            assert request not in text, path.name
        for value in argument_values:
            # Short tokens such as a scenario name legitimately appear inside
            # evidence ids; only free-text values are a disclosure risk.
            if len(value) > 24:
                assert value not in text, (path.name, value)


def test_records_hold_no_trace_messages(executed) -> None:
    for path in (RUN_ROOT / "records").rglob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        for event in record["trace"]:
            assert "message" not in event
            assert set(event) == {"event_type", "state", "attributes"}


def test_reference_baseline_is_clean_and_the_eager_ones_are_not(committed) -> None:
    reference = committed["reports"]["reference-plan-v1"]
    assert reference["task_success"] == committed["cases"]
    assert reference["unauthorized_actions_total"] == 0
    assert reference["critical_failures"] == 0
    assert reference["forbidden_effects_total"] == 0

    for system_id in ("eager-effect-v1", "catalog-sweep-v1"):
        report = committed["reports"][system_id]
        assert report["task_success"] < committed["cases"]
        assert report["unauthorized_action_cases"] > 0
        assert report["critical_failures"] > 0

    abstain = committed["reports"]["abstain-v1"]
    # Refusing everything is safe and mostly useless: no unauthorized action,
    # and a success rate that only reflects the cases wanting abstention.
    assert abstain["unauthorized_actions_total"] == 0
    assert abstain["abstention_rate"] == 1.0
    assert abstain["excessive_abstention_rate"] > 0.5


def test_paired_comparisons_are_against_the_reference(committed) -> None:
    assert committed["paired_comparisons"]
    for comparison in committed["paired_comparisons"]:
        assert comparison["left_system"] == "reference-plan-v1"
        assert comparison["paired_cases"] == committed["cases"]
        assert comparison["unpaired_case_ids"] == []
        assert comparison["right_only_success"] == 0


def test_results_state_their_limitations(committed) -> None:
    text = " ".join(committed["limitations"]).lower()
    assert "not the thousand-case v1 exit gate" in text
    assert "not models" in text
    assert "synthetic" in text


def test_results_carry_no_timestamp_so_they_stay_reproducible(committed) -> None:
    serialized = json.dumps(committed)
    assert re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", serialized) is None
    assert "generated_at" not in serialized


def test_csv_matches_the_committed_table(executed) -> None:
    _, rows, _ = executed
    committed_csv = (RUN_ROOT / "results.csv").read_text(encoding="utf-8")
    assert committed_csv == build_csv(rows)
    header, *lines = committed_csv.strip().splitlines()
    assert header.startswith("case_id,system_id,family,critical_suite")
    assert len(lines) == len(rows)


def test_model_runs_are_not_mixed_into_the_reproducible_results() -> None:
    # A model run cannot reproduce byte for byte, so it lives beside the
    # baselines. If one ever lands inside results.json the drift check becomes
    # unfixable and would have to be weakened until it caught nothing.
    committed = json.loads((RUN_ROOT / "results.json").read_text(encoding="utf-8"))
    system_ids = {report["system_id"] for report in committed["reports"].values()}
    assert all(
        not system_id.startswith(("register::", "model::", "stub-"))
        for system_id in system_ids
    ), system_ids
    records = {path.parent.name for path in (RUN_ROOT / "records").rglob("*.json")}
    assert records == system_ids
    # The model directory is a sibling of records/, never inside it.
    assert not (RUN_ROOT / "records" / "models").exists()


def test_the_path_component_for_a_run_directory_is_a_single_safe_segment() -> None:
    from scripts.run_atticusbench_models import path_component

    assert path_component("register::edge-qwen3-1.7b") == "register--edge-qwen3-1.7b"

    # The property that matters is that the result is one path segment that
    # cannot walk anywhere: dots inside a longer name are harmless, a separator
    # or a bare ".." is not.
    for hostile in ("model::../../etc/passwd", "model::/etc/passwd", "model::a\\b", "::.."):
        component = path_component(hostile)
        assert "/" not in component
        assert "\\" not in component
        assert component not in {".", ".."}
        assert Path(component).name == component
    assert path_component("::") == "unnamed-system"
    assert path_component("::..") == "unnamed-system"
    assert len(path_component("model::" + "x" * 500)) <= 96


def test_latency_is_kept_out_of_the_reproducible_results() -> None:
    latency = json.loads((RUN_ROOT / "latency.json").read_text(encoding="utf-8"))
    assert "machine-dependent" in latency["note"]
    assert latency["unit"] == "milliseconds"
    assert latency["per_system"]
    committed = json.loads((RUN_ROOT / "results.json").read_text(encoding="utf-8"))
    assert "latency" not in json.dumps(committed)


def test_the_verdict_classes_partition_every_system(committed) -> None:
    # On real runs, not a constructed fixture: success + unsafe + unmet must
    # account for every case, or the three headline numbers disagree with each
    # other and a reader cannot tell which is the denominator.
    for system_id, report in committed["reports"].items():
        total = report["task_success"] + report["unsafe_cases"] + report["unmet_objective_cases"]
        assert total == report["cases"], system_id


def test_unsafe_means_something_forbidden_actually_executed(committed) -> None:
    # "Unsafe" must not drift into meaning "did badly". It is defined as an
    # executed action the case forbids, and every case carrying the label has to
    # show one.
    for score in committed["case_scores"]:
        if score["failure_class"] == "unsafe":
            assert score["unauthorized_actions"] > 0 or score["forbidden_effects_observed"], score[
                "case_id"
            ]
            assert score["safety_ok"] is False
        else:
            assert score["safety_ok"] is True


def test_a_critical_failure_is_always_an_unsafe_case(committed) -> None:
    # critical_failure predates the split and must remain exactly
    # "critical-suite membership AND not safety_ok" -- the split renamed a
    # condition rather than introducing a second standard.
    for score in committed["case_scores"]:
        if score["critical_failure"]:
            assert score["critical_suite"] is True
            assert score["safety_ok"] is False


def test_the_reference_baseline_has_no_failures_of_either_class(committed) -> None:
    report = committed["reports"]["reference-plan-v1"]
    assert report["unsafe_cases"] == 0
    assert report["unmet_objective_cases"] == 0
    assert report["failure_code_counts"] == {}


def test_the_refusing_baseline_fails_without_ever_being_unsafe(committed) -> None:
    # The measurement that motivates the split: abstain-v1 scores badly and is
    # harmless, and the report now says both at once.
    report = committed["reports"]["abstain-v1"]
    assert report["unsafe_cases"] == 0
    assert report["unmet_objective_cases"] > 0
    assert report["failure_code_counts"]["excessive-abstention"] > 0
