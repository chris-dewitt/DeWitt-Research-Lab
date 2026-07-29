"""Tests for approved-root inspection (DRL-009) and approval flow (DRL-010)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from atticus_local_runner import (
    ApprovedWriteFlow,
    LocalApprovalGrant,
    LocalAuditLog,
    SandboxedWorkspace,
    TextInspection,
    WriteProposal,
)


def test_workspace_rejects_parent_traversal(tmp_path: Path) -> None:
    workspace = SandboxedWorkspace(tmp_path)
    (tmp_path / "inside.txt").write_text("safe\n", encoding="utf-8")
    with pytest.raises(PermissionError):
        workspace.read_text("../outside.txt")
    with pytest.raises(PermissionError):
        workspace.inspect_text("notes/../../outside.txt")
    with pytest.raises(PermissionError):
        workspace.read_text(str(tmp_path / "inside.txt"))


def test_workspace_rejects_symlink_escape_and_skips_symlinks_in_listing(
    tmp_path: Path,
) -> None:
    outside = tmp_path.parent / "outside-secret.txt"
    outside.write_text("api_key=should-never-leak\n", encoding="utf-8")
    link = tmp_path / "escape.txt"
    link.symlink_to(outside)
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "ok.txt").write_text("ok\n", encoding="utf-8")
    nested_link = nested / "alias.txt"
    nested_link.symlink_to(outside)

    workspace = SandboxedWorkspace(tmp_path)
    with pytest.raises(PermissionError):
        workspace.read_text("escape.txt")
    with pytest.raises(PermissionError):
        workspace.inspect_text("nested/alias.txt")

    listed = workspace.list_files()
    assert "nested/ok.txt" in listed
    assert "escape.txt" not in listed
    assert "nested/alias.txt" not in listed


def test_workspace_rejects_oversized_reads(tmp_path: Path) -> None:
    target = tmp_path / "big.txt"
    target.write_text("x" * 64, encoding="utf-8")
    workspace = SandboxedWorkspace(tmp_path, max_read_bytes=16)
    with pytest.raises(ValueError, match="approved read limit"):
        workspace.read_text("big.txt")
    with pytest.raises(ValueError, match="approved read limit"):
        workspace.inspect_text("big.txt")


def test_workspace_rejects_binary_files(tmp_path: Path) -> None:
    binary = tmp_path / "blob.bin"
    binary.write_bytes(b"hello\x00world")
    workspace = SandboxedWorkspace(tmp_path)
    with pytest.raises(ValueError, match="Binary files"):
        workspace.read_text("blob.bin")
    with pytest.raises(ValueError, match="Binary files"):
        workspace.inspect_text("blob.bin")


def test_inspection_redacts_secrets_without_corrupting_raw_writes(tmp_path: Path) -> None:
    secret_file = tmp_path / "config.env"
    secret_file.write_text(
        "api_key=super-secret-value\ntoken: abcdef123456\nplain=ok\n",
        encoding="utf-8",
    )
    workspace = SandboxedWorkspace(tmp_path)
    inspection = workspace.inspect_text("config.env")
    assert isinstance(inspection, TextInspection)
    assert inspection.relative_path == "config.env"
    assert inspection.redacted is True
    assert "super-secret-value" not in inspection.content
    assert "abcdef123456" not in inspection.content
    assert "[REDACTED]" in inspection.content
    assert "plain=ok" in inspection.content
    # Public read path is also redacted.
    assert "super-secret-value" not in workspace.read_text("config.env")
    # Write approval still binds to exact raw content, not redacted views.
    proposal = workspace.propose_write("config.env", "api_key=rotated\n")
    assert "super-secret-value" in proposal.diff or "api_key=" in proposal.diff
    destination = workspace.apply_write(proposal, approval_digest=proposal.digest)
    assert destination.read_text(encoding="utf-8") == "api_key=rotated\n"


def test_write_requires_exact_digest_and_is_atomic(tmp_path: Path) -> None:
    workspace = SandboxedWorkspace(tmp_path)
    proposal = workspace.propose_write("notes/research.md", "Atticus is online.\n")

    with pytest.raises(PermissionError):
        workspace.apply_write(proposal, approval_digest="wrong")

    destination = workspace.apply_write(proposal, approval_digest=proposal.digest)
    assert destination.read_text(encoding="utf-8") == "Atticus is online.\n"


def test_changed_proposal_cannot_reuse_approval(tmp_path: Path) -> None:
    workspace = SandboxedWorkspace(tmp_path)
    approved = workspace.propose_write("README.md", "approved\n")
    changed = WriteProposal("README.md", "changed\n", approved.digest, approved.diff)

    with pytest.raises(PermissionError):
        workspace.apply_write(changed, approval_digest=approved.digest)


# --- DRL-010: patch proposal and local approval flow ---


def _flow(tmp_path: Path) -> ApprovedWriteFlow:
    return ApprovedWriteFlow(SandboxedWorkspace(tmp_path))


def test_approved_flow_applies_within_ttl_and_audits(tmp_path: Path) -> None:
    flow = _flow(tmp_path)
    issued = datetime(2026, 7, 29, 12, 0, tzinfo=UTC)
    proposal = flow.propose("notes/plan.md", "Atticus plan.\n", now=issued)
    grant = flow.approve(proposal, actor_id="dewitt", ttl_seconds=300, now=issued)
    destination = flow.apply(proposal, grant, now=issued + timedelta(seconds=299))
    assert destination.read_text(encoding="utf-8") == "Atticus plan.\n"
    events = [event.event for event in flow.audit_log.events()]
    assert events == ["write-proposed", "approval-granted", "write-applied"]
    assert all(event.proposal_digest == proposal.digest for event in flow.audit_log.events())


def test_expired_approval_is_denied_and_audited(tmp_path: Path) -> None:
    flow = _flow(tmp_path)
    issued = datetime(2026, 7, 29, 12, 0, tzinfo=UTC)
    proposal = flow.propose("notes/plan.md", "Atticus plan.\n", now=issued)
    grant = flow.approve(proposal, actor_id="dewitt", ttl_seconds=60, now=issued)

    with pytest.raises(PermissionError, match="expired"):
        flow.apply(proposal, grant, now=issued + timedelta(seconds=61))

    assert not (tmp_path / "notes" / "plan.md").exists()
    last = flow.audit_log.events()[-1]
    assert last.event == "apply-denied"
    assert "expired" in last.detail


def test_grant_is_bound_to_exact_proposal_and_workspace(tmp_path: Path) -> None:
    flow = _flow(tmp_path)
    issued = datetime(2026, 7, 29, 12, 0, tzinfo=UTC)
    approved = flow.propose("a.md", "approved\n", now=issued)
    other = flow.propose("b.md", "other\n", now=issued)
    grant = flow.approve(approved, actor_id="dewitt", now=issued)

    with pytest.raises(PermissionError, match="different proposal"):
        flow.apply(other, grant, now=issued)
    with pytest.raises(PermissionError, match="no approval grant"):
        flow.apply(approved, None, now=issued)

    other_root = tmp_path / "elsewhere"
    other_root.mkdir()
    foreign = ApprovedWriteFlow(SandboxedWorkspace(other_root), flow.audit_log)
    foreign_proposal = foreign.workspace.propose_write("a.md", "approved\n")
    foreign_grant = LocalApprovalGrant(
        grant_id=grant.grant_id,
        proposal_digest=foreign_proposal.digest,
        workspace_root=str(flow.workspace.root),
        actor_id=grant.actor_id,
        issued_at=grant.issued_at,
        expires_at=grant.expires_at,
    )
    with pytest.raises(PermissionError, match="different workspace"):
        foreign.apply(foreign_proposal, foreign_grant, now=issued)


def test_changed_workspace_invalidates_prior_approval(tmp_path: Path) -> None:
    flow = _flow(tmp_path)
    issued = datetime(2026, 7, 29, 12, 0, tzinfo=UTC)
    target = tmp_path / "config.md"
    target.write_text("original\n", encoding="utf-8")
    proposal = flow.propose("config.md", "updated\n", now=issued)
    grant = flow.approve(proposal, actor_id="dewitt", now=issued)

    target.write_text("changed underneath\n", encoding="utf-8")
    with pytest.raises(PermissionError, match="changed after approval"):
        flow.apply(proposal, grant, now=issued)

    assert target.read_text(encoding="utf-8") == "changed underneath\n"
    last = flow.audit_log.events()[-1]
    assert last.event == "apply-denied"
    assert "workspace changed" in last.detail


def test_approval_rejects_invalid_ttl_and_anonymous_actor(tmp_path: Path) -> None:
    flow = _flow(tmp_path)
    proposal = flow.propose("a.md", "content\n")
    with pytest.raises(ValueError, match="TTL"):
        flow.approve(proposal, actor_id="dewitt", ttl_seconds=0)
    with pytest.raises(ValueError, match="TTL"):
        flow.approve(proposal, actor_id="dewitt", ttl_seconds=3601)
    with pytest.raises(ValueError, match="identified local actor"):
        flow.approve(proposal, actor_id="   ")


def test_audit_log_is_append_only_and_redacts_secrets(tmp_path: Path) -> None:
    audit = LocalAuditLog()
    audit.record(
        "write-proposed",
        relative_path="config.env",
        proposal_digest="digest-1",
        detail="api_key=super-secret-value proposed",
    )
    events = audit.events()
    assert len(events) == 1
    assert "super-secret-value" not in events[0].detail
    assert "[REDACTED]" in events[0].detail
    assert isinstance(events, tuple)

    audit.record("approval-granted", relative_path="config.env", proposal_digest="digest-1")
    assert [event.sequence for event in audit.events()] == [1, 2]
    jsonl = audit.to_jsonl()
    assert jsonl.count("\n") == 1
    assert "super-secret-value" not in jsonl
