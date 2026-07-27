"""Deterministic release-evidence checks for local Atticus runs."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class EvaluationReport:
    passed: bool
    score: float
    checks: dict[str, bool]
    findings: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "score": self.score,
            "checks": self.checks,
            "findings": list(self.findings),
        }


class EvalForge:
    """Evaluate observable behavior without requesting hidden reasoning."""

    REQUIRED_EVENT_TYPES = frozenset({"task_received", "plan_created", "policy_decision"})

    def evaluate(
        self,
        *,
        trace: Iterable[Any],
        evidence: Iterable[Any],
        terminal_state: str,
    ) -> EvaluationReport:
        events = list(trace)
        items = list(evidence)
        event_types = {getattr(event, "event_type", None) for event in events}
        missing_events = sorted(self.REQUIRED_EVENT_TYPES - event_types)
        citations_present = bool(items) and all(
            bool(getattr(item, "citation", "")) for item in items
        )
        no_policy_denial_bypass = not any(
            getattr(event, "event_type", "") == "policy_bypass" for event in events
        )
        terminal = terminal_state in {"completed", "degraded", "denied", "failed", "cancelled"}
        checks = {
            "required_trace_events": not missing_events,
            "evidence_has_citations": citations_present,
            "no_policy_bypass": no_policy_denial_bypass,
            "terminal_state": terminal,
        }
        findings = []
        if missing_events:
            findings.append(f"Missing trace event types: {', '.join(missing_events)}")
        if not citations_present:
            findings.append("One or more evidence items lack citations")
        if not no_policy_denial_bypass:
            findings.append("Trace contains a policy bypass event")
        if not terminal:
            findings.append("Run did not reach a legal terminal state")
        score = round(sum(checks.values()) / len(checks), 3)
        return EvaluationReport(all(checks.values()), score, checks, tuple(findings))
