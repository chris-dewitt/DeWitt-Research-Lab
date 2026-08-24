from __future__ import annotations

import json
from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from atlas_service import AtlasService
from atticus_control_plane import ApprovalService, PolicyEngine, build_local_runtime
from atticus_control_plane.cli import main, render_human_report
from atticus_control_plane.orchestrator import (
    AtticusOrchestrator,
    PUBLIC_REPLAY_SITE_URL,
    format_quantity,
)
from atticus_control_plane.registry import ToolOutput, ToolRegistry
from atticus_control_plane.run_record import FORBIDDEN_RECORD_KEYS, write_run_record
from balancelab_ai import BalanceSheet, RateScenario, ScenarioEngine
from drl_protocol import (
    EvidenceItem,
    RiskTier,
    RunState,
    TaskRequest,
    TaskResult,
    ToolCall,
    ToolDefinition,
    TraceEvent,
)
from evalforge_service import EvalForge


def test_integrated_atticus_workflow_completes_with_evidence() -> None:
    request = TaskRequest(
        "test-integrated",
        "Use inflation and Federal Reserve evidence to run a bear-steepener bank scenario",
        public_session=True,
        as_of="2026-07-24",
    )

    result = build_local_runtime().run(request)

    assert result.state is RunState.COMPLETED
    assert len(result.evidence) == 5
    assert result.evaluation["passed"] is True
    assert result.evaluation["score"] == 1.0
    assert result.artifacts["scenario_result"]["annual_nii_change"] == Decimal("15.81")
    assert result.artifacts["calculation_artifact"]["scenario_name"] == "bear-steepener"
    assert "linked_workflow" in result.artifacts
    assert all(item.citation for item in result.evidence)
    assert any(event.event_type == "policy_decision" for event in result.trace)
    assert any(event.event_type == "workflow_linked" for event in result.trace)
    blob = " ".join(result.limitations)
    assert "ADR-0010" not in blob
    assert "DRL-019" not in blob
    assert "DIR-004" not in blob
    assert "canned fixtures" in blob
    assert PUBLIC_REPLAY_SITE_URL in blob
    assert result.summary.startswith("Fixture evidence shows")
    assert "synthetic communication" in result.summary


def test_format_quantity_strips_trailing_zeros() -> None:
    assert format_quantity("4.1900000000 percent") == "4.19 percent"
    assert format_quantity("3.30386 percent") == "3.30386 percent"
    assert format_quantity("not-a-number") == "not-a-number"


def test_balancelab_calculation_is_hand_verifiable() -> None:
    result = ScenarioEngine().project(
        BalanceSheet(Decimal("8500"), Decimal("6200"), Decimal("900")),
        RateScenario("bear-steepener", 25, 75),
    )

    assert result.asset_income_change == Decimal("23.38")
    assert result.deposit_expense_change == Decimal("5.43")
    assert result.wholesale_expense_change == Decimal("2.14")
    assert result.annual_nii_change == Decimal("15.81")
    assert result.curve_slope_change_bps == 50


def test_atlas_enforces_publication_time() -> None:
    with pytest.raises(LookupError):
        AtlasService().latest("CPI_YOY", as_of=date(2026, 7, 1))


def test_policy_denies_private_tool_in_public_session() -> None:
    call = ToolCall("call-1", "private.read", {}, RiskTier.READ_COMPUTE)
    decision = PolicyEngine().decide(
        request=TaskRequest("task-1", "read private material", public_session=True),
        call=call,
        definition=ToolDefinition(
            "private.read",
            "Private test tool",
            RiskTier.READ_COMPUTE,
            False,
        ),
    )
    assert decision.allowed is False
    assert decision.requires_approval is False


def test_changed_arguments_invalidate_approval() -> None:
    approvals = ApprovalService()
    original = ToolCall(
        "call-2",
        "repo.patch",
        {"path": "README.md", "content": "safe"},
        RiskTier.REVERSIBLE_CHANGE,
    )
    changed = ToolCall(
        "call-2",
        "repo.patch",
        {"path": "SECURITY.md", "content": "different"},
        RiskTier.REVERSIBLE_CHANGE,
    )
    issued_at = datetime(2026, 7, 27, tzinfo=UTC)
    grant = approvals.grant(
        original,
        session_id="session-1",
        actor_id="dewitt",
        now=issued_at,
    )

    assert approvals.verify(
        grant,
        original,
        session_id="session-1",
        now=issued_at,
    )
    assert not approvals.verify(
        grant,
        changed,
        session_id="session-1",
        now=issued_at,
    )


