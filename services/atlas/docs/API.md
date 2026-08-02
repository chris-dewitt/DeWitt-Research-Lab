---
document_id: DRL-ATL-101
title: "Atlas API and Contract Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atlas API and Contract Specification

    ## Contract philosophy

    The API is task-oriented and asynchronous where work can outlive an ordinary request. Canonical JSON Schemas are authoritative; OpenAPI is generated or contract-tested against them. Streaming is a presentation mechanism and preserves the same event semantics.

    **Base path:** `/api/atlas/v1`

    ## Resource model

    - Source and SourcePolicy.
- Acquisition, RawObject, DocumentVersion, Series, ObservationVersion, and Release.
- IndexSnapshot and ConnectorRun.
- ResearchQuery, EvidenceBundle, Claim, ChartArtifact, and ResearchSnapshot.

    ## Endpoint surface

    | Method | Path | Purpose |
|---|---|---|
| POST | `/research` | submit bounded research question |
| GET | `/research/{id}` | status and result |
| GET | `/research/{id}/events` | resumable progress |
| GET | `/evidence-bundles/{id}` | machine/human evidence |
| GET | `/series/{id}` | metadata and observations |
| GET | `/documents/{id}` | metadata and permitted extract |
| POST | `/snapshots` | create immutable snapshot |
| GET | `/snapshots/{id}` | manifest and artifacts |
| POST | `/connectors/{id}/runs` | privileged ingestion job |

    ## Events and streaming

    - Ingestion discovered, fetched, validated, quarantined, and published.
- Research retrieval started, evidence added, analysis completed, and snapshot created.
- Progress exposes counts/status, not restricted raw content.

    Every stream starts with a versioned acceptance event, uses monotonic sequence numbers, carries a trace ID, and ends exactly once as `completed`, `failed`, `cancelled`, or `expired`. Consumers tolerate unknown additive events and resume from an acknowledged sequence when supported.

    ## Error taxonomy

    - Source unavailable or changed.
- Rights policy blocks access/export.
- Validation or quarantine failure.
- Invalid or ambiguous time semantics.
- No eligible evidence at as-of cutoff.
- Retrieval budget exhausted.
- Deterministic calculation failed.
- Snapshot or index version drift.

    Errors use a stable DRL error code, safe user message, retryability, correlation ID, and optional structured details. Stack traces, secrets, credentials, raw private files, and protected prompts never cross the public boundary.

    ## Idempotency, concurrency, deadlines

    Mutating or expensive commands accept an idempotency key bound to the normalized request digest. Reuse with different content fails. Optimistic versions/ETags protect mutable policy, approval, configuration, and user state. Each request has an absolute deadline; retries consume a bounded budget and may not duplicate effects.

    ## Identity and authorization

    Limited read-only/demo routes may permit anonymous sessions with strict quotas. Authenticated routes verify issuer, audience, expiry, subject, session, and scopes. Service calls use workload identity and audience-bound tokens. Every receiving service authorizes independently.

    ## Versioning

    Source-normalization versions and index snapshots are separate from the API version. Research results pin both. Connector semantic changes require a new normalization version and migration/rebuild.

    Breaking changes require a new major schema/route, migration guide, compatibility tests, deprecation window, and ADR. Additive optional fields are compatible; unknown security-critical enums fail closed.

    ## Contract test minimum

    - all examples validate against schema;
    - OpenAPI and canonical schema remain synchronized;
    - allow/deny scopes and tenant/session isolation are tested;
    - malformed, oversized, adversarial, timed-out, cancelled, and duplicate requests receive bounded behavior;
    - previous supported minor-version fixtures remain in CI.
