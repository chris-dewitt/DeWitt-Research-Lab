"""Guard the personal academic portfolio contract for dewitt-labs.com."""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]

PUBLIC_DOCS = [
    "docs/01-product/PORTFOLIO_V1_PRD.md",
    "docs/08-web-brand/BRAND_SYSTEM.md",
    "docs/08-web-brand/WEBSITE_PRODUCT_AND_DESIGN_SPEC.md",
    "docs/08-web-brand/HOMEPAGE_SPEC.md",
    "docs/08-web-brand/SITE_COPY.md",
    "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md",
]

HOMEPAGE_DOCS = [
    "docs/08-web-brand/HOMEPAGE_SPEC.md",
    "docs/08-web-brand/SITE_COPY.md",
    "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md",
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def prose(rel: str) -> str:
    return " ".join(read(rel).split())


@pytest.mark.parametrize("rel", PUBLIC_DOCS)
def test_public_docs_center_the_person_and_current_degree(rel: str) -> None:
    text = prose(rel)
    assert "Christopher Noxon DeWitt" in text
    assert "Master of Applied Data Science" in text
    assert "University of North Carolina at Chapel Hill" in text
    assert "graduate work in computer science" in text


@pytest.mark.parametrize("rel", HOMEPAGE_DOCS)
def test_homepage_actions_are_research_then_projects(rel: str) -> None:
    text = read(rel)
    research = text.find("View my research")
    projects = text.find("Explore my projects")
    assert research >= 0 and projects >= 0
    assert research < projects


@pytest.mark.parametrize("rel", HOMEPAGE_DOCS)
def test_homepage_does_not_brand_itself_as_a_lab_or_workshop(rel: str) -> None:
    text = read(rel)
    hero = text[text.find("```text") : text.find("```", text.find("```text") + 3)]
    assert "DEWITT RESEARCH WORKSHOP" not in hero
    assert "DEWITT RESEARCH LABORATORY" not in hero
    assert "INTELLIGENCE FOR GOOD" not in hero.upper()


def test_atticus_domain_remains_planned() -> None:
    routing = yaml.safe_load((ROOT / "configs/domain-routing.yaml").read_text())
    atticus = next(app for app in routing["applications"] if app["id"] == "atticus")
    assert atticus["status"] == "planned"


def test_site_copy_links_the_live_replay_viewer() -> None:
    text = read("docs/08-web-brand/SITE_COPY.md")
    assert "https://chris-dewitt.github.io/DeWitt-Research-Lab/" in text
    assert "no hosted player yet" not in text
