---
document_id: DRL-ARC-015
title: "Service Objectives, Resilience, and Disaster Recovery"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Service Objectives, Resilience, and Disaster Recovery

## V1 objectives

Targets are refined after baseline testing.

- static website monthly availability: 99.9% target;
- public API successful request availability excluding quota/policy denials: 99.0% target;
- public replay availability independent of GPU: 99.5% target;
- trace metadata completeness: 99.9% of accepted tasks;
- unauthorized consequential actions in release/production confirmed incidents: zero tolerance;
- p95 cold Atticus response: visible status within 2 seconds, useful replay offered within 5 seconds;
- RPO critical transactional state: 24 hours maximum initially, target lower after cost review;
- RTO website/replay: 4 hours; transactional services: 8 hours initial target.

## Failure isolation

- website and docs survive specialist/model outage;
- one specialist outage does not corrupt others;
- public and private data stores/buckets separated;
- model serving failure cannot bypass policy;
- evaluation outage cannot delete traces;
- queue backpressure protects databases and GPUs.

## Recovery drills

Before V1:

- restore Cloud SQL backup to isolated project;
- restore replay/report object versions;
- redeploy previous service/model revisions;
- rotate compromised service and local-device credentials;
- disable public live tools while retaining static/replay site;
- reconstruct release from source, lockfiles, Terraform, and artifact manifest.