def test_reversible_tool_pauses_without_bound_approval() -> None:
    class ReversiblePlanner:
        def plan(self, request: TaskRequest) -> list[ToolCall]:
            return [
                ToolCall(
                    f"{request.task_id}-patch",
                    "repo.patch",
                    {"path": "README.md"},
                    RiskTier.REVERSIBLE_CHANGE,
                )
            ]

    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            "repo.patch",
            "Simulated reversible tool for approval test",
            RiskTier.REVERSIBLE_CHANGE,
            False,
        ),
        lambda _: ToolOutput(message="This must not execute without approval"),
    )
    orchestrator = AtticusOrchestrator(
        registry=registry,
        policy=PolicyEngine(),
        approvals=ApprovalService(),
        evaluator=EvalForge(),
        planner=ReversiblePlanner(),
    )
    result = orchestrator.run(TaskRequest("approval-test", "Give me a laboratory guide"))

    assert result.state is RunState.AWAITING_APPROVAL
    assert "approval required" in result.summary.lower()


def test_human_report_lists_tools_and_says_evalforge_is_the_score() -> None:
    result = TaskResult(
        "atticus-demo",
        RunState.COMPLETED,
        "Atticus completed the bounded workflow and returned cited evidence.",
        evidence=[
            EvidenceItem(
                "fedlens-doc-1",
                "FedLens",
                "Latest fixture statement",
                "2026-07-24",
                "text",
                "cite",
            ),
            EvidenceItem(
                "balancelab-bear-steepener",
                "BalanceLab",
                "Synthetic regional-bank rate scenario",
                "2026-07-27",
                "nii",
                "cite",
            ),
        ],
        trace=[
            TraceEvent(
                "e1",
                "atticus-demo",
                RunState.EXECUTING,
                "tool_completed",
                "done",
                attributes={"tool": "fedlens.compare_latest"},
            ),
            TraceEvent(
                "e2",
                "atticus-demo",
                RunState.EXECUTING,
                "tool_completed",
                "done",
                attributes={"tool": "balancelab.run_scenario"},
            ),
        ],
        evaluation={"score": 1.0},
    )
    card = render_human_report(
        result,
        "model planner via qwen (ollama)",
        log_path=None,
    )
    assert "ok  fedlens.compare_latest" in card
    assert "ok  balancelab.run_scenario" in card
    assert "fedlens-doc-1" in card
    assert "EVALFORGE: 1.0" in card
    assert "not a specialist" in card
    assert "--json" in card
    assert "RUN RECORD: (not written)" in card
    assert "PUBLIC RECORDINGS: https://chris-dewitt.github.io/DeWitt-Research-Lab/" in card
    assert "www.dewitt-labs.com" in card


def test_progress_emits_tool_names_not_the_objective() -> None:
    request = TaskRequest(
        "progress-test",
        "Use inflation and Federal Reserve evidence to run a bear-steepener bank scenario",
        public_session=True,
        as_of="2026-07-24",
    )
    seen: list[tuple[str, str]] = []
    result = build_local_runtime().run(request, progress=lambda e, d: seen.append((e, d)))
    assert result.state is RunState.COMPLETED
    events = [event for event, _ in seen]
    assert events[0] == "planning"
    assert "tool_started" in events
    assert "tool_completed" in events
    assert events[-1] == "finished"
    blob = " ".join(f"{event} {detail}" for event, detail in seen)
    assert request.objective not in blob
    assert "atlas.research_snapshot" in blob


def test_run_record_persists_ids_not_content(tmp_path) -> None:
    request = TaskRequest(
        "record-test",
        "Use inflation and Federal Reserve evidence to run a bear-steepener bank scenario",
        public_session=True,
        as_of="2026-07-24",
    )
    result = build_local_runtime().run(request)
    path = write_run_record(
        result,
        planner_line="deterministic fixture planner",
        plan_source="fixture",
        root=tmp_path,
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    blob = json.dumps(payload)
    assert not (set(payload) & FORBIDDEN_RECORD_KEYS)
    assert request.objective not in blob
    assert result.summary not in blob
    for item in result.evidence:
        assert item.content not in blob
        assert item.evidence_id in payload["evidence_ids"]
    assert "atlas.research_snapshot" in payload["tools_completed"]
    assert payload["evalforge_score"] == 1.0
    assert payload["evidence_count"] == 5
    assert payload["state"] == "completed"


def test_cli_writes_progress_and_a_run_record(
    tmp_path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("ATTICUS_RUN_RECORD_DIR", str(tmp_path))
    monkeypatch.delenv("ATTICUS_MODEL", raising=False)
    monkeypatch.setattr(
        "sys.argv",
        ["atticus-demo", "--public"],
    )
    assert main() == 0
    captured = capsys.readouterr()
    assert "progress: planning atticus-demo" in captured.err
    assert "progress: tool_started atlas.research_snapshot" in captured.err
    assert "progress: finished completed" in captured.err
    assert "run-record:" in captured.err
    records = list(tmp_path.glob("atticus-demo-*.json"))
    assert len(records) == 1
    assert "RUN RECORD:" in captured.out
    assert "EVIDENCE: 5 items" in captured.out
