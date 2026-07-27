---
document_id: DRL-GCP-010
title: "Cloud Tasks, Pub/Sub, and Scheduled Work"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Cloud Tasks, Pub/Sub, and Scheduled Work

## Cloud Tasks use

- targeted report generation;
- bounded ingestion unit;
- webhook-like internal execution;
- rate-limited specialist job;
- retry with per-task schedule.

## Pub/Sub use

- `document.ingested` fan-out;
- `model.released` consumers;
- `evaluation.completed` updates;
- `source.updated` independent processing;
- operational domain events.

## Scheduler

Cloud Scheduler triggers documented HTTP/job endpoints for source collection, maintenance, evaluation sampling, and budget reports. Scheduled jobs use idempotency window and source watermark.

## Reliability

- dead-letter destinations;
- max attempts/age;
- deduplication and outbox where state consistency matters;
- tenant and trace context;
- payload contains references rather than sensitive bulk content;
- consumer validates schema/version.
