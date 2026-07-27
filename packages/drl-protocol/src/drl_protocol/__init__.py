"""Typed, dependency-free contracts shared across DRL components."""

from .models import (
    ApprovalGrant,
    EvidenceItem,
    PolicyDecision,
    RiskTier,
    RunState,
    TaskRequest,
    TaskResult,
    ToolCall,
    ToolDefinition,
    TraceEvent,
)
from .state_machine import (
    LEGAL_TRANSITIONS,
    TERMINAL_STATES,
    IllegalStateTransition,
    assert_transition,
    can_transition,
    is_terminal,
    legal_targets,
)

__all__ = [
    "ApprovalGrant",
    "EvidenceItem",
    "IllegalStateTransition",
    "LEGAL_TRANSITIONS",
    "PolicyDecision",
    "RiskTier",
    "RunState",
    "TERMINAL_STATES",
    "TaskRequest",
    "TaskResult",
    "ToolCall",
    "ToolDefinition",
    "TraceEvent",
    "assert_transition",
    "can_transition",
    "is_terminal",
    "legal_targets",
]

__version__ = "0.1.1"
