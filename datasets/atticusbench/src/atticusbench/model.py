"""Typed views over AtticusBench case and fixture documents.

The YAML files on disk are the authority. These dataclasses are a narrow,
read-only projection of them so the harness never mutates corpus content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from drl_protocol import RiskTier

#: Fixture and plan documents spell tiers as strings; the protocol uses an
#: ``IntEnum``. The mapping is explicit so an unknown tier fails loudly instead
#: of defaulting to something permissive.
RISK_TIERS: dict[str, RiskTier] = {
    "explain": RiskTier.EXPLAIN,
    "read_compute": RiskTier.READ_COMPUTE,
    "reversible_change": RiskTier.REVERSIBLE_CHANGE,
    "consequential": RiskTier.CONSEQUENTIAL,
    "prohibited": RiskTier.PROHIBITED,
}


def risk_tier(name: str) -> RiskTier:
    try:
        return RISK_TIERS[name]
    except KeyError as exc:  # pragma: no cover - schema rejects this first
        raise ValueError(f"unknown risk tier {name!r}") from exc


@dataclass(frozen=True, slots=True)
class DeclaredEffect:
    """A side effect a fixture tool performs when it executes."""

    kind: str
    target: str
    reversible: bool = False


@dataclass(frozen=True, slots=True)
class DeclaredFailure:
    """A failure mode a fixture tool raises instead of returning output."""

    failure_class: str
    message: str


@dataclass(frozen=True, slots=True)
class ArgumentContract:
    """Argument validation a fixture tool enforces before it does anything."""

    required: tuple[str, ...] = ()
    allowed: tuple[str, ...] = ()
    patterns: dict[str, str] = field(default_factory=dict)
    max_length: dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ArgumentContract:
        return cls(
            required=tuple(document.get("required") or ()),
            allowed=tuple(document.get("allowed") or ()),
            patterns={str(k): str(v) for k, v in (document.get("patterns") or {}).items()},
            max_length={str(k): int(v) for k, v in (document.get("max_length") or {}).items()},
        )


@dataclass(frozen=True, slots=True)
class FixtureTool:
    """One deterministic tool in an environment fixture."""

    name: str
    description: str
    risk_tier_name: str
    public_allowed: bool
    idempotent: bool = True
    response: dict[str, Any] = field(default_factory=dict)
    effect: DeclaredEffect | None = None
    failure: DeclaredFailure | None = None
    injection_marker: bool = False
    argument_contract: ArgumentContract | None = None
    example_arguments: dict[str, Any] = field(default_factory=dict)
    example_violates_contract: bool = False

    @property
    def tier(self) -> RiskTier:
        return risk_tier(self.risk_tier_name)

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> FixtureTool:
        effect = document.get("effect")
        failure = document.get("failure")
        return cls(
            name=str(document["name"]),
            description=str(document["description"]),
            risk_tier_name=str(document["risk_tier"]),
            public_allowed=bool(document["public_allowed"]),
            idempotent=bool(document.get("idempotent", True)),
            response=dict(document.get("response") or {}),
            effect=(
                DeclaredEffect(
                    kind=str(effect["kind"]),
                    target=str(effect["target"]),
                    reversible=bool(effect.get("reversible", False)),
                )
                if effect
                else None
            ),
            failure=(
                DeclaredFailure(
                    failure_class=str(failure["class"]),
                    message=str(failure["message"]),
                )
                if failure
                else None
            ),
            injection_marker=bool(document.get("injection_marker", False)),
            argument_contract=(
                ArgumentContract.from_document(dict(document["argument_contract"]))
                if document.get("argument_contract")
                else None
            ),
            example_arguments=dict(document.get("example_arguments") or {}),
            example_violates_contract=bool(document.get("example_violates_contract", False)),
        )


@dataclass(frozen=True, slots=True)
class Fixture:
    """A resettable environment: a frozen clock plus a deterministic catalog."""

    fixture_id: str
    version: str
    description: str
    clock: str
    tools: tuple[FixtureTool, ...]
    provenance: dict[str, Any]
    content_digest: str | None
    source_path: str

    @property
    def as_of(self) -> str:
        """The fixture clock as an ISO date, which cases inherit."""

        return self.clock_datetime.date().isoformat()

    @property
    def clock_datetime(self) -> datetime:
        stamp = self.clock.replace("Z", "+00:00")
        return datetime.fromisoformat(stamp).astimezone(UTC)

    def tool(self, name: str) -> FixtureTool | None:
        return next((tool for tool in self.tools if tool.name == name), None)

    @property
    def tool_names(self) -> tuple[str, ...]:
        return tuple(tool.name for tool in self.tools)

    @classmethod
    def from_document(cls, document: dict[str, Any], *, source_path: str) -> Fixture:
        return cls(
            fixture_id=str(document["fixture_id"]),
            version=str(document["version"]),
            description=str(document["description"]),
            clock=str(document["clock"]),
            tools=tuple(FixtureTool.from_document(item) for item in document["tools"]),
            provenance=dict(document["provenance"]),
            content_digest=(
                str(document["content_digest"]) if document.get("content_digest") else None
            ),
            source_path=source_path,
        )


@dataclass(frozen=True, slots=True)
class PlanStep:
    """One proposed call in a case's reference plan."""

    step_id: str
    tool: str
    arguments: dict[str, Any]
    declared_risk_tier: str | None = None


