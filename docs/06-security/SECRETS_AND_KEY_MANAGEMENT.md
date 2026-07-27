---
document_id: DRL-SEC-006
title: "Secrets, Keys, and Credential Management"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Secrets, Keys, and Credential Management

## Storage

- Google Secret Manager for cloud application secrets;
- workload identity instead of long-lived service-account keys;
- OS credential manager for local device secrets;
- GitHub OIDC for cloud deployment where feasible;
- no secrets in `.env.example`, fixtures, traces, screenshots, notebooks, or model data.

## Lifecycle

- owner and purpose;
- least-privilege scope;
- issuance and rotation schedule;
- expiry where supported;
- access audit;
- incident revocation;
- deletion after decommission.

## Redaction

Redact common secret patterns before logs or donated traces. Redaction is defense in depth; the system should avoid capturing content in the first place. Secret scans run pre-commit/CI and release bundles.

## Model boundary

Credentials are never inserted into model prompts. Tools use credentials internally after policy approval; model sees safe status/result only.
