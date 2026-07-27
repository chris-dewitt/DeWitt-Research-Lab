"""Contract tests for Atticus run-state transitions and orchestration legality."""

from __future__ import annotations

import pytest
from atticus_control_plane import ApprovalService, PolicyEngine, build_local_runtime
from atticus_control_plane.orchestrator import AtticusOrchestrator
from atticus_control_plane.registry import ToolOutput, ToolRegistry
from drl_protocol import (
    LEGAL_TRANSITIONS,
    TERMINAL_STATES,
    IllegalStateTransition,
    RiskTier,
    RunState,
    TaskRequest,
    ToolCall,
    ToolDefinition,
    assert_transition,
    can_transition,
    is_terminal,
    legal_targets,
)
from evalforge_service import EvalForge


def test_terminal_states_have_no_outgoing_edges() -> None:
    for state in TERMINAL_STATES:
        assert legal_targets(state) == frozenset()
        assert is_terminal(state)


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (RunState.RECEIVED, RunState.PLANNING),
        (RunState.RECEIVED, RunState.CANCELLED),
        (RunState.PLANNING, RunState.EXECUTING),
        (RunState.PLANNING, RunState.AWAITING_APPROVAL),
        (RunState.PLANNING, RunState.DENIED),
        (RunState.PLANNING, RunState.CANCELLED),
        (RunState.AWAITING_APPROVAL, RunState.EXECUTING),
        (RunState.AWAITING_APPROVAL, RunState.CANCELLED),
        (RunState.EXECUTING, RunState.EVALUATING),
        (RunState.EXECUTING, RunState.CANCELLED),
        (RunState.EVALUATING, RunState.COMPLETED),
        (RunState.EVALUATING, RunState.DEGRADED),
        (RunState.EVALUATING, RunState.FAILED),
    ],
)
def test_legal_transitions_are_accepted(current: RunState, target: RunState) -> None:
    assert can_transition(current, target)
    assert assert_transition(current, target) is target


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (RunState.COMPLETED, RunState.PLANNING),
        (RunState.DENIED, RunState.EXECUTING),
        (RunState.CANCELLED, RunState.EXECUTING),
        (RunState.FAILED, RunState.EVALUATING),
        (RunState.RECEIVED, RunState.COMPLETED),
        (RunState.PLANNING, RunState.COMPLETED),
        (RunState.EXECUTING, RunState.COMPLETED),
        (RunState.EVALUATING, RunState.CANCELLED),
    ],
)
def test_illegal_transitions_are_rejected(current: RunState, target: RunState) -> None:
    assert not can_transition(current, target)
    with pytest.raises(IllegalStateTransition, match="Illegal Atticus state transition"):
        assert_transition(current, target)


def test_legal_transition_table_covers_every_nonterminal_state() -> None:
    nonterminal = set(RunState) - set(TERMINAL_STATES)
    assert set(LEGAL_TRANSITIONS) == nonterminal
    for current, targets in LEGAL_TRANSITIONS.items():
        assert targets
        assert current not in targets


def test_empty_objective_is_rejected() -> None:
    with pytest.raises(ValueError, match="objective"):
        build_local_runtime().run(TaskRequest("bad-empty", "   "))


def test_empty_task_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="Task ID"):
        build_local_runtime().run(TaskRequest("  ", "Give me a laboratory guide"))


def test_empty_session_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="Session ID"):
        build_local_runtime().run(
            TaskRequest("bad-session", "Give me a laboratory guide", session_id="")
        )


def test_unknown_tool_is_denied_without_execution() -> None:
    class UnknownToolPlanner:
        def plan(self, request: TaskRequest) -> list[ToolCall]:
            return [
                ToolCall(
                    f"{request.task_id}-unknown",
                    "not.a.real.tool",
                    {},
                    RiskTier.READ_COMPUTE,
                )
            ]

    orchestrator = AtticusOrchestrator(
        registry=ToolRegistry(),
        policy=PolicyEngine(),
        approvals=ApprovalService(),
        evaluator=EvalForge(),
        planner=UnknownToolPlanner(),
    )
    result = orchestrator.run(TaskRequest("deny-unknown", "Use an unknown tool"))

    assert result.state is RunState.DENIED
    assert is_terminal(result.state)
    assert any(event.event_type == "policy_decision" for event in result.trace)
    assert "not registered" in result.summary.lower()
    assert result.evidence == []


