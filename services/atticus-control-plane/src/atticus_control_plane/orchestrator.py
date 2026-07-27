"""Bounded Atticus orchestration state machine."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime

from drl_ai_core import redact_text
from drl_protocol import (
    ApprovalGrant,
    EvidenceItem,
    RunState,
    TaskRequest,
    TaskResult,
    TraceEvent,
)
from evalforge_service import EvalForge

from .approvals import ApprovalService
from .planner import FixturePlanner, Planner
from .policy import PolicyEngine
from .registry import ToolRegistry

_LEGAL_TRANSITIONS: dict[RunState, frozenset[RunState]] = {
    RunState.RECEIVED: frozenset({RunState.PLANNING, RunState.CANCELLED}),
    RunState.PLANNING: frozenset(
        {RunState.EXECUTING, RunState.AWAITING_APPROVAL, RunState.DENIED, RunState.FAILED}
    ),
    RunState.AWAITING_APPROVAL: frozenset(
        {RunState.EXECUTING, RunState.CANCELLED, RunState.DENIED}
    ),
    RunState.EXECUTING: frozenset(
        {RunState.EVALUATING, RunState.DEGRADED, RunState.DENIED, RunState.FAILED}
    ),
    RunState.EVALUATING: frozenset({RunState.COMPLETED, RunState.DEGRADED, RunState.FAILED}),
}


class AtticusOrchestrator:
    """Plan, authorize, execute, evaluate, and report bounded workflows."""

    def __init__(
        self,
        *,
        registry: ToolRegistry,
        policy: PolicyEngine,
        approvals: ApprovalService,
        evaluator: EvalForge,
        planner: Planner | None = None,
    ) -> None:
        self.registry = registry
        self.policy = policy
        self.approvals = approvals
        self.evaluator = evaluator
        self.planner = planner or FixturePlanner()

    @staticmethod
    def _event(
        request: TaskRequest,
        state: RunState,
        event_type: str,
        message: str,
        *,
        sequence: int,
        **attributes: object,
    ) -> TraceEvent:
        return TraceEvent(
            event_id=f"{request.task_id}-event-{sequence:03d}",
            task_id=request.task_id,
            state=state,
            event_type=event_type,
            message=redact_text(message),
            attributes=dict(attributes),
        )

    @staticmethod
    def _transition(current: RunState, target: RunState) -> RunState:
        if target not in _LEGAL_TRANSITIONS.get(current, frozenset()):
            raise RuntimeError(
                f"Illegal Atticus state transition: {current.value} -> {target.value}"
            )
        return target

    def run(
        self,
        request: TaskRequest,
        *,
        grants: Iterable[ApprovalGrant] = (),
    ) -> TaskResult:
        if not request.objective.strip():
            raise ValueError("Task objective cannot be empty")

        trace: list[TraceEvent] = []
        evidence: list[EvidenceItem] = []
        artifacts: dict[str, object] = {}
        grant_by_digest = {grant.call_digest: grant for grant in grants}
        state = RunState.RECEIVED
        trace.append(self._event(request, state, "task_received", "Task accepted.", sequence=1))

        state = self._transition(state, RunState.PLANNING)
        plan = self.planner.plan(request)
        trace.append(
            self._event(
                request,
                state,
                "plan_created",
                f"Created bounded plan with {len(plan)} step(s).",
                sequence=2,
                tools=[call.tool_name for call in plan],
            )
        )

        decisions = []
        for index, call in enumerate(plan, start=1):
            decision = self.policy.decide(
                request=request,
                call=call,
                definition=self.registry.definition(call.tool_name),
            )
            decisions.append(decision)
            trace.append(
                self._event(
                    request,
                    state,
                    "policy_decision",
                    decision.reason,
                    sequence=2 + index,
                    tool=call.tool_name,
                    allowed=decision.allowed,
                    requires_approval=decision.requires_approval,
                    call_digest=decision.call_digest,
                )
            )
            if not decision.allowed:
                state = self._transition(state, RunState.DENIED)
                return TaskResult(
                    request.task_id,
                    state,
                    f"Atticus denied {call.tool_name}: {decision.reason}",
                    evidence,
                    trace,
                    artifacts,
                    limitations=["No denied tool was executed."],
                )
            if decision.requires_approval:
                grant = grant_by_digest.get(decision.call_digest)
                if not self.approvals.verify(
                    grant,
                    call,
                    session_id=request.session_id,
                    now=datetime.now(UTC),
                ):
                    state = self._transition(state, RunState.AWAITING_APPROVAL)
                    trace.append(
                        self._event(
                            request,
                            state,
                            "approval_required",
                            f"Approval required for {call.tool_name}.",
                            sequence=len(trace) + 1,
                            call_digest=decision.call_digest,
                        )
                    )
                    return TaskResult(
                        request.task_id,
                        state,
                        f"Approval required before {call.tool_name} can run.",
                        evidence,
                        trace,
                        artifacts,
                        limitations=["Execution paused; no unapproved action was performed."],
                    )

        state = self._transition(state, RunState.EXECUTING)
        failures: list[str] = []
        for call in plan:
            trace.append(
                self._event(
                    request,
                    state,
                    "tool_started",
                    f"Invoking {call.tool_name}.",
                    sequence=len(trace) + 1,
                    tool=call.tool_name,
                )
            )
            try:
                output = self.registry.invoke(call.tool_name, call.arguments)
            except (KeyError, LookupError, TypeError, ValueError) as exc:
                failures.append(f"{call.tool_name}: {exc}")
                trace.append(
                    self._event(
                        request,
                        state,
                        "tool_failed",
                        f"{call.tool_name} failed: {exc}",
                        sequence=len(trace) + 1,
                        tool=call.tool_name,
                    )
                )
                continue
            evidence.extend(output.evidence)
            artifacts.update(output.artifacts)
            trace.append(
                self._event(
                    request,
                    state,
                    "tool_completed",
                    output.message or f"{call.tool_name} completed.",
                    sequence=len(trace) + 1,
                    tool=call.tool_name,
                    evidence_ids=[item.evidence_id for item in output.evidence],
                )
            )

        if failures and not evidence:
            state = self._transition(state, RunState.FAILED)
            return TaskResult(
                request.task_id,
                state,
                "The workflow failed before producing supported evidence.",
                evidence,
                trace,
                artifacts,
                limitations=failures,
            )

        state = self._transition(state, RunState.EVALUATING)
        trace.append(
            self._event(
                request,
                state,
                "evaluation_started",
                "Submitting observable trace and evidence to EvalForge.",
                sequence=len(trace) + 1,
            )
        )

        intended_terminal = RunState.DEGRADED if failures else RunState.COMPLETED
        report = self.evaluator.evaluate(
            trace=trace,
            evidence=evidence,
            terminal_state=intended_terminal.value,
        )
        state = self._transition(state, intended_terminal)
        trace.append(
            self._event(
                request,
                state,
                "task_completed",
                f"Workflow finished with EvalForge score {report.score:.3f}.",
                sequence=len(trace) + 1,
                evaluation_passed=report.passed,
            )
        )

        summary = self._synthesize(evidence, failures)
        limitations = [
            "Macro, market, and Fed inputs are synthetic fixtures for local development.",
            "BalanceLab uses a simplified educational repricing model, not production bank data.",
            "The deterministic planner stands in for Atticus Core until the model bake-off.",
        ]
        limitations.extend(failures)
        return TaskResult(
            request.task_id,
            state,
            summary,
            evidence,
            trace,
            artifacts,
            report.to_dict(),
            limitations,
        )

    @staticmethod
    def _synthesize(evidence: list[EvidenceItem], failures: list[str]) -> str:
        by_id = {item.evidence_id: item for item in evidence}
        cpi = next((item.content for key, item in by_id.items() if "CPI_YOY" in key), None)
        two_year = next((item.content for key, item in by_id.items() if "UST_2Y" in key), None)
        ten_year = next((item.content for key, item in by_id.items() if "UST_10Y" in key), None)
        fed = next(
            (item.content for key, item in by_id.items() if key.startswith("fedlens-")),
            None,
        )
        balance = next(
            (item.content for key, item in by_id.items() if key.startswith("balancelab-")),
            None,
        )
        if cpi and two_year and ten_year and fed and balance:
            degraded = " One or more optional steps failed." if failures else ""
            return (
                f"Fixture evidence shows CPI at {cpi}, the two-year yield at {two_year}, "
                f"and the ten-year yield at {ten_year}. FedLens analyzed the latest "
                f"synthetic communication: “{fed}” BalanceLab then applied a +25/+75 "
                f"basis-point bear-steepener to the synthetic regional bank. {balance}{degraded}"
            )
        if evidence:
            return "Atticus completed the bounded workflow and returned cited evidence."
        return "Atticus completed without publishable evidence."
