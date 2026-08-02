---
document_id: DRL-AGT-002
title: "Agent Mission 02: Architecture, Protocol, and Shared Packages"
version: 3.1.0
status: APPROVED EXECUTION MISSION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Agent Mission 02: Architecture, Protocol, and Shared Packages

    ## Mission objective

    Implement the canonical DRL protocol, state-machine contracts, shared Python and TypeScript SDKs, provenance/evidence types, error model, idempotency primitives, and contract simulator used by every project.

    This mission is executed on a dedicated feature branch and ends in a reviewable pull request. It is not permission to reinterpret the laboratory. The agent must read the root `LABORATORY_BIBLE.md`, `AGENTS.md`, decision register, current `WORKLOG.md`, and all prerequisites below before changing files.

    
## Open Research Charter obligations

This mission must preserve DRL's open-by-construction identity. Read `OPEN_RESEARCH_CHARTER.md` and the relevant `docs/09-open-source/` standards. For every material feature, record the public artifact, license, modification surface, self-hosted path, upstream dependencies, reproducibility evidence, and any open exception. Prefer upstream contribution over permanent private forks. Use “open source,” “open weight,” and “source available” precisely.

## Entry prerequisites

    - Mission 01 workspace and schema validation merged.
- Architecture and protocol documents approved.
- Security mission can review proposed authority-sensitive changes before merge.

    If a prerequisite is absent, stale, contradictory, or unapproved, stop and create a blocker in the handoff ledger. Do not fill an architectural gap with an undocumented personal preference.

    ## Owned paths

    - schemas/**
- packages/protocol/**
- packages/provenance/**
- packages/sdk-python/**
- packages/sdk-typescript/**
- packages/observability/**
- docs/02-architecture/**
- tests/contracts/**

    Ownership means primary modification responsibility for this mission. Small necessary changes outside these paths require explicit notation in the worklog; changes to another project's public contract require its owner mission or an ADR.

    ## Forbidden or protected paths

    - Do not modify `LABORATORY_BIBLE.md` except through an approved constitutional ADR.
- Do not commit credentials, private files, employer material, unlicensed corpora, model weights without release policy, or generated secrets.
- Do not weaken security, privacy, evaluation, accessibility, or open-weight requirements to make a demo pass.
- Do not mark a feature or metric complete without evidence.
- Do not implement policy decisions, model behavior, domain calculations, or cloud deployment.
- Do not embed provider-specific types in canonical protocol.

    ## Required work packages

    ### WP-02-01: Implement generated or hand-maintained canonical types with cross-language conformance.
### WP-02-02: Implement task/run/event/error/claim/evidence/artifact/approval envelopes.
### WP-02-03: Implement run state machine and property-based transition tests.
### WP-02-04: Implement idempotency-key and request-digest helpers.
### WP-02-05: Implement provenance and content-digest utilities.
### WP-02-06: Implement safe trace event builder and redaction hooks.
### WP-02-07: Create protocol simulator and example end-to-end fixture trace.
### WP-02-08: Generate OpenAPI foundation and SDK compatibility report.

    Each work package must produce implementation or controlled-document changes, tests or validation evidence, and a worklog entry. Create focused commits after each coherent package.

    ## ADR and director approval triggers

    - Changing public schemas or event semantics.
- Selecting transport beyond approved HTTP/SSE baseline.
- Making MCP the internal source of truth.
- Adding fields that carry hidden reasoning or raw secret content.

    For each trigger, write the ADR first, mark it `PROPOSED`, identify alternatives and consequences, and wait for the Director's approval before implementation. The agent may prepare a nonbinding spike in an isolated path if the ADR explicitly allows it.

    ## Verification matrix

    - Cross-language roundtrip fixtures.
- JSON Schema and OpenAPI conformance.
- State-machine property tests and illegal transition rejection.
- Idempotency duplicate/mismatch tests.
- Digest canonicalization tests.
- Backward-compatibility fixture tests.

    Record exact commands, environment, revision, outcomes, skipped checks, and artifact locations. “Tests passed” without commands and evidence is insufficient.

    ## Pull-request deliverables

    - Versioned protocol packages.
- Generated docs and examples.
- Simulator and signed fixture trace.
- Compatibility and contract reports.
- Migration/deprecation policy implementation.

    The PR description maps each deliverable to requirement IDs and acceptance criteria, names every changed public contract, provides screenshots/reports where relevant, lists risks and limitations, and includes rollback/migration behavior.

    ## Handoff requirements

    - List exact public contracts and versions.
- Identify remaining security/policy hooks.
- Provide fixture trace IDs and commands to consume SDKs.
- Name any proposed schema ADR.

    The next agent must be able to start without reconstructing unstated reasoning. The handoff identifies what is complete, what remains, what failed, decisions/ADRs, changed paths, test commands, produced artifacts, known debt, security/privacy effects, and exact recommended next issue.

    ## Stop conditions

    - Cross-language semantics cannot agree.
- Canonicalization/digest algorithm is undecided.
- A contract would require storing prohibited content.

    ## Definition of mission complete

    - all work packages are complete or explicitly deferred by approved decision;
    - owned documents and contracts are internally consistent;
    - required tests and evidence pass;
    - no critical TODO, placeholder, fake metric, unreviewed license, or silent security weakening remains;
    - feature branch is pushed and a focused PR is opened;
    - `WORKLOG.md` and the sequential handoff ledger are updated;
    - the next mission has a precise, executable starting point.
