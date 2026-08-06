#!/usr/bin/env python3
"""Validate Mission 00 program registers and executable issue bodies."""

from __future__ import annotations

import re
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, cast

import yaml

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def load_yaml(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        error(f"cannot load {relative}: {exc}")
        return {}
    if not isinstance(value, dict):
        error(f"{relative} must contain a mapping")
        return {}
    return value


def validate_issue_register() -> None:
    register = load_yaml("requirements/issue-register.yaml")
    requirements = cast(
        list[dict[str, Any]],
        load_yaml("requirements/requirements.yaml").get("requirements", []),
    )
    labels = cast(
        list[dict[str, Any]], load_yaml(".github/labels.yml").get("labels", [])
    )

    known_requirements = {
        item_id for item in requirements if isinstance((item_id := item.get("id")), str)
    }
    known_labels = {
        item_name for item in labels if isinstance((item_name := item.get("name")), str)
    }
    milestones = cast(list[dict[str, Any]], register.get("milestones", []))
    issues = cast(list[dict[str, Any]], register.get("issues", []))

    milestone_ids = {
        milestone_id
        for item in milestones
        if isinstance((milestone_id := item.get("id")), str)
    }
    issue_by_id: dict[str, dict[str, Any]] = {
        issue_id: item
        for item in issues
        if isinstance((issue_id := item.get("id")), str)
    }
    allowed_issue_statuses = {
        "READY",
        "QUEUED",
        "IN_PROGRESS",
        "EVIDENCE_READY",
        "COMPLETE",
        "BLOCKED",
    }
    expected_ids = {f"DRL-{number:03d}" for number in range(1, 34)}
    actual_ids = set(issue_by_id)
    if actual_ids != expected_ids:
        error(
            "issue register IDs differ from DRL-001..DRL-033: "
            f"missing={sorted(expected_ids - actual_ids)}, "
            f"extra={sorted(actual_ids - expected_ids)}"
        )

    graph: dict[str, set[str]] = defaultdict(set)
    indegree = dict.fromkeys(actual_ids, 0)
    required_headings = (
        "## Metadata",
        "## User / research value",
        "## Acceptance criteria",
        "## Verification plan",
        "## Rollback",
        "## Evidence required for closure",
    )

    for issue_id, issue in issue_by_id.items():
        if issue.get("mission") not in range(16):
            error(f"{issue_id}: mission must be an integer from 0 through 15")
        if issue.get("status") not in allowed_issue_statuses:
            error(f"{issue_id}: invalid status {issue.get('status')!r}")
        if not str(issue.get("evidence_owner", "")).strip():
            error(f"{issue_id}: evidence_owner is required")
        if issue.get("milestone") not in milestone_ids:
            error(f"{issue_id}: unknown milestone {issue.get('milestone')!r}")

        for requirement in issue.get("requirements", []):
            if requirement not in known_requirements:
                error(f"{issue_id}: unknown requirement {requirement}")
        for label in issue.get("labels", []):
            if label not in known_labels:
                error(f"{issue_id}: unknown label {label}")
        for evidence in issue.get("evidence", []):
            if not (ROOT / str(evidence)).is_file():
                error(f"{issue_id}: evidence path does not exist: {evidence}")

        dependencies = issue.get("dependencies", [])
        if not isinstance(dependencies, list):
            error(f"{issue_id}: dependencies must be a list")
            dependencies = []
        for dependency_value in dependencies:
            dependency = str(dependency_value)
            if dependency not in actual_ids:
                error(f"{issue_id}: unknown dependency {dependency}")
                continue
            if dependency == issue_id:
                error(f"{issue_id}: issue cannot depend on itself")
                continue
            graph[dependency].add(issue_id)
            indegree[issue_id] += 1

        body_value = str(issue.get("body", ""))
        body_path = (ROOT / body_value).resolve()
        if ROOT not in body_path.parents:
            error(f"{issue_id}: body path escapes repository: {body_value}")
        elif not body_path.is_file():
            error(f"{issue_id}: missing body {body_value}")
        else:
            body = body_path.read_text(encoding="utf-8")
            if not body.startswith(f"# {issue_id}:"):
                error(f"{issue_id}: body title must start with '# {issue_id}:'")
            for heading in required_headings:
                if heading not in body:
                    error(f"{issue_id}: body missing heading {heading!r}")

    ready = deque(sorted(issue_id for issue_id, degree in indegree.items() if degree == 0))
    visited = 0
    while ready:
        issue_id = ready.popleft()
        visited += 1
        for child in sorted(graph[issue_id]):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    if visited != len(actual_ids):
        error("issue dependency graph contains a cycle")


def validate_work_packages() -> None:
    packages = cast(
        list[dict[str, Any]],
        load_yaml("requirements/work-packages.yaml").get("work_packages", []),
    )
    ids = [str(item.get("id")) for item in packages]
    if len(ids) != len(set(ids)):
        error("work package IDs are not unique")
    if len(ids) != 122:
        error(f"expected 122 work packages, found {len(ids)}")

    allowed_statuses = {"PLANNED", "IN_PROGRESS", "COMPLETE", "BLOCKED", "DEFERRED"}
    for package in packages:
        package_id = str(package.get("id", "<missing>"))
        if package.get("status") not in allowed_statuses:
            error(f"{package_id}: invalid status {package.get('status')!r}")
        if package.get("mission") not in range(16):
            error(f"{package_id}: mission must be an integer from 0 through 15")
        if package.get("status") == "COMPLETE":
            evidence = package.get("evidence", [])
            if not evidence:
                error(f"{package_id}: COMPLETE package requires evidence")
            for relative in evidence:
                if not (ROOT / str(relative)).exists():
                    error(f"{package_id}: evidence path does not exist: {relative}")


def validate_pnpm_pin() -> None:
    package_json = (ROOT / "package.json").read_text(encoding="utf-8")
    package_match = re.search(r'"packageManager"\s*:\s*"pnpm@([^"]+)"', package_json)
    if package_match is None:
        error("package.json must pin pnpm with packageManager")

    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    action_block = re.search(
        r"uses:\s*pnpm/action-setup@v\d+(.*?)(?=\n\s*-\s+uses:|\n\s*-\s+name:)",
        workflow,
        flags=re.DOTALL,
    )
    if action_block is None:
        error("CI must configure pnpm/action-setup")
    elif re.search(r"^\s+version:", action_block.group(1), flags=re.MULTILINE):
        error("pnpm version must be specified only by package.json#packageManager")


def main() -> int:
    validate_issue_register()
    validate_work_packages()
    validate_pnpm_pin()
    if ERRORS:
        for message in ERRORS:
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"PROGRAM VALIDATION FAILED ({len(ERRORS)} errors)", file=sys.stderr)
        return 1
    print("PROGRAM VALIDATION PASSED (33 issues, 122 work packages, acyclic dependencies)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
