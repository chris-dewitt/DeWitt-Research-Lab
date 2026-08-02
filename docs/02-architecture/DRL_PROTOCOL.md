---
document_id: DRL-ARC-002
title: "DRL Protocol and Canonical Contracts"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# DRL Protocol and Canonical Contracts

## Purpose

The DRL Protocol is the versioned language shared by Atticus, specialist systems, SDKs, the local runner, EvalForge, replays, and the website. It prevents providers and frameworks from leaking their private message formats into domain logic.

## Contract families

### Identity and context

- `ActorContext`: actor ID, tenant, session, roles, device, authentication strength.
- `RequestContext`: locale, timezone, as-of date, privacy mode, budget, correlation IDs.

### Tasks

- `TaskRequest`: immutable user objective and constraints.
- `TaskPlan`: short steps, selected skill, anticipated tools, risk estimate.
- `TaskState`: queued, planning, waiting_approval, running, degraded, completed, failed, canceled.

### Skills and tools

- `SkillDefinition`: trigger, purpose, required tools, preconditions, output schema, policy profile.
- `ToolDefinition`: name, semantic version, input/output schemas, risk tier, scopes, idempotency class, timeout, data classification.
- `ToolCall`: exact arguments, call ID, task/trace IDs, requested scope, source plan step.
- `ToolResult`: status, typed output, evidence, side effects, retry hint, redactions.

### Permission and approval

- `PolicyDecision`: allow, deny, require_approval, require_step_up; rule IDs and explanation.
- `ApprovalRequest`: exact operation hash, user-facing summary, data movement, risk, expiry.
- `ApprovalGrant`: approver, method, signed binding, allowed once or bounded duration.

### Evidence and calculations

- `EvidenceItem`: source URI/identifier, publisher, title, timestamps, excerpt/hash, license, retrieval metadata.
- `Claim`: statement, supporting/contradicting evidence IDs, confidence, inference flag.
- `CalculationArtifact`: engine/version, inputs, assumptions, outputs, units, tolerances, code/data hashes.

### Trace and evaluation

- `TraceEvent`: event ID, parent, timestamp, component, event type, redacted attributes.
- `ExecutionTrace`: ordered DAG and manifest.
- `EvaluationRequest` and `EvaluationResult`: suite/version, cases, metrics, thresholds, findings.

### Error

- `DRLError`: stable code, human message, retryability, responsible component, safe details, correlation ID.

## Versioning

- Schemas use semantic versions.
- Additive optional fields are minor changes.
- Required-field, semantic, or enum removals are major changes.
- Services advertise supported protocol range.
- Replays pin exact schema versions and retain migration adapters.
- Unknown fields are preserved where possible but never trusted without validation.

## Idempotency

Every tool declares one of:

- `pure`: no side effect;
- `read`: no external mutation;
- `idempotent_write`: repeat with same idempotency key is safe;
- `non_idempotent`: requires explicit execution token and cannot auto-retry.

The dispatcher generates idempotency keys from task, tool, arguments, and approved operation. Result storage occurs before acknowledging completion where practical.

## MCP interoperability

MCP adapters may expose DRL tools using current protocol transports. DRL retains its own policy, tenant, approval, trace, and data-classification layer. An MCP server declaration is not sufficient authorization.

## Canonical location

Machine-readable schemas live in `schemas/`. Generated types are committed only when reproducible and verified against source schemas.
