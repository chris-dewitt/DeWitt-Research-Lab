---
document_id: DRL-SUB-CORE
title: "DRL AI Core Package Agent Instructions"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# DRL AI Core Package Agent Instructions

This file supplements the repository-wide `AGENTS.md`. Read the controlling component `docs/SPEC.md`, laboratory-wide specifications, current mission, worklog, and ADRs before changes. This subtree is not an isolated product: preserve DRL protocol, identity, policy, consent, provenance, trace, evaluation, open-weight, accessibility, licensing, and release invariants.

## Working rules

- Change public contracts only through coordinated versioned review.
- Add tests for success, malformed input, denial/authorization, timeout, cancellation, retry/idempotency, recovery, and sensitive-data handling as relevant.
- Update the component specification, examples, evaluation, security, roadmap, and requirement links when behavior changes.
- Use fixtures and mocks by default; never require private data or a production cloud project for tests.
- Record exact commands and evidence in the mission handoff and PR.
- Stop for ADR/director approval on scope, trust-boundary, data/model source, license, cost, or incompatible API decisions.


## Subtree authority and invariants

Own genuinely shared provider, structured-output, execution control, tracing, provenance, redaction, cost, and typed configuration utilities used by multiple components. Do not turn the package into a service locator or domain dumping ground. Provider routing discloses model identity and follows open-weight policy; retries honor idempotency and cancellation.

Every extraction names real consumers, dependency direction, stable error semantics, tests, and removal/migration from original owners.
