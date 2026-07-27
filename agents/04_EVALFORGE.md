---
document_id: DRL-AGT-004
title: "Agent Mission 04: EvalForge Foundation"
version: 3.0.0
status: APPROVED EXECUTION MISSION
owner: DeWitt
last_updated: 2026-07-26
---


    # Agent Mission 04: EvalForge Foundation

    ## Mission objective

    Implement the evaluation SDK, manifest schema, local runner, deterministic scorers, result store interface, comparison/statistics, report generator, CI gate, and target adapter contracts before optimizing Atticus or specialists.

    This mission is executed on a dedicated feature branch and ends in a reviewable pull request. It is not permission to reinterpret the laboratory. The agent must read the root `LABORATORY_BIBLE.md`, `AGENTS.md`, decision register, current `WORKLOG.md`, and all prerequisites below before changing files.

    ## Entry prerequisites

    - Protocol and security foundations merged.
- Project claim maps and AtticusBench task schema approved.
- Private/public dataset access tiers defined.

    If a prerequisite is absent, stale, contradictory, or unapproved, stop and create a blocker in the handoff ledger. Do not fill an architectural gap with an undocumented personal preference.

    ## Owned paths

    - services/evalforge/**
- packages/evalforge-sdk/**
- datasets/**/schemas/**
- docs/05-evaluation/**
- tests/evalforge/**
- .github/workflows/evals*.yml

    Ownership means primary modification responsibility for this mission. Small necessary changes outside these paths require explicit notation in the worklog; changes to another project's public contract require its owner mission or an ADR.

    ## Forbidden or protected paths

    - Do not modify `LABORATORY_BIBLE.md` except through an approved constitutional ADR.
- Do not commit credentials, private files, employer material, unlicensed corpora, model weights without release policy, or generated secrets.
- Do not weaken security, privacy, evaluation, accessibility, or open-weight requirements to make a demo pass.
- Do not mark a feature or metric complete without evidence.
- Do not publish private holdouts.
- Do not declare LLM judges authoritative.
- Do not tune models against protected release sets.

    ## Required work packages

    ### WP-04-01: Implement suite/case/target/scorer/gate manifests and validation.
### WP-04-02: Implement deterministic local execution and artifact recording.
### WP-04-03: Implement paired baseline/candidate analysis and bootstrap intervals.
### WP-04-04: Implement JSON, Markdown, HTML, JUnit, and PR-summary reports.
### WP-04-05: Implement accepted-baseline registry and manual promotion.
### WP-04-06: Implement target adapters for local function, HTTP, OpenAI-compatible endpoint, and trace import.
### WP-04-07: Implement CI gate with seeded pass/fail regressions.
### WP-04-08: Design judge/human-review interfaces and calibration records without making them release-critical yet.

    Each work package must produce implementation or controlled-document changes, tests or validation evidence, and a worklog entry. Create focused commits after each coherent package.

    ## ADR and director approval triggers

    - Changing statistical decision policy or critical-gate exception rules.
- Using a model judge without approved calibration.
- Changing private-holdout access.
- Publishing a leaderboard claim.

    For each trigger, write the ADR first, mark it `PROPOSED`, identify alternatives and consequences, and wait for DeWitt's approval before implementation. The agent may prepare a nonbinding spike in an isolated path if the ADR explicitly allows it.

    ## Verification matrix

    - Synthetic known-score framework self-tests.
- Statistical simulation and confidence interval tests.
- Adapter contract and malicious-output tests.
- Dataset access/canary tests.
- Seeded CI gate demonstration.
- Report digest/signature verification.

    Record exact commands, environment, revision, outcomes, skipped checks, and artifact locations. “Tests passed” without commands and evidence is insufficient.

    ## Pull-request deliverables

    - Installable EvalForge SDK/CLI.
- Fast CI suite and full-suite job interface.
- Comparison and report examples.
- Baseline registry and gate evidence.
- Documentation for every project owner to add a claim suite.

    The PR description maps each deliverable to requirement IDs and acceptance criteria, names every changed public contract, provides screenshots/reports where relevant, lists risks and limitations, and includes rollback/migration behavior.

    ## Handoff requirements

    - Provide exact evaluator integration contract to all missions.
- List missing domain-specific suites.
- Record performance/cost and private holdout access.
- Name judge-calibration work remaining.

    The next agent must be able to start without reconstructing unstated reasoning. The handoff identifies what is complete, what remains, what failed, decisions/ADRs, changed paths, test commands, produced artifacts, known debt, security/privacy effects, and exact recommended next issue.

    ## Stop conditions

    - Statistical behavior disagrees with specification.
- Private datasets cannot be isolated.
- The gate can be bypassed or report can be forged.

    ## Definition of mission complete

    - all work packages are complete or explicitly deferred by approved decision;
    - owned documents and contracts are internally consistent;
    - required tests and evidence pass;
    - no critical TODO, placeholder, fake metric, unreviewed license, or silent security weakening remains;
    - feature branch is pushed and a focused PR is opened;
    - `WORKLOG.md` and the sequential handoff ledger are updated;
    - the next mission has a precise, executable starting point.
