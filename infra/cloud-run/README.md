---
document_id: DRL-SYS-022
title: "Cloud Run Service Standard"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Cloud Run Service Standard

Every service must define:

- container image;
- non-root execution where supported;
- health and readiness endpoints;
- resource limits;
- concurrency;
- timeout;
- min and max instances;
- authentication;
- ingress;
- service account;
- secret references;
- structured logs;
- OpenTelemetry export;
- quota and budget behavior;
- rollback command.

GPU inference must document model load time, cold-start behavior, memory, concurrency, and scale-to-zero tradeoffs.
