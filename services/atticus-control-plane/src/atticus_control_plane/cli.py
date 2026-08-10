"""Command-line demonstration of the integrated DRL research workflow."""

from __future__ import annotations

import argparse
import json

from drl_protocol import TaskRequest

from .model_planner import ModelPlanner
from .runtime import build_runtime_from_env

DEFAULT_OBJECTIVE = (
    "Using the latest available public inflation evidence and Federal Reserve "
    "communication, construct a plausible synthetic bear-steepener scenario "
    "and analyze its impact on the sample regional bank."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Atticus foundation demo")
    parser.add_argument("objective", nargs="?", default=DEFAULT_OBJECTIVE)
    parser.add_argument("--as-of", default="2026-07-24")
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
    if planner.last_plan_source == "model":
        return f"model planner via {configured}"
    return f"{configured} configured, but plan came from {planner.last_plan_source}"


def main() -> int:
    args = build_parser().parse_args()
    request = TaskRequest(
        task_id="atticus-demo",
        objective=args.objective,
        public_session=args.public,
        as_of=args.as_of,
    )
    runtime = build_runtime_from_env()
    result = runtime.run(request)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, default=str))
    else:
        print("DEWITT RESEARCH WORKSHOP // ATTICUS LOCAL FOUNDATION")
        print(f"PLANNER: {describe_planner(runtime)}")
        print(f"STATE: {result.state.value}")
        print()
        print(result.summary)
        print()
        print(f"EVIDENCE: {len(result.evidence)} items")
        print(f"EVALFORGE: {result.evaluation.get('score', 'not-run')}")
        print("LIMITATIONS:")
        for limitation in result.limitations:
            print(f"- {limitation}")
    return 0 if result.state.value in {"completed", "degraded"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
