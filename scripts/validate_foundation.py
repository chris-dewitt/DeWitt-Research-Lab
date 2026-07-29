#!/usr/bin/env python3
"""Deep, reproducible validation for the DRL documentation-first V1 foundation."""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def words(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return len(re.findall(r"\b[\w'-]+\b", text))


# Required foundation surfaces.
required = [
    "README.md",
    "LABORATORY_BIBLE.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE-STRATEGY.md",
    "TRADEMARK_POLICY.md",
    "SECURITY.md",
    "ROADMAP.md",
    "WORKLOG.md",
    "OPEN_RESEARCH_CHARTER.md",
    "OPEN_SOURCE_IDENTITY_UPGRADE.md",
    "docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md",
    "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md",
    "docs/08-web-brand/WIX_EDITOR_HANDOFF_CHECKLIST.md",
    "docs/07-platform-gcp/DOMAIN_DNS_AND_WIX_RUNBOOK.md",
    "docs/adr/ADR-0008-wix-canonical-public-site.md",
    "configs/domain-routing.yaml",
    "docs/00-program/REQUIREMENT_CATALOG.md",
    "docs/00-program/IMPLEMENTATION_BACKLOG.md",
    "docs/12-acceptance/V1_RELEASE_CRITERIA.md",
    "agents/SEQUENTIAL_EXECUTION_PLAN.md",
    "requirements/requirements.yaml",
    "requirements/work-packages.yaml",
    "schemas/openapi/drl-public-api.openapi.yaml",
    "datasets/atticusbench/docs/SPEC.md",
]
for rel in required:
    if not (ROOT / rel).is_file():
        error(f"Missing required file: {rel}")

component_specs = [
    "apps/lab-web/docs/SPEC.md",
    "apps/atticus-console/docs/SPEC.md",
    "apps/atticus-local-runner/docs/SPEC.md",
    "services/atticus-control-plane/docs/SPEC.md",
    "services/atlas/docs/SPEC.md",
    "services/fedlens/docs/SPEC.md",
    "services/balancelab-ai/docs/SPEC.md",
    "services/evalforge/docs/SPEC.md",
    "models/atticus-core/docs/SPEC.md",
    "models/atticus-edge/docs/SPEC.md",
    "datasets/atticusbench/docs/SPEC.md",
    "packages/drl-protocol/docs/SPEC.md",
    "packages/drl-ai-core/docs/SPEC.md",
    "packages/atticus-sdk/docs/SPEC.md",
    "packages/evalforge-sdk/docs/SPEC.md",
]
for rel in component_specs:
    p = ROOT / rel
    if not p.exists():
        error(f"Missing component specification: {rel}")
    elif words(p) < 450:
        error(f"Component specification is too shallow (<450 words): {rel} ({words(p)})")


# Open-source institutional identity surfaces.
open_identity_required = [
    "docs/09-open-source/OPEN_SOURCE_IDENTITY_SYSTEM.md",
    "docs/09-open-source/OPEN_TECHNOLOGY_CATALOG.md",
    "docs/03-model/ATTICUS_OPEN_MODEL_COMMONS_RELEASE_TRAIN.md",
    "docs/08-web-brand/OPEN_SOURCE_VISUAL_IDENTITY.md",
    "configs/open-artifact-policy.yaml",
    "configs/open-stack.yaml",
    "scripts/validate_open_identity.py",
]
for rel in open_identity_required:
    if not (ROOT / rel).is_file():
        error(f"Missing open-source identity surface: {rel}")

# Controlled Markdown metadata and IDs.
allowed_status = {
    "DRAFT",
    "IN REVIEW",
    "APPROVED FOUNDATION",
    "APPROVED EXECUTION MISSION",
    "APPROVED OPERATING PROCEDURE",
    "RELEASE CANDIDATE",
    "PUBLIC RELEASE",
    "SUPERSEDED",
    "ARCHIVED",
}
ids: dict[str, list[str]] = defaultdict(list)
controlled_count = 0
for path in sorted(ROOT.rglob("*.md")):
    rel = str(path.relative_to(ROOT))
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        # Templates and a handful of generated/user-facing readmes may be uncontrolled.
        if rel.startswith(("docs/", "agents/")) and "/templates/" not in rel:
            warn(f"Markdown file has no controlled frontmatter: {rel}")
        continue
    controlled_count += 1
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except Exception as exc:
        error(f"Invalid frontmatter YAML in {rel}: {exc}")
        continue
    for key in ("document_id", "title", "version", "status", "owner", "last_updated"):
        if key not in meta or meta[key] in (None, ""):
            error(f"Missing {key} in frontmatter: {rel}")
    doc_id = str(meta.get("document_id", ""))
    if doc_id:
        ids[doc_id].append(rel)
    status = str(meta.get("status", ""))
    if status and status not in allowed_status:
        error(f"Unknown controlled-document status {status!r}: {rel}")
    if meta.get("last_updated"):
        raw_date = str(meta["last_updated"])
        try:
            parsed = dt.date.fromisoformat(raw_date)
        except ValueError:
            error(f"Invalid last_updated date {raw_date!r} (expected YYYY-MM-DD): {rel}")
        else:
            # Allow one day of clock/timezone skew; anything later is a typo.
            if parsed > dt.date.today() + dt.timedelta(days=1):
                error(f"Future last_updated date: {rel}")

for doc_id, paths in ids.items():
    if len(paths) > 1:
        error(f"Duplicate document_id {doc_id}: {paths}")
if controlled_count < 200:
    error(f"Expected at least 200 controlled Markdown documents; found {controlled_count}")

# Depth checks for constitutional/root docs and missions.
thresholds = {
    "LABORATORY_BIBLE.md": 3500,
    "AGENTS.md": 1000,
    "README.md": 700,
    "CONTRIBUTING.md": 700,
    "GOVERNANCE.md": 500,
    "LICENSE-STRATEGY.md": 700,
    "docs/00-program/REQUIREMENT_CATALOG.md": 1800,
    "datasets/atticusbench/docs/SPEC.md": 700,
}
for rel, minimum in thresholds.items():
    p = ROOT / rel
    if p.exists() and words(p) < minimum:
        error(f"Document too shallow: {rel} has {words(p)} words; minimum {minimum}")

missions = sorted((ROOT / "agents").glob("[0-9][0-9]_*.md"))
if len(missions) != 16:
    error(f"Expected 16 numbered agent missions; found {len(missions)}")
for mission in missions:
    if words(mission) < 650:
        error(f"Agent mission too shallow: {mission.relative_to(ROOT)} ({words(mission)} words)")
    text = mission.read_text(encoding="utf-8")
    for section in (
        "Mission objective",
        "Entry prerequisites",
        "Owned paths",
        "Required work packages",
        "ADR and director",
        "Verification matrix",
        "Handoff requirements",
        "Definition of mission complete",
    ):
        if section.lower() not in text.lower():
            error(f"Agent mission missing section {section!r}: {mission.relative_to(ROOT)}")

# YAML parse and machine registries.
for path in sorted(list(ROOT.rglob("*.yaml")) + list(ROOT.rglob("*.yml"))):
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        error(f"Invalid YAML {path.relative_to(ROOT)}: {exc}")

try:
    requirement_doc = yaml.safe_load((ROOT / "requirements/requirements.yaml").read_text())
    requirements = requirement_doc["requirements"]
    req_ids = [r["id"] for r in requirements]
    if len(requirements) < 100:
        error(f"Expected >=100 approved V1 requirements; found {len(requirements)}")
    if len(req_ids) != len(set(req_ids)):
        error("Duplicate IDs in requirements/requirements.yaml")
    for req in requirements:
        for key in ("id", "statement", "owner", "canonical_spec", "priority", "status"):
            if not req.get(key):
                error(f"Requirement missing {key}: {req}")
        target = ROOT / req["canonical_spec"]
        if not target.exists():
            error(
                f"Requirement canonical_spec does not exist: {req['id']} -> {req['canonical_spec']}"
            )
except Exception as exc:
    error(f"Cannot validate requirements registry: {exc}")

try:
    wp_doc = yaml.safe_load((ROOT / "requirements/work-packages.yaml").read_text())
    work_packages = wp_doc["work_packages"]
    wp_ids = [w["id"] for w in work_packages]
    if len(work_packages) < 95:
        error(f"Expected >=95 work packages; found {len(work_packages)}")
    if len(wp_ids) != len(set(wp_ids)):
        error("Duplicate IDs in work-packages.yaml")
    for mission_num in range(16):
        if not any(w["mission"] == mission_num for w in work_packages):
            error(f"No work package registered for mission {mission_num:02d}")
except Exception as exc:
    error(f"Cannot validate work-package registry: {exc}")

# JSON schemas and examples.
schema_paths = sorted((ROOT / "schemas").glob("*.schema.json"))
if len(schema_paths) < 20:
    error(f"Expected >=20 JSON Schemas; found {len(schema_paths)}")
schema_docs: dict[str, dict[str, Any]] = {}
resources = []
for path in schema_paths:
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        sid = schema.get("$id")
        if not sid:
            error(f"Schema missing $id: {path.relative_to(ROOT)}")
            continue
        if sid in schema_docs:
            error(f"Duplicate schema $id {sid}")
        schema_docs[sid] = schema
        resources.append((sid, Resource.from_contents(schema)))
    except Exception as exc:
        error(f"Invalid JSON Schema {path.relative_to(ROOT)}: {exc}")
registry = Registry().with_resources(resources)

example_paths = sorted((ROOT / "schemas/examples").glob("*.json"))
if len(example_paths) != len(schema_paths):
    error(f"Expected one example per schema ({len(schema_paths)}); found {len(example_paths)}")
for example_path in example_paths:
    schema_path = ROOT / "schemas" / (example_path.stem + ".schema.json")
    if not schema_path.exists():
        error(f"Example has no matching schema: {example_path.relative_to(ROOT)}")
        continue
    try:
        instance = json.loads(example_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
        errs = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        for validation_error in errs[:20]:
            error(
                f"Schema example invalid {example_path.relative_to(ROOT)} "
                f"at {list(validation_error.path)}: {validation_error.message}"
            )
    except Exception as exc:
        error(f"Cannot validate example {example_path.relative_to(ROOT)}: {exc}")

# OpenAPI parse and local ref existence.
openapi_path = ROOT / "schemas/openapi/drl-public-api.openapi.yaml"
try:
    api = yaml.safe_load(openapi_path.read_text(encoding="utf-8"))
    if not str(api.get("openapi", "")).startswith("3.1"):
        error("OpenAPI contract must use 3.1")
    if len(api.get("paths", {})) < 8:
        error("OpenAPI contract is unexpectedly shallow")
    for ref in re.findall(r"\$ref:\s*['\"]?([^'\"\s}]+)", openapi_path.read_text()):
        if ref.startswith("#") or "://" in ref:
            continue
        ref_file = (openapi_path.parent / ref.split("#", 1)[0]).resolve()
        if not ref_file.exists():
            error(f"OpenAPI local $ref missing: {ref}")
except Exception as exc:
    error(f"Invalid OpenAPI foundation: {exc}")

# Markdown relative links. Ignore generated/site routes and anchors.
link_re = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
for path in sorted(ROOT.rglob("*.md")):
    text = path.read_text(encoding="utf-8", errors="replace")
    for raw in link_re.findall(text):
        target = raw.strip().split()[0].strip("<>")
        if not target or target.startswith(
            ("http://", "https://", "mailto:", "#", "sandbox:", "codex:")
        ):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            error(f"Markdown link escapes repository: {path.relative_to(ROOT)} -> {raw}")
            continue
        if not resolved.exists():
            error(f"Broken relative Markdown link: {path.relative_to(ROOT)} -> {raw}")

# Important configuration semantics.
try:
    quotas = yaml.safe_load((ROOT / "configs/quotas.yaml").read_text())
    text = json.dumps(quotas)
    if "250" not in text or "150" not in text:
        error("Quota/cost configuration does not preserve $150 warning / $250 hard planning cap")
    routing = yaml.safe_load((ROOT / "configs/model-routing.yaml").read_text())
    if "open" not in json.dumps(routing).lower():
        error("Model routing configuration does not explicitly preserve open-weight path")
except Exception as exc:
    error(f"Cannot validate key configurations: {exc}")

# No obviously stale generated validation claims.
for stale in ("PACKAGE_MANIFEST.json", "VALIDATION_REPORT.md"):
    if not (ROOT / stale).exists():
        warn(f"{stale} will be generated during final packaging")

print(f"Controlled documents: {controlled_count}")
print(f"Requirements: {len(requirements) if 'requirements' in locals() else 0}")
print(f"Work packages: {len(work_packages) if 'work_packages' in locals() else 0}")
print(f"Schemas/examples: {len(schema_paths)}/{len(example_paths)}")
print(f"Agent missions: {len(missions)}")
for warning in WARNINGS:
    print(f"WARNING: {warning}")
if ERRORS:
    print("\nVALIDATION FAILED")
    for item in ERRORS:
        print(f"ERROR: {item}")
    sys.exit(1)
print("\nVALIDATION PASSED")
