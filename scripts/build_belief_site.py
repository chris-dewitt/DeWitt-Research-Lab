#!/usr/bin/env python
"""Build the CFI-007 belief-trajectory viewer.

Renders synthetic belief paths and the estimators applied to them as static
HTML. Fixtures are generated from fixed seeds rather than read from disk, so the
output is byte-identical on every machine and there is no data file to drift
from the code that produces it.

    uv run python scripts/build_belief_site.py --out site/beliefs --metadata
    uv run python scripts/build_belief_site.py --list
    uv run python scripts/build_belief_site.py --only walk-fitted-as-reverting

This is a local viewer. Nothing here is published, and `site/` is gitignored.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research" / "cfi" / "src"))

from drl_cfi.viewer import (  # noqa: E402
    BeliefSiteError,
    build_site,
    default_cases,
    ordered,
    select_cases,
    site_metadata,
)

DEFAULT_OUT = ROOT / "site" / "beliefs"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--metadata", action="store_true", help="also write site.json describing what was built"
    )
    parser.add_argument("--list", action="store_true", help="list the available fixtures and exit")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--only", action="append", metavar="NAME", help="build only these fixtures (repeatable)"
    )
    group.add_argument(
        "--empty-state",
        action="store_true",
        help="render the empty index deliberately, with no trajectories",
    )
    args = parser.parse_args(argv)

    try:
        cases = default_cases()
        if args.list:
            for case in ordered(cases):
                print(f"{case.state:9} {case.name}")
            return 0
        selected = select_cases(cases, only=args.only, empty=args.empty_state)
        written = build_site(selected, args.out)
        # Inside the try: a metadata failure must exit 1 like any other, rather
        # than escaping as a traceback after the pages were already written.
        if args.metadata:
            meta = args.out / "site.json"
            meta.write_text(json.dumps(site_metadata(selected), indent=2) + "\n", encoding="utf-8")
            written.append(meta)
    except BeliefSiteError as exc:
        print(f"belief site build failed: {exc}", file=sys.stderr)
        return 1

    for path in written:
        print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
    print(f"\n{len(written)} file(s) written to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
