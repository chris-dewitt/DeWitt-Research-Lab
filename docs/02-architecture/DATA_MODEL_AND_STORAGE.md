---
document_id: DRL-ARC-009
title: "Canonical Data Model and Storage Strategy"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Canonical Data Model and Storage Strategy

## PostgreSQL domains

- identity and tenant;
- sessions and tasks;
- skills/tools/versions;
- policy decisions and approvals;
- trace metadata and event indexes;
- evidence metadata and claims;
- model registry and invocations;
- evaluation suites, runs, metrics, findings;
- public corpus metadata;
- synthetic institutions and scenario runs;
- release and document registry.

Large bodies, documents, datasets, checkpoints, audio where allowed, reports, and replay bundles live in object storage with immutable version and hash references.

## Vector storage

Use pgvector initially for documentation and bounded corpora where operational simplicity outweighs specialized scale. Vector records retain tenant/public scope, embedding model/revision, source/chunk IDs, timestamps, and content hashes. Retrieval is hybrid where useful and always applies authorization filters before ranking.

## Temporal fields

Evidence and data records distinguish:

- `event_time`;
- `publication_time`;
- `effective_time`;
- `ingested_at`;
- `valid_from` / `valid_to` for versioned interpretation;
- `observed_at` for market snapshots.

“As of” queries use explicit semantics, not ingestion time alone.

## Migration policy

- forward-only versioned migrations in normal deployment;
- migration tested against representative data;
- expand/migrate/contract for breaking changes;
- rollback plan may use application revision and forward correction rather than unsafe down migration;
- backups and restore test before destructive migration.
