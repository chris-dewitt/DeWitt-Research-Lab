---
document_id: DRL-BAL-102
title: "BalanceLab AI Data and Persistence Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # BalanceLab AI Data and Persistence Specification

    ## Principles

    BalanceLab AI stores only state required for declared purposes. Storage location, classification, retention, deletion, telemetry eligibility, training eligibility, and rights are explicit fields or policies—not conventions inferred from code.

    ## Canonical entities

    - Synthetic institution and generator/source metadata.
- Product, position, cash-flow, pricing, and behavioral assumptions.
- Curve and scenario definitions.
- Run phases and deterministic results.
- Reconciliation and calculation artifact.
- Explanation and report linked to immutable artifacts.

    ## Classification and handling

    - Public synthetic sample data and fixtures.
- Private user-uploaded data excluded from training/public research by default.
- Anonymous mode uses samples or ephemeral uploads only if enabled.
- Employer data is explicitly prohibited.

    ## Persistence services

    - PostgreSQL for metadata, scenarios, run state, artifact index, and access.
- Object storage for immutable artifacts, reports, and upload quarantine.
- Local file execution path for offline use.
- No vector store is needed for calculations; method-document retrieval is separate.

    ## Retention and deletion

    - Public samples and release artifacts are retained/versioned.
- Anonymous uploads and session data are deleted quickly after run.
- Authenticated saved scenarios remain user-controlled and deletable.
- Rejected files have short restricted quarantine.
- Deleting an artifact schedules deletion of derived explanations/reports where possible.

    Deletion is a traceable workflow with an identifier and terminal outcome. Backup expiration is described honestly. Legal/security holds, if any, are explicit and restricted.

    ## Provenance and lineage

    - Institution source or generator version and seed.
- Scenario JSON, normalized digest, and user confirmations.
- Engine code, method, config, dependencies, and run environment.
- Calculation steps, reconciliations, and artifact digest.
- Explanation model, prompt/template, and evidence references.
- Reviewer and publication record.

    Every derived artifact records source identifiers, acquisition time, effective/as-of time where applicable, transformation version, code/model/configuration revisions, rights decision, and content digest. Untraceable artifacts cannot support public claims.

    ## Migration policy

    - Financial schemas have explicit versions and converters.
- Artifacts are immutable; method changes create new artifacts.
- Product/position changes include golden compatibility fixtures.
- Migrations never invent missing assumptions silently; defaults are recorded or user action is required.

    Migrations are versioned and tested on representative data. Destructive migrations require backup, rehearsal, verification, and director approval. Protocol-facing changes coordinate schema/API versions.

    ## Required tests

    - required fields, uniqueness, referential integrity, enum and unit domains;
    - timezone and historical/as-of semantics;
    - idempotent ingestion and partial-write recovery;
    - tenant/session/access isolation;
    - retention and deletion;
    - lineage completeness and artifact digest;
    - representative scale and recovery behavior.
