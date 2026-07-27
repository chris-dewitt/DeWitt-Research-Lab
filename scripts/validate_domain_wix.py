#!/usr/bin/env python3
"""Validate canonical domain and Wix institutional-site contracts."""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []


def req(rel):
    p = ROOT / rel
    if not p.exists():
        errors.append(f"missing: {rel}")
    return p


required = [
    "docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md",
    "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md",
    "docs/08-web-brand/WIX_EDITOR_HANDOFF_CHECKLIST.md",
    "docs/07-platform-gcp/DOMAIN_DNS_AND_WIX_RUNBOOK.md",
    "docs/adr/ADR-0008-wix-canonical-public-site.md",
    "configs/domain-routing.yaml",
]
for r in required:
    req(r)
config = yaml.safe_load((ROOT / "configs/domain-routing.yaml").read_text())
if config.get("canonical_origin") != "https://www.dwit-labs.com":
    errors.append("wrong canonical origin")
if config.get("institutional_site", {}).get("platform") != "Wix":
    errors.append("Wix not recorded as platform")
if config.get("policies", {}).get("primary_apps_embedded_in_wix") is not False:
    errors.append("primary apps must not be iframe-only")
hosts = [a.get("host") for a in config.get("applications", [])]
for h in ("atticus.dwit-labs.com", "docs.dwit-labs.com", "status.dwit-labs.com"):
    if h not in hosts:
        errors.append(f"missing planned host: {h}")
for rel in (
    "README.md",
    "LABORATORY_BIBLE.md",
    "docs/08-web-brand/HOMEPAGE_SPEC.md",
    "docs/12-acceptance/V1_RELEASE_CRITERIA.md",
):
    text = (ROOT / rel).read_text()
    if "www.dwit-labs.com" not in text:
        errors.append(f"canonical domain absent: {rel}")
requirements = yaml.safe_load((ROOT / "requirements/requirements.yaml").read_text())["requirements"]
ids = {r["id"] for r in requirements}
for rid in (
    "DRL-WEB-011",
    "DRL-WEB-012",
    "DRL-WEB-013",
    "DRL-PLT-011",
    "DRL-PLT-012",
    "DRL-SEC-013",
):
    if rid not in ids:
        errors.append(f"missing requirement: {rid}")
if errors:
    print("DOMAIN/WIX VALIDATION FAILED")
    for e in errors:
        print("ERROR:", e)
    sys.exit(1)
print("DOMAIN/WIX VALIDATION PASSED")
