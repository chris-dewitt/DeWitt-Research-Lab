---
document_id: DRL-GCP-013
title: "CI/CD, Environments, and Release Deployment"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# CI/CD, Environments, and Release Deployment

## Pull request

- document/schema checks;
- Python/TypeScript lint, type, tests;
- security/dependency/IaC scan;
- build containers and web;
- contract tests;
- sampled EvalForge suite;
- Terraform format/validate/plan for infra changes;
- preview assets where safe.

## Merge

- publish internal images by digest;
- deploy dev;
- migrate dev;
- smoke and integration tests;
- record deployment manifest.

## Release candidate

- signed tag;
- deploy stage with immutable artifacts;
- migration rehearsal;
- full evaluation/security/accessibility/load/cost suites;
- backup/rollback drill;
- release evidence review.

## Production

- protected approval;
- deploy backward-compatible migrations;
- gradual traffic or canary;
- verify SLO and integrated workflow;
- promote traffic;
- publish release notes/artifacts;
- roll back on predefined triggers.
