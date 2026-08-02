---
document_id: DRL-FED-102
title: "FedLens Data and Persistence Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # FedLens Data and Persistence Specification

    ## Principles

    FedLens stores only state required for declared purposes. Storage location, classification, retention, deletion, telemetry eligibility, training eligibility, and rights are explicit fields or policies—not conventions inferred from code.

    ## Canonical entities

    - Source, document, document version, segment, and correction ledger.
- Meeting, release, speaker, role, and institutional metadata.
- Alignment and exact/semantic change spans.
- Human/model annotations and adjudication.
- Search/index snapshot.
- Event-study definition and result.
- Policy research snapshot.

    ## Classification and handling

    - Official public Federal Reserve documents with source-specific rights records.
- Public market data under its own terms.
- Human annotations eligible for public research only with contributor consent/license.
- User queries and donated traces remain separate from the corpus.

    ## Persistence services

    - Immutable source documents and research artifacts in object storage.
- PostgreSQL for metadata, segments, alignments, annotations, and event studies.
- Lexical and pgvector indexes.
- Parquet/CSV research assets with checksums.

    ## Retention and deletion

    - Public corpus versions retained for reproducibility unless rights change.
- Intermediate parses may be rebuilt while lineage persists.
- Published event-study inputs/results retained with research.
- User sessions follow Atticus policy.
- Rejected or ambiguous annotations remain in restricted audit storage.

    Deletion is a traceable workflow with an identifier and terminal outcome. Backup expiration is described honestly. Legal/security holds, if any, are explicit and restricted.

    ## Provenance and lineage

    - Source URL, retrieval and checksum.
- Publication, meeting, correction, and effective timestamps.
- Parser, segmenter, alignment algorithm, model/prompt/config, and reviewer.
- Market source, exchange/calendar, timezone, benchmark, and method.
- Code revision, environment, and artifact digest.

    Every derived artifact records source identifiers, acquisition time, effective/as-of time where applicable, transformation version, code/model/configuration revisions, rights decision, and content digest. Untraceable artifacts cannot support public claims.

    ## Migration policy

    - Corpus releases are immutable; new parsers create new derived releases.
- Alignment algorithm changes preserve prior results.
- Taxonomy changes include mapping and adjudication.
- Event-study method changes create a new version and rerun, never overwrite.

    Migrations are versioned and tested on representative data. Destructive migrations require backup, rehearsal, verification, and director approval. Protocol-facing changes coordinate schema/API versions.

    ## Required tests

    - required fields, uniqueness, referential integrity, enum and unit domains;
    - timezone and historical/as-of semantics;
    - idempotent ingestion and partial-write recovery;
    - tenant/session/access isolation;
    - retention and deletion;
    - lineage completeness and artifact digest;
    - representative scale and recovery behavior.
