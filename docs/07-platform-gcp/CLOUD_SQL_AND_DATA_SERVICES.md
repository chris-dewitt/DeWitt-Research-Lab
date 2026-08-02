---
document_id: DRL-GCP-009
title: "Cloud SQL PostgreSQL and Data Service Design"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Cloud SQL PostgreSQL and Data Service Design

## Usage

PostgreSQL stores transactional metadata, identities/tenants, tasks, approvals, trace indexes, evidence metadata, evaluation, corpora metadata, and synthetic scenarios. pgvector supports bounded retrieval indexes where tested.

## Controls

- current supported PostgreSQL major version selected by ADR;
- private connectivity;
- connection pooling appropriate to Cloud Run;
- IAM/database credentials and Secret Manager as selected;
- automated backups and point-in-time recovery where budget permits;
- deletion protection in production;
- maintenance window;
- query and connection monitoring;
- tenant-aware repository layer;
- migrations in CI/stage;
- least-privilege database roles per service.

## pgvector

Store embedding model/revision, dimension, source hash, and index configuration. Benchmark exact/approximate search, filters, corpus size, and update behavior. Do not choose a dedicated vector database before measured need.
