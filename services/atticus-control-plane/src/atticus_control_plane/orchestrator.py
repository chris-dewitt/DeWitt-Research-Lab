"""Bounded Atticus orchestration state machine."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from datetime import UTC, datetime
from typing import Any

from drl_ai_core import canonical_digest, redact_text
from drl_protocol import (
    ApprovalGrant,
    EvidenceItem,
    RunState,
    TaskRequest,
    TaskResult,
    TraceEvent,
    assert_transition,
    is_terminal,
)
from evalforge_service import EvalForge

from .approvals import ApprovalService
from .planner import FixturePlanner, Planner
from .policy import PolicyEngine
from .registry import ToolRegistry

CancelCheck = Callable[[], bool]
ProgressFn = Callable[[str, str], None]


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
    def _validate_request(request: TaskRequest) -> None:
        if not request.task_id.strip():
            raise ValueError("Task ID cannot be empty")
        if not request.objective.strip():
            raise ValueError("Task objective cannot be empty")
        if not request.session_id.strip():
            raise ValueError("Session ID cannot be empty")

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
        return assert_transition(current, target)

    def _cancelled_result(
        self,
        request: TaskRequest,
        *,
        state: RunState,
        trace: list[TraceEvent],
        evidence: list[EvidenceItem],
        artifacts: dict[str, object],
        message: str,
    ) -> TaskResult:
        if is_terminal(state) and state is not RunState.CANCELLED:
            raise RuntimeError(f"Cannot cancel from terminal state {state.value}")
        if state is not RunState.CANCELLED:
            state = self._transition(state, RunState.CANCELLED)
        trace.append(
            self._event(
                request,
                state,
                "task_cancelled",
                message,
                sequence=len(trace) + 1,
            )
        )
        return TaskResult(
            request.task_id,
            state,
            message,
            evidence,
            trace,
            artifacts,
            limitations=["Cancellation stopped the workflow before further side effects."],
        )

    def run(
        self,
        request: TaskRequest,
        *,
        grants: Iterable[ApprovalGrant] = (),
        cancel_check: CancelCheck | None = None,
        progress: ProgressFn | None = None,
    ) -> TaskResult:
        self._validate_request(request)
        should_cancel = cancel_check or (lambda: False)

        def emit(event: str, detail: str = "") -> None:
            # Ids and tool names only. Never the objective or tool payloads.
            if progress is not None:
                progress(event, detail)

        trace: list[TraceEvent] = []
        evidence: list[EvidenceItem] = []
        artifacts: dict[str, object] = {}
        grant_by_digest = {grant.call_digest: grant for grant in grants}
        state = RunState.RECEIVED
        trace.append(self._event(request, state, "task_received", "Task accepted.", sequence=1))

        if should_cancel():
            emit("finished", "cancelled")
            return self._cancelled_result(
                request,
                state=state,
                trace=trace,
                evidence=evidence,
                artifacts=artifacts,
                message="Task cancelled before planning.",
            )

        state = self._transition(state, RunState.PLANNING)
        emit("planning", request.task_id)
        plan = self.planner.plan(request)
        emit("plan_created", f"{len(plan)}-steps")
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

        if should_cancel():
            emit("finished", "cancelled")
            return self._cancelled_result(
                request,
                state=state,
                trace=trace,
                evidence=evidence,
                artifacts=artifacts,
                message="Task cancelled after planning and before tool dispatch.",
            )

        for index, call in enumerate(plan, start=1):
            decision = self.policy.decide(
                request=request,
                call=call,
                definition=self.registry.definition(call.tool_name),
            )
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
                emit("finished", state.value)
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
                    if should_cancel():
                        emit("finished", "cancelled")
                        return self._cancelled_result(
                            request,
                            state=state,
                            trace=trace,
                            evidence=evidence,
                            artifacts=artifacts,
                            message=(
                                f"Task cancelled while awaiting approval for {call.tool_name}."
                            ),
                        )
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
                    emit("finished", state.value)
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
            if should_cancel():
                emit("finished", "cancelled")
                return self._cancelled_result(
                    request,
                    state=state,
                    trace=trace,
                    evidence=evidence,
                    artifacts=artifacts,
                    message=f"Task cancelled before invoking {call.tool_name}.",
                )
            emit("tool_started", call.tool_name)
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
                emit("tool_failed", call.tool_name)
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
            emit("tool_completed", call.tool_name)
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
            emit("finished", state.value)
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
        emit("evaluating", request.task_id)
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
        evaluation = report.to_dict()
        summary = self._synthesize(evidence, failures)
        linked = self._link_workflow(
            request=request,
            evidence=evidence,
            artifacts=artifacts,
            summary=summary,
            evaluation=evaluation,
        )
        artifacts["linked_workflow"] = linked
        link_map = linked["links"]
        trace.append(
            self._event(
                request,
                RunState.EVALUATING,
                "workflow_linked",
                "Linked Atlas, FedLens, BalanceLab, report, and evaluation digests.",
                sequence=len(trace) + 1,
                link_keys=sorted(link_map.keys()),
                workflow_digest=linked["workflow_digest"],
            )
        )
        state = self._transition(state, intended_terminal)
        if not is_terminal(state):
            raise RuntimeError(f"Expected terminal state, got {state.value}")
        trace.append(
            self._event(
                request,
                state,
                "task_completed",
                f"Workflow finished with EvalForge score {report.score:.3f}.",
                sequence=len(trace) + 1,
                evaluation_passed=report.passed,
                workflow_digest=linked["workflow_digest"],
            )
        )

        limitations = self._limitations_for(evidence)
        limitations.extend(failures)
        emit("finished", state.value)
        return TaskResult(
            request.task_id,
            state,
            summary,
            evidence,
            trace,
            artifacts,
            evaluation,
            limitations,
        )

    @staticmethod
    def _limitations_for(evidence: list[EvidenceItem]) -> list[str]:
        live = any(
            item.citation and not item.citation.startswith("fixture://")
            for item in evidence
            if item.evidence_id.startswith(("atlas-", "fedlens-"))
        )
        if live:
            return [
                "Atlas/FedLens used the local official-feed store (ADR-0010, opt-in).",
                "BalanceLab still uses a simplified educational bank, not a live institution.",
                "DIR-004 (Core/Edge selection) is still open; a local run is not a selection.",
                "Linked workflow is prototype maturity; signed replay is DRL-019.",
            ]
        return [
            "Macro, market, and Fed inputs are synthetic fixtures for local development.",
            "BalanceLab uses a simplified educational repricing model, not production bank data.",
            "DIR-004 (Core/Edge selection) is still open; a local run is not a selection.",
            "Linked workflow is prototype maturity; signed replay is DRL-019.",
        ]

    @staticmethod
    def _link_workflow(
        *,
        request: TaskRequest,
        evidence: list[EvidenceItem],
        artifacts: dict[str, object],
        summary: str,
        evaluation: dict[str, object],
    ) -> dict[str, Any]:
        """Build one inspectable link graph for the five DRL-018 artifacts."""

        atlas_ids = [item.evidence_id for item in evidence if item.evidence_id.startswith("atlas-")]
        fed_ids = [item.evidence_id for item in evidence if item.evidence_id.startswith("fedlens-")]
        balance_ids = [
            item.evidence_id for item in evidence if item.evidence_id.startswith("balancelab-")
        ]
        calculation = artifacts.get("calculation_artifact")
        calculation_digest = None
        if isinstance(calculation, dict):
            calculation_digest = calculation.get("digest")
        report_payload = {"task_id": request.task_id, "summary": summary}
        report_digest = f"sha256:{canonical_digest(report_payload)}"
        evaluation_digest = f"sha256:{canonical_digest(evaluation)}"
        links: dict[str, dict[str, object]] = {
            "atlas": {
                "artifact_key": "atlas_snapshot",
                "evidence_ids": atlas_ids,
                "present": "atlas_snapshot" in artifacts and bool(atlas_ids),
            },
            "fedlens": {
                "artifact_key": "fed_cited_comparison",
                "evidence_ids": fed_ids,
                "present": "fed_language_comparison" in artifacts and bool(fed_ids),
            },
            "balancelab": {
                "artifact_key": "calculation_artifact",
                "evidence_ids": balance_ids,
                "digest": calculation_digest,
                "present": isinstance(calculation, dict) and bool(balance_ids),
            },
            "report": {
                "digest": report_digest,
                "present": bool(summary.strip()),
            },
            "evaluation": {
                "digest": evaluation_digest,
                "passed": bool(evaluation.get("passed")),
                "present": "passed" in evaluation,
            },
        }
        workflow_digest = f"sha256:{canonical_digest({'task_id': request.task_id, 'links': links})}"
        return {
            "task_id": request.task_id,
            "maturity": "prototype",
            "workflow_digest": workflow_digest,
            "links": links,
        }

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
