"""Enforce that controlled brand text agrees across every document and code path.

`DOCUMENT_CONTROL.md` states that stale or contradictory documentation is a defect.
The mission line previously lived in eight hand-maintained places, so a Director
change to it silently left seven of them wrong. `BRAND_SYSTEM.md` is the canonical
owner; everything else must agree with it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BRAND_SYSTEM = ROOT / "docs" / "08-web-brand" / "BRAND_SYSTEM.md"

# Files that quote the mission line and must stay in agreement with BRAND_SYSTEM.md.
QUOTING_PATHS = [
    "README.md",
    "LABORATORY_BIBLE.md",
    "docs/09-open-source/OPEN_SOURCE_IDENTITY_SYSTEM.md",
    "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md",
    "docs/08-web-brand/HOMEPAGE_SPEC.md",
    "services/atticus-control-plane/src/atticus_control_plane/tools.py",
    "scripts/audit_wix_site.py",
]

# Mission lines that have been retired and must not reappear anywhere.
RETIRED_MISSION_LINES = [
    "AI for Good. AI for all.",
    "Intelligence of the people and for the people.",
]

SEARCH_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml"}
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".ruff_cache", ".mypy_cache"}

# Historical records must quote retired text verbatim to stay meaningful.
# DIRECTORS_MEMO.md instructs agents to "preserve closed entries; do not erase
# institutional memory", so a decision row naming the superseded line is correct.
HISTORY_EXEMPT = {"DIRECTORS_MEMO.md", "CHANGELOG.md", "WORKLOG.md"}


def canonical_mission_line() -> str:
    """Extract the mission line from its canonical owner, BRAND_SYSTEM.md."""
    text = BRAND_SYSTEM.read_text()
    match = re.search(r"##\s*Mission line\s*\n+\*\*(.+?)\*\*", text, re.S)
    assert match, "BRAND_SYSTEM.md no longer declares a '## Mission line' section"
    return match.group(1).strip()


def iter_repo_files() -> list[Path]:
    out: list[Path] = []
    for path in ROOT.rglob("*"):
        if path.suffix not in SEARCH_SUFFIXES or not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        out.append(path)
    return out


def test_canonical_mission_line_is_declared() -> None:
    line = canonical_mission_line()
    assert line
    assert line.endswith("."), f"mission line should be punctuated: {line!r}"


@pytest.mark.parametrize("rel", QUOTING_PATHS)
def test_quoting_files_match_canonical_mission_line(rel: str) -> None:
    line = canonical_mission_line()
    text = (ROOT / rel).read_text()
    assert line in text, (
        f"{rel} does not contain the canonical mission line {line!r} from BRAND_SYSTEM.md. "
        "Update it, or drop it from QUOTING_PATHS if it should no longer carry the line."
    )


def test_no_retired_mission_line_survives_anywhere() -> None:
    offenders: list[str] = []
    for path in iter_repo_files():
        if path == Path(__file__):
            continue
        if path.relative_to(ROOT).as_posix() in HISTORY_EXEMPT:
            continue
        if path.match("agents/handoffs/*"):
            continue
        text = path.read_text(errors="replace")
        for retired in RETIRED_MISSION_LINES:
            if retired in text:
                offenders.append(f"{path.relative_to(ROOT)}: {retired!r}")
    assert not offenders, "retired mission line still present:\n" + "\n".join(offenders)
