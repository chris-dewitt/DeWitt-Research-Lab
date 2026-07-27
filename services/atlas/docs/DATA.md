---
document_id: DRL-ATL-102
title: "Atlas Data and Persistence Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atlas Data and Persistence Specification

    ## Principles

    Atlas stores only state required for declared purposes. Storage location, classification, retention, deletion, telemetry eligibility, training eligibility, and rights are explicit fields or policies—not conventions inferred from code.

    ## Canonical entities

    - Source and rights registry.
- Raw acquisition/object and checksum.
- Document, series, observation, release, and revision versions.
- Transformation job and quality result.
- Search/index snapshot.
- Research query, evidence bundle, chart/calculation artifact, and snapshot.

    ## Classification and handling

    - Public redistributable.
- Public metadata/link-only.
- Public restricted extract.
- DRL-private licensed research.
- Prohibited.
- V1 public Atlas uses only approved public sources; user queries and donated traces remain separate.

    ## Persistence services

    - Cloud Storage for immutable raw and derived artifacts.
- PostgreSQL for metadata, bitemporal observations, rights, lineage, and jobs.
- pgvector plus lexical search for approved chunks.
- Parquet snapshots for reproduction.
- A warehouse is optional later, not a V1 dependency.

    ## Retention and deletion

    - Source artifacts follow source-specific rights policy.
- Quarantined failures retain only long enough for diagnosis.
- Published research snapshots remain available/versioned.
- Anonymous query logs are short-lived and excluded from training by default.
- Embeddings and extracts are deleted/rebuilt if rights change.

    Deletion is a traceable workflow with an identifier and terminal outcome. Backup expiration is described honestly. Legal/security holds, if any, are explicit and restricted.

    ## Provenance and lineage

    - URL/API identifier, retrieval metadata, checksum, parser and normalizer revisions.
- Observation, release, effective, revision, ingestion, and as-of times.
- Rights decision and export constraints.
- Every chart/table/claim links to exact document or observation versions.
- Published snapshots include code/config/environment manifests.

    Every derived artifact records source identifiers, acquisition time, effective/as-of time where applicable, transformation version, code/model/configuration revisions, rights decision, and content digest. Untraceable artifacts cannot support public claims.

    ## Migration policy

    - Canonical schemas are versioned and migration-tested.
- Bitemporal records append versions instead of overwriting.
- Index rebuilds create new snapshots and promote atomically.
- Rights changes trigger access, index, derivative, and publication review.

    Migrations are versioned and tested on representative data. Destructive migrations require backup, rehearsal, verification, and director approval. Protocol-facing changes coordinate schema/API versions.

    ## Required tests

    - required fields, uniqueness, referential integrity, enum and unit domains;
    - timezone and historical/as-of semantics;
    - idempotent ingestion and partial-write recovery;
    - tenant/session/access isolation;
    - retention and deletion;
    - lineage completeness and artifact digest;
    - representative scale and recovery behavior.
