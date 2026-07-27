---
document_id: DRL-AGT-900
title: "Sequential Agent Handoff Template"
version: 3.0.0
status: APPROVED OPERATING PROCEDURE
owner: DeWitt
last_updated: 2026-07-26
---

# Sequential Agent Handoff Template

Copy this template into `WORKLOG.md` at mission start and completion. A handoff is a reproducibility artifact, not a friendly summary.

## Handoff identity

- Mission / agent:
- Branch:
- Pull request:
- Starting commit:
- Ending commit:
- Started / completed UTC:
- Environment used:

## Objective and result

- Planned objective:
- Actual result:
- Status: `COMPLETE`, `PARTIAL`, `BLOCKED`, or `FAILED`
- Scope changes and approval reference:

## Work packages and requirements

| Work package | Requirement IDs | Status | Commits | Evidence |
|---|---|---|---|---|
| | | | | |

## Public contracts changed

List APIs, schemas, events, configuration, CLI, storage formats, model/data artifacts, or user-visible behavior. State `NONE` when applicable. Include version and migration implications.

## Decisions and assumptions

- ADRs created or updated:
- Director decisions consumed:
- Temporary assumptions:
- Assumptions invalidated:

## Verification

```text
Exact commands executed
```

| Check | Result | Artifact / log | Notes |
|---|---|---|---|
| | | | |

## Security, privacy, license, and cost impact

- New trust boundaries or permissions:
- Data classes touched:
- Telemetry/content capture changes:
- Third-party dependencies/licenses:
- Cloud cost or capacity impact:
- Threat tests performed:

## Known limitations and debt

Each item must include severity, owner mission, issue, and whether it blocks the next mission or V1.

## Dirty state and temporary resources

- Uncommitted files: `NONE` or list
- Temporary cloud resources and teardown status:
- Local data/checkpoints not in Git:
- Secrets or credentials created and storage location (never values):

## Next-agent start instructions

1. Checkout/pull instructions.
2. Commands to verify inherited state.
3. First recommended issue/work package.
4. Files/contracts that must not be changed casually.
5. Outstanding approvals/blockers.

## Attestation

I did not mark work complete without evidence, did not commit secrets/private/employer material, and documented all known contract, security, privacy, license, and cost effects.
