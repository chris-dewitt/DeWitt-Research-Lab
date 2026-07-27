"""Canonical Atticus run-state transition rules.

These rules are side-effect free. Orchestrators must call ``assert_transition``
before mutating run state so illegal paths fail loudly in tests and CI.
"""

from __future__ import annotations

from .models import RunState

LEGAL_TRANSITIONS: dict[RunState, frozenset[RunState]] = {
    RunState.RECEIVED: frozenset({RunState.PLANNING, RunState.CANCELLED, RunState.FAILED}),
    RunState.PLANNING: frozenset(
        {
            RunState.EXECUTING,
            RunState.AWAITING_APPROVAL,
            RunState.DENIED,
            RunState.FAILED,
            RunState.CANCELLED,
        }
    ),
    RunState.AWAITING_APPROVAL: frozenset(
        {RunState.EXECUTING, RunState.CANCELLED, RunState.DENIED}
    ),
    RunState.EXECUTING: frozenset(
        {
            RunState.EVALUATING,
            RunState.DEGRADED,
            RunState.DENIED,
            RunState.FAILED,
            RunState.CANCELLED,
        }
    ),
    RunState.EVALUATING: frozenset({RunState.COMPLETED, RunState.DEGRADED, RunState.FAILED}),
}

TERMINAL_STATES: frozenset[RunState] = frozenset(
    {
        RunState.COMPLETED,
        RunState.DEGRADED,
        RunState.DENIED,
        RunState.FAILED,
        RunState.CANCELLED,
    }
)


class IllegalStateTransition(RuntimeError):
    """Raised when an orchestrator attempts a disallowed transition."""


def is_terminal(state: RunState) -> bool:
    """Return True when the run may not transition further."""

    return state in TERMINAL_STATES


def can_transition(current: RunState, target: RunState) -> bool:
    """Return whether ``current -> target`` is a legal transition."""

    return target in LEGAL_TRANSITIONS.get(current, frozenset())


def assert_transition(current: RunState, target: RunState) -> RunState:
    """Validate and return ``target``, or raise ``IllegalStateTransition``."""

    if not can_transition(current, target):
        raise IllegalStateTransition(
            f"Illegal Atticus state transition: {current.value} -> {target.value}"
        )
    return target


def legal_targets(current: RunState) -> frozenset[RunState]:
    """Return the allowed next states for ``current``."""

    return LEGAL_TRANSITIONS.get(current, frozenset())
