---
document_id: DRL-AGT-003
title: "Agent Mission 03: Security, Privacy, Policy, and Identity"
version: 3.0.0
status: APPROVED EXECUTION MISSION
owner: DeWitt
last_updated: 2026-07-26
---


    # Agent Mission 03: Security, Privacy, Policy, and Identity

    ## Mission objective

    Implement deterministic authorization and policy evaluation, risk tiers, approval binding, privacy/telemetry controls, threat-model test harnesses, identity abstractions, secret handling standards, and abuse/cost guardrails.

    This mission is executed on a dedicated feature branch and ends in a reviewable pull request. It is not permission to reinterpret the laboratory. The agent must read the root `LABORATORY_BIBLE.md`, `AGENTS.md`, decision register, current `WORKLOG.md`, and all prerequisites below before changing files.

    ## Entry prerequisites

    - Protocol packages merged.
- Threat model and data classification approved.
- Identity provider choice is either approved or kept behind an adapter.

    If a prerequisite is absent, stale, contradictory, or unapproved, stop and create a blocker in the handoff ledger. Do not fill an architectural gap with an undocumented personal preference.

    ## Owned paths

    - packages/policy/**
- packages/security/**
- packages/identity/**
- configs/risk-tiers.yaml
- configs/tool-policy.yaml
- configs/telemetry.yaml
- configs/retention.yaml
- configs/quotas.yaml
- docs/06-security/**
- tests/security/**

    Ownership means primary modification responsibility for this mission. Small necessary changes outside these paths require explicit notation in the worklog; changes to another project's public contract require its owner mission or an ADR.

    ## Forbidden or protected paths

    - Do not modify `LABORATORY_BIBLE.md` except through an approved constitutional ADR.
- Do not commit credentials, private files, employer material, unlicensed corpora, model weights without release policy, or generated secrets.
- Do not weaken security, privacy, evaluation, accessibility, or open-weight requirements to make a demo pass.
- Do not mark a feature or metric complete without evidence.
- Do not implement unrestricted shell or local tools.
- Do not make model output an authorization input beyond untrusted risk hints.
- Do not collect content under generic analytics.

    ## Required work packages

    ### WP-03-01: Implement rule-driven deny-by-default policy engine.
### WP-03-02: Implement resource/action scope normalization and risk classification.
### WP-03-03: Implement approval request/grant digest binding, expiry, versioning, and revocation.
### WP-03-04: Implement consent snapshot, telemetry filtering, and content-capture separation.
### WP-03-05: Implement quota/budget/circuit-breaker primitives.
### WP-03-06: Implement identity/session/service principal adapters and authorization helpers.
### WP-03-07: Build security fixtures for injection, replay, cross-session access, egress, and secret redaction.
### WP-03-08: Produce threat-model-to-control-to-test matrix and incident hooks.

    Each work package must produce implementation or controlled-document changes, tests or validation evidence, and a worklog entry. Create focused commits after each coherent package.

    ## ADR and director approval triggers

    - Changing public/private/local data boundaries.
- Allowing an R3/R4 action without approved policy.
- Selecting long-term retention or analytics content capture beyond approved config.
- Changing identity or key architecture.
- Introducing a new external egress category.

    For each trigger, write the ADR first, mark it `PROPOSED`, identify alternatives and consequences, and wait for DeWitt's approval before implementation. The agent may prepare a nonbinding spike in an isolated path if the ADR explicitly allows it.

    ## Verification matrix

    - Policy table allow/deny/approval cases.
- Approval substitution, replay, race, expiry, and scope narrowing.
- Cross-session and object-reference tests.
- Telemetry payload inspection and redaction.
- Quota/circuit-breaker property tests.
- Secret and log leak tests.
- Threat-model seeded adversarial cases.

    Record exact commands, environment, revision, outcomes, skipped checks, and artifact locations. “Tests passed” without commands and evidence is insufficient.

    ## Pull-request deliverables

    - Policy/security packages and config parser.
- Security test suite and coverage map.
- Consent/telemetry implementation contract.
- Identity and secret adapter interfaces.
- Incident signals and operator documentation.

    The PR description maps each deliverable to requirement IDs and acceptance criteria, names every changed public contract, provides screenshots/reports where relevant, lists risks and limitations, and includes rollback/migration behavior.

    ## Handoff requirements

    - Provide APIs to Architecture and Atticus missions.
- List tools/actions requiring future policy entries.
- Record denied design requests and ADRs.
- State residual risks and independent-review needs.

    The next agent must be able to start without reconstructing unstated reasoning. The handoff identifies what is complete, what remains, what failed, decisions/ADRs, changed paths, test commands, produced artifacts, known debt, security/privacy effects, and exact recommended next issue.

    ## Stop conditions

    - A proposed behavior violates the local/private boundary.
- Approval cannot be bound unambiguously.
- Security test reveals a critical architecture flaw.

    ## Definition of mission complete

    - all work packages are complete or explicitly deferred by approved decision;
    - owned documents and contracts are internally consistent;
    - required tests and evidence pass;
    - no critical TODO, placeholder, fake metric, unreviewed license, or silent security weakening remains;
    - feature branch is pushed and a focused PR is opened;
    - `WORKLOG.md` and the sequential handoff ledger are updated;
    - the next mission has a precise, executable starting point.
