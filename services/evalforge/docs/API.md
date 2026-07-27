---
document_id: DRL-EVL-101
title: "EvalForge API and Contract Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # EvalForge API and Contract Specification

    ## Contract philosophy

    The API is task-oriented and asynchronous where work can outlive an ordinary request. Canonical JSON Schemas are authoritative; OpenAPI is generated or contract-tested against them. Streaming is a presentation mechanism and preserves the same event semantics.

    **Base path:** `/api/evalforge/v1`

    ## Resource model

    - Suite, DatasetVersion, Case, and Slice.
- Target, RuntimeConfig, PromptToolSnapshot, and Environment.
- Run, SampleResult, Trace, Score, and Artifact.
- JudgeConfig, HumanReview, Comparison, Baseline, GateDecision, Exception, Report, and LeaderboardEntry.

    ## Endpoint surface

    | Method | Path | Purpose |
|---|---|---|
| POST | `/runs` | schedule evaluation |
| GET | `/runs/{id}` | status and summary |
| GET | `/runs/{id}/events` | resumable progress |
| GET | `/results/{id}` | authorized detailed result |
| POST | `/comparisons` | paired baseline/candidate analysis |
| POST | `/baselines/promotions` | privileged accepted baseline |
| GET | `/reports/{id}` | signed report and manifest |
| GET | `/leaderboards/{id}` | approved public leaderboard |

    ## Events and streaming

    - Run queued, started, sample completed, scorer completed, and terminal.
- Budget warning, early stop, and infrastructure retry.
- Comparison completed, gate passed/failed/excepted, baseline promoted, report signed/published.

    Every stream starts with a versioned acceptance event, uses monotonic sequence numbers, carries a trace ID, and ends exactly once as `completed`, `failed`, `cancelled`, or `expired`. Consumers tolerate unknown additive events and resume from an acknowledged sequence when supported.

    ## Error taxonomy

    - Invalid manifest or schema.
- Target unavailable or incompatible.
- Dataset rights or access failure.
- Scorer or judge failure.
- Insufficient paired samples.
- Budget exhausted.
- Contamination or leakage flag.
- Artifact digest or signature mismatch.

    Errors use a stable DRL error code, safe user message, retryability, correlation ID, and optional structured details. Stack traces, secrets, credentials, raw private files, and protected prompts never cross the public boundary.

    ## Idempotency, concurrency, deadlines

    Mutating or expensive commands accept an idempotency key bound to the normalized request digest. Reuse with different content fails. Optimistic versions/ETags protect mutable policy, approval, configuration, and user state. Each request has an absolute deadline; retries consume a bounded budget and may not duplicate effects.

    ## Identity and authorization

    Limited read-only/demo routes may permit anonymous sessions with strict quotas. Authenticated routes verify issuer, audience, expiry, subject, session, and scopes. Service calls use workload identity and audience-bound tokens. Every receiving service authorizes independently.

    ## Versioning

    Suites and datasets are immutable by version. Scorer semantic changes require a new version. Accepted baselines pin the complete manifest. Report schema evolves additively within a major line.

    Breaking changes require a new major schema/route, migration guide, compatibility tests, deprecation window, and ADR. Additive optional fields are compatible; unknown security-critical enums fail closed.

    ## Contract test minimum

    - all examples validate against schema;
    - OpenAPI and canonical schema remain synchronized;
    - allow/deny scopes and tenant/session isolation are tested;
    - malformed, oversized, adversarial, timed-out, cancelled, and duplicate requests receive bounded behavior;
    - previous supported minor-version fixtures remain in CI.
