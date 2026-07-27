---
document_id: DRL-SUB-INFRA
title: "Infrastructure Agent Instructions"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Infrastructure Agent Instructions

This file supplements the repository-wide `AGENTS.md`. Read the controlling component `docs/SPEC.md`, laboratory-wide specifications, current mission, worklog, and ADRs before changes. This subtree is not an isolated product: preserve DRL protocol, identity, policy, consent, provenance, trace, evaluation, open-weight, accessibility, licensing, and release invariants.

## Working rules

- Change public contracts only through coordinated versioned review.
- Add tests for success, malformed input, denial/authorization, timeout, cancellation, retry/idempotency, recovery, and sensitive-data handling as relevant.
- Update the component specification, examples, evaluation, security, roadmap, and requirement links when behavior changes.
- Use fixtures and mocks by default; never require private data or a production cloud project for tests.
- Record exact commands and evidence in the mission handoff and PR.
- Stop for ADR/director approval on scope, trust-boundary, data/model source, license, cost, or incompatible API decisions.


## Subtree authority and invariants

Own Terraform modules/environment composition, deployment workflows, service identities, observability, budgets, backup/restore, and operational runbooks. Dev/stage/prod/research isolation and least privilege are mandatory. Never commit state/secrets, use wildcard admin roles, point default commands at production, or create always-on GPUs without approval.

Run formatting/validation/security/policy checks, disposable plan/apply/destroy, deployment/rollback smoke, restore drill, budget/alert test, and capture estimated/actual costs.
