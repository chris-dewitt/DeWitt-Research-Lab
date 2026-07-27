---
document_id: DRL-ARC-013
title: "Error Taxonomy and Recovery Model"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Error Taxonomy and Recovery Model

## Stable error domains

- `REQUEST_*` validation and unsupported scope;
- `AUTH_*` authentication/session;
- `POLICY_*` deny, approval, expiry;
- `MODEL_*` unavailable, timeout, invalid structure, context;
- `TOOL_*` validation, unavailable, partial side effect;
- `DATA_*` missing, stale, license, provenance;
- `RETRIEVAL_*` empty, contradictory, index stale;
- `CALC_*` invalid assumptions, numerical failure;
- `EVAL_*` suite, judge, threshold;
- `QUOTA_*` request/cost/rate;
- `INTERNAL_*` unexpected.

## User messages

Expose what happened, impact, safe next action, and correlation ID. Do not expose stack traces, secrets, internal hostnames, or policy internals useful for bypass.

## Retry matrix

- validation/policy deny: no automatic retry;
- timeout before side effect: bounded retry if tool is pure/read/idempotent;
- ambiguous non-idempotent result: reconcile, never blind retry;
- invalid model JSON: one constrained repair, then fallback/fail;
- stale retrieval index: fallback to direct source or warn;
- evaluator unavailable: task may complete with evaluation pending only if no safety gate depends on it.

## Circuit breakers

Repeated provider/tool failures open circuit, prevent request storms, expose degraded status, and route to replay/alternative where allowed.
