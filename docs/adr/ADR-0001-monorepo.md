---
document_id: DRL-ADR-0001
title: "Use a Monorepo"
version: 1.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# ADR-0001: Use a monorepo

## Decision

All DRL applications, services, packages, model recipes, datasets, infrastructure, and documentation begin in one monorepo.

## Rationale

Shared schemas, sequential agents, unified CI, coordinated V1, and cross-system integration outweigh independent release convenience at this stage.

## Consequences

Component boundaries remain explicit. Packages may publish independently later.
