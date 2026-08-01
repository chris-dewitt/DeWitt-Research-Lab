from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from atlas_service import AtlasService
from atticus_control_plane import ApprovalService, PolicyEngine, build_local_runtime
from atticus_control_plane.orchestrator import AtticusOrchestrator
from atticus_control_plane.registry import ToolOutput, ToolRegistry
from balancelab_ai import BalanceSheet, RateScenario, ScenarioEngine
from drl_protocol import (
    RiskTier,
    RunState,
    TaskRequest,
    ToolCall,
    ToolDefinition,
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
