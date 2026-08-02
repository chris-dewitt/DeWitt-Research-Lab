---
document_id: DRL-PKG-004
title: "EvalForge SDK Package"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# EvalForge SDK Package

## Purpose

Provide case/suite definitions, target adapters, deterministic graders, calibrated model-judge interfaces, trace/trajectory scoring, statistical comparison, gate decisions, and machine/HTML reports suitable for local development and CI.

## Required capabilities and invariants

- Deterministic checks dominate authorization, schema, numerical, and citation-link validity.
- Model judges are versioned, calibrated, uncertainty-aware, and never sole arbiters of critical safety.
- Runs capture target/config/data/scorer digests and environment.
- Baseline/candidate comparisons include uncertainty and practical thresholds.
- Reports separate aggregate, slices, critical failures, and raw artifacts.

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

- `cases` and `suites`: versioned data models, loaders, filters, and validation.
- `targets`: local callable, HTTP, OpenAI-compatible, trace-import, and replay adapters.
- `graders`: invariant, schema, policy, tool/argument, trajectory, artifact, citation, numeric, latency, and cost graders.
- `judges`: optional calibrated model/human review interfaces.
- `runner`: deterministic scheduling, seeds, concurrency, retries, artifact capture, and resume.
- `statistics`: paired comparison, bootstrap intervals, multiple slices, practical thresholds.
- `gates`: critical-failure rules and baseline/candidate decision policy.
- `reports`: JSON, Markdown, HTML, JUnit, PR summary, and release manifest.

## Run reproducibility

A run records suite/case/target/scorer versions and digests, code revision, environment/container, random seeds, concurrency, timeouts, model configuration, tool catalog, policy, and artifact store. Resume never silently mixes incompatible configurations. Raw sensitive payload capture follows the evaluation environment's data policy.

## Statistical and judgment discipline

The SDK distinguishes missing result, system error, scorer error, abstention, and failed task. Aggregation cannot hide critical failures. Model judges report prompt/model/version, calibration set, agreement, and uncertainty. Human adjudication is versioned evidence. Release gates are configured before candidate results where practical.

## Operational readiness

Before publication, a clean consumer project must install the package, execute the documented example, receive stable typed errors for invalid input, and verify the built artifact against its source revision. The release notes identify supported Python/platform versions, deprecations, and any experimental interfaces.
