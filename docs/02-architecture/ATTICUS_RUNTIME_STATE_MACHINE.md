---
document_id: DRL-ARC-003
title: "Atticus Runtime State Machine"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Atticus Runtime State Machine

## Task lifecycle

```text
RECEIVED
  -> VALIDATED
  -> CLASSIFIED
  -> PLANNED
  -> POLICY_CHECK
       -> DENIED
       -> WAITING_APPROVAL -> APPROVED / EXPIRED / REJECTED
       -> DISPATCHING
  -> RUNNING
       -> OBSERVING -> REPLAN (bounded)
       -> DEGRADED
       -> FAILED
  -> SYNTHESIZING
  -> EVALUATING
  -> COMPLETED / COMPLETED_WITH_WARNINGS
```

## Rules

- Every transition emits a trace event.
- A task cannot move from `WAITING_APPROVAL` to `RUNNING` unless the grant matches operation hash, actor, tenant, resource, arguments, and expiry.
- Replanning is bounded by step, tool-call, wall-clock, token, and cost budgets.
- The model cannot directly mutate task state; it returns typed proposals processed by the orchestrator.
- Cancel is checked before dispatch and between long-running steps.
- A non-idempotent tool cannot automatically retry after ambiguous timeout.
- `COMPLETED_WITH_WARNINGS` lists missing evidence, degraded services, or failed optional evaluators.

## Recovery

Failures are classified:

- invalid request: ask for clarification or fail without retry;
- policy denial: explain allowed alternative;
- transient provider: retry with bounded backoff or fallback;
- schema/model output invalid: constrained repair attempt, then alternate model or failure;
- tool validation: return error to planner with no side effect;
- partial side effect: reconciliation workflow and human notice;
- specialist unavailable: approved degraded path or replay;
- evaluation failure: mark run unsuccessful even if synthesis exists.

## Checkpointing

Long workflows store state after each tool result and before consequential dispatch. Checkpoints exclude secrets and raw private content unless storage policy permits. Recovered tasks revalidate identity, policy, approval expiry, model/tool versions, and cost budget.
