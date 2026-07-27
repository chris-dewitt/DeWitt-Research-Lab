"""Deterministic policy engine. Model output never authorizes an action."""

from __future__ import annotations

from drl_ai_core import canonical_digest
from drl_protocol import PolicyDecision, RiskTier, TaskRequest, ToolCall, ToolDefinition


class PolicyEngine:
    """Deny by default and require approval at configured risk tiers."""

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
        if request.public_session and not definition.public_allowed:
            return PolicyDecision(False, False, "Tool is not available to public sessions", digest)
        requires_approval = call.risk_tier >= RiskTier.REVERSIBLE_CHANGE
        return PolicyDecision(
            True,
            requires_approval,
            "Allowed by deterministic catalog policy",
            digest,
        )
