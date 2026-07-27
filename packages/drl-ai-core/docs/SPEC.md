---
document_id: DRL-PKG-002
title: "DRL AI Core Package"
version: 3.2.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-27
---

# DRL AI Core Package

## Purpose

Provide carefully bounded shared infrastructure used by more than one component: model-provider abstractions, structured-output validation, retries/deadlines/cancellation, tracing, provenance helpers, safe redaction, configuration, cost accounting, and deterministic IDs/digests.

## Required capabilities and invariants

- Avoid a “god package”; project-specific domain logic stays in its service.
- Provider interfaces disclose model identity and never silently route to closed weights in the V1 production path.
- Retry utilities require idempotency declarations.
- Redaction is defense-in-depth, not permission to capture private content.
- Every public utility has unit/property tests and stable error semantics.

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

- `providers`: open-weight model endpoint interfaces, identity disclosure, and
  typed completion constraints/errors.
- `mock_provider`: deterministic unpaid open-weight fixture provider for local
  development and CI.
- `gateway`: disclosed primary/fallback routing that rejects silent closed-weight
  substitution on open-weight paths.
- `structured_output`: schema-constrained parse/repair with bounded attempts and
  content-minimized trace evidence. Untrusted model text is never elevated into
  system/policy instructions during repair; `$schema`/`$id` on instances cannot
  redefine the fixed control-plane schema; repair budgets are hard caps.
- `execution`: deadlines, cancellation, retry budgets, circuit breakers, and idempotency declarations.
- `telemetry`: content-minimized logs/traces/metrics and correlation propagation.
- `provenance`: source/artifact/claim binding helpers.
- `redaction`: deterministic configurable secret/PII defense-in-depth.
- `cost`: token/compute/storage/network attribution and budget signals.
- `config`: typed layered configuration with explicit environment provenance.

## Provider and failure semantics

Provider calls return model identity, revision, quantization/runtime profile, timing, token/compute usage, finish reason, and structured errors. A fallback is policy, not exception handling: callers state eligible routes and disclosure. Timeouts and cancellation propagate. Retries are bounded and occur only when side effects are absent or idempotent.

## Dependency boundaries

The package may depend on `drl-protocol` but not on applications or specialist services. It cannot import domain models from Atlas/FedLens/BalanceLab, persist session content, or become a service locator. Extraction requires at least two real consumers and a named maintainer.

## Operational readiness

Before publication, a clean consumer project must install the package, execute the documented example, receive stable typed errors for invalid input, and verify the built artifact against its source revision. The release notes identify supported Python/platform versions, deprecations, and any experimental interfaces.
