"""Signed success and degraded replay packaging tests (DRL-019)."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
from evalforge_service import (
    capture_reference_replays,
    verify_manifest_signature,
    verify_replay_bundle,
)
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"
FIXTURE_ROOT = ROOT / "services" / "evalforge" / "fixtures" / "signed_replays"


def _schema_registry() -> Registry:
    registry = Registry()
    for path in SCHEMAS.glob("*.schema.json"):
        document = json.loads(path.read_text(encoding="utf-8"))
        registry = registry.with_resource(
            document["$id"],
            Resource.from_contents(document, default_specification=DRAFT202012),
        )
    return registry


def test_capture_and_verify_success_and_degraded_replays(tmp_path: Path) -> None:
    written = capture_reference_replays(tmp_path)
    assert set(written) == {"success", "degraded"}
    for outcome, bundle in written.items():
        findings = verify_replay_bundle(bundle)
        assert findings == [], (outcome, findings)
        manifest = json.loads((bundle / "replay-manifest.json").read_text(encoding="utf-8"))
        assert verify_manifest_signature(manifest)
        assert manifest["live_at_capture"] is False
        schema = json.loads((SCHEMAS / "replay-manifest.schema.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema, registry=_schema_registry()).validate(manifest)
        summary = json.loads((bundle / "task-summary.json").read_text(encoding="utf-8"))
        if outcome == "success":
            assert summary["state"] == "completed"
        else:
            assert summary["state"] == "degraded"
            assert any("force_fail" in item or "forced" in item for item in summary["limitations"])


def test_committed_reference_fixtures_verify() -> None:
    assert FIXTURE_ROOT.is_dir()
    for outcome in ("success", "degraded"):
        findings = verify_replay_bundle(FIXTURE_ROOT / outcome)
        assert findings == [], (outcome, findings)
        manifest = json.loads(
            (FIXTURE_ROOT / outcome / "replay-manifest.json").read_text(encoding="utf-8")
        )
        schema = json.loads((SCHEMAS / "replay-manifest.schema.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema, registry=_schema_registry()).validate(manifest)
