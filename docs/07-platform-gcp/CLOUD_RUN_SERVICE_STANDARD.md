---
document_id: DRL-GCP-005
title: "Cloud Run Service and Job Standard"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Cloud Run Service and Job Standard

## Service requirements

- non-root container user;
- read-only filesystem where feasible;
- health/readiness/startup endpoints;
- graceful shutdown and request cancellation;
- structured logs and trace propagation;
- explicit concurrency, CPU, memory, min/max instances;
- request timeout consistent with work type;
- workload identity;
- secrets referenced, not embedded;
- image pinned by digest in release manifest;
- resource labels;
- no local persistent-state assumption.

## Scale-to-zero

Default dev and low-traffic services to zero minimum instances unless background work requires otherwise. Because scaling from zero is request-triggered, asynchronous workers use Cloud Run Jobs, worker pools, scheduled wake, or explicit task design rather than assuming idle background loops restart themselves.

## Revisions

Use immutable revisions, staging smoke tests, gradual traffic migration, and immediate rollback capability. Model and application revisions are independent metadata even when packaged together.

## Jobs

Jobs have bounded tasks, retries, timeout, checkpoint strategy, and idempotent outputs. A failed job does not silently promote partial data.
