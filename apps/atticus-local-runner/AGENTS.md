---
document_id: DRL-SUB-LOC
title: "Atticus Local Runner Agent Instructions"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Atticus Local Runner Agent Instructions

This file supplements the repository-wide `AGENTS.md`. Read the controlling component `docs/SPEC.md`, laboratory-wide specifications, current mission, worklog, and ADRs before changes. This subtree is not an isolated product: preserve DRL protocol, identity, policy, consent, provenance, trace, evaluation, open-weight, accessibility, licensing, and release invariants.

## Working rules

- Change public contracts only through coordinated versioned review.
- Add tests for success, malformed input, denial/authorization, timeout, cancellation, retry/idempotency, recovery, and sensitive-data handling as relevant.
- Update the component specification, examples, evaluation, security, roadmap, and requirement links when behavior changes.
- Use fixtures and mocks by default; never require private data or a production cloud project for tests.
- Record exact commands and evidence in the mission handoff and PR.
- Stop for ADR/director approval on scope, trust-boundary, data/model source, license, cost, or incompatible API decisions.


## Subtree authority and invariants

Own outbound-only device transport, pairing/revocation, OS-protected credentials, local open-weight inference adapters, voice, approved-directory file/repository tools, command sandbox, private memory, local audit, installation/update/removal, and network/data evidence. Default deny. Never scan broad user directories, open inbound ports, record audio invisibly, or send local content to cloud without explicit workflow approval and minimum-payload policy.

Use synthetic local fixtures and clean Windows test environments. Security tests must include traversal/symlink, injection, malicious repo, secret redaction, replay, revoked device, offline mode, and cloud-disconnect behavior.
