---
document_id: DRL-ARC-004
title: "Policy and Tool Execution Architecture"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Policy and Tool Execution Architecture

## Separation of duties

1. Model/planner proposes a tool call.
2. Registry resolves exact tool version and schema.
3. Validator rejects unknown or malformed arguments.
4. Policy engine evaluates actor, tenant, environment, resource, risk, data movement, and prior approvals.
5. Approval service obtains a bound grant if required.
6. Dispatcher executes through a tool-specific adapter under least-privilege identity.
7. Result is normalized, redacted, stored, and traced.
8. EvalForge may assess behavior but cannot authorize it.

## Tool manifest

Every tool manifest includes:

- canonical name and version;
- human and model descriptions;
- input/output JSON Schemas;
- owner and support status;
- risk tier and required scopes;
- allowed actors/environments;
- data classes accepted/returned;
- external destinations;
- side-effect and idempotency class;
- timeout, retry, and concurrency limits;
- audit fields and redaction policy;
- test fixtures and safety cases.

## Tool groups

- public read tools;
- public deterministic compute tools;
- specialist research tools;
- local private read tools;
- local reversible write tools;
- consequential external tools;
- administrative tools unavailable to the model.

## Dynamic tools

Community plugins may register only through signed manifests and review. Public Atticus uses an allowlist frozen by release. Runtime discovery cannot grant a tool more scope than its deployment identity and policy configuration.
