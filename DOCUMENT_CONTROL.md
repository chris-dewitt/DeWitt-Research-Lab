---
document_id: DRL-ROOT-DOCCTRL
title: "Document Control and Authority"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Document Control and Authority

## Purpose

DRL is documentation-first but not documentation-bound. Controlled documents state authority, version, status, owner, and update date; machine contracts and tests enforce the most important behavior. Stale or contradictory documentation is a defect.

## Status vocabulary

- `DRAFT` — incomplete and non-authoritative.
- `IN REVIEW` — proposed; implementation must not depend on it as settled.
- `APPROVED FOUNDATION` — approved design/requirement for implementation.
- `APPROVED EXECUTION MISSION` — authorized agent work scope.
- `RELEASE CANDIDATE` — frozen for independent validation.
- `PUBLIC RELEASE` — matches a published version/artifact.
- `SUPERSEDED` — retained for history and linked to successor.
- `ARCHIVED` — no longer maintained; not implied current.

## Identifier families

`DRL-PRG` program, `DRL-PRD` product, `DRL-ARC` architecture, `DRL-MOD` model, `DRL-DAT` data, `DRL-EVL` evaluation, `DRL-SEC` security, `DRL-PLT` platform, `DRL-WEB` web/brand, `DRL-OSS` open source, `DRL-RSH` research, `DRL-OPS` operations, `DRL-ACC` acceptance, `DRL-AGT` agent missions, plus component-specific identifiers.

## Change procedure

1. Identify controlling requirements/contracts and reason for change.
2. Determine whether an ADR or director approval is required.
3. Update all affected documents, schemas, tests, examples, migration notes, and traceability—not only one prose file.
4. Increment version according to impact: patch for clarification, minor for compatible requirement additions, major for incompatible semantic change.
5. Record change in worklog/changelog and link superseded material.
6. Re-run document and contract validation.

## Authority order

Laboratory Bible; approved ADR/director decisions; laboratory-wide controlled specifications; component specifications; machine-readable contracts/configuration; mission/worklog; implementation/tests; issues/conversation. A lower source cannot silently overrule a higher one. When evidence disproves a higher-level assumption, propose a controlled correction.

## Public synchronization

Repository documents are the source for the website documentation portal. Public release pages must identify the commit/version they render. Draft and private documents are excluded by explicit publishing metadata, not by obscurity.