def test_cancellation_before_planning_is_terminal() -> None:
    result = build_local_runtime().run(
        TaskRequest("cancel-early", "Use inflation evidence"),
        cancel_check=lambda: True,
    )

    assert result.state is RunState.CANCELLED
    assert is_terminal(result.state)
    assert any(event.event_type == "task_cancelled" for event in result.trace)
    assert result.evidence == []


def test_cancellation_after_planning_before_dispatch() -> None:
    checks = iter([False, True])

    def cancel_check() -> bool:
        return next(checks)

    result = build_local_runtime().run(
        TaskRequest("cancel-planned", "Use inflation evidence"),
        cancel_check=cancel_check,
    )

    assert result.state is RunState.CANCELLED
    assert any(event.event_type == "plan_created" for event in result.trace)
    assert any(event.event_type == "task_cancelled" for event in result.trace)
    assert not any(event.event_type == "tool_started" for event in result.trace)


def test_cancellation_while_awaiting_approval() -> None:
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
            "Simulated reversible tool for cancellation test",
            RiskTier.REVERSIBLE_CHANGE,
            False,
        ),
        lambda _: ToolOutput(message="must not execute"),
    )
    checks = iter([False, False, True])

    def cancel_check() -> bool:
        return next(checks)

    result = AtticusOrchestrator(
        registry=registry,
        policy=PolicyEngine(),
        approvals=ApprovalService(),
        evaluator=EvalForge(),
        planner=ReversiblePlanner(),
    ).run(TaskRequest("cancel-approval", "Patch a file"), cancel_check=cancel_check)

    assert result.state is RunState.CANCELLED
    assert any(event.event_type == "policy_decision" for event in result.trace)
    assert any(event.event_type == "task_cancelled" for event in result.trace)
    assert not any(event.event_type == "tool_started" for event in result.trace)


def test_successful_fixture_workflow_ends_in_legal_terminal_state() -> None:
    result = build_local_runtime().run(
        TaskRequest(
            "success-terminal",
            "Use inflation and Federal Reserve evidence to run a bear-steepener bank scenario",
            public_session=True,
            as_of="2026-07-24",
        )
    )

    assert result.state is RunState.COMPLETED
    assert is_terminal(result.state)
    states = [event.state for event in result.trace]
    assert states[0] is RunState.RECEIVED
    assert RunState.PLANNING in states
    assert RunState.EXECUTING in states
    assert RunState.EVALUATING in states
    assert states[-1] is RunState.COMPLETED


def test_cancel_check_iterator_exhaustion_defaults_to_continue() -> None:
    """A cancel probe that returns False forever must not invent cancellation."""

    def never_cancel() -> bool:
        return False

    result = build_local_runtime().run(
        TaskRequest(
            "no-cancel",
            "Use inflation and Federal Reserve evidence to run a bear-steepener bank scenario",
            public_session=True,
            as_of="2026-07-24",
        ),
        cancel_check=never_cancel,
    )
    assert result.state is RunState.COMPLETED


def test_failed_tool_path_without_evidence_is_failed_terminal() -> None:
    class FailingPlanner:
        def plan(self, request: TaskRequest) -> list[ToolCall]:
            return [
                ToolCall(
                    f"{request.task_id}-fail",
                    "always.fail",
                    {},
                    RiskTier.READ_COMPUTE,
                )
            ]

    registry = ToolRegistry()

    def boom(_: dict[str, object]) -> ToolOutput:
        raise ValueError("forced failure")

    registry.register(
        ToolDefinition(
            "always.fail",
            "Always fails",
            RiskTier.READ_COMPUTE,
            True,
        ),
        boom,
    )
    result = AtticusOrchestrator(
        registry=registry,
        policy=PolicyEngine(),
        approvals=ApprovalService(),
        evaluator=EvalForge(),
        planner=FailingPlanner(),
    ).run(TaskRequest("fail-path", "Force a failure"))

    assert result.state is RunState.FAILED
    assert is_terminal(result.state)
    assert any(event.event_type == "tool_failed" for event in result.trace)
