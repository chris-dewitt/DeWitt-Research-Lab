#!/usr/bin/env python3
"""Validate DRL's constitutional, public, and enforceable open identity."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def require(path: str) -> Path:
    p = ROOT / path
    if not p.exists():
        errors.append(f"missing required open-identity artifact: {path}")
    return p


required = [
    "OPEN_RESEARCH_CHARTER.md",
    "OPEN_SOURCE_IDENTITY_UPGRADE.md",
    "docs/09-open-source/OPEN_SOURCE_IDENTITY_SYSTEM.md",
    "docs/09-open-source/OPEN_ARTIFACT_STANDARD.md",
    "docs/09-open-source/OPEN_MODEL_COMMONS.md",
    "docs/09-open-source/OPEN_TECHNOLOGY_CATALOG.md",
    "docs/09-open-source/FORKABILITY_AND_SELF_HOSTING_STANDARD.md",
    "docs/08-web-brand/OPEN_SOURCE_PORTAL_AND_COMMONS.md",
    "docs/08-web-brand/OPEN_SOURCE_VISUAL_IDENTITY.md",
    "docs/03-model/ATTICUS_OPEN_MODEL_COMMONS_RELEASE_TRAIN.md",
    "configs/open-artifact-policy.yaml",
    "configs/open-stack.yaml",
    "configs/open-source-metrics.yaml",
    "schemas/open-artifact-release.schema.json",
    "schemas/open-exception.schema.json",
    "schemas/upstream-dependency.schema.json",
]
for rel in required:
    require(rel)

charter = (ROOT / "OPEN_RESEARCH_CHARTER.md").read_text(encoding="utf-8")
for phrase in (
    "Open-source software",
    "Open Source AI",
    "Open-weight model",
    "Forkability",
    "upstream",
):
    if phrase.lower() not in charter.lower():
        errors.append(f"charter missing identity concept: {phrase}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
if "OPEN_RESEARCH_CHARTER.md" not in readme or "open by construction" not in readme.lower():
    errors.append(
        "README does not foreground the Open Research Charter/open-by-construction identity"
    )

for rel in ("docs/08-web-brand/HOMEPAGE_SPEC.md", "apps/lab-web/docs/SPEC.md"):
    text = (ROOT / rel).read_text(encoding="utf-8")
    if "/open-source" not in text and "Open Source" not in text:
        errors.append(f"web surface does not expose Open Source portal: {rel}")

requirements = yaml.safe_load(
    (ROOT / "requirements/requirements.yaml").read_text(encoding="utf-8")
)["requirements"]
oss = [r for r in requirements if str(r.get("id", "")).startswith("DRL-OSS-")]
if len(oss) < 24:
    errors.append(f"expected at least 24 enforceable DRL-OSS requirements; found {len(oss)}")
if not all(r.get("priority") == "V1-MUST" for r in oss):
    errors.append("all open-source identity requirements must be V1-MUST")

policy = yaml.safe_load((ROOT / "configs/open-artifact-policy.yaml").read_text(encoding="utf-8"))
if policy.get("default_software_license") != "Apache-2.0":
    errors.append("open artifact policy must preserve Apache-2.0 software default")
if not policy.get("exception_process", {}).get("director_approval_required"):
    errors.append("open exception policy must require director approval")

stack = yaml.safe_load((ROOT / "configs/open-stack.yaml").read_text(encoding="utf-8"))
components = stack.get("components", [])
if len(components) < 10:
    errors.append("open stack catalog is unexpectedly shallow")
for component in components:
    for field in (
        "id",
        "name",
        "license",
        "classification",
        "canonical_url",
        "status",
        "owner",
        "exit_strategy",
    ):
        if not component.get(field):
            errors.append(
                f"open stack component missing {field}: {component.get('id', '<unknown>')}"
            )

for schema_name in ("open-artifact-release", "open-exception", "upstream-dependency"):
    schema = ROOT / "schemas" / f"{schema_name}.schema.json"
    example = ROOT / "schemas" / "examples" / f"{schema_name}.json"
    if schema.exists():
        json.loads(schema.read_text(encoding="utf-8"))
    if example.exists():
        json.loads(example.read_text(encoding="utf-8"))

for adr in (
    "docs/adr/ADR-0006-opentofu-first-iac.md",
    "docs/adr/ADR-0007-valkey-cache-coordination.md",
):
    text = require(adr).read_text(encoding="utf-8") if (ROOT / adr).exists() else ""
    if "status: IN REVIEW" not in text or "director" not in text.lower():
        errors.append(f"open-stack substitution is not preserved as director decision gate: {adr}")

if errors:
    print("OPEN IDENTITY VALIDATION FAILED")
    for item in errors:
        print(f"ERROR: {item}")
    sys.exit(1)
print(
    f"OPEN IDENTITY VALIDATION PASSED ({len(oss)} V1 requirements, {len(components)} stack records)"
)
