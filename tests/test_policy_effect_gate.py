"""The effect gate (ADR-0011): approval on declared effect, not only on tier.

These are the deny-path and abuse-case tests the security-change gate in
`AGENTS.md` section 7 requires. The positive path is here too, because a gate
that refuses everything is not a gate.
"""

from __future__ import annotations

import pytest
from atticus_control_plane.approvals import ApprovalService
from atticus_control_plane.policy import PolicyEngine
from drl_protocol import (
    BOUNDARY_CROSSING_EFFECTS,
    EffectType,
    RiskTier,
    TaskRequest,
    ToolCall,
    ToolDefinition,
)


def _call(tier: RiskTier, *, name: str = "demo.tool", arguments: dict | None = None) -> ToolCall:
    return ToolCall("call-1", name, arguments if arguments is not None else {"k": "v"}, tier)


def _definition(
    tier: RiskTier,
    effect: EffectType,
    *,
    name: str = "demo.tool",
    public_allowed: bool = False,
) -> ToolDefinition:
    return ToolDefinition(name, "a demo tool", tier, public_allowed, True, effect)


def _request(*, public: bool = False) -> TaskRequest:
    return TaskRequest("task-1", "do the thing", public_session=public)


@pytest.fixture
def policy() -> PolicyEngine:
    return PolicyEngine()


def test_read_tier_boundary_crossing_effect_requires_approval(policy: PolicyEngine) -> None:
    # DIR-011: this is the case that used to execute with no approval.
    decision = policy.decide(
        request=_request(),
        call=_call(RiskTier.READ_COMPUTE),
        definition=_definition(RiskTier.READ_COMPUTE, EffectType.EXTERNAL_EFFECT),
    )
    assert decision.allowed is True
    assert decision.requires_approval is True
    assert decision.gating_effect is EffectType.EXTERNAL_EFFECT
    assert "crosses a trust boundary" in decision.reason


def test_explain_tier_privileged_effect_requires_approval(policy: PolicyEngine) -> None:
    decision = policy.decide(
        request=_request(),
        call=_call(RiskTier.EXPLAIN),
        definition=_definition(RiskTier.EXPLAIN, EffectType.PRIVILEGED),
    )
    assert decision.requires_approval is True
    assert decision.gating_effect is EffectType.PRIVILEGED


@pytest.mark.parametrize("effect", sorted(BOUNDARY_CROSSING_EFFECTS))
def test_no_tier_exempts_a_boundary_crossing_effect(
    policy: PolicyEngine, effect: EffectType
) -> None:
    for tier in (RiskTier.EXPLAIN, RiskTier.READ_COMPUTE):
        decision = policy.decide(
            request=_request(),
            call=_call(tier),
            definition=_definition(tier, effect),
        )
        assert decision.requires_approval is True, (tier, effect)


@pytest.mark.parametrize(
    "effect",
    [EffectType.OBSERVE, EffectType.READ, EffectType.DRAFT, EffectType.MODIFY],
)
def test_read_tier_local_effects_stay_ungated(policy: PolicyEngine, effect: EffectType) -> None:
    # The line is deliberate: gating every declared effect would put ordinary
    # reads and drafts behind approval, which is the reason ADR-0011 rejected
    # the retier-everything option.
    decision = policy.decide(
        request=_request(),
        call=_call(RiskTier.READ_COMPUTE),
        definition=_definition(RiskTier.READ_COMPUTE, effect),
    )
    assert decision.allowed is True
    assert decision.requires_approval is False
    assert decision.gating_effect is None


def test_tier_gate_still_fires_without_a_declared_effect(policy: PolicyEngine) -> None:
    decision = policy.decide(
        request=_request(),
        call=_call(RiskTier.REVERSIBLE_CHANGE),
        definition=_definition(RiskTier.REVERSIBLE_CHANGE, EffectType.MODIFY),
    )
    assert decision.requires_approval is True
    # Tier fired, not effect, and the decision says which.
    assert decision.gating_effect is None
    assert "crosses a trust boundary" not in decision.reason


def test_prohibited_effect_is_denied_outright(policy: PolicyEngine) -> None:
    decision = policy.decide(
        request=_request(),
        call=_call(RiskTier.READ_COMPUTE),
        definition=_definition(RiskTier.READ_COMPUTE, EffectType.PROHIBITED),
    )
    assert decision.allowed is False
    assert decision.requires_approval is False
    assert "prohibited effect" in decision.reason


def test_a_caller_cannot_declare_its_own_effect(policy: PolicyEngine) -> None:
    # A ToolCall carries no effect field at all: the catalog is the only source.
    # This test exists so that adding one to ToolCall later fails loudly here.
    assert not hasattr(_call(RiskTier.READ_COMPUTE), "effect_type")

    catalog = _definition(RiskTier.READ_COMPUTE, EffectType.EXTERNAL_EFFECT)
    decision = policy.decide(
        request=_request(), call=_call(RiskTier.READ_COMPUTE), definition=catalog
    )
    assert decision.requires_approval is True


