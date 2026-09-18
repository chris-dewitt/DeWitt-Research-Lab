"""Build an executable tool registry from a declarative environment fixture.

The fixture files carry no code. This module turns their declarations into
handlers, and records every invocation and every declared side effect in an
effect ledger. The ledger is what lets a scorer say "an external write actually
happened" instead of inferring it from prose.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from atticus_control_plane.registry import ToolOutput, ToolRegistry
from drl_protocol import EvidenceItem, ToolDefinition

from .model import ArgumentContract, Fixture, FixtureTool

#: Longest argument value the fixture will inspect. A fixture is repository
#: content rather than user input, but an unbounded value handed to a regular
#: expression is a denial-of-service shape we decline to carry at all.
MAX_ARGUMENT_LENGTH = 2000


class ArgumentContractViolation(ValueError):
    """The call did not satisfy the tool's declared argument contract.

    Raised as ``ValueError`` so the orchestrator records ``tool_failed``: a
    malformed call is a failed call, not a silently accepted one.
    """


class FixtureToolFailure(ValueError):
    """A declared fixture failure. Raised as ``ValueError`` so the orchestrator
    records ``tool_failed`` and continues its bounded recovery path."""

    def __init__(self, failure_class: str, message: str) -> None:
        super().__init__(f"{failure_class}: {message}")
        self.failure_class = failure_class


@dataclass(slots=True)
class RecordedEffect:
    """One side effect that actually executed."""

    tool: str
    kind: str
    target: str
    reversible: bool


@dataclass(slots=True)
class EffectLedger:
    """Observable record of tool invocations and their side effects."""

    invocations: list[str] = field(default_factory=list)
    effects: list[RecordedEffect] = field(default_factory=list)
    injection_markers: list[str] = field(default_factory=list)

    @property
    def effect_kinds(self) -> tuple[str, ...]:
        return tuple(effect.kind for effect in self.effects)

    def duplicate_invocations(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for name in self.invocations:
            counts[name] = counts.get(name, 0) + 1
        return {name: count for name, count in counts.items() if count > 1}

    def as_dict(self) -> dict[str, Any]:
        return {
            "invocations": list(self.invocations),
            "effects": [
                {
                    "tool": effect.tool,
                    "kind": effect.kind,
                    "target": effect.target,
                    "reversible": effect.reversible,
                }
                for effect in self.effects
            ],
            "injection_markers_served": list(self.injection_markers),
            "duplicate_invocations": self.duplicate_invocations(),
        }


def _evidence(document: dict[str, Any]) -> EvidenceItem:
    return EvidenceItem(
        str(document["evidence_id"]),
        str(document["source"]),
        str(document["title"]),
        str(document["observed_at"]),
        str(document["content"]),
        str(document["citation"]),
        dict(document.get("metadata") or {}),
    )


def _check_arguments(
    tool_name: str,
    arguments: dict[str, Any],
    contract: ArgumentContract,
) -> None:
    """Validate a call against the tool's declared contract.

    Every rejection is explicit. A tool that quietly accepted an out-of-contract
    path or an unknown key would make a path-escape case unscoreable.
    """

    missing = [key for key in contract.required if key not in arguments]
    if missing:
        raise ArgumentContractViolation(
            f"{tool_name}: missing required argument(s): {', '.join(sorted(missing))}"
        )
    if contract.allowed:
        unexpected = [key for key in arguments if key not in contract.allowed]
        if unexpected:
            raise ArgumentContractViolation(
                f"{tool_name}: unexpected argument(s): {', '.join(sorted(unexpected))}"
            )
    for key, limit in contract.max_length.items():
        value = arguments.get(key)
        if isinstance(value, str) and len(value) > limit:
            raise ArgumentContractViolation(
                f"{tool_name}: argument {key!r} exceeds {limit} characters"
            )
    for key, pattern in contract.patterns.items():
        if key not in arguments:
            continue
        value = arguments[key]
        if not isinstance(value, str):
            raise ArgumentContractViolation(
                f"{tool_name}: argument {key!r} must be a string to match its contract"
            )
        if len(value) > MAX_ARGUMENT_LENGTH:
            raise ArgumentContractViolation(
                f"{tool_name}: argument {key!r} is too long to validate"
            )
        if re.fullmatch(pattern, value) is None:
            raise ArgumentContractViolation(
                f"{tool_name}: argument {key!r} does not satisfy its contract"
            )


def _handler(tool: FixtureTool, ledger: EffectLedger) -> Any:
    response = tool.response
    evidence_documents = list(response.get("evidence") or [])
    artifacts = dict(response.get("artifacts") or {})
    message = str(response.get("message", "") or "")

    def handle(arguments: dict[str, Any]) -> ToolOutput:
        ledger.invocations.append(tool.name)
        if tool.argument_contract is not None:
            _check_arguments(tool.name, arguments, tool.argument_contract)
        if tool.failure is not None:
            # A failing tool performs no side effect, which is the property a
            # recovery case needs: the failure must not leave partial state.
            raise FixtureToolFailure(tool.failure.failure_class, tool.failure.message)
        if tool.effect is not None:
            ledger.effects.append(
                RecordedEffect(
                    tool=tool.name,
                    kind=tool.effect.kind,
                    target=tool.effect.target,
                    reversible=tool.effect.reversible,
                )
            )
        if tool.injection_marker:
            ledger.injection_markers.append(tool.name)
        evidence = [_evidence(document) for document in evidence_documents]
        rendered = message
        if "{" in message and arguments:
            # Fixture messages may echo a declared argument key. Missing keys are
            # left as-is rather than raising: the case, not the fixture, decides
            # whether a bad argument is a failure.
            try:
                rendered = message.format(**arguments)
            except (KeyError, IndexError, ValueError):
                rendered = message
        return ToolOutput(evidence=evidence, artifacts=dict(artifacts), message=rendered)

    return handle


def build_registry(
    fixture: Fixture,
    *,
    offered_tools: tuple[str, ...] | None = None,
) -> tuple[ToolRegistry, EffectLedger]:
    """Register the fixture's tools and return the registry and its ledger.

    ``offered_tools`` restricts the catalog to the subset a case declares, so a
    case cannot accidentally be scored against a tool it never offered.
    """

    ledger = EffectLedger()
    registry = ToolRegistry()
    for tool in fixture.tools:
        if offered_tools is not None and tool.name not in offered_tools:
            continue
        registry.register(
            ToolDefinition(
                tool.name,
                tool.description,
                tool.tier,
                tool.public_allowed,
                tool.idempotent,
            ),
            _handler(tool, ledger),
        )
    return registry, ledger
