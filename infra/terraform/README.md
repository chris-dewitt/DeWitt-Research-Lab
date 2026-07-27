---
document_id: DRL-SYS-021
title: "Terraform Plan"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Terraform Plan

## Planned modules

- project-services
- artifact-registry
- cloud-run-service
- cloud-run-job
- cloud-sql
- storage-bucket
- secret-manager
- service-account
- monitoring
- budgets
- networking
- firebase integration

## Environments

Each environment composes modules and has separate state.

- `dev`
- `staging`
- `prod`

Remote state and bootstrap strategy require an approved implementation ADR.

## Security

- least privilege;
- workload identity where applicable;
- no user-managed service-account keys;
- secret references rather than values;
- public ingress only where explicitly required;
- private database access;
- deletion protection in production.
