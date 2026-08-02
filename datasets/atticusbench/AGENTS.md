---
document_id: DRL-SUB-ATB
title: "AtticusBench Agent Instructions"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# AtticusBench Agent Instructions

This file supplements the repository-wide `AGENTS.md`. Read the controlling component `docs/SPEC.md`, laboratory-wide specifications, current mission, worklog, and ADRs before changes. This subtree is not an isolated product: preserve DRL protocol, identity, policy, consent, provenance, trace, evaluation, open-weight, accessibility, licensing, and release invariants.

## Working rules

- Change public contracts only through coordinated versioned review.
- Add tests for success, malformed input, denial/authorization, timeout, cancellation, retry/idempotency, recovery, and sensitive-data handling as relevant.
- Update the component specification, examples, evaluation, security, roadmap, and requirement links when behavior changes.
- Use fixtures and mocks by default; never require private data or a production cloud project for tests.
- Record exact commands and evidence in the mission handoff and PR.
- Stop for ADR/director approval on scope, trust-boundary, data/model source, license, cost, or incompatible API decisions.


## Subtree authority and invariants

Own benchmark schemas/cases/fixtures, taxonomy, split/hidden-test controls, author/review workflow, contamination audit, baselines, release card/manifests, and leaderboard integrity. Never put private donated data directly into training/evaluation, expose hidden answers, let model judges solely decide critical safety, or tune thresholds after seeing a candidate without recorded rationale.

Every case has resettable state, declared policy/tool context, hard invariants, scorer versions, provenance/rights, review class, and content digest.