def test_tier_spoofing_is_still_denied_before_the_effect_gate(policy: PolicyEngine) -> None:
    # A caller claiming a lower tier than the catalog is denied, and the denial
    # does not depend on the effect being harmless.
    decision = policy.decide(
        request=_request(),
        call=_call(RiskTier.EXPLAIN),
        definition=_definition(RiskTier.CONSEQUENTIAL, EffectType.EXTERNAL_EFFECT),
    )
    assert decision.allowed is False
    assert "risk tier does not match" in decision.reason


def test_public_session_denial_precedes_the_effect_gate(policy: PolicyEngine) -> None:
    decision = policy.decide(
        request=_request(public=True),
        call=_call(RiskTier.READ_COMPUTE),
        definition=_definition(
            RiskTier.READ_COMPUTE, EffectType.EXTERNAL_EFFECT, public_allowed=False
        ),
    )
    assert decision.allowed is False
    assert decision.requires_approval is False
    assert "public sessions" in decision.reason


def test_unregistered_tool_is_denied_whatever_it_claims(policy: PolicyEngine) -> None:
    decision = policy.decide(request=_request(), call=_call(RiskTier.READ_COMPUTE), definition=None)
    assert decision.allowed is False
    assert "not registered" in decision.reason


def test_an_approval_for_the_exact_call_satisfies_the_effect_gate() -> None:
    policy = PolicyEngine()
    approvals = ApprovalService()
    call = _call(RiskTier.READ_COMPUTE)
    decision = policy.decide(
        request=_request(),
        call=call,
        definition=_definition(RiskTier.READ_COMPUTE, EffectType.EXTERNAL_EFFECT),
    )
    assert decision.requires_approval is True

    grant = approvals.grant(call, session_id="local-demo", actor_id="operator")
    assert grant.call_digest == decision.call_digest
    assert approvals.verify(grant, call, session_id="local-demo") is True


def test_a_grant_for_different_arguments_does_not_satisfy_the_effect_gate() -> None:
    policy = PolicyEngine()
    approvals = ApprovalService()
    approved = _call(RiskTier.READ_COMPUTE, arguments={"k": "approved"})
    executed = _call(RiskTier.READ_COMPUTE, arguments={"k": "something-else"})
    grant = approvals.grant(approved, session_id="local-demo", actor_id="operator")

    decision = policy.decide(
        request=_request(),
        call=executed,
        definition=_definition(RiskTier.READ_COMPUTE, EffectType.EXTERNAL_EFFECT),
    )
    assert decision.requires_approval is True
    assert grant.call_digest != decision.call_digest
    assert approvals.verify(grant, executed, session_id="local-demo") is False


def test_a_grant_from_another_session_does_not_satisfy_the_effect_gate() -> None:
    approvals = ApprovalService()
    call = _call(RiskTier.READ_COMPUTE)
    grant = approvals.grant(call, session_id="session-a", actor_id="operator")
    assert approvals.verify(grant, call, session_id="session-b") is False


def test_the_default_definition_is_ungated() -> None:
    # An existing registration that predates the effect field keeps its
    # behavior: read effect, no effect gate.
    legacy = ToolDefinition("legacy.tool", "no effect declared", RiskTier.READ_COMPUTE, True)
    assert legacy.effect_type is EffectType.READ
    decision = PolicyEngine().decide(
        request=_request(),
        call=_call(RiskTier.READ_COMPUTE, name="legacy.tool"),
        definition=legacy,
    )
    assert decision.requires_approval is False


def test_an_unrecognized_effect_declaration_is_denied(policy: PolicyEngine) -> None:
    # A gate that cannot read a tool's effect must not conclude it has none.
    nonsense = ToolDefinition(
        "demo.tool", "a demo tool", RiskTier.READ_COMPUTE, False, True, "whatever"
    )  # type: ignore[arg-type]
    decision = policy.decide(
        request=_request(), call=_call(RiskTier.READ_COMPUTE), definition=nonsense
    )
    assert decision.allowed is False
    assert "unrecognized effect type" in decision.reason


def test_a_raw_string_effect_still_fails_closed(policy: PolicyEngine) -> None:
    # ToolDefinition is an unvalidated dataclass. If a future catalog loader
    # hands it the plain string instead of the enum member, the gate must still
    # fire — identity comparison would have quietly permitted it.
    raw_prohibited = ToolDefinition(
        "demo.tool", "a demo tool", RiskTier.READ_COMPUTE, False, True, "prohibited"
    )  # type: ignore[arg-type]
    decision = policy.decide(
        request=_request(), call=_call(RiskTier.READ_COMPUTE), definition=raw_prohibited
    )
    assert decision.allowed is False
    assert "prohibited effect" in decision.reason

    raw_external = ToolDefinition(
        "demo.tool", "a demo tool", RiskTier.READ_COMPUTE, False, True, "external_effect"
    )  # type: ignore[arg-type]
    gated = policy.decide(
        request=_request(), call=_call(RiskTier.READ_COMPUTE), definition=raw_external
    )
    assert gated.requires_approval is True
