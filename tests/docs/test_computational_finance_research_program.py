"""Guards for the Computational Finance of Intelligence program (DRL-031)."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PLAN = (
    ROOT
    / "docs"
    / "10-research"
    / "COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md"
)


def test_program_has_one_bridge_and_three_paper_tracks() -> None:
    assert PLAN.is_file()
    text = PLAN.read_text(encoding="utf-8")
    assert "document_id: DRL-RES-005" in text
    assert "Shared bridge — Belief Diffusion" in text
    for title in (
        "The Option Value of Thinking",
        "Language, Arbitrage, and the Price of Belief",
        "A Market of Minds",
    ):
        assert title in text
    assert "not counted as a required fourth paper" in text


def test_program_bounds_agent_research_authority() -> None:
    text = PLAN.read_text(encoding="utf-8")
    prose = " ".join(text.split())
    for required in (
        "Agents are bounded research operators",
        "Agents require a gate to",
        "Agents must never",
        "G2 Data",
        "G4 Confirmatory",
        "G6 Release",
        "No experiment result is claimed",
    ):
        assert required in prose
    assert "infer consent from public availability" in text
    assert "use an LLM judge as the sole authority" in text


def test_program_names_first_agent_packet_and_issue_registration() -> None:
    text = PLAN.read_text(encoding="utf-8")
    assert "The next agent should execute **CFI-002 only**" in text
    assert "CFI-003" in text
    assert "CFI-901" in text

    register = yaml.safe_load(
        (ROOT / "requirements" / "issue-register.yaml").read_text(encoding="utf-8")
    )
    issue = next(item for item in register["issues"] if item["id"] == "DRL-031")
    assert issue["mission"] == 15
    assert issue["status"] == "IN_PROGRESS"
    assert issue["dependencies"] == ["DRL-028"]

    memo = (ROOT / "DIRECTORS_MEMO.md").read_text(encoding="utf-8")
    assert "RES-017" in memo
