"""Expiring, digest-bound local write approvals with redacted audit evidence.

Models and remote callers may propose writes; only a deterministic local flow
may apply them. Every consequential decision is bound to the exact proposal
digest, scoped to one workspace root, expires, and leaves a redacted
append-only audit record (DRL-SEC-003, DRL-SEC-004).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from drl_ai_core import canonical_digest, redact_text

from .workspace import SandboxedWorkspace, WriteProposal

MAX_APPROVAL_TTL_SECONDS = 3600
DEFAULT_APPROVAL_TTL_SECONDS = 300


@dataclass(frozen=True, slots=True)
class LocalApprovalGrant:
    """One expiring approval bound to an exact proposal in one workspace."""

    grant_id: str
    proposal_digest: str
    workspace_root: str
    actor_id: str
    issued_at: datetime
    expires_at: datetime

    def is_valid(self, *, proposal_digest: str, workspace_root: str, at: datetime) -> bool:
        return (
            self.proposal_digest == proposal_digest
            and self.workspace_root == workspace_root
            and at < self.expires_at
        )


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """One immutable, redacted local audit record."""

    sequence: int
    occurred_at: datetime
    event: str
    relative_path: str
    proposal_digest: str
    detail: str


class LocalAuditLog:
    """Append-only audit trail; records are redacted and never rewritten."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(
        self,
        event: str,
        *,
        relative_path: str,
        proposal_digest: str,
        detail: str = "",
        now: datetime | None = None,
    ) -> AuditEvent:
        entry = AuditEvent(
            sequence=len(self._events) + 1,
            occurred_at=now or datetime.now(UTC),
            event=event,
            relative_path=relative_path,
            proposal_digest=proposal_digest,
            detail=redact_text(detail),
        )
        self._events.append(entry)
        return entry

    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)

    def to_jsonl(self) -> str:
        lines = [
            json.dumps(
                {
                    "sequence": event.sequence,
                    "occurred_at": event.occurred_at.isoformat(),
                    "event": event.event,
                    "relative_path": event.relative_path,
                    "proposal_digest": event.proposal_digest,
                    "detail": event.detail,
                },
                sort_keys=True,
            )
            for event in self._events
        ]
        return "\n".join(lines)


class ApprovedWriteFlow:
    """Propose, approve, and apply workspace writes under expiry and audit."""

    def __init__(self, workspace: SandboxedWorkspace, audit_log: LocalAuditLog | None = None):
        self.workspace = workspace
        self.audit_log = audit_log if audit_log is not None else LocalAuditLog()

    def propose(
        self, relative_path: str, content: str, *, now: datetime | None = None
    ) -> WriteProposal:
        proposal = self.workspace.propose_write(relative_path, content)
        self.audit_log.record(
            "write-proposed",
            relative_path=relative_path,
            proposal_digest=proposal.digest,
            detail=f"{len(content.encode('utf-8'))} bytes proposed",
            now=now,
        )
        return proposal

    def approve(
        self,
        proposal: WriteProposal,
        *,
        actor_id: str,
        ttl_seconds: int = DEFAULT_APPROVAL_TTL_SECONDS,
        now: datetime | None = None,
    ) -> LocalApprovalGrant:
        if not actor_id.strip():
            raise ValueError("Approval requires an identified local actor")
        if ttl_seconds <= 0 or ttl_seconds > MAX_APPROVAL_TTL_SECONDS:
            raise ValueError(
                f"Approval TTL must be between 1 and {MAX_APPROVAL_TTL_SECONDS} seconds"
            )
        issued_at = now or datetime.now(UTC)
        workspace_root = str(self.workspace.root)
        grant = LocalApprovalGrant(
            grant_id=f"local-grant-{canonical_digest([proposal.digest, actor_id])[:16]}",
            proposal_digest=proposal.digest,
            workspace_root=workspace_root,
            actor_id=actor_id,
            issued_at=issued_at,
            expires_at=issued_at + timedelta(seconds=ttl_seconds),
        )
        self.audit_log.record(
            "approval-granted",
            relative_path=proposal.relative_path,
            proposal_digest=proposal.digest,
            detail=f"actor={actor_id} expires_at={grant.expires_at.isoformat()}",
            now=now,
        )
        return grant

    def apply(
        self,
        proposal: WriteProposal,
        grant: LocalApprovalGrant | None,
        *,
        now: datetime | None = None,
    ) -> Path:
        checked_at = now or datetime.now(UTC)
        workspace_root = str(self.workspace.root)
        if grant is None or not grant.is_valid(
            proposal_digest=proposal.digest,
            workspace_root=workspace_root,
            at=checked_at,
        ):
            if grant is None:
                reason = "no approval grant presented"
            elif grant.proposal_digest != proposal.digest:
                reason = "approval bound to a different proposal"
            elif grant.workspace_root != workspace_root:
                reason = "approval bound to a different workspace"
            else:
                reason = "approval expired"
            self.audit_log.record(
                "apply-denied",
                relative_path=proposal.relative_path,
                proposal_digest=proposal.digest,
                detail=reason,
                now=now,
            )
            raise PermissionError(f"Write not applied: {reason}")
        try:
            destination = self.workspace.apply_write(
                proposal, approval_digest=grant.proposal_digest
            )
        except PermissionError:
            self.audit_log.record(
                "apply-denied",
                relative_path=proposal.relative_path,
                proposal_digest=proposal.digest,
                detail="workspace changed after approval",
                now=now,
            )
            raise
        self.audit_log.record(
            "write-applied",
            relative_path=proposal.relative_path,
            proposal_digest=proposal.digest,
            detail=f"grant={grant.grant_id}",
            now=now,
        )
        return destination