@dataclass(frozen=True, slots=True)
class ApprovalSpec:
    """An approval grant the harness issues before executing the reference plan."""

    step_id: str
    ttl_seconds: int = 300
    granted_arguments: dict[str, Any] | None = None
    issued_offset_seconds: int = 0


@dataclass(frozen=True, slots=True)
class Invariants:
    """Hard expectations. These, not plan equality, decide whether a run passed."""

    must_call: tuple[str, ...] = ()
    must_not_call: tuple[str, ...] = ()
    forbidden_effects: tuple[str, ...] = ()
    require_approval_event: bool = False
    require_policy_denial: bool = False
    require_evidence_citations: bool = False
    require_calculation_delegation: bool = False
    expect_abstention: bool = False
    max_steps: int | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> Invariants:
        max_steps = document.get("max_steps")
        return cls(
            must_call=tuple(document.get("must_call") or ()),
            must_not_call=tuple(document.get("must_not_call") or ()),
            forbidden_effects=tuple(document.get("forbidden_effects") or ()),
            require_approval_event=bool(document.get("require_approval_event", False)),
            require_policy_denial=bool(document.get("require_policy_denial", False)),
            require_evidence_citations=bool(document.get("require_evidence_citations", False)),
            require_calculation_delegation=bool(
                document.get("require_calculation_delegation", False)
            ),
            expect_abstention=bool(document.get("expect_abstention", False)),
            max_steps=int(max_steps) if max_steps is not None else None,
        )


@dataclass(frozen=True, slots=True)
class Case:
    """One executable benchmark case."""

    case_id: str
    version: str
    family: str
    split: str
    risk_tier_name: str
    mode: str
    critical_suite: bool
    request: str
    environment_fixture: str
    available_tools: tuple[str, ...]
    policy_version: str
    capability_under_test: str
    failure_under_test: str
    perturbation: str
    reference_plan: tuple[PlanStep, ...]
    approvals: tuple[ApprovalSpec, ...]
    expected_terminal_states: frozenset[str]
    invariants: Invariants
    scorers: tuple[str, ...]
    provenance: dict[str, Any]
    content_digest: str | None
    source_path: str

    @property
    def public_session(self) -> bool:
        return self.mode == "public-session"

    @classmethod
    def from_document(cls, document: dict[str, Any], *, source_path: str) -> Case:
        return cls(
            case_id=str(document["case_id"]),
            version=str(document["version"]),
            family=str(document["family"]),
            split=str(document["split"]),
            risk_tier_name=str(document["risk_tier"]),
            mode=str(document["mode"]),
            critical_suite=bool(document.get("critical_suite", False)),
            request=str(document["request"]),
            environment_fixture=str(document["environment_fixture"]),
            available_tools=tuple(document["available_tools"]),
            policy_version=str(document["policy_version"]),
            capability_under_test=str(document["capability_under_test"]),
            failure_under_test=str(document["failure_under_test"]),
            perturbation=str(document.get("perturbation", "none")),
            reference_plan=tuple(
                PlanStep(
                    step_id=str(step["step_id"]),
                    tool=str(step["tool"]),
                    arguments=dict(step["arguments"]),
                    declared_risk_tier=(
                        str(step["declared_risk_tier"]) if step.get("declared_risk_tier") else None
                    ),
                )
                for step in document["reference_plan"]
            ),
            approvals=tuple(
                ApprovalSpec(
                    step_id=str(item["step_id"]),
                    ttl_seconds=int(item.get("ttl_seconds", 300)),
                    granted_arguments=(
                        dict(item["granted_arguments"])
                        if item.get("granted_arguments") is not None
                        else None
                    ),
                    issued_offset_seconds=int(item.get("issued_offset_seconds", 0)),
                )
                for item in document.get("approvals") or ()
            ),
            expected_terminal_states=frozenset(document["expected_terminal_states"]),
            invariants=Invariants.from_document(dict(document["invariants"])),
            scorers=tuple(document["scorers"]),
            provenance=dict(document["provenance"]),
            content_digest=(
                str(document["content_digest"]) if document.get("content_digest") else None
            ),
            source_path=source_path,
        )
