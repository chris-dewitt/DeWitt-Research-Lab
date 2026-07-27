from __future__ import annotations

from pathlib import Path

import pytest
from atticus_local_runner import SandboxedWorkspace, WriteProposal


def test_workspace_rejects_parent_traversal(tmp_path: Path) -> None:
    workspace = SandboxedWorkspace(tmp_path)
    with pytest.raises(PermissionError):
        workspace.read_text("../outside.txt")


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
