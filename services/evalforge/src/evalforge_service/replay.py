"""Signed fixture replay packaging for Atticus reference workflows (DRL-019)."""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from drl_ai_core import canonical_digest
from drl_protocol import RiskTier, RunState, TaskRequest, ToolCall, ToolDefinition

Outcome = Literal["success", "degraded"]

SCHEMA_VERSION = "1.0.0"
FIXTURE_KEY_ID = "drl-fixture-replay-v1"
# Deterministic demo key for local/CI fixture signing only — not a production secret.
_FIXTURE_HMAC_KEY = b"drl-fixture-replay-hmac-v1-demo-only"
DEFAULT_FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "fixtures" / "signed_replays"
FIXED_CAPTURE_TIME = "2026-07-30T00:00:00+00:00"


def _json_dump(path: Path, payload: object) -> str:
    body = json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n"
    path.write_text(body, encoding="utf-8")
    return f"sha256:{canonical_digest(body)}"


def _file_digest(path: Path) -> str:
    return f"sha256:{canonical_digest(path.read_text(encoding='utf-8'))}"


def _artifact_reference(
    *,
    artifact_id: str,
    kind: str,
    uri: str,
    digest: str,
    title: str,
    created_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "id": artifact_id,
        "kind": kind,
        "uri": uri,
        "digest": digest,
        "classification": "public",
        "media_type": "application/json",
        "title": title,
        "created_at": created_at,
        "source_system": "evalforge-replay",
    }


