"""Deterministic baseline systems under test.

None of these is a model. They are fixed policies whose behavior is fully
predictable, which is what a benchmark needs before it can claim anything about
a model: if the metric vector cannot separate a safe planner from an eager one,
the metric vector is broken, not the model.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

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


class BenchPlanner(Protocol):
    """What the harness needs from a planner.

    ``last_plan`` exists so the harness can record what was proposed without
    calling ``plan`` a second time. For a fixed policy a second call is free;
    for a model it is a second inference, and two inferences per case would
    make the recorded plan and the executed plan potentially different runs.
    """

    last_plan: list[ToolCall]

    def plan(self, request: TaskRequest) -> list[ToolCall]: ...


class StaticPlanner:
    """A planner that replays a precomputed call list."""

    def __init__(self, calls: list[ToolCall]) -> None:
        self._calls = calls
        self.last_plan: list[ToolCall] = []

    def plan(self, request: TaskRequest) -> list[ToolCall]:
        del request
        self.last_plan = list(self._calls)
        return list(self.last_plan)


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
    """One system under test: a fixed policy, or a model."""

    system_id: str
    description: str
    #: Builds a fresh planner for one case. Fresh per case because a planner
    #: records what it last proposed, and a shared one would leak the previous
    #: case's plan into this case's record.
    build_planner: Callable[[Case, Fixture], BenchPlanner]
    uses_declared_approvals: bool


def static_system(
    system_id: str,
    description: str,
    plan_for: Callable[[Case, Fixture], list[ToolCall]],
    *,
    uses_declared_approvals: bool = False,
) -> System:
    """Wrap a deterministic plan function as a system under test."""

    def build(case: Case, fixture: Fixture) -> BenchPlanner:
        return StaticPlanner(plan_for(case, fixture))

    return System(
        system_id=system_id,
        description=description,
        build_planner=build,
        uses_declared_approvals=uses_declared_approvals,
    )


BASELINE_SYSTEMS: tuple[System, ...] = (
    static_system(
        "reference-plan-v1",
        (
            "Replays the case's recorded safe plan and presents the approval grants "
            "the case declares. Upper bound for the corpus, not a model result."
        ),
        reference_plan,
        uses_declared_approvals=True,
    ),
    static_system(
        "eager-effect-v1",
        (
            "Calls every offered tool that declares a side effect, at its catalog "
            "tier, with no approval grant."
        ),
        eager_effect_plan,
    ),
    static_system(
        "catalog-sweep-v1",
        "Calls every offered tool in catalog order with no approval grant.",
        catalog_sweep_plan,
    ),
    static_system(
        "abstain-v1",
        "Plans no tool call in any case.",
        abstain_plan,
    ),
)


def system(system_id: str) -> System:
    for candidate in BASELINE_SYSTEMS:
        if candidate.system_id == system_id:
            return candidate
    raise KeyError(f"unknown system {system_id!r}")
