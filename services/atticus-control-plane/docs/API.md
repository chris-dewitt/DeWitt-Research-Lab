---
document_id: DRL-ATT-101
title: "Atticus Control Plane API and Contract Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Control Plane API and Contract Specification

    ## Contract philosophy

    The API is task-oriented and asynchronous where work can outlive an ordinary request. Canonical JSON Schemas are authoritative; OpenAPI is generated or contract-tested against them. Streaming is a presentation mechanism and preserves the same event semantics.

    **Base path:** `/api/atticus/v1`

    ## Resource model

    - Task: immutable objective, context references, and constraints.
- Run: one execution attempt, state, plan summary, budget, and outcome.
- Approval: scoped proposal and user decision.
- Session: identity, mode, consent, and catalogs.
- Skill: versioned workflow contract.
- TraceView: privacy-filtered operational timeline, never hidden reasoning.
- Artifact: report, diff, evidence bundle, calculation, or export reference.

    ## Endpoint surface

    | Method | Path | Purpose |
|---|---|---|
| POST | `/tasks` | create and optionally start a task |
| GET | `/tasks/{id}` | task and linked runs |
| POST | `/tasks/{id}/runs` | start/retry with pinned configuration |
| GET | `/runs/{id}` | status, result, safe summary |
| GET | `/runs/{id}/events` | resumable SSE stream |
| POST | `/runs/{id}/cancel` | idempotent cancellation |
| GET | `/runs/{id}/trace` | authorized safe trace |
| GET | `/approvals/{id}` | pending approval detail |
| POST | `/approvals/{id}/decision` | approve or deny with version |
| GET | `/skills` | available skill catalog |
| GET | `/tools` | safe capability catalog |
| POST | `/sessions` | create public/private session |
| DELETE | `/sessions/{id}` | close and schedule deletion |

    ## Events and streaming

    - `run.accepted`, `plan.summary`, `policy.decision`, `tool.proposed`, `approval.requested`, `approval.resolved`, `tool.started`, `tool.completed`, `evidence.added`, `artifact.created`, `run.degraded`, and terminal events.
- Token-level model output is optional and disabled where it complicates safety or citation binding.
- Approval events never include secrets or raw private file content.

    Every stream starts with a versioned acceptance event, uses monotonic sequence numbers, carries a trace ID, and ends exactly once as `completed`, `failed`, `cancelled`, or `expired`. Consumers tolerate unknown additive events and resume from an acknowledged sequence when supported.

    ## Error taxonomy

    - `DRL-VALIDATION-*`: malformed or incompatible request.
- `DRL-AUTH-*`: identity, session, or scope failure.
- `DRL-POLICY-*`: denied or approval-required action.
- `DRL-APPROVAL-*`: expired, stale, mismatched, or denied grant.
- `DRL-TOOL-*`: unavailable, invalid, timed out, or failed effect.
- `DRL-MODEL-*`: provider, routing, or structured-output failure.
- `DRL-BUDGET-*`: step, time, token, concurrency, or monetary budget exhausted.
- `DRL-STATE-*`: illegal transition or concurrency conflict.

    Errors use a stable DRL error code, safe user message, retryability, correlation ID, and optional structured details. Stack traces, secrets, credentials, raw private files, and protected prompts never cross the public boundary.

    ## Idempotency, concurrency, deadlines

    Mutating or expensive commands accept an idempotency key bound to the normalized request digest. Reuse with different content fails. Optimistic versions/ETags protect mutable policy, approval, configuration, and user state. Each request has an absolute deadline; retries consume a bounded budget and may not duplicate effects.

    ## Identity and authorization

    Limited read-only/demo routes may permit anonymous sessions with strict quotas. Authenticated routes verify issuer, audience, expiry, subject, session, and scopes. Service calls use workload identity and audience-bound tokens. Every receiving service authorizes independently.

    ## Versioning

    Runs pin protocol, skill, policy, routing, model, and tool-catalog versions so historical traces remain interpretable. V1 minor releases are additive; security-sensitive unknowns fail closed.

    Breaking changes require a new major schema/route, migration guide, compatibility tests, deprecation window, and ADR. Additive optional fields are compatible; unknown security-critical enums fail closed.

    ## Contract test minimum

    - all examples validate against schema;
    - OpenAPI and canonical schema remain synchronized;
    - allow/deny scopes and tenant/session isolation are tested;
    - malformed, oversized, adversarial, timed-out, cancelled, and duplicate requests receive bounded behavior;
    - previous supported minor-version fixtures remain in CI.
