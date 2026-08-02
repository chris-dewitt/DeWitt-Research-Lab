---
document_id: DRL-ARC-012
title: "Observability and Trace Model"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Observability and Trace Model

## Signals

- distributed traces for user request, model calls, tools, policy, approvals, retrieval, calculations, evaluations;
- metrics for latency, throughput, errors, denials, approvals, tokens, cost, queue depth, cold starts, retrieval, and evaluation drift;
- structured logs for operational events with content minimized;
- audit records for consequential actions and administrative changes.

## Trace requirements

- W3C trace context where possible;
- parent-child relationship across async jobs;
- stable DRL event names mapped to OpenTelemetry semantic conventions;
- model provider, exact model revision, token counts, tool name, and outcome;
- prompt/tool content captured only under explicit safe telemetry configuration;
- separate public-safe replay from restricted operational trace;
- sampling never drops required audit events.

## Metrics

Service metrics include RED (rate, errors, duration) and resource saturation. AI metrics include time to first token, generation throughput, invalid structured outputs, fallback rate, route/tool accuracy from sampled evals, citation failures, policy denial, approval abandonment, and cost per successful task.

## Correlation

User-facing error and report includes a safe correlation ID. Operators can resolve to restricted trace without exposing IDs that allow enumeration.
