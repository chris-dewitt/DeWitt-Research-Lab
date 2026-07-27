---
document_id: DRL-FED-101
title: "FedLens API and Contract Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # FedLens API and Contract Specification

    ## Contract philosophy

    The API is task-oriented and asynchronous where work can outlive an ordinary request. Canonical JSON Schemas are authoritative; OpenAPI is generated or contract-tested against them. Streaming is a presentation mechanism and preserves the same event semantics.

    **Base path:** `/api/fedlens/v1`

    ## Resource model

    - FedDocument, DocumentVersion, Segment, and Correction.
- Meeting, ReleaseEvent, Speaker, and SpeakerRole.
- Alignment, ChangeSpan, Annotation, and SearchResult.
- EventStudyDefinition, EventStudyResult, and PolicySnapshot.

    ## Endpoint surface

    | Method | Path | Purpose |
|---|---|---|
| GET | `/documents` | filter corpus |
| GET | `/documents/{id}` | exact permitted version and metadata |
| POST | `/comparisons` | align and compare versions or meetings |
| POST | `/search` | temporal, metadata, and text search |
| GET | `/meetings/{id}/timeline` | meeting evidence timeline |
| POST | `/event-studies` | deterministic bounded analysis |
| GET | `/event-studies/{id}` | status and artifacts |
| POST | `/snapshots` | create reproducible policy snapshot |

    ## Events and streaming

    - Corpus acquisition, version, parse, index, and publication.
- Comparison completed and annotation reviewed.
- Event study accepted, computed, failed, and snapshot published.

    Every stream starts with a versioned acceptance event, uses monotonic sequence numbers, carries a trace ID, and ends exactly once as `completed`, `failed`, `cancelled`, or `expired`. Consumers tolerate unknown additive events and resume from an acknowledged sequence when supported.

    ## Error taxonomy

    - Ambiguous meeting or version.
- Source correction or integrity mismatch.
- Alignment confidence below threshold.
- Unsupported market instrument or window.
- Missing market data or calendar ambiguity.
- Rights-restricted content.
- As-of evidence unavailable.

    Errors use a stable DRL error code, safe user message, retryability, correlation ID, and optional structured details. Stack traces, secrets, credentials, raw private files, and protected prompts never cross the public boundary.

    ## Idempotency, concurrency, deadlines

    Mutating or expensive commands accept an idempotency key bound to the normalized request digest. Reuse with different content fails. Optimistic versions/ETags protect mutable policy, approval, configuration, and user state. Each request has an absolute deadline; retries consume a bounded budget and may not duplicate effects.

    ## Identity and authorization

    Limited read-only/demo routes may permit anonymous sessions with strict quotas. Authenticated routes verify issuer, audience, expiry, subject, session, and scopes. Service calls use workload identity and audience-bound tokens. Every receiving service authorizes independently.

    ## Versioning

    Corpus and annotation releases use data/model versions separate from API versions. Event-study method versions are immutable. Corrections append document versions and trigger derived-artifact review.

    Breaking changes require a new major schema/route, migration guide, compatibility tests, deprecation window, and ADR. Additive optional fields are compatible; unknown security-critical enums fail closed.

    ## Contract test minimum

    - all examples validate against schema;
    - OpenAPI and canonical schema remain synchronized;
    - allow/deny scopes and tenant/session isolation are tested;
    - malformed, oversized, adversarial, timed-out, cancelled, and duplicate requests receive bounded behavior;
    - previous supported minor-version fixtures remain in CI.
