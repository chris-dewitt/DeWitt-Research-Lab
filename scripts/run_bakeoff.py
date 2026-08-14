#!/usr/bin/env python3
"""Run the Stage-B Atticus bake-off and emit the evidence package.

By default this runs in ``fixture`` mode with scripted providers, which is
reproducible in CI and — by design — can never produce a winner: the evidence
gate rejects any selection whose metrics were not measured on hardware.

``--live`` runs the suite against the endpoints the register says have been
stood up. Give a candidate a ``serving`` block and it is included; leave it out
and it is skipped, because nobody having served a model is not the same as that
model failing:

    serving:
      runtime: ollama
      model: gemma4:26b
      base_url: http://localhost:11434/v1   # optional
      quantization: Q4_K_M                  # optional

A live run measures on real hardware, so pass ``--measurement-mode hardware``
to have it count as such. The gate is identical in both modes and is not
relaxed by either.

    uv run python scripts/probe_model.py          # confirm the endpoint first
    uv run python scripts/run_bakeoff.py --live --measurement-mode hardware

Exit codes:
  0  the run completed and produced an evidence package
  1  the run could not produce trustworthy evidence

A run that completes without naming a winner exits 0. "No winner yet" is a
successful, informative outcome, not a failure.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from drl_ai_core import ScriptedProvider, run_bakeoff, summarise_blockers
from drl_ai_core.bakeoff import load_bakeoff_register
from drl_ai_core.bakeoff_harness import BakeoffError, build_live_providers
from drl_ai_core.http_provider import DEFAULT_STALL_TIMEOUT_SECONDS
from drl_ai_core.providers import CompletionConstraints, ModelProvider

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "models" / "bakeoff" / "candidates.yaml"
SUITE = ROOT / "models" / "bakeoff" / "task_suite.yaml"

# A deliberately mediocre script: it answers the routing tasks and nothing else,
# so fixture runs produce visibly incomplete evidence rather than a suspicious
# clean sweep.
FIXTURE_SCRIPT = {
    "balance of risks": "fedlens",
    "bear steepener": "balancelab",
    "look into rates": "Which rates did you mean — policy, curve, or deposit?",
    "escalate to Core": "escalate to core",
    "classify intent": "failures",
}


def build_fixture_providers(register_path: Path) -> dict[str, ModelProvider]:
    """Return a scripted provider for each registered candidate.

    Candidates left out of this mapping are skipped rather than scored zero.
    """
    register = load_bakeoff_register(register_path)
    providers: dict[str, ModelProvider] = {}
    for row in register.get("candidates", []):
        providers[str(row["id"])] = ScriptedProvider(
            FIXTURE_SCRIPT,
            provider_id=f"fixture::{row['id']}",
            model_family=str(row.get("family", "")),
            revision=str(row.get("revision_label", "")),
            license_label=str(row.get("license_label", "")),
        )
    return providers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=REGISTER)
    parser.add_argument("--suite", type=Path, default=SUITE)
    parser.add_argument(
        "--live",
        action="store_true",
        help="run against the endpoints the register declares under 'serving'",
    )
    parser.add_argument(
        "--base-url",
        help="override every candidate's endpoint (one runtime serving each in turn)",
    )
    parser.add_argument(
        "--stall-timeout",
        type=float,
        default=DEFAULT_STALL_TIMEOUT_SECONDS,
        help="seconds of silence tolerated from a live endpoint before it is called dead",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=900.0,
        help="total ceiling per task, in seconds",
    )
    parser.add_argument(
        "--measurement-mode",
        choices=("fixture", "hardware"),
        default="fixture",
        help="fixture runs can never produce a selection; hardware runs may.",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    parser.add_argument("--out", type=Path, help="write the report to this path")
    args = parser.parse_args()

    if args.live:
        providers = build_live_providers(
            args.register,
            base_url_override=args.base_url,
            stall_timeout=args.stall_timeout,
        )
        if not providers:
            print(
                "No candidate in the register declares a 'serving' block, so there "
                "is nothing to run live. Add one to the candidate you have stood up.",
                file=sys.stderr,
            )
            return 1
        constraints: CompletionConstraints | None = CompletionConstraints(
            timeout_seconds=args.timeout, temperature=0.0, require_open_weight=True
        )
        print(f"running live against: {', '.join(sorted(providers))}\n", file=sys.stderr)
    else:
        providers = build_fixture_providers(args.register)
        constraints = None
        if args.measurement_mode == "hardware":
            # Labelling scripted providers as hardware-measured would defeat the
            # one gate condition fixtures cannot otherwise clear.
            print(
                "refusing --measurement-mode hardware without --live: fixture "
                "providers did not measure anything on hardware.",
                file=sys.stderr,
            )
            return 1

    try:
        report = run_bakeoff(
            providers,
            register_path=args.register,
            suite_path=args.suite,
            constraints=constraints,
            measurement_mode=args.measurement_mode,
        )
    except BakeoffError as exc:
        print(f"bake-off could not produce evidence: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(report.as_dict(), indent=2) if args.json else report.to_markdown()
    print(rendered)
    if args.out:
        args.out.write_text(rendered, encoding="utf-8")

    if not report.any_selection:
        print("\nNo winner declared. DIR-004 remains open. Blocked by:", file=sys.stderr)
        for blocker in summarise_blockers(report):
            print(f"  - {blocker}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
