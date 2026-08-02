---
document_id: DRL-OPS-003
title: "Release, Versioning, and Change Management"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Release, Versioning, and Change Management

## Release domains

Application, package, protocol, model, dataset, document, and infrastructure versions are distinct and collected in a laboratory release manifest.

## Release steps

- scope freeze and issue closure review;
- changelog and migration notes;
- complete CI and EvalForge gates;
- security/privacy/license review;
- stage deployment and integrated demo;
- backup/rollback test;
- artifact build, SBOM, hashes, signatures where available;
- director approval;
- production rollout and verification;
- publish source/model/data/docs/report;
- monitor and post-release review.

Emergency fixes follow abbreviated process but retain evidence and retrospective.
