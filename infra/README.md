---
document_id: DRL-SYS-020
title: "Infrastructure Directory"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Infrastructure

This directory owns reproducible local and Google Cloud environments.

## Layout

```text
infra/
  terraform/
    modules/
    environments/
      dev/
      staging/
      prod/
  colab/
  cloud-run/
  observability/
```

## Rules

- Terraform is authoritative for cloud resources.
- No secrets in state inputs or source control.
- Production changes use pull requests and plans.
- Every service has health, readiness, logs, metrics, budgets, and rollback.
- Development supports mocks and local containers.
