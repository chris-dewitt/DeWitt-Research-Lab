"""Tests for approved-root repository inspection (DRL-009)."""

from __future__ import annotations

from pathlib import Path

import pytest
from atticus_local_runner import SandboxedWorkspace, TextInspection, WriteProposal


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
