"""Exact-call approval binding for Atticus."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from drl_ai_core import canonical_digest
from drl_protocol import ApprovalGrant, ToolCall


class ApprovalService:
    """Create and verify task-scoped, expiring approval grants."""

    @staticmethod
    def digest(call: ToolCall) -> str:
        return canonical_digest(
            {
                "call_id": call.call_id,
                "tool_name": call.tool_name,
                "arguments": call.arguments,
                "risk_tier": int(call.risk_tier),
            }
        )

    def grant(
        self,
        call: ToolCall,
        *,
        session_id: str,
        actor_id: str,
        ttl_seconds: int = 300,
        now: datetime | None = None,
    ) -> ApprovalGrant:
        if ttl_seconds <= 0 or ttl_seconds > 3600:
            raise ValueError("Approval TTL must be between 1 and 3600 seconds")
        issued_at = now or datetime.now(UTC)
        digest = self.digest(call)
        return ApprovalGrant(
            grant_id=f"grant-{digest[:16]}",
            call_digest=digest,
            session_id=session_id,
            actor_id=actor_id,
            expires_at=issued_at + timedelta(seconds=ttl_seconds),
        )

    def verify(
        self,
        grant: ApprovalGrant | None,
        call: ToolCall,
        *,
        session_id: str,
        now: datetime | None = None,
    ) -> bool:
        if grant is None:
            return False
        checked_at = now or datetime.now(UTC)
        return grant.is_valid(
            call_digest=self.digest(call),
            session_id=session_id,
            at=checked_at,
        )
