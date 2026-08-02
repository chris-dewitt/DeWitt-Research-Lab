---
document_id: DRL-SUB-CON
title: "Atticus Console Agent Instructions"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Atticus Console Agent Instructions

This file supplements the repository-wide `AGENTS.md`. Read the controlling component `docs/SPEC.md`, laboratory-wide specifications, current mission, worklog, and ADRs before changes. This subtree is not an isolated product: preserve DRL protocol, identity, policy, consent, provenance, trace, evaluation, open-weight, accessibility, licensing, and release invariants.

## Working rules

- Change public contracts only through coordinated versioned review.
- Add tests for success, malformed input, denial/authorization, timeout, cancellation, retry/idempotency, recovery, and sensitive-data handling as relevant.
- Update the component specification, examples, evaluation, security, roadmap, and requirement links when behavior changes.
- Use fixtures and mocks by default; never require private data or a production cloud project for tests.
- Record exact commands and evidence in the mission handoff and PR.
- Stop for ADR/director approval on scope, trust-boundary, data/model source, license, cost, or incompatible API decisions.


## Subtree authority and invariants

Own the reusable console UI/state machine for request, planning, tool events, policy, approval, evidence, calculation, evaluation, cancellation, terminal result, and replay. Treat server events as untrusted/versioned input. Never infer success from a closed stream or grant authority in client state. Approval UI must display action, target, effect, scopes, expiry, and request digest context and must invalidate stale decisions.

Test reconnect/resume, duplicate/out-of-order events, policy denial, expired approval, cancellation races, screen readers, keyboard-only use, slow networks, and mobile layouts.
