---
document_id: DRL-ADR-0002
title: "Google-First Cloud"
version: 1.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# ADR-0002: Use a Google-first cloud architecture

## Decision

Colab and Vertex AI support training; Cloud Run, Cloud SQL, Cloud Storage, Artifact Registry, Secret Manager, Firebase Authentication, and Terraform support the computational and interactive application platform. Wix at `www.dwit-labs.com` is the canonical institutional site under ADR-0008.

## Consequences

Adapters preserve portability. No core domain logic may depend directly on provider-specific SDKs.


## Clarification under ADR-0008

Google-first remains the infrastructure decision for training, inference, APIs, databases, application frontends, and observability. It no longer implies that the canonical institutional homepage must be hosted on Firebase.
