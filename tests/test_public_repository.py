from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from scripts import generate_manifest
from scripts import validate_public_repository as audit

ROOT = Path(__file__).resolve().parents[1]


def test_current_tracked_source_passes_public_audit() -> None:
    findings, file_count = audit.source_findings(ROOT)
    assert file_count >= 600
    assert findings == []


def test_secret_shapes_fail_without_echoing_the_value() -> None:
    fake = "ghp_" + "A" * 36
    findings = audit.scan_text("notes/example.md", f"token={fake}")
    assert [finding.rule for finding in findings] == ["credential-pattern"]
    assert fake not in findings[0].render()


def test_employer_contact_and_local_path_fail_closed() -> None:
    email = "person" + "@example.com"
    local_path = "C:" + "\\Users\\someone\\private.txt"
    employer = "Bank" + " of America"
    text = f"{employer}\n{email}\n{local_path}"
    rules = {finding.rule for finding in audit.scan_text("notes/example.md", text)}
    assert rules == {"employer-identifier", "local-path", "public-contact"}


def test_approved_contact_and_no_reply_metadata_pass() -> None:
    text = "director@dewitt-labs.com\n168304930+chris-dewitt@users.noreply.github.com"
    assert audit.scan_text("README.md", text) == []


def test_manifest_contains_only_supplied_regular_files(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("alpha", encoding="utf-8")
    (tmp_path / "b.txt").write_text("beta", encoding="utf-8")
    manifest = generate_manifest.build_manifest(
        tmp_path,
        ["b.txt", "a.txt"],
        source_revision="a" * 40,
        generated_at="2026-08-17T00:00:00+00:00",
    )
    assert manifest["entry_count"] == 2
    entries = manifest["entries"]
    assert isinstance(entries, list)
    assert [entry["path"] for entry in entries] == ["a.txt", "b.txt"]
    json.dumps(manifest)


def test_history_gate_reports_count_without_address() -> None:
    institutional = "student" + "@unc.edu"
    public = "168304930+chris-dewitt@users.noreply.github.com"
    findings = audit.history_findings_for_emails([institutional, public])
    assert len(findings) == 1
    finding = findings[0]
    assert institutional not in finding.render()
    assert "1 reachable commits" in finding.render()


def test_release_gate_accepts_historical_institutional_address(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """RES-022 accepts the historical address, so it must not fail the gate."""
    institutional = "student" + "@unc.edu"

    # Still reported, so the exposure stays visible and countable...
    findings = audit.history_findings_for_emails([institutional])
    assert len(findings) == 1

    # ...but a --release run exits clean rather than blocking on it.
    monkeypatch.setattr(audit, "history_findings", lambda: (findings, 1))
    monkeypatch.setattr(sys, "argv", ["validate_public_repository.py", "--release"])
    assert audit.main() == 0
