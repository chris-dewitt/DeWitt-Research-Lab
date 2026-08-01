"""Guards for TR-2026-001 technical report (DRL-028)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "docs" / "10-research" / "reports" / "TR-2026-001-integrated-workflow.md"

FORBIDDEN = re.compile(
    r"(?i)\b(api[_-]?key|sk-[A-Za-z0-9]{12,}|BEGIN [A-Z ]+PRIVATE KEY|"
    r"password\s*[:=]|ssn|social security)\b"
)


def test_technical_report_has_methods_rights_limitations_and_reproduction() -> None:
    assert REPORT.is_file()
    text = REPORT.read_text(encoding="utf-8")
    assert "TR-2026-001" in text
    assert "maturity: prototype" in text
    for section in (
        "## Citation",
        "## 2. Methods",
        "## 3. Code and revision anchors",
        "## 4. Data rights and provenance",
        "## 6. Limitations",
        "## 7. Reproduction",
    ):
        assert section in text, section
    assert "make demo" in text
    assert "linked_workflow" in text
    assert "15.81" in text
    assert FORBIDDEN.search(text) is None
    assert "not a production" in text.lower() or "demo HMAC" in text
