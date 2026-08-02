---
document_id: DRL-PRG-008
title: "Quality Management Plan"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Quality Management Plan

## Quality definition

A DRL component is high quality when it is useful, correct for its defined scope, secure, observable, reproducible, understandable, accessible, and honest about limitations. Attractive UI and benchmark scores are insufficient without operational evidence.

## Evidence pyramid

1. **Static evidence:** schema validation, type checks, lint, dependency and secret scans.
2. **Unit evidence:** domain, policy, calculation, and serialization tests.
3. **Contract evidence:** provider, service, and SDK compatibility tests.
4. **Integration evidence:** database, queue, storage, identity, and model-runtime tests.
5. **Trajectory evidence:** full Atticus tool/approval traces scored by EvalForge.
6. **System evidence:** live end-to-end workflows, load, failure injection, rollback.
7. **Human evidence:** usability, accessibility, reviewer calibration, research review.
8. **Operational evidence:** staging metrics, budget, incident and recovery drills.

## Release-blocking categories

- unauthorized side effect;
- cross-tenant leakage;
- secret exposure;
- incorrect deterministic calculation above documented tolerance;
- missing license rights for released artifact;
- benchmark contamination affecting claims;
- inability to roll back a production migration;
- inaccessible critical public flow;
- public claim lacking evidence;
- broken clean-checkout setup for the supported profile.

## Documentation quality

Controlled documents must define:

- purpose and scope;
- requirements and non-goals;
- actors/owners;
- inputs and outputs;
- normal and failure flows;
- security/privacy considerations;
- observability;
- testing and acceptance;
- open decisions and references.

The document checker verifies frontmatter, IDs, links, status, forbidden placeholders, and traceability. Human review verifies clarity and contradictions.

## Quality cadence

- Per commit: focused tests.
- Per PR: scope-specific gates and documentation.
- Nightly or scheduled: larger benchmarks and dependency scans.
- Per release candidate: complete security, evaluation, accessibility, migration, backup, and cost suites.
- Post-release: sampled production traces, incident review, drift and regression monitoring.
