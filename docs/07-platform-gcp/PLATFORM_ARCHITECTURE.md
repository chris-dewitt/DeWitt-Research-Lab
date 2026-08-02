---
document_id: DRL-GCP-001
title: "Google Cloud Platform Architecture"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Google Cloud Platform Architecture

## V1 service map

| Capability | Service | Rationale |
|---|---|---|
| Next.js website | Firebase App Hosting | GitHub integration, managed Next.js support, custom domain |
| Public APIs | Cloud Run services | container portability, managed identity, scale-to-zero |
| Open-weight inference | Cloud Run GPU | bursty public workload and scale-to-zero; validate cold-start/cost |
| Batch ingestion/evals | Cloud Run Jobs | bounded container jobs |
| Training | Vertex AI custom jobs | reproducible managed jobs and GPU selection |
| Exploration | Colab | interactive notebooks, not production |
| Relational/vector data | Cloud SQL PostgreSQL + pgvector | one managed system for metadata and bounded vector use |
| Artifacts/corpora | Cloud Storage | object versioning/lifecycle |
| Targeted async work | Cloud Tasks | rate-controlled HTTP tasks |
| Fan-out events | Pub/Sub | decoupled event delivery |
| Secrets | Secret Manager | versioning/audit with workload identity |
| Images/packages | Artifact Registry | current Google container/artifact registry |
| Logs/metrics/traces | Cloud Logging/Monitoring + OTel | operational visibility |
| Identity | Firebase Auth + workload identity | public users and services |

## Project layout

Use separate projects to reduce blast radius:

```text
drl-shared       DNS/artifact policy/optional shared CI identities
drl-dev          developer cloud services and synthetic data
drl-stage        production-like release candidate
drl-prod         public services and production state
drl-research     Vertex jobs, datasets, checkpoints, no prod credentials
```

Billing budgets and alerts exist per project and aggregate account.

## Region

Choose a primary US region after Cloud Run GPU, Cloud SQL, Firebase, and Vertex availability/cost review. Co-locate latency-sensitive services and data. Public datasets may be multi-region object storage only when justified. Record residency and egress implications.

## Network

- public ingress only for web/API endpoints that require it;
- authenticated internal service endpoints;
- Cloud SQL private connectivity/direct VPC egress where selected;
- restricted egress for tool workers;
- no public database;
- separate administrative access paths;
- local runner connects outbound over TLS.
