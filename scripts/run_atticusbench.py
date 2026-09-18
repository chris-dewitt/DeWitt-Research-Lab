#!/usr/bin/env python
"""Run the AtticusBench public split against the deterministic baselines.

Every case executes through the real Atticus orchestrator, policy engine, and
approval service. The script writes one content-minimized record per run, one
results file holding the metric vector per system and per family, a flat CSV for
analysis, and a separate latency file.

    uv run python scripts/run_atticusbench.py
    uv run python scripts/run_atticusbench.py --json
    uv run python scripts/run_atticusbench.py --check     # fail if outputs drift
    uv run python scripts/run_atticusbench.py --system reference-plan-v1

Records carry ids, digests, and scores. They deliberately do not carry the
request text, tool arguments, evidence content, or trace messages: AGENTS.md
forbids logging prompt or tool content by default, and a benchmark record does
not need it.

Timing is machine-dependent, so it is written to `latency.json` only and is
excluded from `results.json` and from every digest. Rerunning on the same commit
must reproduce `results.json` byte for byte.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
for _relative in (
    "packages/drl-protocol/src",
    "packages/drl-ai-core/src",
    "services/atlas/src",
    "services/fedlens/src",
    "services/balancelab-ai/src",
    "services/evalforge/src",
    "services/atticus-control-plane/src",
    "datasets/atticusbench/src",
):
    sys.path.insert(0, str(REPO_ROOT / _relative))

from atticusbench import (  # noqa: E402
    BASELINE_SYSTEMS,
    Case,
    CaseRun,
    CaseScore,
    Corpus,
    aggregate,
    load_corpus,
    paired_comparison,
    run_case,
    score_case,
    system,
)
from drl_ai_core import canonical_digest  # noqa: E402

RUN_ROOT = REPO_ROOT / "runs" / "atticusbench"

#: Version of the scoring code that produced a results file. Bump it whenever a
#: metric definition changes, so an old results file is never silently compared
#: against new semantics.
SCORER_VERSION = "1.0.0"
SUITE_VERSION = "0.1.0"


def record_for(run: CaseRun, score: CaseScore) -> dict[str, Any]:
    """Build the persisted, content-minimized record for one run."""

    return {
        "schema_version": "1.0.0",
        "suite": "atticusbench",
        "suite_version": SUITE_VERSION,
        "scorer_version": SCORER_VERSION,
        "case_id": run.case_id,
        "case_digest": run.case_digest,
        "system_id": run.system_id,
        "family": run.family,
        "split": run.split,
        "mode": run.mode,
        "critical_suite": run.critical_suite,
        "fixture_id": run.fixture_id,
        "planned_tools": list(run.planned_tools),
        "terminal_state": run.terminal_state,
        "trace": [
            {
                "event_type": event.event_type,
                "state": event.state,
                "attributes": event.attributes,
            }
            for event in run.observed.events
        ],
        "tools_started": list(run.tools_started),
        "tools_completed": list(run.tools_completed),
        "tools_failed": list(run.tools_failed),
        "evidence_ids": list(run.evidence_ids),
        "evidence_count": run.observed.evidence_count,
        "artifact_keys": list(run.artifact_keys),
        "artifact_digests": list(run.artifact_digests),
        "effect_ledger": run.ledger,
        "evaluation": run.evaluation,
        "score": score.as_dict(),
    }


def execute(
    corpus: Corpus,
    *,
    system_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
) -> tuple[list[tuple[Case, CaseRun, CaseScore]], dict[str, list[CaseScore]]]:
    systems = (
        [system(system_id) for system_id in system_ids] if system_ids else list(BASELINE_SYSTEMS)
    )
    cases = [case for case in corpus.cases if not case_ids or case.case_id in case_ids]

    rows: list[tuple[Case, CaseRun, CaseScore]] = []
    by_system: dict[str, list[CaseScore]] = {baseline.system_id: [] for baseline in systems}
    for baseline in systems:
        for case in cases:
            fixture = corpus.fixture(case.environment_fixture)
            run = run_case(case, fixture, baseline)
            score = score_case(case, run)
            rows.append((case, run, score))
            by_system[baseline.system_id].append(score)
    return rows, by_system


def build_results(
    corpus: Corpus,
    rows: list[tuple[Case, CaseRun, CaseScore]],
    by_system: dict[str, list[CaseScore]],
) -> dict[str, Any]:
    reports = {
        system_id: aggregate(system_id, scores).as_dict() for system_id, scores in by_system.items()
    }
    comparisons = []
    reference = "reference-plan-v1"
    if reference in by_system:
        for system_id, scores in by_system.items():
            if system_id == reference:
                continue
            comparisons.append(paired_comparison(by_system[reference], scores))

    payload = {
        "schema_version": "1.0.0",
        "suite": "atticusbench",
        "suite_version": SUITE_VERSION,
        "split": "public-test",
        "scorer_version": SCORER_VERSION,
        "corpus_digest": corpus.digest(),
        "cases": len(corpus.cases),
        "fixtures": len(corpus.fixtures),
        "systems": [
            {
                "system_id": baseline.system_id,
                "description": baseline.description,
                "uses_declared_approvals": baseline.uses_declared_approvals,
            }
            for baseline in BASELINE_SYSTEMS
            if baseline.system_id in by_system
        ],
        "reports": reports,
        "paired_comparisons": comparisons,
        "case_scores": [score.as_dict() for _, _, score in rows],
        "limitations": [
            (
                "Thirty-two public cases across ten families is a seed corpus, not the "
                "thousand-case V1 exit gate. Intervals are wide and every family slice "
                "is three to five cases."
            ),
            (
                "The systems under test are fixed deterministic policies, not models. "
                "Nothing here measures a model's capability or selects one."
            ),
            (
                "Fixtures are synthetic. A system that passes here has satisfied declared "
                "invariants in a declared environment, which is not evidence of real-world "
                "reliability."
            ),
            (
                "Terminal-state expectations encode one intended safe outcome per case. A "
                "different safe outcome can score as a failure, which is a known limit of "
                "the current oracle."
            ),
        ],
    }
    payload["results_digest"] = f"sha256:{canonical_digest(payload)}"
    return payload


def build_csv(rows: list[tuple[Case, CaseRun, CaseScore]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(
        [
            "case_id",
            "system_id",
            "family",
            "critical_suite",
            "terminal_state",
            "terminal_ok",
            "must_call_coverage",
            "steps",
            "within_step_budget",
            "unauthorized_actions",
            "forbidden_effects",
            "approval_recall",
            "policy_denial_ok",
            "citations_ok",
            "delegation_ok",
            "abstained",
            "excessive_abstention",
            "success",
            "critical_failure",
        ]
    )
    for _, _, score in rows:
        writer.writerow(
            [
                score.case_id,
                score.system_id,
                score.family,
                int(score.critical_suite),
                score.terminal_state,
                int(score.terminal_ok),
                f"{score.must_call_coverage:.3f}",
                score.steps,
                int(score.within_step_budget),
                score.unauthorized_actions,
                len(score.forbidden_effects_observed),
                "" if score.approval_recall is None else f"{score.approval_recall:.1f}",
                "" if score.policy_denial_ok is None else int(score.policy_denial_ok),
                "" if score.citations_ok is None else int(score.citations_ok),
                "" if score.delegation_ok is None else int(score.delegation_ok),
                int(score.abstained),
                int(score.excessive_abstention),
                int(score.success),
                int(score.critical_failure),
            ]
        )
    return buffer.getvalue()


def build_latency(rows: list[tuple[Case, CaseRun, CaseScore]]) -> dict[str, Any]:
    by_system: dict[str, list[float]] = {}
    for _, run, _ in rows:
        by_system.setdefault(run.system_id, []).append(run.latency_ms)
    return {
        "note": (
            "Wall-clock timings are machine-dependent and are excluded from results.json "
            "and from every digest. They are recorded because the specification asks for "
            "latency context, not because they are reproducible."
        ),
        "unit": "milliseconds",
        "per_system": {
            system_id: {
                "runs": len(values),
                "total_ms": round(sum(values), 3),
                "mean_ms": round(sum(values) / len(values), 3),
                "max_ms": round(max(values), 3),
            }
            for system_id, values in sorted(by_system.items())
        },
    }


def render(results: dict[str, Any]) -> str:
    lines = [
        f"AtticusBench {results['split']} — suite {results['suite_version']}, "
        f"scorer {results['scorer_version']}",
        f"  corpus digest  {results['corpus_digest']}",
        f"  cases          {results['cases']}",
        "",
        f"{'system':<22}{'success':>9}{'ci95':>16}{'unauth':>8}{'effects':>9}"
        f"{'critical':>10}{'abstain':>9}{'steps':>7}",
    ]
    for system_id, report in results["reports"].items():
        low, high = report["task_success_ci95"]
        lines.append(
            f"{system_id:<22}"
            f"{report['task_success']}/{report['cases']:<6}"
            f"{f'[{low:.2f}, {high:.2f}]':>16}"
            f"{report['unauthorized_action_cases']:>8}"
            f"{report['forbidden_effects_total']:>9}"
            f"{report['critical_failures']:>10}"
            f"{report['abstention_rate']:>9.2f}"
            f"{report['steps_mean']:>7.2f}"
        )
    lines.append("")
    lines.append("Per-family task success")
    families = sorted(
        {family for report in results["reports"].values() for family in report["per_family"]}
    )
    header = f"{'family':<26}" + "".join(
        f"{system_id.replace('-v1', ''):>18}" for system_id in results["reports"]
    )
    lines.append(header)
    for family in families:
        row = f"{family:<26}"
        for report in results["reports"].values():
            slice_report = report["per_family"].get(family)
            if slice_report is None:
                row += f"{'-':>18}"
            else:
                row += f"{f'{slice_report["task_success"]}/{slice_report["cases"]}':>18}"
        lines.append(row)
    lines.append("")
    for comparison in results["paired_comparisons"]:
        lines.append(
            f"paired {comparison['left_system']} vs {comparison['right_system']}: "
            f"difference {comparison['success_rate_difference']:+.3f} on "
            f"{comparison['paired_cases']} cases, discordant "
            f"{comparison['left_only_success']}/{comparison['right_only_success']}, "
            f"exact McNemar p={comparison['mcnemar_exact_p']:.6f}"
        )
    critical = {
        system_id: report["critical_failure_case_ids"]
        for system_id, report in results["reports"].items()
        if report["critical_failure_case_ids"]
    }
    lines.append("")
    if critical:
        lines.append("Critical-suite failures (release-blocking for a release candidate)")
        for system_id, case_ids in critical.items():
            lines.append(f"  {system_id}: {', '.join(case_ids)}")
    else:
        lines.append("No critical-suite failures observed.")
    return "\n".join(lines)


def write_outputs(
    rows: list[tuple[Case, CaseRun, CaseScore]],
    results: dict[str, Any],
    *,
    root: Path,
) -> list[Path]:
    written: list[Path] = []
    for _, run, score in rows:
        directory = root / "records" / run.system_id
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{run.case_id}.json"
        path.write_text(json.dumps(record_for(run, score), indent=2) + "\n", encoding="utf-8")
        written.append(path)

    root.mkdir(parents=True, exist_ok=True)
    results_path = root / "results.json"
    results_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    written.append(results_path)

    csv_path = root / "results.csv"
    csv_path.write_text(build_csv(rows), encoding="utf-8")
    written.append(csv_path)

    latency_path = root / "latency.json"
    latency_path.write_text(json.dumps(build_latency(rows), indent=2) + "\n", encoding="utf-8")
    written.append(latency_path)
    return written


def check_outputs(
    rows: list[tuple[Case, CaseRun, CaseScore]],
    results: dict[str, Any],
    *,
    root: Path,
) -> list[str]:
    """Compare a fresh run against the committed outputs."""

    problems: list[str] = []
    for _, run, score in rows:
        path = root / "records" / run.system_id / f"{run.case_id}.json"
        expected = json.dumps(record_for(run, score), indent=2) + "\n"
        if not path.exists():
            problems.append(f"missing record: {path.relative_to(REPO_ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            problems.append(f"record drifted: {path.relative_to(REPO_ROOT)}")

    results_path = root / "results.json"
    expected_results = json.dumps(results, indent=2) + "\n"
    if not results_path.exists():
        problems.append("missing runs/atticusbench/results.json")
    elif results_path.read_text(encoding="utf-8") != expected_results:
        problems.append("runs/atticusbench/results.json drifted")

    csv_path = root / "results.csv"
    if not csv_path.exists():
        problems.append("missing runs/atticusbench/results.csv")
    elif csv_path.read_text(encoding="utf-8") != build_csv(rows):
        problems.append("runs/atticusbench/results.csv drifted")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--system", action="append", dest="systems", help="run only this system")
    parser.add_argument("--case", action="append", dest="cases", help="run only this case")
    parser.add_argument("--json", action="store_true", help="print the results payload as JSON")
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare a fresh run against committed outputs instead of writing them",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=RUN_ROOT,
        help="directory for run records and results (default runs/atticusbench)",
    )
    args = parser.parse_args(argv)

    corpus = load_corpus()
    rows, by_system = execute(corpus, system_ids=args.systems, case_ids=args.cases)
    results = build_results(corpus, rows, by_system)

    partial = bool(args.systems or args.cases)
    if args.check:
        if partial:
            print("--check requires the full corpus and every system", file=sys.stderr)
            return 2
        problems = check_outputs(rows, results, root=args.out)
        print(json.dumps(results, indent=2) if args.json else render(results))
        if problems:
            print("", file=sys.stderr)
            for problem in problems:
                print(f"drift: {problem}", file=sys.stderr)
            return 1
        print("\nCommitted outputs match this run.")
        return 0

    if not partial:
        written = write_outputs(rows, results, root=args.out)
        print(f"wrote {len(written)} files under {args.out.relative_to(REPO_ROOT)}")
    print(json.dumps(results, indent=2) if args.json else render(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
