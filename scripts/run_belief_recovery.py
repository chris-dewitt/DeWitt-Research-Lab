#!/usr/bin/env python
"""Run the CFI-005 synthetic parameter-recovery study.

Simulates belief paths at known parameters, fits them back with the baselines in
`drl_cfi.baselines`, and reports the recovery error. It asserts nothing: whether
a given bias is tolerable is a protocol question and no protocol has passed G3.

    uv run python scripts/run_belief_recovery.py
    uv run python scripts/run_belief_recovery.py --json --out recovery.json

Every number is reproducible from `--seed`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "research" / "cfi" / "src"))

from drl_cfi.baselines import RecoveryReport, recovery_study  # noqa: E402

#: The study's design. These truths are inside the schema's representable range
#: by construction — a path that saturates is refused by the simulator rather
#: than silently flattened, which is what an earlier version of this study did.
DESIGNS: tuple[tuple[str, dict[str, float]], ...] = (
    ("diffusion", {"drift": 0.4, "volatility": 0.8}),
    (
        "ornstein_uhlenbeck",
        {"reversion_rate": 1.5, "level": 0.7, "volatility": 0.6},
    ),
    (
        "jump_diffusion",
        {
            "drift": 0.0,
            "volatility": 0.5,
            "jump_intensity": 0.8,
            "jump_mean": 0.0,
            "jump_scale": 1.2,
        },
    ),
)


def as_dict(report: RecoveryReport) -> dict[str, Any]:
    return {
        "model": report.model,
        "replications": report.replications,
        "steps": report.steps,
        "dt": report.dt,
        "horizon": report.steps * report.dt,
        "parameters": [
            {
                "name": p.name,
                "truth": p.truth,
                "mean_estimate": p.mean_estimate,
                "bias": p.bias,
                "relative_bias": p.relative_bias,
                "spread": p.spread,
                "root_mean_square_error": p.root_mean_square_error,
            }
            for p in report.parameters
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replications", type=int, default=200)
    parser.add_argument("--steps", type=int, default=400)
    parser.add_argument("--dt", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260825)
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument("--out", type=Path, help="write the report to this path")
    args = parser.parse_args(argv)

    reports = [
        recovery_study(
            model,
            replications=args.replications,
            steps=args.steps,
            dt=args.dt,
            seed=args.seed,
            **truth,
        )
        for model, truth in DESIGNS
    ]

    if args.json:
        payload = json.dumps(
            {
                "seed": args.seed,
                "studies": [as_dict(report) for report in reports],
            },
            indent=2,
        )
    else:
        payload = "\n\n".join(report.render() for report in reports)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
