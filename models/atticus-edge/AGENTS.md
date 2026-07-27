---
document_id: DRL-SUB-MODE
title: "Atticus Edge Model Agent Instructions"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Atticus Edge Model Agent Instructions

This file supplements the repository-wide `AGENTS.md`. Read the controlling component `docs/SPEC.md`, laboratory-wide specifications, current mission, worklog, and ADRs before changes. This subtree is not an isolated product: preserve DRL protocol, identity, policy, consent, provenance, trace, evaluation, open-weight, accessibility, licensing, and release invariants.

## Working rules

- Change public contracts only through coordinated versioned review.
- Add tests for success, malformed input, denial/authorization, timeout, cancellation, retry/idempotency, recovery, and sensitive-data handling as relevant.
- Update the component specification, examples, evaluation, security, roadmap, and requirement links when behavior changes.
- Use fixtures and mocks by default; never require private data or a production cloud project for tests.
- Record exact commands and evidence in the mission handoff and PR.
- Stop for ADR/director approval on scope, trust-boundary, data/model source, license, cost, or incompatible API decisions.


## Subtree authority and invariants

Own Edge selection/distillation/fine-tuning, low-latency routing/tool/approval/voice-command behavior, escalation thresholds, local quantization/runtime matrix, evaluation, model card, and release artifacts. Edge must abstain/escalate rather than hallucinate unsupported complex work. Preserve privacy and offline operation targets.

Test on documented hardware profiles and quantify routing correctness, false non-escalation, permission behavior, latency, memory, energy/resource use where measurable, and degraded/offline paths.
