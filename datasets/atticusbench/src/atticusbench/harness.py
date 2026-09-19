"""Execute one AtticusBench case against one system under test.

Execution goes through the real Atticus orchestrator, policy engine, and
approval service. The harness supplies only the environment and the planner, so
a case measures the shipped authorization path rather than a copy of it.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from atticus_control_plane.approvals import ApprovalService
from atticus_control_plane.orchestrator import AtticusOrchestrator
from atticus_control_plane.policy import PolicyEngine
from drl_protocol import ApprovalGrant, TaskRequest, ToolCall
from evalforge_service import EvalForge
from evalforge_service.observed import ObservedEvent, ObservedRun

from .environment import EffectLedger, build_registry
from .model import Case, Fixture
from .systems import System, tier_for

#: Trace attributes that are safe to persist. Tool arguments, evidence content,
#: and trace messages are deliberately absent: AGENTS.md forbids logging prompt
#: or tool content by default, and a benchmark record needs ids and scores only.
RETAINED_ATTRIBUTES: frozenset[str] = frozenset(
    {
        "tool",
        "tools",
        "allowed",
        "requires_approval",
        "gating_effect",
        "call_digest",
        "evidence_ids",
        "link_keys",
        "workflow_digest",
        "evaluation_passed",
    }
)


@dataclass(frozen=True, slots=True)
class CaseRun:
    """Content-minimized observation of one case/system execution."""

    case_id: str
    system_id: str
    family: str
    split: str
    mode: str
    critical_suite: bool
    case_digest: str
    fixture_id: str
    planned_tools: tuple[str, ...]
    terminal_state: str
    observed: ObservedRun
    ledger: dict[str, Any]
    evaluation: dict[str, Any]
    evidence_ids: tuple[str, ...]
    artifact_keys: tuple[str, ...]
    artifact_digests: tuple[str, ...]
    latency_ms: float

    @property
    def tools_started(self) -> tuple[str, ...]:
        return tuple(
            str(event.attributes.get("tool", ""))
            for event in self.observed.events
            if event.event_type == "tool_started"
        )

    @property
    def tools_completed(self) -> tuple[str, ...]:
        return tuple(
            str(event.attributes.get("tool", ""))
            for event in self.observed.events
            if event.event_type == "tool_completed"
        )

    @property
    def tools_failed(self) -> tuple[str, ...]:
        return tuple(
            str(event.attributes.get("tool", ""))
            for event in self.observed.events
            if event.event_type == "tool_failed"
        )


def _retained(attributes: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in attributes.items() if key in RETAINED_ATTRIBUTES}


def _observed_events(result: Any) -> tuple[ObservedEvent, ...]:
    return tuple(
        ObservedEvent(
            event_type=event.event_type,
            state=str(getattr(event.state, "value", event.state)),
            # Messages can echo fixture document text, including injected
            # instructions. They are not retained.
            message="",
            attributes=_retained(dict(event.attributes)),
        )
        for event in result.trace
    )


def _grants(
    case: Case,
    fixture: Fixture,
    *,
    approvals: ApprovalService,
    session_id: str,
    actor_id: str,
    now: datetime,
) -> list[ApprovalGrant]:
    """Issue the approval grants the case declares.

    A grant binds to the exact call digest, so a case can approve one set of
    arguments and execute another to test digest binding, or issue a grant in
    the past to test expiry.
    """

    by_step = {step.step_id: step for step in case.reference_plan}
    grants: list[ApprovalGrant] = []
    for approval in case.approvals:
        step = by_step[approval.step_id]
        arguments = (
            dict(approval.granted_arguments)
            if approval.granted_arguments is not None
            else dict(step.arguments)
        )
        approved_call = ToolCall(
            f"{case.case_id}-{step.step_id}",
            step.tool,
            arguments,
            tier_for(fixture, step.tool, step.declared_risk_tier),
        )
        grants.append(
            approvals.grant(
                approved_call,
                session_id=session_id,
                actor_id=actor_id,
                ttl_seconds=approval.ttl_seconds,
                now=now + timedelta(seconds=approval.issued_offset_seconds),
            )
        )
    return grants


def run_case(case: Case, fixture: Fixture, system: System) -> CaseRun:
    """Run one case against one system and return a content-minimized record."""

    registry, ledger = build_registry(fixture, offered_tools=case.available_tools)
    planner = system.build_planner(case, fixture)
    orchestrator = AtticusOrchestrator(
        registry=registry,
        policy=PolicyEngine(),
        approvals=ApprovalService(),
        evaluator=EvalForge(),
        planner=planner,
    )
    session_id = f"atticusbench-{case.case_id}"
    actor_id = f"atticusbench-{system.system_id}"
    request = TaskRequest(
        task_id=case.case_id,
        objective=case.request,
        session_id=session_id,
        actor_id=actor_id,
        public_session=case.public_session,
        as_of=fixture.as_of,
        metadata={
            "benchmark": "atticusbench",
            "split": case.split,
            "family": case.family,
            "system_id": system.system_id,
            "policy_version": case.policy_version,
        },
    )
    grants = (
        _grants(
            case,
            fixture,
            approvals=ApprovalService(),
            session_id=session_id,
            actor_id=actor_id,
            now=datetime.now(UTC),
        )
        if system.uses_declared_approvals
        else []
    )

    started = time.perf_counter()
    result = orchestrator.run(request, grants=grants)
    latency_ms = (time.perf_counter() - started) * 1000.0
    # What the planner proposed, read back rather than recomputed: recomputing
    # would be a second inference for a model system.
    planned = list(planner.last_plan)

    terminal_state = str(getattr(result.state, "value", result.state))
    artifacts = dict(result.artifacts or {})
    return CaseRun(
        case_id=case.case_id,
        system_id=system.system_id,
        family=case.family,
        split=case.split,
        mode=case.mode,
        critical_suite=case.critical_suite,
        case_digest=case.content_digest or "",
        fixture_id=fixture.fixture_id,
        planned_tools=tuple(call.tool_name for call in planned),
        terminal_state=terminal_state,
        observed=ObservedRun(
            case_id=case.case_id,
            slice_id=case.family,
            terminal_state=terminal_state,
            events=_observed_events(result),
            evidence_count=len(result.evidence),
            summary="",
            metadata={
                "system_id": system.system_id,
                "injection_markers_served": len(ledger.injection_markers),
            },
        ),
        ledger=_ledger_summary(ledger),
        evaluation=dict(result.evaluation or {}),
        evidence_ids=tuple(item.evidence_id for item in result.evidence),
        artifact_keys=tuple(sorted(artifacts)),
        artifact_digests=tuple(sorted(_artifact_digests(artifacts))),
        latency_ms=latency_ms,
    )


def _ledger_summary(ledger: EffectLedger) -> dict[str, Any]:
    return ledger.as_dict()


def _artifact_digests(artifacts: dict[str, Any]) -> list[str]:
    """Collect digests produced by deterministic calculation artifacts."""

    digests: list[str] = []
    for value in artifacts.values():
        if isinstance(value, dict):
            digest = value.get("digest")
            if isinstance(digest, str) and digest:
                digests.append(digest)
    return digests
