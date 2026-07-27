---
document_id: DRL-BAL-101
title: "BalanceLab AI API and Contract Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # BalanceLab AI API and Contract Specification

    ## Contract philosophy

    The API is task-oriented and asynchronous where work can outlive an ordinary request. Canonical JSON Schemas are authoritative; OpenAPI is generated or contract-tested against them. Streaming is a presentation mechanism and preserves the same event semantics.

    **Base path:** `/api/balancelab/v1`

    ## Resource model

    - Institution, Position, ProductType, and CashFlowProfile.
- Curve, Scenario, AssumptionSet, and ValidationResult.
- Run, ProjectionSlice, Metric, and Reconciliation.
- CalculationArtifact, Comparison, and Report.

    ## Endpoint surface

    | Method | Path | Purpose |
|---|---|---|
| GET | `/institutions/samples` | public sample catalog |
| POST | `/institutions/validate` | validate upload or object |
| POST | `/scenarios/validate` | normalize and validate scenario |
| POST | `/runs` | execute deterministic engine |
| GET | `/runs/{id}` | status and safe summary |
| GET | `/artifacts/{id}` | calculation artifact and manifest |
| POST | `/comparisons` | compare approved artifacts |
| POST | `/reports` | create audited report |

    ## Events and streaming

    - Validation completed or failed.
- Run accepted, phase progressed, reconciled, completed, or failed.
- Artifact and report created.
- Progress events never label provisional numbers as final.

    Every stream starts with a versioned acceptance event, uses monotonic sequence numbers, carries a trace ID, and ends exactly once as `completed`, `failed`, `cancelled`, or `expired`. Consumers tolerate unknown additive events and resume from an acknowledged sequence when supported.

    ## Error taxonomy

    - Invalid units, dates, or schema.
- Unbalanced institution.
- Unsupported product or scenario.
- Ambiguous material natural-language assumption.
- Numerical, convergence, or reconciliation failure.
- Artifact or method version mismatch.
- Upload rejected by security or privacy policy.

    Errors use a stable DRL error code, safe user message, retryability, correlation ID, and optional structured details. Stack traces, secrets, credentials, raw private files, and protected prompts never cross the public boundary.

    ## Idempotency, concurrency, deadlines

    Mutating or expensive commands accept an idempotency key bound to the normalized request digest. Reuse with different content fails. Optimistic versions/ETags protect mutable policy, approval, configuration, and user state. Each request has an absolute deadline; retries consume a bounded budget and may not duplicate effects.

    ## Identity and authorization

    Limited read-only/demo routes may permit anonymous sessions with strict quotas. Authenticated routes verify issuer, audience, expiry, subject, session, and scopes. Service calls use workload identity and audience-bound tokens. Every receiving service authorizes independently.

    ## Versioning

    Engine methods, data schema, scenario catalog, synthetic generator, and artifact format are versioned separately. Material method changes create new artifacts and baselines; old artifacts remain readable.

    Breaking changes require a new major schema/route, migration guide, compatibility tests, deprecation window, and ADR. Additive optional fields are compatible; unknown security-critical enums fail closed.

    ## Contract test minimum

    - all examples validate against schema;
    - OpenAPI and canonical schema remain synchronized;
    - allow/deny scopes and tenant/session isolation are tested;
    - malformed, oversized, adversarial, timed-out, cancelled, and duplicate requests receive bounded behavior;
    - previous supported minor-version fixtures remain in CI.
