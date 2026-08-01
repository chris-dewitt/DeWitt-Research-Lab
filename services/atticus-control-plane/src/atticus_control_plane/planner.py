"""Bounded deterministic planner used until an evaluated open model is selected."""

from __future__ import annotations

from typing import Protocol

from drl_protocol import RiskTier, TaskRequest, ToolCall


class Planner(Protocol):
    """Structural interface for evaluated planning implementations."""

    def plan(self, request: TaskRequest) -> list[ToolCall]: ...


class FixturePlanner:
    """Create visible, bounded plans from a small supported intent set."""

    def plan(self, request: TaskRequest) -> list[ToolCall]:
        objective = request.objective.lower()
        as_of = request.as_of or "2026-07-24"
        integrated_terms = ("inflation", "federal reserve", "fed ", "bear-steepener", "bank")
        if any(term in objective for term in integrated_terms):
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
