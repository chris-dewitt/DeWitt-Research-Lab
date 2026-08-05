#!/usr/bin/env python3
"""Build the static replay viewer.

Renders the signed replay bundles to a directory of self-contained HTML that can
be served from GitHub Pages or any static host — no backend, no model, no cloud
account.

    uv run python scripts/build_replay_site.py --out site/replays

Bundles whose manifest signature or artifact digests fail verification are not
rendered; the build fails instead. A replay page claims "this is what happened",
and publishing an unverified recording under that claim would be worse than
publishing nothing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from evalforge_service.replay_site import (
    ReplaySiteError,
    build_site,
    load_bundle,
    site_metadata,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLES = ROOT / "services" / "evalforge" / "fixtures" / "signed_replays"
DEFAULT_OUT = ROOT / "site" / "replays"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundles", type=Path, default=DEFAULT_BUNDLES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--metadata",
        action="store_true",
        help="also write site.json describing what was published",
    )
    args = parser.parse_args()

    try:
        written = build_site(args.bundles, args.out)
    except ReplaySiteError as exc:
        print(f"replay site build failed: {exc}", file=sys.stderr)
        return 1

    if args.metadata:
        bundles = [
            load_bundle(p) for p in sorted(args.bundles.iterdir()) if p.is_dir()
        ]
        meta_path = args.out / "site.json"
        meta_path.write_text(json.dumps(site_metadata(bundles), indent=2), encoding="utf-8")
        written.append(meta_path)

    for path in written:
        print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
    print(f"\n{len(written)} file(s) written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
