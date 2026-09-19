"""Deterministic policy engine. Model output never authorizes an action."""

from __future__ import annotations

from drl_ai_core import canonical_digest
from drl_protocol import (
    BOUNDARY_CROSSING_EFFECTS,
    EffectType,
    PolicyDecision,
    RiskTier,
    TaskRequest,
    ToolCall,
    ToolDefinition,
)


class PolicyEngine:
    """Deny by default, and require approval on tier or on declared effect.

    Two independent conditions require an approval. The risk tier ranks how
    consequential an action is to the operator's own state. The declared effect
    says whether it crosses a trust boundary. Neither implies the other: a
    cross-session read is tier one and irreversible in its consequence, which is
    why gating on tier alone let one through (ADR-0011, and TR-2026-003 section
    5.3 for the measurement that found it).

    Both conditions read the **catalog** definition. A caller's declared tier is
    already rejected on mismatch, and a caller cannot declare an effect at all,
    so neither a planner nor a model can lower its own gate.
    """

    def decide(
        self,
        *,
        request: TaskRequest,
        call: ToolCall,
        definition: ToolDefinition | None,
    ) -> PolicyDecision:
        digest = canonical_digest(
            {
                "call_id": call.call_id,
                "tool_name": call.tool_name,
                "arguments": call.arguments,
                "risk_tier": int(call.risk_tier),
            }
        )
        if definition is None:
            return PolicyDecision(False, False, "Tool is not registered", digest)
        if call.risk_tier != definition.risk_tier:
            return PolicyDecision(False, False, "Call risk tier does not match catalog", digest)
        if call.risk_tier >= RiskTier.PROHIBITED:
            return PolicyDecision(False, False, "Tier 4 actions are prohibited", digest)
        # Normalize the catalog's declaration once. ``ToolDefinition`` is an
        # unvalidated dataclass, so a future loader could hand this the plain
        # string "external_effect" or something meaningless. An unintelligible
        # declaration is denied rather than treated as harmless: a gate that
        # cannot read a tool's effect must not conclude it has none.
        try:
            effect = EffectType(definition.effect_type)
        except ValueError:
            return PolicyDecision(
                False,
                False,
                "Tool declares an unrecognized effect type",
                digest,
            )
        if effect is EffectType.PROHIBITED:
            return PolicyDecision(
                False,
                False,
                "Tool declares a prohibited effect",
                digest,
            )
        if request.public_session and not definition.public_allowed:
            return PolicyDecision(False, False, "Tool is not available to public sessions", digest)

        tier_gates = call.risk_tier >= RiskTier.REVERSIBLE_CHANGE
        effect_gates = effect in BOUNDARY_CROSSING_EFFECTS
        if effect_gates and not tier_gates:
            reason = (
                "Allowed by deterministic catalog policy; approval required because "
                f"the declared effect {effect.value} crosses a trust "
                "boundary at this tier"
            )
        else:
            reason = "Allowed by deterministic catalog policy"
        return PolicyDecision(
            True,
            tier_gates or effect_gates,
            reason,
            digest,
            gating_effect=effect if effect_gates else None,
        )
