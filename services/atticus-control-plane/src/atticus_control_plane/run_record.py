"""Local Atticus run records: ids and scores, never prompt or tool content.

AGENTS.md forbids logging prompt, file, email, voice, or tool content by
default. The operator still needs a file that says whether a long local run
finished, which tools ran, and what EvalForge scored. This module writes that
file and refuses to persist the fields that would violate the rule.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from drl_protocol import TaskResult

__all__ = [
    "FORBIDDEN_RECORD_KEYS",
    "default_run_record_dir",
    "write_run_record",
]

#: Keys that must never appear in a persisted run record.
FORBIDDEN_RECORD_KEYS = frozenset(
    {
        "objective",
        "content",
        "prompt",
        "arguments",
        "summary",
        "trace",
        "limitations",
        "artifacts",
        "evidence",
        "message",
    }
)


def default_run_record_dir() -> Path:
    """Directory for local records. Override with ATTICUS_RUN_RECORD_DIR."""
    raw = os.environ.get("ATTICUS_RUN_RECORD_DIR", "").strip()
    if raw:
        return Path(raw)
    return Path.cwd() / "runs" / "atticus"


def _walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_walk_keys(item))
    return keys


def _tool_names(result: TaskResult, event_type: str) -> list[str]:
    names: list[str] = []
    for event in result.trace:
        if event.event_type != event_type:
            continue
        tool = event.attributes.get("tool")
        if isinstance(tool, str) and tool:
            names.append(tool)
    return names


def write_run_record(
    result: TaskResult,
    *,
    planner_line: str,
    plan_source: str,
    root: Path | None = None,
    clock: datetime | None = None,
) -> Path:
    """Write an ids-and-scores record and return its path.

    Raises ``ValueError`` if a forbidden key would be persisted. That is a
    programming error, not an operator one: the record is built here, so a
    leak means this function grew a field it must not have.
    """
    written_at = clock or datetime.now(UTC)
    stamp = written_at.strftime("%Y%m%dT%H%M%SZ")
    linked = result.artifacts.get("linked_workflow")
    workflow_digest = None
    if isinstance(linked, dict):
        digest = linked.get("workflow_digest")
        if isinstance(digest, str):
            workflow_digest = digest
    record: dict[str, Any] = {
        "schema": "atticus-run-record/v1",
        "task_id": result.task_id,
        "state": result.state.value,
        "written_at": written_at.isoformat(),
        "planner": planner_line,
        "plan_source": plan_source,
        "tools_completed": _tool_names(result, "tool_completed"),
        "tools_failed": _tool_names(result, "tool_failed"),
        "evidence_ids": [item.evidence_id for item in result.evidence],
        "evalforge_score": result.evaluation.get("score"),
        "evalforge_passed": result.evaluation.get("passed"),
        "artifact_keys": sorted(result.artifacts),
        "workflow_digest": workflow_digest,
        "limitation_count": len(result.limitations),
        "evidence_count": len(result.evidence),
    }
    leaked = _walk_keys(record) & FORBIDDEN_RECORD_KEYS
    if leaked:
        raise ValueError(f"run record would persist forbidden keys: {sorted(leaked)}")
    target = root or default_run_record_dir()
    target.mkdir(parents=True, exist_ok=True)
    path = target / f"{result.task_id}-{stamp}.json"
    path.write_text(json.dumps(record, indent=2, default=str) + "\n", encoding="utf-8")
    return path
