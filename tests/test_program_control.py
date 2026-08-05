from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def run_validator() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_program.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_program_validator_passes() -> None:
    result = run_validator()
    assert result.returncode == 0, result.stdout + result.stderr


def test_issue_register_has_one_owner_and_evidence_owner_per_issue() -> None:
    register = yaml.safe_load((ROOT / "requirements/issue-register.yaml").read_text())
    issues = register["issues"]
    assert len(issues) == 30
    assert len({issue["id"] for issue in issues}) == len(issues)
    for issue in issues:
        assert isinstance(issue["mission"], int)
        assert issue["evidence_owner"].strip()


@pytest.mark.parametrize(
    "body_name",
    ["DRL-001.md", "DRL-004.md", "DRL-005.md", "DRL-007.md", "DRL-030.md"],
)
def test_representative_issue_bodies_are_executable(body_name: str) -> None:
    body = (ROOT / ".github/ISSUE_BODIES" / body_name).read_text(encoding="utf-8")
    for heading in (
        "## Acceptance criteria",
        "## Verification plan",
        "## Rollback",
        "## Evidence required for closure",
    ):
        assert heading in body


def test_ci_has_one_pnpm_version_source() -> None:
    """package.json#packageManager must be the only source of the pnpm version.

    Locating the step by action version pinned this test to `@v4` and broke it on a
    routine bump to `@v6.0.9`. The action's own version is irrelevant to the
    invariant — what matters is that the step does not also declare `version:`,
    which makes pnpm/action-setup reject the workflow.
    """
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    package = (ROOT / "package.json").read_text(encoding="utf-8")
    assert '"packageManager": "pnpm@' in package

    match = re.search(r"uses:\s*pnpm/action-setup@\S+", workflow)
    assert match, "ci.yml no longer sets up pnpm via pnpm/action-setup"
    action = workflow[match.end() :].split("- uses: actions/setup-node", maxsplit=1)[0]
    assert "version:" not in action
