---
document_id: DRL-SUB-WEB
title: "Lab Web Agent Instructions"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Lab Web Agent Instructions

This file supplements the repository-wide `AGENTS.md`. Read the controlling component `docs/SPEC.md`, laboratory-wide specifications, current mission, worklog, and ADRs before changes. This subtree is not an isolated product: preserve DRL protocol, identity, policy, consent, provenance, trace, evaluation, open-weight, accessibility, licensing, and release invariants.

## Working rules

- Change public contracts only through coordinated versioned review.
- Add tests for success, malformed input, denial/authorization, timeout, cancellation, retry/idempotency, recovery, and sensitive-data handling as relevant.
- Update the component specification, examples, evaluation, security, roadmap, and requirement links when behavior changes.
- Use fixtures and mocks by default; never require private data or a production cloud project for tests.
- Record exact commands and evidence in the mission handoff and PR.
- Stop for ADR/director approval on scope, trust-boundary, data/model source, license, cost, or incompatible API decisions.


## Subtree authority and invariants

Own the public Next.js laboratory experience, repository-driven content, design system, Atticus console client integration, demo replay, accessibility, performance, consent-aware analytics, and SEO. Do not implement server-side authority or fabricate live data. Every visible system status, model identity, benchmark result, and research claim must come from a controlled artifact or be clearly labeled as mock/replay.

Primary verification includes TypeScript checks, unit/component tests, browser end-to-end flows, accessibility audits, reduced-motion and keyboard checks, content-schema/link validation, visual regressions, performance budgets, and live-backend degradation tests.