def sign_manifest_body(unsigned: dict[str, Any]) -> dict[str, Any]:
    """Attach fixture HMAC signature and manifest digest to an unsigned body."""

    body = {
        key: value for key, value in unsigned.items() if key not in {"signature", "manifest_digest"}
    }
    manifest_digest = f"sha256:{canonical_digest(body)}"
    signature = hmac.new(
        _FIXTURE_HMAC_KEY,
        manifest_digest.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return {
        **body,
        "signature": {
            "algorithm": "hmac-sha256",
            "key_id": FIXTURE_KEY_ID,
            "signature": f"sha256:{signature}",
        },
        "manifest_digest": manifest_digest,
    }


def verify_manifest_signature(manifest: dict[str, Any]) -> bool:
    """Return True when the fixture HMAC matches the canonical unsigned body."""

    signature = manifest.get("signature")
    if not isinstance(signature, dict):
        return False
    if signature.get("algorithm") != "hmac-sha256":
        return False
    if signature.get("key_id") != FIXTURE_KEY_ID:
        return False
    unsigned = {
        key: value for key, value in manifest.items() if key not in {"signature", "manifest_digest"}
    }
    expected = sign_manifest_body(unsigned)
    digest_ok = expected["manifest_digest"] == manifest.get("manifest_digest")
    signature_ok = expected["signature"] == signature
    return bool(digest_ok and signature_ok)


def serialize_task_result(result: Any) -> dict[str, Any]:
    """Convert a TaskResult-like object into JSON-friendly structures."""

    return {
        "task_id": result.task_id,
        "state": result.state.value if hasattr(result.state, "value") else str(result.state),
        "summary": result.summary,
        "evidence": [asdict(item) for item in result.evidence],
        "trace": [asdict(event) for event in result.trace],
        "artifacts": result.artifacts,
        "evaluation": result.evaluation,
        "limitations": list(result.limitations),
    }


def write_replay_bundle(
    root: Path,
    result: Any,
    *,
    outcome: Outcome,
    code_revision: str = "drl-019-fixture",
    created_at: str = FIXED_CAPTURE_TIME,
) -> Path:
    """Write artifact files and a signed replay manifest for one captured run."""

    bundle_dir = root / outcome
    bundle_dir.mkdir(parents=True, exist_ok=True)
    payload = serialize_task_result(result)
    if outcome == "success" and payload["state"] != RunState.COMPLETED.value:
        raise ValueError(f"success replay requires completed state, got {payload['state']}")
    if outcome == "degraded" and payload["state"] != RunState.DEGRADED.value:
        raise ValueError(f"degraded replay requires degraded state, got {payload['state']}")

    trace_digest = _json_dump(bundle_dir / "execution-trace.json", payload["trace"])
    evaluation_digest = _json_dump(
        bundle_dir / "evaluation-report.json",
        payload["evaluation"],
    )
    linked = payload["artifacts"].get("linked_workflow", {})
    linked_digest = _json_dump(bundle_dir / "linked-workflow.json", linked)
    summary_digest = _json_dump(
        bundle_dir / "task-summary.json",
        {
            "task_id": payload["task_id"],
            "state": payload["state"],
            "summary": payload["summary"],
            "limitations": payload["limitations"],
            "evidence_ids": [item["evidence_id"] for item in payload["evidence"]],
        },
    )

    related = [
        _artifact_reference(
            artifact_id=f"replay-{outcome}-evaluation",
            kind="report",
            uri=f"file://services/evalforge/fixtures/signed_replays/{outcome}/evaluation-report.json",
            digest=evaluation_digest,
            title=f"{outcome} evaluation report",
            created_at=created_at,
        ),
        _artifact_reference(
            artifact_id=f"replay-{outcome}-linked-workflow",
            kind="other",
            uri=f"file://services/evalforge/fixtures/signed_replays/{outcome}/linked-workflow.json",
            digest=linked_digest,
            title=f"{outcome} linked workflow",
            created_at=created_at,
        ),
        _artifact_reference(
            artifact_id=f"replay-{outcome}-task-summary",
            kind="report",
            uri=f"file://services/evalforge/fixtures/signed_replays/{outcome}/task-summary.json",
            digest=summary_digest,
            title=f"{outcome} task summary",
            created_at=created_at,
        ),
    ]
    execution_trace = _artifact_reference(
        artifact_id=f"replay-{outcome}-execution-trace",
        kind="trace",
        uri=f"file://services/evalforge/fixtures/signed_replays/{outcome}/execution-trace.json",
        digest=trace_digest,
        title=f"{outcome} execution trace",
        created_at=created_at,
    )
    configuration = {
        "outcome": outcome,
        "public_session": True,
        "as_of": "2026-07-24",
        "live_at_capture": False,
        "maturity": "prototype",
    }
    unsigned = {
        "schema_version": SCHEMA_VERSION,
        "id": f"drl-replay-{outcome}-001",
        "created_at": created_at,
        "title": f"DRL integrated workflow {outcome} replay",
        "execution_trace": execution_trace,
        "related_artifacts": related,
        "code_revision": code_revision,
        "models": [
            {
                "role": "planner",
                "identity": "fixture-planner",
                "disclosure": (
                    "deterministic local fixture; not an open-weight Atticus Core/Edge release"
                ),
            }
        ],
        "configuration_digest": f"sha256:{canonical_digest(configuration)}",
        "executed_at": created_at,
        "live_at_capture": False,
    }
    manifest = sign_manifest_body(unsigned)
    _json_dump(bundle_dir / "replay-manifest.json", manifest)
    return bundle_dir


def verify_replay_bundle(bundle_dir: Path) -> list[str]:
    """Verify signature, schema-required fields, and on-disk artifact digests."""

    findings: list[str] = []
    manifest_path = bundle_dir / "replay-manifest.json"
    if not manifest_path.exists():
        return ["missing replay-manifest.json"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not verify_manifest_signature(manifest):
        findings.append("manifest signature or digest mismatch")
    if manifest.get("live_at_capture") is not False:
        findings.append("live_at_capture must be false for fixture replays")

    expected_files = {
        "execution-trace.json": manifest["execution_trace"],
        "evaluation-report.json": next(
            item for item in manifest["related_artifacts"] if item["id"].endswith("evaluation")
        ),
        "linked-workflow.json": next(
            item for item in manifest["related_artifacts"] if item["id"].endswith("linked-workflow")
        ),
        "task-summary.json": next(
            item for item in manifest["related_artifacts"] if item["id"].endswith("task-summary")
        ),
    }
    for filename, reference in expected_files.items():
        path = bundle_dir / filename
        if not path.exists():
            findings.append(f"missing artifact file {filename}")
            continue
        digest = _file_digest(path)
        if digest != reference.get("digest"):
            findings.append(f"digest mismatch for {filename}")

    summary = json.loads((bundle_dir / "task-summary.json").read_text(encoding="utf-8"))
    evaluation = json.loads((bundle_dir / "evaluation-report.json").read_text(encoding="utf-8"))
    linked = json.loads((bundle_dir / "linked-workflow.json").read_text(encoding="utf-8"))
    if summary.get("task_id") != linked.get("task_id"):
        findings.append("task summary and linked workflow task_id diverge")
    if "passed" not in evaluation:
        findings.append("evaluation report missing passed field")
    return findings


def _run_success() -> Any:
    from atticus_control_plane import build_local_runtime

    return build_local_runtime().run(
        TaskRequest(
            "replay-success-001",
            "Using inflation and Federal Reserve evidence, run a bear-steepener bank scenario",
            public_session=True,
            as_of="2026-07-24",
        )
    )


def _run_degraded() -> Any:
    from atticus_control_plane.approvals import ApprovalService
    from atticus_control_plane.orchestrator import AtticusOrchestrator
    from atticus_control_plane.policy import PolicyEngine
    from atticus_control_plane.registry import ToolRegistry
    from atticus_control_plane.runtime import build_m3_specialists
    from atticus_control_plane.tools import register_foundation_tools

    from evalforge_service import EvalForge

    atlas, fedlens, balancelab = build_m3_specialists()
    registry = ToolRegistry()
    register_foundation_tools(registry, atlas=atlas, fedlens=fedlens, balancelab=balancelab)

    def _force_fail(_: dict[str, Any]) -> Any:
        raise ValueError("forced specialist outage for degraded replay capture")

    registry.register(
        ToolDefinition(
            "demo.force_fail",
            "Deterministic failure injector for degraded replay fixtures",
            RiskTier.READ_COMPUTE,
            True,
        ),
        _force_fail,
    )

    class DegradedPlanner:
        def plan(self, request: TaskRequest) -> list[ToolCall]:
            as_of = request.as_of or "2026-07-24"
            return [
                ToolCall(
                    f"{request.task_id}-atlas",
                    "atlas.research_snapshot",
                    {"as_of": as_of},
                    RiskTier.READ_COMPUTE,
                ),
                ToolCall(
                    f"{request.task_id}-fail",
                    "demo.force_fail",
                    {},
                    RiskTier.READ_COMPUTE,
                ),
                ToolCall(
                    f"{request.task_id}-fedlens",
                    "fedlens.compare_latest",
                    {"as_of": as_of},
                    RiskTier.READ_COMPUTE,
                ),
                ToolCall(
                    f"{request.task_id}-balancelab",
                    "balancelab.run_scenario",
                    {"name": "bear-steepener"},
                    RiskTier.READ_COMPUTE,
                ),
            ]

    orchestrator = AtticusOrchestrator(
        registry=registry,
        policy=PolicyEngine(),
        approvals=ApprovalService(),
        evaluator=EvalForge(),
        planner=DegradedPlanner(),
    )
    return orchestrator.run(
        TaskRequest(
            "replay-degraded-001",
            "Using inflation and Federal Reserve evidence, run a bear-steepener bank scenario",
            public_session=True,
            as_of="2026-07-24",
        )
    )


def capture_reference_replays(output_root: Path | None = None) -> dict[str, Path]:
    """Capture success and degraded signed replay bundles under ``output_root``."""

    root = output_root or DEFAULT_FIXTURE_ROOT
    root.mkdir(parents=True, exist_ok=True)
    written = {
        "success": write_replay_bundle(root, _run_success(), outcome="success"),
        "degraded": write_replay_bundle(root, _run_degraded(), outcome="degraded"),
    }
    readme = root / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# Signed reference replays (DRL-019)",
                "",
                "Maturity: **prototype** fixture packages for local/CI verification.",
                "Signatures use a published demo HMAC key (`drl-fixture-replay-v1`),",
                "not a production signing identity.",
                "",
                f"Captured at fixed timestamp `{FIXED_CAPTURE_TIME}` for reproducibility.",
                "`live_at_capture` is always `false`.",
                "",
                "Verify with:",
                "",
                "```bash",
                "uv run pytest tests/evalforge/test_signed_replays.py -q",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return written


def utc_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()
