---
document_id: DRL-GCP-003
title: "IAM and Workload Identity Design"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# IAM and Workload Identity Design

## Principles

- one service account per deployable workload or trust boundary;
- no default compute identities with broad roles;
- no user-managed long-lived service-account keys;
- GitHub deployment through OIDC/workload identity federation where feasible;
- environment-specific identities;
- deny production access from research project;
- periodic permission review.

## Example identities

- `lab-web-runtime`;
- `atticus-control-runtime`;
- `atticus-model-runtime`;
- `atlas-runtime` and `atlas-ingest`;
- `fedlens-runtime` and `fedlens-ingest`;
- `balancelab-runtime`;
- `evalforge-runtime` and `evalforge-batch`;
- `release-deployer`;
- `vertex-training`;
- `backup-operator`.

Each receives specific database, bucket, topic, task, secret, and model permissions. Services call one another using audience-bound identity tokens; trusting the network alone is insufficient.
