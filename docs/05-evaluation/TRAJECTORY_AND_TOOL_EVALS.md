---
document_id: DRL-EVA-004
title: "Agent Trajectory and Tool-Use Evaluation"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Agent Trajectory and Tool-Use Evaluation

## Trajectory graph

EvalForge consumes normalized trace events and reconstructs plan, policy, approval, tool, evidence, model, and result edges.

## Assertions

- required action occurred before dependent step;
- forbidden action never occurred;
- tool version and arguments valid;
- policy decision preceded dispatch;
- approval matched exact operation;
- retry count and backoff bounded;
- non-idempotent action not duplicated;
- model did not synthesize final answer before required calculation/evidence;
- final report references actual artifacts;
- task terminal state matches results.

## Alternative valid trajectories

Cases may specify a partial order and invariants rather than exact sequence. This avoids overfitting to one orchestrator while still enforcing safety and task logic.

## Efficiency

Measure excess steps relative to acceptable lower bound, but do not reward unsafe shortcuts. Report tokens/tool calls/latency separately.
