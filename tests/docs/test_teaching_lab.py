"""Guards for the integrated workflow teaching lab (DRL-020)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "docs" / "10-research" / "teaching" / "INTEGRATED_WORKFLOW_LAB.md"

FORBIDDEN = re.compile(
    r"(?i)\b(api[_-]?key|sk-[A-Za-z0-9]{12,}|BEGIN [A-Z ]+PRIVATE KEY|"
    r"password\s*[:=]|employer|ssn|social security)\b"
)


def test_teaching_lab_exists_with_exercises_and_no_private_markers() -> None:
    assert LAB.is_file()
    text = LAB.read_text(encoding="utf-8")
    assert "Integrated Workflow Teaching Lab" in text
    assert "Maturity: **prototype**" in text
    for marker in (
        "## Lab 0",
        "## Lab 1",
        "## Lab 2",
        "## Lab 3",
        "## Lab 4",
        "## Lab 5",
        "**Exercise",
        "make demo",
        "linked_workflow",
        "15.81",
    ):
        assert marker in text, marker
    assert FORBIDDEN.search(text) is None
    assert "No private datasets" in text or "no private data" in text.lower()
