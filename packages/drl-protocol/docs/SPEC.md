---
document_id: DRL-PKG-001
title: "DRL Protocol Package"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-27
---

# DRL Protocol Package

## Purpose

Provide the canonical, versioned Python and TypeScript representations of DRL JSON Schema contracts plus validation, serialization, compatibility, digest, and migration utilities. It contains no business logic, network calls, model calls, policy decisions, or database access.

## Required capabilities and invariants

- Generate Pydantic and TypeScript types from canonical schemas or verify hand-maintained equivalence.
- Resolve canonical `$id` references and validate examples.
- Enforce deterministic canonical JSON/digest rules.
- Provide compatibility tests and explicit migrations.
- Publish schema bundle and language packages with aligned semantic versions.

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

- `schemas`: package and resolve the canonical schema bundle.
- `models`: generated/verified Python and TypeScript types.
- `state_machine`: legal Atticus `RunState` transitions, terminal-state helpers,
  and illegal-transition rejection used by orchestrators and contract tests.
- `validation`: strict validation with typed path-aware errors.
- `canonical`: canonical JSON profile and `sha256:` digest helpers.
- `compatibility`: compare old/new schemas and supported-version matrix.
- `migration`: explicit pure transformations between supported versions.
- `examples`: load and round-trip contract fixtures.

Public functions must be deterministic and side-effect free except explicit file loading. Unknown fields, enum values, invalid formats, duplicate IDs, or mismatched digests fail with stable DRL error codes. Validation errors must not echo sensitive payloads by default.

## Canonicalization and signatures

The package specifies Unicode normalization, key ordering, number representation, excluded signature fields, and media type for digesting. Signature verification is separate from digest comparison. Consumers never compute a digest from pretty-printed or language-native representations without canonical serialization.

## Cross-language parity

Python and TypeScript encode the same required/optional/null semantics, enums, formats, and defaults. Round-trip tests use golden examples and fuzz/property cases. Generated code is reproducible and checked for drift in CI. Language packages cannot add silent defaults that change signed or persisted content.
