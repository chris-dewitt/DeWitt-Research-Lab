---
document_id: DRL-ARC-010
title: "Events, Queues, Idempotency, and Concurrency"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Events, Queues, Idempotency, and Concurrency

## Synchronous versus asynchronous

Use synchronous request/response for short bounded reads and calculations. Use asynchronous jobs for ingestion, model training, large evaluation suites, report generation, and long research workflows.

## Delivery services

- Cloud Tasks: targeted HTTP work requiring scheduling, rate control, and per-task retries.
- Pub/Sub: fan-out domain events and independent consumers.

Selection is per workload and documented; they are not interchangeable abstractions.

## Event envelope

Includes event ID, type/version, source, subject, tenant, occurred/published times, trace context, data classification, payload schema, and deduplication key.

## Concurrency controls

- optimistic version on mutable task/session objects;
- advisory/application locks for singleton ingestion or migration;
- per-tenant and per-tool concurrency budgets;
- GPU request queue and admission control;
- idempotency ledger for side effects;
- outbox pattern for database state plus event publication where needed.

## Dead letters

Failed asynchronous work enters a dead-letter state with redacted error, attempts, next action, and operator runbook. It is not retried forever. Reprocessing creates a new trace linked to the original.
