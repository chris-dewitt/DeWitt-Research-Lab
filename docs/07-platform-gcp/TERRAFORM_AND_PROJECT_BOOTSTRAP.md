---
document_id: DRL-GCP-002
title: "Terraform, Project Bootstrap, and State"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Terraform, Project Bootstrap, and State

## Layout

```text
infra/terraform/
  modules/
    project-services/
    iam/
    artifact-registry/
    cloud-run-service/
    cloud-run-job/
    cloud-run-gpu/
    cloud-sql/
    storage-bucket/
    pubsub/
    cloud-tasks/
    secret/
    monitoring/
    firebase-app-hosting/
    budgets/
  environments/
    dev/
    stage/
    prod/
    research/
```

## State

- remote state bucket isolated and versioned;
- state access limited to infrastructure operators and CI;
- no secrets intentionally stored in Terraform state when avoidable;
- state locking/serialized applies;
- plans stored as CI artifacts with redaction;
- production apply requires protected environment approval.

## Module standards

- typed variables and validations;
- least-privilege service accounts created per workload;
- required labels: environment, system, owner, cost-center/research-program;
- log/monitor defaults;
- lifecycle and deletion protection for stateful production resources;
- outputs do not reveal secrets;
- examples and tests/validation.

## Bootstrap

Project/bootstrap privileges are separate from normal Terraform deployment. Document the few manual prerequisites and immediately move normal resources under code.
