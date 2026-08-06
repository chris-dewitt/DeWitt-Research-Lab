"""Security and governance guards for the DRL-033 public artifact boundary."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator, FormatChecker

from scripts.prepare_public_replay_release import (
    DEFAULT_POLICY,
    PublicArtifactError,
    prepare_release,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = "1feda7f4df59781c86a331d9b0100b08f4eb71a2"


def _fake_site(tmp_path: Path) -> Path:
    policy = yaml.safe_load(DEFAULT_POLICY.read_text(encoding="utf-8"))
    site = tmp_path / "site"
    site.mkdir()
    for name in policy["artifact"]["expected_source_files"]:
        if name.endswith(".json"):
            content = '{"fixture": true}\n'
        else:
            content = f"<!doctype html><title>{name}</title><p>REPLAY</p>\n"
        (site / name).write_text(content, encoding="utf-8")
    return site


def test_release_contains_only_allowlisted_content_and_public_envelope(
    tmp_path: Path,
) -> None:
    site = _fake_site(tmp_path)
    output = tmp_path / "public"

    manifest = prepare_release(site, output, SOURCE_SHA)

    assert manifest["classification"] == "public_only"
    assert manifest["lifecycle_state"] == "experimental"
    assert manifest["contact"] == "director@dewitt-labs.com"
    assert manifest["source_revision"] == SOURCE_SHA
    assert manifest["target_repository"] == "chris-dewitt/DeWitt-Research-Artifacts"
    assert manifest["open_exception"]["exception_id"] == "DRL-OEX-0001"
    assert manifest["licenses"] == {
        "renderer_software": "Apache-2.0",
        "rendered_content": "CC-BY-4.0",
    }

    admitted = {item["path"] for item in manifest["files"]}
    assert admitted == {"degraded.html", "index.html", "site.json", "success.html"}
    assert {path.name for path in output.iterdir()} == admitted | {
        ".nojekyll",
        "README.md",
        "release-manifest.json",
    }
    for item in manifest["files"]:
        digest = hashlib.sha256((output / item["path"]).read_bytes()).hexdigest()
        assert item["sha256"] == digest
    assert json.loads((output / "release-manifest.json").read_text()) == manifest


def test_open_exception_satisfies_the_canonical_schema() -> None:
    schema = json.loads(
        (ROOT / "schemas/open-exception.schema.json").read_text(encoding="utf-8")
    )
    exception = json.loads(
        (ROOT / "configs/open-exceptions/DRL-OEX-0001.json").read_text(
            encoding="utf-8"
        )
    )

    Draft202012Validator(schema, format_checker=FormatChecker()).validate(exception)


def test_unexpected_file_fails_closed(tmp_path: Path) -> None:
    site = _fake_site(tmp_path)
    (site / "private-notes.md").write_text("not public", encoding="utf-8")

    with pytest.raises(PublicArtifactError, match="allowlist mismatch"):
        prepare_release(site, tmp_path / "public", SOURCE_SHA)


@pytest.mark.parametrize(
    "secret",
    [
        "-----BEGIN PRIVATE KEY-----",
        "github_pat_abcdefghijklmnopqrstuvwxyz123456",
        r"C:\Users\director\private\trace.json",
        "/home/runner/work/private/repository",
    ],
)
def test_sensitive_markers_fail_closed(tmp_path: Path, secret: str) -> None:
    site = _fake_site(tmp_path)
    (site / "index.html").write_text(secret, encoding="utf-8")

    with pytest.raises(PublicArtifactError, match="contains forbidden"):
        prepare_release(site, tmp_path / "public", SOURCE_SHA)


def test_symlink_fails_closed(tmp_path: Path) -> None:
    site = _fake_site(tmp_path)
    target = site / "index.html"
    target.unlink()
    try:
        os.symlink(site / "success.html", target)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")

    with pytest.raises(PublicArtifactError, match="symlinks are prohibited"):
        prepare_release(site, tmp_path / "public", SOURCE_SHA)


def test_workflow_builds_on_push_but_publishes_only_on_manual_dispatch() -> None:
    workflow = (ROOT / ".github/workflows/publish-replays.yml").read_text(
        encoding="utf-8"
    )

    assert "actions/deploy-pages" not in workflow
    assert "pages: write" not in workflow
    assert "workflow_dispatch:" in workflow
    assert "github.ref != 'refs/heads/main'" in workflow
    assert "github.ref == 'refs/heads/main'" in workflow
    assert "secrets.PUBLIC_ARTIFACT_TOKEN" in workflow
    assert "chris-dewitt/DeWitt-Research-Artifacts" in workflow
    assert "rsync -a --delete --exclude='.git'" in workflow
