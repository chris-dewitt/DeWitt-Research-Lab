#!/usr/bin/env python
"""Measure local models on the AtticusBench public split.

On a workstation with the Ollama daemon up, this is the whole workflow:

    make atticusbench-models                      # every model the register serves
    uv run python scripts/run_atticusbench_models.py --model qwen3:1.7b
    uv run python scripts/run_atticusbench_models.py --stub      # no daemon needed

The deterministic baselines in `runs/atticusbench/results.json` bound the corpus
and are reproducible; a model run is not. Model runs therefore land under
`runs/atticusbench/models/<system>/<run-id>/` with a provenance manifest and are
never mixed into the reproducible results file or its drift check.

A model here is given no approval grants. Handing a system under test the
approvals a human would have issued and then reporting how it behaves without
them would not be a measurement of anything.

Nothing about a local endpoint attests to a license or to exact weights, so the
recorded identity is what `models/bakeoff/candidates.yaml` declares. An ad-hoc
`--model` tag is recorded as unregistered, with its license unknown, because a
tag is not provenance.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
# The repository root carries `scripts` as a namespace package, so the record
# shape and the run root come from the baseline runner rather than a copy.
sys.path.insert(0, str(REPO_ROOT))
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
    Corpus,
    aggregate,
    load_corpus,
    paired_comparison,
    run_case,
    score_case,
)
from atticusbench.model_system import model_system, plan_digest, provenance  # noqa: E402
from atticusbench.stub_provider import StubPlanProvider  # noqa: E402
from drl_ai_core.bakeoff_harness import build_live_providers  # noqa: E402
from drl_ai_core.http_provider import (  # noqa: E402
    DEFAULT_STALL_TIMEOUT_SECONDS,
    HttpOpenAICompatibleProvider,
)
from drl_ai_core.providers import CompletionConstraints, ModelProvider  # noqa: E402

from scripts.generate_manifest import git_output  # noqa: E402
from scripts.run_atticusbench import (  # noqa: E402
    RUN_ROOT,
    SCORER_VERSION,
    SUITE_VERSION,
    record_for,
)

MODEL_RUN_ROOT = RUN_ROOT / "models"
REGISTER = REPO_ROOT / "models" / "bakeoff" / "candidates.yaml"
DEFAULT_BASE_URL = "http://localhost:11434/v1"


def display_path(path: Path) -> str:
    """Repo-relative where possible, absolute when --out points elsewhere."""

    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _git(*arguments: str) -> str | None:
    """Run one read-only git command, or return None when git cannot answer.

    `scripts/generate_manifest.py` already resolves the binary through
    ``shutil.which`` and runs a fixed argv with no shell; reusing it keeps one
    hardened call site instead of two.
    """

    try:
        return git_output(REPO_ROOT, *arguments)
    except (RuntimeError, OSError):
        return None


def repo_commit() -> str:
    """The commit a run was produced from, or a marker saying it is unknown."""

    revision = (_git("rev-parse", "HEAD") or "").strip()
    return revision or "unknown"


def working_tree_is_dirty() -> bool:
    """True when the tree has uncommitted changes, or when git cannot say.

    Unknown is reported as dirty on purpose: a manifest claiming a clean tree it
    could not verify is worse than one that overstates the doubt.
    """

    output = _git("status", "--porcelain")
    if output is None:
        return True
    return bool(output.strip())


def ad_hoc_provider(tag: str, base_url: str, *, stall_timeout: float) -> ModelProvider:
    """Build a provider for a model tag that the register does not describe."""

    return HttpOpenAICompatibleProvider(
        model=tag,
        base_url=base_url,
        provider_id=f"adhoc::{tag}",
        model_family=f"unregistered:{tag}",
        revision=f"ollama:{tag}",
        # An unregistered tag carries no license evidence. Saying "unknown" is
        # the only honest label, and the evidence gate reads this field.
        license_label="unknown",
        open_weight=True,
        runtime="ollama",
        stream=True,
        stall_timeout=stall_timeout,
    )


def resolve_providers(args: argparse.Namespace) -> dict[str, ModelProvider]:
    if args.stub:
        return {"stub-plan-v1": StubPlanProvider()}

    providers: dict[str, ModelProvider] = {}
    if args.models:
        for tag in args.models:
            providers[f"model::{tag}"] = ad_hoc_provider(
                tag, args.base_url, stall_timeout=args.stall_timeout
            )
        return providers

    registered = build_live_providers(
        REGISTER,
        base_url_override=args.base_url if args.base_url != DEFAULT_BASE_URL else None,
        stall_timeout=args.stall_timeout,
    )
    providers.update({f"register::{cid}": provider for cid, provider in registered.items()})
    return providers


def preflight(system_id: str, provider: ModelProvider) -> str | None:
    """Return a human-actionable reason this provider cannot be measured."""

    identity = provider.identity
    try:
        healthy = provider.health()
    except Exception as exc:  # noqa: BLE001 - any failure here is a skip reason
        return f"{system_id}: health check raised {type(exc).__name__}: {exc}"
    if not healthy:
        return (
            f"{system_id}: endpoint did not answer. Start the daemon (`ollama serve`) "
            "and confirm `curl http://localhost:11434/v1/models` lists the tag."
        )
    catalog = getattr(provider, "catalog_ids", None)
    model = getattr(provider, "model", None)
    if callable(catalog) and isinstance(model, str):
        try:
            served = catalog()
        except Exception:  # noqa: BLE001 - treat an unreadable catalog as unknown
            served = frozenset()
        if served and model not in served:
            return (
                f"{system_id}: the daemon answering /v1/models does not serve "
                f"{model!r}. Run `ollama pull {model}` on the host that answers "
                f"that port. Identity: {identity.model_family}."
            )
    return None


def run_one(
    corpus: Corpus,
    system_id: str,
    provider: ModelProvider,
    *,
    case_ids: list[str] | None,
    repeats: int,
    constraints: CompletionConstraints | None,
) -> dict[str, Any]:
    """Run the split against one model, ``repeats`` times."""

    planners: dict[str, Any] = {}

    def remember(case: Any, planner: Any) -> None:
        planners[case.case_id] = planner

    system = model_system(system_id, provider, constraints=constraints, observer=remember)
    cases = [case for case in corpus.cases if not case_ids or case.case_id in case_ids]

    attempts: list[dict[str, Any]] = []
    for attempt in range(1, repeats + 1):
        records: list[dict[str, Any]] = []
        scores = []
        started = time.perf_counter()
        planners.clear()
        for case in cases:
            fixture = corpus.fixture(case.environment_fixture)
            run = run_case(case, fixture, system)
            score = score_case(case, run)
            planner = planners.get(case.case_id)
            outcome = planner.outcome.as_dict() if planner is not None else {}
            record = record_for(run, score)
            record["model"] = {
                "system_id": system_id,
                "attempt": attempt,
                "plan_outcome": outcome,
                "plan_digest": plan_digest(list(planner.last_plan) if planner else []),
            }
            records.append(record)
            scores.append(score)
            print(
                f"  {case.case_id:<20} {run.terminal_state:<18} "
                f"{'pass' if score.success else 'fail':<5} {outcome.get('source', '')}",
                file=sys.stderr,
            )
        elapsed = time.perf_counter() - started
        attempts.append(
            {
                "attempt": attempt,
                "report": aggregate(system_id, scores).as_dict(),
                "case_scores": [score.as_dict() for score in scores],
                "records": records,
                "wall_clock_seconds": round(elapsed, 3),
                "plan_sources": _source_counts(records),
            }
        )
    return {"system_id": system_id, "attempts": attempts}


def _source_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        source = str(record.get("model", {}).get("plan_outcome", {}).get("source", "unknown"))
        # Collapse the detail after the colon: "no-plan: provider error: ..." is
        # one category for counting, and the detail stays on the record.
        key = source.split(":", 1)[0]
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def write_run(
    result: dict[str, Any],
    provider: ModelProvider,
    corpus: Corpus,
    *,
    run_id: str,
    args: argparse.Namespace,
    root: Path = MODEL_RUN_ROOT,
) -> Path:
    system_id = str(result["system_id"])
    directory = root / system_id.replace("::", "--") / run_id
    (directory / "records").mkdir(parents=True, exist_ok=True)

    for attempt in result["attempts"]:
        for record in attempt["records"]:
            name = f"{record['case_id']}-attempt{attempt['attempt']:02d}.json"
            (directory / "records" / name).write_text(
                json.dumps(record, indent=2) + "\n", encoding="utf-8"
            )

    manifest = {
        "schema_version": "1.0.0",
        "suite": "atticusbench",
        "suite_version": SUITE_VERSION,
        "scorer_version": SCORER_VERSION,
        "split": "public-test",
        "run_id": run_id,
        "started_at": run_id,
        "system_id": system_id,
        "register_backed": system_id.startswith("register::"),
        "model": provenance(provider),
        "corpus_digest": corpus.digest(),
        "cases": len(corpus.cases),
        "repeats": args.repeats,
        "sampling": {
            "temperature": args.temperature,
            "max_output_tokens": args.max_output_tokens,
            "stop_after_json": True,
            "approvals_presented": 0,
        },
        "environment": {
            "code_commit": repo_commit(),
            "working_tree_dirty": working_tree_is_dirty(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor() or "unknown",
            "base_url": args.base_url,
        },
        "attempts": [
            {
                "attempt": attempt["attempt"],
                "report": attempt["report"],
                "wall_clock_seconds": attempt["wall_clock_seconds"],
                "plan_sources": attempt["plan_sources"],
                "case_scores": attempt["case_scores"],
            }
            for attempt in result["attempts"]
        ],
        "limitations": [
            (
                "A model run is not reproducible. Sampling, the served weights, and "
                "the host all move; the daemon's tag is not a digest pin. Nothing "
                "here is drift-checked and nothing here belongs in results.json."
            ),
            (
                "No approval grants were presented, so every case that needs one is "
                "measured as an approval pause."
            ),
            (
                "Identity is the register's declaration, not an attestation by the "
                "endpoint. An unregistered --model tag records license unknown."
            ),
            (
                "33 public cases with published expectations. A model trained on this "
                "repository would be measured on its own training data."
            ),
        ],
    }
    (directory / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return directory


def baseline_reports() -> dict[str, Any]:
    path = RUN_ROOT / "results.json"
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return dict(payload.get("reports", {}))


def baseline_case_scores(system_id: str) -> list[Any]:
    """Load committed baseline case scores for a paired comparison."""

    path = RUN_ROOT / "results.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [row for row in payload.get("case_scores", []) if row.get("system_id") == system_id]


def render(results: list[dict[str, Any]], corpus: Corpus) -> str:
    baselines = baseline_reports()
    lines = [
        "",
        f"AtticusBench model runs — {len(corpus.cases)} cases, scorer {SCORER_VERSION}",
        f"  corpus digest  {corpus.digest()}",
        "",
        f"{'system':<34}{'success':>10}{'unauth':>8}{'effects':>9}{'critical':>10}"
        f"{'abstain':>9}{'no-plan':>9}{'seconds':>9}",
    ]
    for report in baselines.values():
        lines.append(
            f"{('baseline ' + report['system_id']):<34}"
            f"{f'{report["task_success"]}/{report["cases"]}':>10}"
            f"{report['unauthorized_action_cases']:>8}"
            f"{report['forbidden_effects_total']:>9}"
            f"{report['critical_failures']:>10}"
            f"{report['abstention_rate']:>9.2f}"
            f"{'-':>9}{'-':>9}"
        )
    for result in results:
        for attempt in result["attempts"]:
            report = attempt["report"]
            sources = attempt["plan_sources"]
            label = f"{result['system_id']} #{attempt['attempt']}"
            lines.append(
                f"{label:<34}"
                f"{f'{report["task_success"]}/{report["cases"]}':>10}"
                f"{report['unauthorized_action_cases']:>8}"
                f"{report['forbidden_effects_total']:>9}"
                f"{report['critical_failures']:>10}"
                f"{report['abstention_rate']:>9.2f}"
                f"{sources.get('no-plan', 0):>9}"
                f"{attempt['wall_clock_seconds']:>9.1f}"
            )

    reference = baseline_case_scores("reference-plan-v1")
    if reference:
        lines.append("")
        for result in results:
            for attempt in result["attempts"]:
                comparison = _paired(reference, attempt["case_scores"])
                lines.append(
                    f"paired vs reference-plan-v1: {result['system_id']} "
                    f"#{attempt['attempt']} difference "
                    f"{comparison['success_rate_difference']:+.3f} on "
                    f"{comparison['paired_cases']} cases, discordant "
                    f"{comparison['left_only_success']}/{comparison['right_only_success']}, "
                    f"exact McNemar p={comparison['mcnemar_exact_p']:.6f}"
                )

    critical = [
        (result["system_id"], attempt["attempt"], report["critical_failure_case_ids"])
        for result in results
        for attempt in result["attempts"]
        if (report := attempt["report"])["critical_failure_case_ids"]
    ]
    lines.append("")
    if critical:
        lines.append("Critical-suite failures")
        for system_id, attempt, case_ids in critical:
            lines.append(f"  {system_id} #{attempt}: {', '.join(case_ids)}")
    else:
        lines.append("No critical-suite failures observed in these model runs.")
    lines.append("")
    lines.append(
        "Model runs are not reproducible and are excluded from results.json and "
        "from every drift check. Per-case detail is in each run's records/."
    )
    return "\n".join(lines)


def _paired(left_rows: list[Any], right_rows: list[Any]) -> dict[str, Any]:
    """Pair committed baseline scores against fresh model scores by case id."""

    from atticusbench.scoring import CaseScore

    def revive(rows: list[Any]) -> list[CaseScore]:
        return [
            CaseScore(
                case_id=row["case_id"],
                system_id=row["system_id"],
                family=row["family"],
                critical_suite=row["critical_suite"],
                terminal_state=row["terminal_state"],
                terminal_ok=row["terminal_ok"],
                must_call_coverage=row["must_call_coverage"],
                steps=row["steps"],
                within_step_budget=row["within_step_budget"],
                unauthorized_actions=row["unauthorized_actions"],
                failure_reasons=tuple(row["failure_reasons"]),
                forbidden_effects_observed=tuple(row["forbidden_effects_observed"]),
                approval_recall=row["approval_recall"],
                policy_denial_ok=row["policy_denial_ok"],
                citations_ok=row["citations_ok"],
                delegation_ok=row["delegation_ok"],
                abstained=row["abstained"],
                abstention_correct=row["abstention_correct"],
                excessive_abstention=row["excessive_abstention"],
                injection_exercised=row["injection_exercised"],
                success=row["success"],
                critical_failure=row["critical_failure"],
            )
            for row in rows
        ]

    return paired_comparison(revive(left_rows), revive(right_rows))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        action="append",
        dest="models",
        help="Ollama tag to measure, repeatable. Skips the register; license is "
        "recorded as unknown.",
    )
    parser.add_argument(
        "--stub",
        action="store_true",
        help="use the built-in stub provider: no daemon, no model, plumbing only",
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--case", action="append", dest="cases", help="limit to this case id")
    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="run the split this many times per model, to see plan stability",
    )
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-output-tokens", type=int, default=2048)
    parser.add_argument("--stall-timeout", type=float, default=DEFAULT_STALL_TIMEOUT_SECONDS)
    parser.add_argument("--json", action="store_true", help="print the run payload as JSON")
    parser.add_argument(
        "--out",
        type=Path,
        default=MODEL_RUN_ROOT,
        help="directory for model run records (default runs/atticusbench/models)",
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="measure without writing records, for a quick look",
    )
    args = parser.parse_args(argv)

    if args.repeats < 1:
        print("--repeats must be at least 1", file=sys.stderr)
        return 2
    if args.stub and args.models:
        print("--stub and --model are mutually exclusive", file=sys.stderr)
        return 2

    corpus = load_corpus()
    providers = resolve_providers(args)
    if not providers:
        print(
            "No model to measure. Either give a tag with --model, add a 'serving' "
            "block to a candidate in models/bakeoff/candidates.yaml, or use --stub "
            "to exercise the path with no daemon.",
            file=sys.stderr,
        )
        return 2

    constraints = CompletionConstraints(
        temperature=args.temperature,
        max_output_tokens=args.max_output_tokens,
        require_open_weight=True,
        stop_after_json=True,
    )

    results: list[dict[str, Any]] = []
    skipped: list[str] = []
    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    for system_id, provider in sorted(providers.items()):
        reason = preflight(system_id, provider)
        if reason is not None:
            skipped.append(reason)
            print(f"skip: {reason}", file=sys.stderr)
            continue
        print(f"running {system_id} ({provider.identity.model_family})", file=sys.stderr)
        result = run_one(
            corpus,
            system_id,
            provider,
            case_ids=args.cases,
            repeats=args.repeats,
            constraints=constraints,
        )
        results.append(result)
        if not args.no_write:
            directory = write_run(result, provider, corpus, run_id=run_id, args=args, root=args.out)
            print(f"wrote {display_path(directory)}", file=sys.stderr)

    if not results:
        print(
            "\nNothing ran. Every provider failed preflight:\n  " + "\n  ".join(skipped),
            file=sys.stderr,
        )
        return 1

    if args.json:
        payload = [
            {
                "system_id": result["system_id"],
                "attempts": [
                    {key: value for key, value in attempt.items() if key != "records"}
                    for attempt in result["attempts"]
                ],
            }
            for result in results
        ]
        print(json.dumps(payload, indent=2))
    else:
        print(render(results, corpus))
    if skipped:
        print("\nSkipped:", file=sys.stderr)
        for reason in skipped:
            print(f"  {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
