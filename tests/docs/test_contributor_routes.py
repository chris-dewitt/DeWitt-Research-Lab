"""Guards for contributor routes and good-first seeds (DRL-029)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUTES = ROOT / "docs" / "09-open-source" / "CONTRIBUTOR_ROUTES.md"
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "good-first.yml"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"


def test_contributor_routes_map_and_good_first_seeds() -> None:
    assert ROUTES.is_file()
    text = ROUTES.read_text(encoding="utf-8")
    assert "Maturity: **prototype**" in text
    assert "make doctor" in text
    assert "make verify" in text
    for seed in ("GFI-001", "GFI-002", "GFI-003", "GFI-004", "GFI-005"):
        assert seed in text, seed
    assert "Sponsors do not" in text
    assert "CONTRIBUTOR_CREDIT_AND_AUTHORSHIP.md" in text

    assert TEMPLATE.is_file()
    template = TEMPLATE.read_text(encoding="utf-8")
    assert "Good first issue" in template
    assert "Acceptance evidence" in template

    contributing = CONTRIBUTING.read_text(encoding="utf-8")
    assert "CONTRIBUTOR_ROUTES.md" in contributing
    assert "good first issue" in contributing.lower()
