#!/usr/bin/env python3
"""Generate a deterministic SHA-256 manifest for the tracked source tree."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess  # nosec B404
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git_output(root: Path, *args: str) -> str:
    git_executable = shutil.which("git")
    if git_executable is None:
        raise RuntimeError("git executable is unavailable")
    # Fixed shell-free Git calls only; no user-controlled command or executable.
    completed = subprocess.run(  # noqa: S603  # nosec B603
        [git_executable, *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "git command failed")
    return completed.stdout


def tracked_paths(root: Path) -> list[str]:
    return [path for path in git_output(root, "ls-files", "-z").split("\0") if path]


def build_manifest(
    root: Path,
    paths: Iterable[str],
    *,
    source_revision: str,
    generated_at: str,
) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for rel in sorted(paths):
        path = root / rel
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Tracked manifest input is not a regular file: {rel}")
        data = path.read_bytes()
        entries.append(
            {
                "path": Path(rel).as_posix(),
                "size_bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return {
        "schema_version": "2.0.0",
        "package": "DeWitt-Research-Lab",
        "source_revision": source_revision,
        "generated_at": generated_at,
        "algorithm": "sha256",
        "entry_count": len(entries),
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "site" / "source-manifest.json",
        help="output path; defaults to ignored release-build storage",
    )
    args = parser.parse_args()

    revision = os.environ.get("GITHUB_SHA") or git_output(ROOT, "rev-parse", "HEAD").strip()
    generated_at = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
    manifest = build_manifest(
        ROOT,
        tracked_paths(ROOT),
        source_revision=revision,
        generated_at=generated_at,
    )
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {manifest['entry_count']} tracked entries to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
