"""DRL-018: one linked evidence-to-scenario workflow trace."""

from __future__ import annotations

from decimal import Decimal

from atticus_control_plane import build_local_runtime
from drl_protocol import RunState, TaskRequest


def test_evidence_to_scenario_links_atlas_fedlens_balancelab_report_evaluation() -> None:
    request = TaskRequest(
        "drl-018-integrated",
        "Using inflation and Federal Reserve evidence, run a bear-steepener bank scenario",
        public_session=True,
        as_of="2026-07-24",
    )
    result = build_local_runtime().run(request)

    assert result.state is RunState.COMPLETED
    assert result.evaluation["passed"] is True
    linked = result.artifacts["linked_workflow"]
    assert linked["task_id"] == request.task_id
    assert linked["maturity"] == "prototype"
    assert linked["workflow_digest"].startswith("sha256:")
    assert set(linked["links"]) == {"atlas", "fedlens", "balancelab", "report", "evaluation"}
    assert all(link["present"] for link in linked["links"].values())

    assert "atlas_snapshot" in result.artifacts
    assert "fed_language_comparison" in result.artifacts
    assert "fed_cited_comparison" in result.artifacts
    assert result.artifacts["calculation_artifact"]["scenario_name"] == "bear-steepener"
    assert result.artifacts["calculation_artifact"]["digest"].startswith("sha256:")
    assert result.artifacts["scenario_result"]["annual_nii_change"] == Decimal("15.81")
    calc_digest = result.artifacts["calculation_artifact"]["digest"]
    assert linked["links"]["balancelab"]["digest"] == calc_digest
    assert linked["links"]["report"]["digest"].startswith("sha256:")
    assert linked["links"]["evaluation"]["digest"].startswith("sha256:")

    assert any(event.event_type == "workflow_linked" for event in result.trace)
    assert any(
        event.event_type == "task_completed" and event.attributes.get("workflow_digest")
        for event in result.trace
    )
    assert all(item.citation for item in result.evidence)
