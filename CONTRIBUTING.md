---
document_id: DRL-ROOT-CONTRIB
title: "Contributing to DeWitt Research Laboratory"
version: 3.2.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-08-01
---

# Contributing to DeWitt Research Laboratory

## Welcome and scope

DRL welcomes collaborators, tinkerers, students, academics, learners, teachers, and engineers. Contributions may include code, tests, connectors, evaluation tasks, datasets with clear rights, documentation, replications, teaching materials, accessibility improvements, security reports, and research criticism.

## Contributor routes (start here)

1. Read this file and `docs/09-open-source/CONTRIBUTOR_ROUTES.md`.
2. Run the tested setup: `make doctor`, `make demo`, `make verify`.
3. Pick a **good first issue** seed (GFI-001…GFI-005) or open one with the Good first issue template.
4. Reserve work in issues before substantial changes; identify requirement IDs and evidence.
5. Follow recognition rules in `docs/09-open-source/CONTRIBUTOR_CREDIT_AND_AUTHORSHIP.md`.

Sponsors do not control roadmap, review, benchmarks, or research conclusions.

## Before opening code

1. Read the Laboratory Bible and the relevant component specification.
2. Search issues and the roadmap; reserve an issue before substantial work.
3. Use the issue template and identify requirement IDs, data classes, risk, dependencies, public-contract impact, and evidence.
4. Discuss architecture, security authority, new data/model sources, or public API changes before implementation. These may require an ADR.
5. Never submit confidential institutional, private/personal, scraped-without-rights, credential-bearing, or provenance-free material.

## Development environment

The supported baseline uses Python 3.12, `uv`, Node/pnpm, Docker Compose, Bash or PowerShell wrappers, Terraform, and Git. The mock/local profile must run without paid APIs. Follow root setup commands; component READMEs may add scoped commands but must not contradict them.

```bash
make bootstrap
make verify
make test
```

A contribution that requires an undisclosed cloud account, key, private dataset, or local manual patch is not reproducible and is not ready for review.

## Branches and commits

- Use a focused feature branch such as `contrib/<issue>-<scope>`.
- Keep commits coherent and reviewable; explain why, not only what.
- Avoid drive-by formatting or unrelated dependency upgrades.
- Preserve generated artifact provenance and do not commit large weights/data without an approved release path.

## Pull-request evidence

A PR must include:

- linked issue and requirement IDs;
- behavior and non-goals;
- contracts or migrations changed;
- tests and exact commands;
- EvalForge suite/threshold where applicable;
- security, privacy, accessibility, license, and cost impact;
- screenshots/traces/reports/manifests when relevant;
- rollback/failure behavior;
- documentation and changelog updates;
- limitations and follow-on work.

## Quality expectations

- Typed, formatted, linted, and tested code.
- Deterministic calculations and reproducible research artifacts.
- Fail-closed authorization and explicit data handling.
- No fabricated metrics, citations, or “live” claims.
- Accessible interfaces and truthful loading/failure states.
- Stable APIs or documented versions/migrations.
- Tests for success, denial, malformed input, timeout, retry, cancellation, and recovery—not only happy paths.

Coverage is an indicator, not the goal. Security policy, protocol schemas, deterministic calculations, and data transformations require especially strong branch/property/golden coverage. UI work requires end-to-end and accessibility evidence in addition to unit tests.

## Data, model, and research contributions

Every source needs identity, rights/terms, provenance, acquisition date, transformations, review class, privacy assessment, and release permissions. Synthetic data must identify the generator and review method. Benchmark submissions must address contamination. Model changes require pinned recipes, artifacts/checksums, baselines, statistical comparisons, model cards, and upstream-license review.

## Contributor recognition and maintainership

Contributors retain attribution under repository history and release notes. Sustained contributors may be invited as reviewers or maintainers under `GOVERNANCE.md`. Titles are earned through demonstrated stewardship; contribution does not imply employment, institutional affiliation, or authority to represent DRL.

## Conduct and support

Follow `CODE_OF_CONDUCT.md`. Use public issues/discussions for non-sensitive support. Report vulnerabilities privately through the process in `SECURITY.md`; do not publish exploitable details before coordinated disclosure.

## Review paths by contribution type

### Compatible code or documentation change

A maintainer may review and merge after required checks and ownership review. Public behavior, stored data, permissions, and release claims must remain unchanged or be updated compatibly.

### New tool, skill, connector, evaluator, or scenario

Provide a manifest, threat/data/license assessment, fixtures, positive and negative tests, example, documentation, and ownership. Tools additionally declare effect, risk tier, scopes, network/data policy, approval policy, idempotency, timeout, and output limits. Connectors require rights/source review. Evaluators require scoring validity and calibration where subjective.

### Architecture or public-contract change

Open an ADR/RFC first. Include alternative approaches, affected consumers, migration, compatibility window, operational and cost impact, and rollback. Prototype code may be accepted only in an isolated experimental path and cannot become a dependency before approval.

### Model or dataset change

Open a research issue with hypothesis, baseline, data/source rights, contamination plan, experiment design, compute budget, release implications, and stopping rule. Upload large artifacts to the approved registry/storage—not Git—and reference immutable digests.

## Dependency policy

New dependencies require a reason, current maintenance/security assessment, license compatibility, size/runtime effect, and why existing platform capabilities are insufficient. Pin direct dependencies through lockfiles. Automated upgrades still require tests and review. Avoid packages whose sole purpose is trivial code DRL can safely own, but do not reimplement security-sensitive primitives casually.

## Documentation discipline

Update the controlling specification when behavior changes, not merely the README. Examples must be executable or validated. Use exact status and maturity language. “Implemented,” “secure,” “real-time,” “accurate,” “open source,” and “production-ready” are evidence-bearing claims. Draft research distinguishes hypotheses, methods, results, interpretation, and limitations.

## Review response and iteration

Review comments should identify the requirement or engineering principle at issue and distinguish blocker, important improvement, question, and optional suggestion. Authors should answer or resolve each thread; silently marking threads resolved is not review. Large changes may be split by work package. Maintainers may close abandoned PRs after notice while preserving credit and inviting a smaller restart.

## Local and cloud safety

Tests and examples use fixtures and disposable development resources. Do not point development commands at a production project by default. Cloud-mutating scripts require explicit project/environment, dry-run where feasible, least-privilege identity, budget awareness, and teardown. Local-runner tests use synthetic directories/repositories and never crawl a contributor's home directory by default.

## Open research alignment

This document is interpreted with the root `OPEN_RESEARCH_CHARTER.md` and the controlled standards in `docs/09-open-source/`.

## Open-research contribution lanes

Contributors may participate through code, model/runtime work, data stewardship, evaluation, security, documentation, accessibility, teaching, independent replication, or upstream maintenance. Review the Open Research Charter and credit policy before contributing. Every PR identifies upstream dependencies changed, artifact/license impact, reproducibility evidence, and whether generally useful work should be proposed upstream.
