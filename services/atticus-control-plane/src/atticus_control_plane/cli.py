"""Command-line demonstration of the integrated DRL research workflow."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from drl_protocol import TaskRequest, TaskResult

from .model_planner import ModelPlanner
from .run_record import write_run_record
from .runtime import build_runtime_from_env, live_data_enabled

DEFAULT_OBJECTIVE = (
    "Using the latest available public inflation evidence and Federal Reserve "
    "communication, construct a plausible synthetic bear-steepener scenario "
    "and analyze its impact on the sample regional bank."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Atticus foundation demo")
    parser.add_argument("objective", nargs="?", default=DEFAULT_OBJECTIVE)
    parser.add_argument(
        "--as-of",
        default=None,
        help="Point-in-time cutoff (default: fixture pin 2026-07-24, or today in live mode)",
    )
    parser.add_argument("--public", action="store_true", help="Apply public-session policy")
    parser.add_argument("--json", action="store_true", help="Print the complete result as JSON")
    return parser


def describe_planner(runtime: object) -> str:
    """Report which planner actually ran.

    The model planner falls back to fixtures on any failure, so a silent
    fallback would otherwise look exactly like success. Naming the planner and
    the model makes the difference observable in the output itself.
    """
    planner = getattr(runtime, "planner", None)
    if not isinstance(planner, ModelPlanner):
        return "deterministic fixture planner (set ATTICUS_MODEL to use a model)"
    identity = planner.gateway.provider().identity
    configured = f"{identity.revision} ({identity.runtime})"
    source = planner.last_plan_source
    if source == "model":
        return f"model planner via {configured}"
    if source == "model+integrated-coverage":
        return f"model planner via {configured} plus catalog coverage"
    return f"{configured} configured, but plan came from {source}"


def describe_plan_source(runtime: object) -> str:
    """Machine-readable plan source for the run record."""
    planner = getattr(runtime, "planner", None)
    if isinstance(planner, ModelPlanner):
        return planner.last_plan_source
    return "fixture"


def progress_to_stderr(event: str, detail: str) -> None:
    """Print a one-line progress update. Stderr keeps ``--json`` stdout clean."""
    line = f"progress: {event}"
    if detail:
        line = f"{line} {detail}"
    print(line, file=sys.stderr, flush=True)


def render_human_report(
    result: TaskResult,
    planner_line: str,
    *,
    log_path: Path | None = None,
) -> str:
    """Printable card for a demo run. Full trace is ``--json``."""
    tools: list[str] = []
    for event in result.trace:
        name = event.attributes.get("tool")
        if event.event_type == "tool_completed" and name:
            tools.append(f"  ok  {name}")
        elif event.event_type == "tool_failed" and name:
            tools.append(f"  FAIL {name}")
    evidence_lines = [f"  - {item.evidence_id}: {item.title}" for item in result.evidence]
    record_line = f"RUN RECORD: {log_path}" if log_path is not None else "RUN RECORD: (not written)"
    lines = [
        "DEWITT RESEARCH WORKSHOP // ATTICUS LOCAL FOUNDATION",
        f"PLANNER: {planner_line}",
        f"STATE: {result.state.value}",
        "",
        result.summary,
        "",
        "TOOLS:",
        *(tools or ["  (none invoked)"]),
        "",
        f"EVIDENCE: {len(result.evidence)} items",
        *(evidence_lines or ["  (none)"]),
        "",
        (
            f"EVALFORGE: {result.evaluation.get('score', 'not-run')} "
            "(scores the finished trajectory; it is not a specialist)"
        ),
        "",
        record_line,
        "Ids and scores only. Re-run with --json to print the full trace.",
        "LIMITATIONS:",
        *[f"- {limitation}" for limitation in result.limitations],
    ]
    return "\n".join(lines)


def main() -> int:
    args = build_parser().parse_args()
    as_of = args.as_of
    if as_of is None:
        as_of = date.today().isoformat() if live_data_enabled() else "2026-07-24"
    request = TaskRequest(
        task_id="atticus-demo",
        objective=args.objective,
        public_session=args.public,
        as_of=as_of,
    )
    runtime = build_runtime_from_env()
    result = runtime.run(request, progress=progress_to_stderr)
    planner_line = describe_planner(runtime)
    try:
        log_path = write_run_record(
            result,
            planner_line=planner_line,
            plan_source=describe_plan_source(runtime),
        )
    except OSError as exc:
        print(f"run-record: write failed: {exc}", file=sys.stderr)
        log_path = None
    else:
        print(f"run-record: {log_path}", file=sys.stderr)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, default=str))
    else:
        print(render_human_report(result, planner_line, log_path=log_path))
    return 0 if result.state.value in {"completed", "degraded"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
