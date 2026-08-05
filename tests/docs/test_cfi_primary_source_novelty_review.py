"""Guards for the CFI-002 primary-source novelty review (DRL-032)."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "docs" / "10-research" / "CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md"


def test_review_is_controlled_and_covers_every_approved_track() -> None:
    text = REVIEW.read_text(encoding="utf-8")
    assert "document_id: DRL-RES-006" in text
    assert "status: IN REVIEW" in text
    assert "G1 stop condition triggered" in text
    for track in (
        "Shared bridge: Belief Diffusion",
        "Paper I: The Option Value of Thinking",
        "Paper II: Language, Arbitrage, and the Price of Belief",
        "Paper III: A Market of Minds",
    ):
        assert track in text


def test_review_names_contribution_collisions_and_provisional_boundary() -> None:
    text = REVIEW.read_text(encoding="utf-8")
    for identifier in (
        "2606.30850",  # BayesBench
        "2606.30852",  # LearnStop
        "U27ZfUx7JE",  # Outcome-Free Audits and Repairs
        "2604.20050",  # Information Aggregation with AI Agents
        "2606.26583",  # Monoculture
        "2607.04389",  # WALLA
    ):
        assert identifier in text
    assert "The evidence set below contains 31 retained primary records" in text
    assert len([line for line in text.splitlines() if line.startswith("| [")]) == 31
    assert "not a systematic review" in text
    assert "No empirical conclusion" in text


def test_drl_032_is_blocked_without_rewriting_approved_questions() -> None:
    register = yaml.safe_load(
        (ROOT / "requirements" / "issue-register.yaml").read_text(encoding="utf-8")
    )
    issue = next(item for item in register["issues"] if item["id"] == "DRL-032")
    assert issue["status"] == "BLOCKED"
    assert issue["director_decisions"] == ["RES-017", "DIR-008"]
    assert REVIEW.relative_to(ROOT).as_posix() in issue["evidence"]

    plan = (
        ROOT / "docs" / "10-research" / "COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md"
    ).read_text(encoding="utf-8")
    assert "When should a bounded intelligent system stop acquiring" in plan
    assert "Do payoff-equivalent descriptions create different human" in plan
    assert "When does market coupling aggregate independent" in plan


def test_decision_and_reference_controls_record_revalidation_gate() -> None:
    memo = (ROOT / "DIRECTORS_MEMO.md").read_text(encoding="utf-8")
    references = (
        ROOT / "docs" / "references" / "TECHNICAL_REFERENCE_REGISTER.md"
    ).read_text(encoding="utf-8")
    assert "| DIR-008 | CFI research |" in memo
    assert "DRL-032 blocked" in memo
    assert "Computational Finance of Intelligence novelty boundary" in references
    assert "2026-09-05 and G1" in references
    assert "Contribution-collapsing control for the original Paper I hypothesis" in references
