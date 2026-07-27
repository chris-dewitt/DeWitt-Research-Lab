"""Canonical in-process contracts for the runnable DRL foundation.

The JSON Schemas in ``/schemas`` remain the wire-format authority. These
dataclasses provide a small standard-library implementation for local
development, tests, and adapters without adding framework coupling.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import IntEnum, StrEnum
from typing import Any, cast


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""

    return datetime.now(UTC)


class RiskTier(IntEnum):
    """Published DRL autonomy tiers."""

    EXPLAIN = 0
    READ_COMPUTE = 1
    REVERSIBLE_CHANGE = 2
    CONSEQUENTIAL = 3
    PROHIBITED = 4


class RunState(StrEnum):
    """Legal high-level states for a bounded Atticus run."""

    RECEIVED = "received"
    PLANNING = "planning"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    EVALUATING = "evaluating"
    COMPLETED = "completed"
    DEGRADED = "degraded"
    DENIED = "denied"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class TaskRequest:
    """A user objective plus the minimum policy context required to execute."""

    task_id: str
    objective: str
    session_id: str = "local-demo"
    actor_id: str = "local-user"
    public_session: bool = False
    as_of: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    """A deterministic tool catalog entry."""

    name: str
    description: str
    risk_tier: RiskTier
    public_allowed: bool
    idempotent: bool = True


@dataclass(frozen=True, slots=True)
class ToolCall:
    """A proposed tool invocation. A proposal is not authorization."""

    call_id: str
    tool_name: str
    arguments: dict[str, Any]
    risk_tier: RiskTier


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    """Deterministic policy result for one exact call."""

    allowed: bool
    requires_approval: bool
    reason: str
    call_digest: str


@dataclass(frozen=True, slots=True)
class ApprovalGrant:
    """Approval bound to an exact call digest and session."""

    grant_id: str
    call_digest: str
    session_id: str
    actor_id: str
    expires_at: datetime

    def is_valid(self, *, call_digest: str, session_id: str, at: datetime) -> bool:
        return (
            self.call_digest == call_digest
            and self.session_id == session_id
            and at <= self.expires_at
        )


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    """A provenance-bearing source or deterministic calculation."""

    evidence_id: str
    source: str
    title: str
    observed_at: str
    content: str
    citation: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class TraceEvent:
    """Content-minimized operational event; never hidden chain-of-thought."""

    event_id: str
    task_id: str
    state: RunState
    event_type: str
    message: str
    created_at: datetime = field(default_factory=utc_now)
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TaskResult:
    """Final task outcome plus inspectable evidence and evaluation."""

    task_id: str
    state: RunState
    summary: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    trace: list[TraceEvent] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    evaluation: dict[str, Any] = field(default_factory=dict)
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        def convert(value: Any) -> Any:
            if isinstance(value, (IntEnum, StrEnum)):
                return value.value
            if isinstance(value, datetime):
                return value.isoformat()
            if isinstance(value, dict):
                return {key: convert(item) for key, item in value.items()}
            if isinstance(value, list):
                return [convert(item) for item in value]
            return value

        return cast(dict[str, Any], convert(asdict(self)))
