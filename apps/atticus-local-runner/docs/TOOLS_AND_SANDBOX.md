---
document_id: DRL-LOC-107
title: "Local Runner Tools and Sandbox"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Local Runner Tools and Sandbox

## Capability tiers

- **Observe:** approved directory metadata/search, Git status/log/diff, tool availability.
- **Read:** explicit file chunks or repository artifacts under size/content limits.
- **Draft:** temporary patch, command plan, email/calendar draft, report.
- **Modify:** approved file writes, staging, local artifact creation.
- **External effect:** commit, push, send, install, open external app/URL, or modify calendar; explicit approval.
- **Prohibited by default:** privilege escalation, credential export, disabling security, broad recursive destruction, arbitrary downloaded executables.

## Sandbox contract

A command runs with a clean bounded environment, explicit working directory, executable/profile allowlist, wall/CPU/memory/output/process limits, disabled network unless its profile permits it, and process-tree cleanup. Paths are canonicalized after symlink/junction resolution and rechecked before each operation. The model cannot construct a raw command that bypasses the typed tool layer.

## Files and repositories

Writes are atomic where practical and produce a diff. Special/device files are rejected. Size and count are bounded. Binary changes require a specialized reviewed tool. Repository reads may be autonomous inside an approved root. Patch application requires a preview; commit and push are separate approvals. Force push, history rewrite, hook execution, destructive clean, and secrets exposure are prohibited by default.

## Plugin manifest

A plugin declares name/version/signature, entry point, input/output schemas, permissions, resource selectors, egress destinations, data handling, supported platforms, health check, and tests. Installation is explicit. Updates may not expand permissions silently and must support rollback.
