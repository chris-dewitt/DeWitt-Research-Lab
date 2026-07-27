---
document_id: DRL-ATT-102
title: "Atticus Control Plane Data and Persistence Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Control Plane Data and Persistence Specification

    ## Principles

    Atticus Control Plane stores only state required for declared purposes. Storage location, classification, retention, deletion, telemetry eligibility, training eligibility, and rights are explicit fields or policies—not conventions inferred from code.

    ## Canonical entities

    - Task, Run, RunStep, Session, SkillVersion, ToolCatalogSnapshot.
- PolicyDecision, ApprovalRequest, ApprovalGrant.
- EvidenceReference, ClaimReference, ArtifactReference, SafeTraceEvent.
- ModelInvocationSummary, CostRecord, QuotaLedger, DeletionRequest.
- Raw prompts/responses are optional protected diagnostics, not assumed trace fields.

    ## Classification and handling

    - Public demo inputs: short-lived public-session operational data, no training by default.
- Authenticated usage: private account/session data under user controls.
- DRL research traces: separate opt-in donation object and research review.
- Local-personal data: stays local unless a bounded payload is explicitly approved.
- Secrets/credentials: never stored in application tables.

    ## Persistence services

    - Cloud SQL PostgreSQL for transactional state, approvals, lineage, quotas, and metadata.
- Cloud Storage for large immutable artifacts and signed evaluation/replay bundles.
- Optional cache for acceleration; correctness never depends on cache durability.
- OS-protected local runner storage for device credentials and private audit.
- Public documentation/research vectors live in dedicated stores, not run-state tables.

    ## Retention and deletion

    - Anonymous sessions use a short configured window and logical deletion on close where feasible.
- Authenticated history is optional, inspectable, and deletable.
- Restricted security-audit metadata may retain longer under a published schedule.
- Donated traces retain according to the consent/data-release version and remain removable before irreversible publication where feasible.
- Sensitive approval previews expire rapidly; minimum proof metadata may persist.

    Deletion is a traceable workflow with an identifier and terminal outcome. Backup expiration is described honestly. Legal/security holds, if any, are explicit and restricted.

    ## Provenance and lineage

    - Every run pins code, protocol, skill, policy, route, model, tool catalog, and environment.
- Evidence and artifacts use stable IDs and content digests.
- Events encode parent/child and causation without hidden reasoning.
- Donated traces receive research IDs and pass de-identification and review before dataset eligibility.

    Every derived artifact records source identifiers, acquisition time, effective/as-of time where applicable, transformation version, code/model/configuration revisions, rights decision, and content digest. Untraceable artifacts cannot support public claims.

    ## Migration policy

    - Use versioned migrations such as Alembic.
- Approval and policy evidence is immutable append-style; corrections supersede.
- Event/schema compatibility fixtures cover the supported V1 minor line.
- Replays use frozen fixtures/artifacts rather than claiming mutable external systems reproduce exactly.

    Migrations are versioned and tested on representative data. Destructive migrations require backup, rehearsal, verification, and director approval. Protocol-facing changes coordinate schema/API versions.

    ## Required tests

    - required fields, uniqueness, referential integrity, enum and unit domains;
    - timezone and historical/as-of semantics;
    - idempotent ingestion and partial-write recovery;
    - tenant/session/access isolation;
    - retention and deletion;
    - lineage completeness and artifact digest;
    - representative scale and recovery behavior.
