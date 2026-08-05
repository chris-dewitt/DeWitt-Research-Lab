#!/usr/bin/env python3
"""Run the Stage-B Atticus bake-off and emit the evidence package.

By default this runs in ``fixture`` mode with scripted providers, which is
reproducible in CI and — by design — can never produce a winner: the evidence
gate rejects any selection whose metrics were not measured on hardware.

To run a real bake-off, register live providers in ``build_providers`` and pass
``--measurement-mode hardware``. Everything else, including the gate, is
unchanged.

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
from drl_ai_core.bakeoff_harness import BakeoffError
from drl_ai_core.providers import ModelProvider

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


def build_providers(register_path: Path) -> dict[str, ModelProvider]:
    """Return the provider for each registered candidate.

    Replace the scripted providers here with real endpoints to run a live
    bake-off. Candidates left out of this mapping are skipped rather than
    scored zero.
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
        "--measurement-mode",
        choices=("fixture", "hardware"),
        default="fixture",
        help="fixture runs can never produce a selection; hardware runs may.",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    parser.add_argument("--out", type=Path, help="write the report to this path")
    args = parser.parse_args()

    try:
        report = run_bakeoff(
            build_providers(args.register),
            register_path=args.register,
            suite_path=args.suite,
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
