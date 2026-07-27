---
document_id: DRL-WEB-101
title: "DRL Web Data and Persistence Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # DRL Web Data and Persistence Specification

    ## Principles

    DRL Web stores only state required for declared purposes. Storage location, classification, retention, deletion, telemetry eligibility, training eligibility, and rights are explicit fields or policies—not conventions inferred from code.

    ## Canonical entities

    - Controlled document and frontmatter metadata.
- Project, system, repository, package, release, and research records.
- Signed metric, evaluation, replay, status, and artifact manifests.
- Session, account, consent, and preference records.
- Public search documents and media metadata.
- Optional privacy-preserving analytics events.

    ## Classification and handling

    - Public controlled content and releases.
- Public operational status and aggregate metrics.
- Private account and session preferences.
- Purpose-limited anonymous analytics.
- Atticus prompt/response/tool content governed by control-plane policy and excluded from generic analytics.

    ## Persistence services

    - Git-controlled Markdown/MDX and machine-readable manifests.
- Static/build indexes.
- Cloud Storage/CDN for media and signed artifacts.
- Firebase/Auth and minimal session store.
- Consent-aware product analytics.
- Search index excluding private/user content.

    ## Retention and deletion

    - Public releases remain versioned.
- Draft previews expire.
- Anonymous session and analytics identifiers are short-lived and disclosed.
- Authenticated preferences/history are user-controlled and deletable.
- Atticus content never flows into ordinary analytics payloads.
- Deleting media invalidates CDN and index references.

    Deletion is a traceable workflow with an identifier and terminal outcome. Backup expiration is described honestly. Legal/security holds, if any, are explicit and restricted.

    ## Provenance and lineage

    - Rendered controlled documents expose ID, version, status, updated date, and source path.
- Metric cards resolve to signed report IDs.
- Replays resolve to trace and artifact manifests.
- Research assets link code, data, model, method, license, and limitations.
- Deployment metadata includes build commit and content digest.

    Every derived artifact records source identifiers, acquisition time, effective/as-of time where applicable, transformation version, code/model/configuration revisions, rights decision, and content digest. Untraceable artifacts cannot support public claims.

    ## Migration policy

    - Frontmatter and content manifests are schema-versioned.
- Route redirects are maintained.
- Removed cited content receives a tombstone/archive notice.
- Search rebuilds atomically.
- Analytics schema changes require privacy review and versioned dashboards.

    Migrations are versioned and tested on representative data. Destructive migrations require backup, rehearsal, verification, and director approval. Protocol-facing changes coordinate schema/API versions.

    ## Required tests

    - required fields, uniqueness, referential integrity, enum and unit domains;
    - timezone and historical/as-of semantics;
    - idempotent ingestion and partial-write recovery;
    - tenant/session/access isolation;
    - retention and deletion;
    - lineage completeness and artifact digest;
    - representative scale and recovery behavior.
