---
document_id: DRL-GCP-011
title: "Cloud Observability, SLOs, and Alerts"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Cloud Observability, SLOs, and Alerts

## Dashboards

- public web and API health;
- Atticus model warm/cold latency, queue, tokens, cost;
- specialist errors and data freshness;
- policy denials/approvals and unusual patterns;
- evaluation drift;
- Cloud SQL connections/latency/storage;
- queue backlog/dead letters;
- project spend and forecast;
- release revision comparison.

## Alerts

Actionable alerts only:

- availability/error budget burn;
- critical security event;
- cross-tenant or unauthorized action finding;
- GPU/max instance/budget threshold;
- stale critical source;
- dead-letter backlog;
- failed backups/restore test;
- database resource saturation;
- certificate/domain issue;
- production release health regression.

Every alert links a runbook and owner. Avoid paging for expected scale-to-zero cold starts.
