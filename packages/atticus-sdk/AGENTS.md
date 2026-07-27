---
document_id: DRL-SUB-SDK
title: "Atticus SDK Agent Instructions"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Atticus SDK Agent Instructions

This file supplements the repository-wide `AGENTS.md`. Read the controlling component `docs/SPEC.md`, laboratory-wide specifications, current mission, worklog, and ADRs before changes. This subtree is not an isolated product: preserve DRL protocol, identity, policy, consent, provenance, trace, evaluation, open-weight, accessibility, licensing, and release invariants.

## Working rules

- Change public contracts only through coordinated versioned review.
- Add tests for success, malformed input, denial/authorization, timeout, cancellation, retry/idempotency, recovery, and sensitive-data handling as relevant.
- Update the component specification, examples, evaluation, security, roadmap, and requirement links when behavior changes.
- Use fixtures and mocks by default; never require private data or a production cloud project for tests.
- Record exact commands and evidence in the mission handoff and PR.
- Stop for ADR/director approval on scope, trust-boundary, data/model source, license, cost, or incompatible API decisions.


## Subtree authority and invariants

Own control-plane clients, tool/skill authoring interfaces, approval domain helpers, local-runner protocol helpers, and offline test harnesses. Tool registration requires risk/effect/scopes/approval/network/data/idempotency metadata and cannot grant permission. Clients preserve correlation, deadlines, consent, event resume, and typed failures without logging credentials/content.

Publish executable examples and compatibility tests against supported control-plane/protocol versions.
