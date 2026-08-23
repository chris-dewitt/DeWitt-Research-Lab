"""Bounded deterministic planner used until an evaluated open model is selected."""

from __future__ import annotations

from typing import Protocol

from drl_protocol import RiskTier, TaskRequest, ToolCall

#: Terms that mean the local integrated demo, not a generic question.
#: Shared with ModelPlanner so a small model cannot skip Atlas, FedLens,
#: or BalanceLab when the fixture planner would have included them.
INTEGRATED_COVERAGE_TERMS = (
    "inflation",
    "federal reserve",
    "fed ",
    "bear-steepener",
    "bank",
)
INTEGRATED_SPECIALISTS = (
    "atlas.research_snapshot",
    "fedlens.compare_latest",
    "balancelab.run_scenario",
)


def needs_integrated_coverage(objective: str) -> bool:
    """True when the objective matches the fixture integrated demo."""
    text = objective.lower()
    return any(term in text for term in INTEGRATED_COVERAGE_TERMS)


class Planner(Protocol):
    """Structural interface for evaluated planning implementations."""

    def plan(self, request: TaskRequest) -> list[ToolCall]: ...


class FixturePlanner:
    """Create visible, bounded plans from a small supported intent set."""

    def plan(self, request: TaskRequest) -> list[ToolCall]:
        as_of = request.as_of or "2026-07-24"
        if needs_integrated_coverage(request.objective):
            return [
                ToolCall(
                    f"{request.task_id}-atlas",
                    "atlas.research_snapshot",
                    {"as_of": as_of},
                    RiskTier.READ_COMPUTE,
                ),
                ToolCall(
                    f"{request.task_id}-fedlens",
                    "fedlens.compare_latest",
                    {"as_of": as_of},
                    RiskTier.READ_COMPUTE,
                ),
                ToolCall(
                    f"{request.task_id}-balancelab",
                    "balancelab.run_scenario",
                    {
                        "name": "bear-steepener",
                        "short_rate_bps": 25,
                        "long_rate_bps": 75,
                    },
                    RiskTier.READ_COMPUTE,
                ),
            ]
        return [
            ToolCall(
                f"{request.task_id}-guide",
                "laboratory.guide",
                {"topic": request.objective},
                RiskTier.EXPLAIN,
            )
        ]
