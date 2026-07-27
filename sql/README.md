---
document_id: DRL-ARC-030
title: "Canonical Persistence Model"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Canonical Persistence Model

The SQL directory contains reference migrations for durable platform state. Domain services may own separate schemas/databases, but identity, trace, consent, artifact, evidence, policy, and release semantics cannot drift from DRL protocol. Production migrations are forward-only, reviewed, reversible through compensating migration/restore, and tested against representative data.

`0000_reference_schema.sql` is an architectural reference, not permission to deploy without service ownership, row-level authorization, retention jobs, indexes, performance tests, and an approved migration plan.
