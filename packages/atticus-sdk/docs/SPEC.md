---
document_id: DRL-PKG-003
title: "Atticus SDK Package"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Atticus SDK Package

## Purpose

Provide clients, tool/skill authoring interfaces, local-runner protocol helpers, approval UI/domain types, and test harnesses for integrating with Atticus without importing control-plane internals.

## Required capabilities and invariants

- Tool authors declare scopes, risk/effects, timeout, network/data policy, schemas, and retry safety.
- Skills are versioned declarative workflows with bounded steps and evaluation suites.
- Clients preserve correlation, deadlines, consent, provenance, and typed errors.
- Provide mock control plane and policy fixtures for offline development.
- SDK cannot grant permission or bypass approval.

## Public surface

The package exposes the smallest stable public surface required by consumers. All inputs/outputs use DRL protocol schemas where a canonical contract exists. Exceptions must be documented, typed, and non-conflicting. Public APIs include examples, failure semantics, deprecation policy, and migration notes.

## Versioning

Semantic versions reflect public behavior. A breaking protocol/schema change requires a major version, migration, compatibility matrix, consumer updates, and approved ADR. Pre-1.0 releases may evolve faster but cannot silently reinterpret persisted or signed artifacts.

## Testing and release evidence

- unit and property tests for core invariants;
- schema/type/example and cross-language round trips where applicable;
- compatibility tests against supported versions;
- security/abuse tests for untrusted input;
- package build/install from clean environment;
- generated SBOM/source/license register;
- signed or checksummed release artifacts;
- README/tutorial executed against the released version.

## Non-goals

The package is not permission to centralize unrelated project logic, add hidden network access, store user content, or create circular dependencies. Shared code is extracted only when semantics are genuinely shared and ownership is clear.

## Module and API plan

- `client`: sync/async control-plane client, SSE event stream, cancellation, and typed errors.
- `tools`: decorators/builders that emit valid tool manifests and adapters.
- `skills`: manifest authoring, validation, test fixtures, and compatibility.
- `approvals`: render-neutral approval request/grant domain helpers.
- `local`: device capability, pairing, signed transport, and result envelopes.
- `testing`: mock sessions, policy decisions, tool failures, replay, and golden traces.

## Tool author contract

A tool supplies input/output schemas, semantic version, effect type, risk tier, scopes, approval policy, timeout, network destinations, data classes, retry/idempotency behavior, safe preview, and redaction strategy. Registration fails when required safety metadata is absent. Tool descriptions are untrusted model context and cannot redefine policy.

## Client guarantees

Clients generate/propagate correlation and idempotency values, honor deadlines, surface policy/approval as distinct states, resume event streams safely, and never treat an interrupted stream as task success. Authentication and private payloads are not logged. Public SDK examples run against deterministic mocks.

## Operational readiness

Before publication, a clean consumer project must install the package, execute the documented example, receive stable typed errors for invalid input, and verify the built artifact against its source revision. The release notes identify supported Python/platform versions, deprecations, and any experimental interfaces.
