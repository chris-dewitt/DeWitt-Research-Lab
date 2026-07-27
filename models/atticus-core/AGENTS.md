---
document_id: DRL-SUB-MODC
title: "Atticus Core Model Agent Instructions"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Atticus Core Model Agent Instructions

This file supplements the repository-wide `AGENTS.md`. Read the controlling component `docs/SPEC.md`, laboratory-wide specifications, current mission, worklog, and ADRs before changes. This subtree is not an isolated product: preserve DRL protocol, identity, policy, consent, provenance, trace, evaluation, open-weight, accessibility, licensing, and release invariants.

## Working rules

- Change public contracts only through coordinated versioned review.
- Add tests for success, malformed input, denial/authorization, timeout, cancellation, retry/idempotency, recovery, and sensitive-data handling as relevant.
- Update the component specification, examples, evaluation, security, roadmap, and requirement links when behavior changes.
- Use fixtures and mocks by default; never require private data or a production cloud project for tests.
- Record exact commands and evidence in the mission handoff and PR.
- Stop for ADR/director approval on scope, trust-boundary, data/model source, license, cost, or incompatible API decisions.


## Subtree authority and invariants

Own Core candidate metadata, training recipes/configuration, checkpoints/manifests, evaluation/safety/license reports, quantization profiles, model card, and public release artifacts. Base selection follows the bakeoff ADR; no model is assumed from popularity. Data manifests and upstream terms are required before training/release. Never commit large weights or private/local-personal data to Git.

Compare upstream baseline and release candidate across capability, routing/tool/argument, permissions, injection, grounding, code/research, latency, memory, and quantization slices with reproducible statistics.
