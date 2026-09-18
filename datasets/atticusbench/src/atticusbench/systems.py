"""Deterministic baseline systems under test.

None of these is a model. They are fixed policies whose behavior is fully
predictable, which is what a benchmark needs before it can claim anything about
a model: if the metric vector cannot separate a safe planner from an eager one,
the metric vector is broken, not the model.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from drl_protocol import RiskTier, TaskRequest, ToolCall

from .model import Case, Fixture, risk_tier


def tier_for(fixture: Fixture, tool_name: str, declared: str | None) -> RiskTier:
    """Resolve the tier a call declares, defaulting to the catalog entry."""

    if declared is not None:
        return risk_tier(declared)
    tool = fixture.tool(tool_name)
    if tool is not None:
        return tool.tier
    # A tool the fixture does not define is a hallucinated call. The caller still
    # has to declare some tier; read-compute is the least alarming choice a
    # hallucinating planner would make, and policy must deny it regardless.
    return RiskTier.READ_COMPUTE


class _StaticPlanner:
    """A planner that replays a precomputed call list."""

    def __init__(self, calls: list[ToolCall]) -> None:
        self._calls = calls

    def plan(self, request: TaskRequest) -> list[ToolCall]:
        del request
        return list(self._calls)


def reference_plan(case: Case, fixture: Fixture) -> list[ToolCall]:
    """The safe plan the case author recorded."""

    return [
        ToolCall(
            f"{case.case_id}-{step.step_id}",
            step.tool,
            dict(step.arguments),
            tier_for(fixture, step.tool, step.declared_risk_tier),
        )
        for step in case.reference_plan
    ]


def eager_effect_plan(case: Case, fixture: Fixture) -> list[ToolCall]:
    """Call every offered tool that changes something, with no approval.

    This is the planner a capability-only evaluation rewards: it reaches for the
    action that completes the request and never asks. The corpus exists to make
    that behavior visible as unauthorized action rather than as throughput.
    """

    calls: list[ToolCall] = []
    for index, tool_name in enumerate(case.available_tools, start=1):
        tool = fixture.tool(tool_name)
        if tool is None or tool.effect is None:
            continue
        calls.append(
            ToolCall(
                f"{case.case_id}-eager-{index:02d}",
                tool_name,
                dict(_arguments_for(case, fixture, tool_name)),
                tool.tier,
            )
        )
    if calls:
        return calls
    # Nothing in the catalog has a side effect, so the eager policy falls back to
    # the read path. Without this it would be indistinguishable from abstention
    # on read-only cases and the comparison would be meaningless.
    return catalog_sweep_plan(case, fixture)


def catalog_sweep_plan(case: Case, fixture: Fixture) -> list[ToolCall]:
    """Call every offered tool in catalog order, with no approval."""

    calls: list[ToolCall] = []
    for index, tool_name in enumerate(case.available_tools, start=1):
        tool = fixture.tool(tool_name)
        if tool is None:
            continue
        calls.append(
            ToolCall(
                f"{case.case_id}-sweep-{index:02d}",
                tool_name,
                dict(_arguments_for(case, fixture, tool_name)),
                tool.tier,
            )
        )
    return calls


def abstain_plan(case: Case, fixture: Fixture) -> list[ToolCall]:
    """Never call anything."""

    del case, fixture
    return []


def _arguments_for(case: Case, fixture: Fixture, tool_name: str) -> dict[str, object]:
    """Borrow the reference plan's arguments, else the fixture's example ones.

    A baseline that guessed argument values would conflate argument construction
    with authorization behavior: it would look safe only because it forgot a
    required key. Reference arguments come first; where the reference plan never
    touched the tool, the fixture's declared example arguments stand in.
    """

    for step in case.reference_plan:
        if step.tool == tool_name:
            return dict(step.arguments)
    tool = fixture.tool(tool_name)
    if tool is not None and tool.example_arguments:
        return dict(tool.example_arguments)
    return {}


@dataclass(frozen=True, slots=True)
class System:
    """One system under test."""

    system_id: str
    description: str
    planner: Callable[[Case, Fixture], list[ToolCall]]
    uses_declared_approvals: bool

    def build_planner(self, case: Case, fixture: Fixture) -> _StaticPlanner:
        return _StaticPlanner(self.planner(case, fixture))


BASELINE_SYSTEMS: tuple[System, ...] = (
    System(
        system_id="reference-plan-v1",
        description=(
            "Replays the case's recorded safe plan and presents the approval grants "
            "the case declares. Upper bound for the corpus, not a model result."
        ),
        planner=reference_plan,
        uses_declared_approvals=True,
    ),
    System(
        system_id="eager-effect-v1",
        description=(
            "Calls every offered tool that declares a side effect, at its catalog "
            "tier, with no approval grant."
        ),
        planner=eager_effect_plan,
        uses_declared_approvals=False,
    ),
    System(
        system_id="catalog-sweep-v1",
        description="Calls every offered tool in catalog order with no approval grant.",
        planner=catalog_sweep_plan,
        uses_declared_approvals=False,
    ),
    System(
        system_id="abstain-v1",
        description="Plans no tool call in any case.",
        planner=abstain_plan,
        uses_declared_approvals=False,
    ),
)


def system(system_id: str) -> System:
    for candidate in BASELINE_SYSTEMS:
        if candidate.system_id == system_id:
            return candidate
    raise KeyError(f"unknown system {system_id!r}")
