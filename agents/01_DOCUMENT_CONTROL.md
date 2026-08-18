---
document_id: DRL-AGT-001
title: "Agent Mission 01: Repository Foundation and Document Control"
version: 3.0.0
status: APPROVED EXECUTION MISSION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Agent Mission 01: Repository Foundation and Document Control

    ## Mission objective

    Make the monorepo mechanically trustworthy: workspace/package scaffolding, document control, schemas/config validation, link checking, developer commands, CI foundation, and generated indexes. Do not implement domain behavior.

    This mission is executed on a dedicated feature branch and ends in a reviewable pull request. It is not permission to reinterpret the laboratory. The agent must read the root `LABORATORY_BIBLE.md`, `AGENTS.md`, decision register, current `WORKLOG.md`, and all prerequisites below before changing files.

    ## Entry prerequisites

    - Mission 00 backlog and ADR queue approved.
- Canonical directory layout accepted.
- Toolchain baseline uv, pnpm, Docker Compose, Terraform, and Python/TypeScript versions approved.

    If a prerequisite is absent, stale, contradictory, or unapproved, stop and create a blocker in the handoff ledger. Do not fill an architectural gap with an undocumented personal preference.

    ## Owned paths

    - pyproject.toml
- package.json
- pnpm-workspace.yaml
- Makefile
- scripts/**
- tests/**
- .github/workflows/**
- docs/**/INDEX.md
- `site/source-manifest.json` (generated in CI/release jobs; not tracked)
- historical validation reports and current CI evidence
- DOCUMENT_CONTROL.md

    Ownership means primary modification responsibility for this mission. Small necessary changes outside these paths require explicit notation in the worklog; changes to another project's public contract require its owner mission or an ADR.

    ## Forbidden or protected paths

    - Do not modify `LABORATORY_BIBLE.md` except through an approved constitutional ADR.
- Do not commit credentials, private files, employer material, unlicensed corpora, model weights without release policy, or generated secrets.
- Do not weaken security, privacy, evaluation, accessibility, or open-weight requirements to make a demo pass.
- Do not mark a feature or metric complete without evidence.
- Do not implement business logic or UI.
- Do not alter protocol semantics; validate only the approved contracts.

    ## Required work packages

    ### WP-01-01: Create one-command setup, lint, typecheck, unit, contract, docs, and validation targets.
### WP-01-02: Implement controlled-document frontmatter, ID, status, link, and reference validators.
### WP-01-03: Validate all JSON Schemas, YAML configuration, OpenAPI, and example fixtures.
### WP-01-04: Create generated specification, ADR, requirement, schema, package, and agent indexes.
### WP-01-05: Establish Python and TypeScript workspace packages with minimal compilable skeletons.
### WP-01-06: Build fast CI with cache and artifact publication; create slower scheduled/full workflow placeholders with explicit gates.
### WP-01-07: Generate SBOM and license inventory foundations.

    Each work package must produce implementation or controlled-document changes, tests or validation evidence, and a worklog entry. Create focused commits after each coherent package.

    ## ADR and director approval triggers

    - Changing language/package managers or monorepo topology.
- Changing document authority/status semantics.
- Adding a build service that creates vendor lock-in.
- Relaxing validation for approved documents.

    For each trigger, write the ADR first, mark it `PROPOSED`, identify alternatives and consequences, and wait for the Director's approval before implementation. The agent may prepare a nonbinding spike in an isolated path if the ADR explicitly allows it.

    ## Verification matrix

    - Fresh clone setup on Linux CI and documented Windows path.
- Python format/lint/type/test and TypeScript format/lint/type/test.
- Broken-link and duplicate-document-ID seeded failure.
- Schema/YAML invalid fixture seeded failure.
- Secret scan, dependency audit, and license inventory smoke test.

    Record exact commands, environment, revision, outcomes, skipped checks, and artifact locations. “Tests passed” without commands and evidence is insufficient.

    ## Pull-request deliverables

    - Compilable monorepo skeleton.
- Deterministic developer command reference.
- Deep validation report and manifest.
- CI workflows and seeded negative tests.
- Generated documentation indexes.

    The PR description maps each deliverable to requirement IDs and acceptance criteria, names every changed public contract, provides screenshots/reports where relevant, lists risks and limitations, and includes rollback/migration behavior.

    ## Handoff requirements

    - Provide exact commands and known platform gaps.
- List workspace/package names and generated files.
- Identify contract/schema issues for Mission 02 rather than editing semantics.
- Record CI duration and flaky/disabled checks.

    The next agent must be able to start without reconstructing unstated reasoning. The handoff identifies what is complete, what remains, what failed, decisions/ADRs, changed paths, test commands, produced artifacts, known debt, security/privacy effects, and exact recommended next issue.

    ## Stop conditions

    - Toolchain version or license conflict.
- A schema is semantically contradictory and needs architecture review.
- CI requires secret or paid resource for baseline.

    ## Definition of mission complete

    - all work packages are complete or explicitly deferred by approved decision;
    - owned documents and contracts are internally consistent;
    - required tests and evidence pass;
    - no critical TODO, placeholder, fake metric, unreviewed license, or silent security weakening remains;
    - feature branch is pushed and a focused PR is opened;
    - `WORKLOG.md` and the sequential handoff ledger are updated;
    - the next mission has a precise, executable starting point.
