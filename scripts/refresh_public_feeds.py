"""CLI: refresh official FRED / Treasury / Fed feeds into data/public-feeds."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.public_feeds.refresh import refresh_public_feeds  # noqa: E402
from scripts.public_feeds.store import CHANGES_NAME, FeedStore  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Ingest official public feeds (FRED, Treasury yields, Fed press RSS). "
            "Yahoo Finance is not a source. Fixtures stay the Atticus default."
        )
    )
    parser.add_argument(
        "--root",
        default=os.environ.get("DRL_FEED_ROOT", "data/public-feeds"),
        help="Store directory (or DRL_FEED_ROOT)",
    )
    parser.add_argument(
        "--print-changes",
        action="store_true",
        help="Print the change report after refresh",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    status = refresh_public_feeds(root=Path(args.root))
    print(json.dumps(status, indent=2))
    if status["observation_count"] == 0 and status["document_count"] == 0:
        print("refresh produced no feed items", file=sys.stderr)
        return 1
    if args.print_changes:
        changes = FeedStore(Path(args.root)).read_json(CHANGES_NAME)
        print(json.dumps(changes, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
