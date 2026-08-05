"""Guard the evidence-first academic website contract.

The website hierarchy is hand-maintained across Wix instructions, copy, product
requirements, and the open application shell. These checks keep the primary
audience and actions from drifting back to an institutional or collaborator-first
site while Wix remains a separately operated surface.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "docs" / "08-web-brand" / "BRAND_SYSTEM.md"

THESIS_PATHS = [
    "README.md",
    "LABORATORY_BIBLE.md",
    "docs/01-product/PORTFOLIO_V1_PRD.md",
    "docs/08-web-brand/WEBSITE_PRODUCT_AND_DESIGN_SPEC.md",
    "docs/08-web-brand/HOMEPAGE_SPEC.md",
    "docs/08-web-brand/SITE_COPY.md",
    "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md",
]

PRIMARY_ACTION_PATHS = [
    "docs/01-product/PORTFOLIO_V1_PRD.md",
    "docs/08-web-brand/HOMEPAGE_SPEC.md",
    "docs/08-web-brand/SITE_COPY.md",
    "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md",
]

PUBLIC_COPY_PATHS = [
    "docs/08-web-brand/HOMEPAGE_SPEC.md",
    "docs/08-web-brand/SITE_COPY.md",
    "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md",
]


def canonical_research_thesis() -> str:
    """Extract the website thesis from its canonical owner."""
    text = BRAND.read_text(encoding="utf-8")
    match = re.search(r"## Research thesis\s+\*\*(.+?)\*\*", text, re.S)
    assert match, "BRAND_SYSTEM.md must own a '## Research thesis' section"
    return match.group(1).strip()


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_research_thesis_is_specific_and_punctuated() -> None:
    thesis = canonical_research_thesis()
    assert thesis == "Engineering complex systems for open, inspectable intelligence."


@pytest.mark.parametrize("rel", THESIS_PATHS)
def test_controlled_positioning_documents_quote_the_thesis(rel: str) -> None:
    assert canonical_research_thesis() in read(rel)


@pytest.mark.parametrize("rel", PRIMARY_ACTION_PATHS)
def test_recorded_run_precedes_the_technical_report(rel: str) -> None:
    text = read(rel)
    watch = text.find("Watch a recorded run")
    report = text.find("Read TR-2026-001")
    assert watch >= 0, f"{rel} is missing the recorded-run action"
    assert report >= 0, f"{rel} is missing the report action"
    assert watch < report, f"{rel} must place the recorded run before the report"


@pytest.mark.parametrize("rel", PUBLIC_COPY_PATHS)
def test_negative_results_are_visible_in_public_copy(rel: str) -> None:
    text = read(rel).lower()
    assert "degraded" in text
    assert "no winner" in text
    assert "six" in text and "reason" in text


@pytest.mark.parametrize("rel", PUBLIC_COPY_PATHS)
def test_public_copy_does_not_render_a_launch_atticus_button(rel: str) -> None:
    text = read(rel)
    assert not re.search(r"\[(?:Launch|Open|Try) Atticus\]", text, re.I)


def test_atticus_domain_is_still_planned() -> None:
    routing = yaml.safe_load((ROOT / "configs" / "domain-routing.yaml").read_text())
    atticus = next(app for app in routing["applications"] if app["id"] == "atticus")
    assert atticus["host"] == "atticus.dewitt-labs.com"
    assert atticus["status"] == "planned"


def test_contributor_posture_is_secondary() -> None:
    for rel in (
        "docs/01-product/PORTFOLIO_V1_PRD.md",
        "docs/01-product/USER_PERSONAS_AND_JOURNEYS.md",
        "docs/08-web-brand/BRAND_SYSTEM.md",
        "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md",
    ):
        assert "secondary" in read(rel).lower(), rel
