---
document_id: DRL-PRG-005
title: "Dependency Graph and Integration Boundaries"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Dependency Graph and Integration Boundaries

## Rules

- Dependencies point inward toward stable packages; services do not import each other's internal modules.
- Cross-service calls use DRL Protocol clients.
- UI imports SDKs and generated types, not service database code.
- EvalForge may consume traces and public contracts but cannot become a hidden runtime dependency for every request.
- Policy evaluation happens before tool execution; post-execution evaluation cannot retroactively make an unsafe action acceptable.

```text
schemas/configs
      |
packages/drl-protocol
      +------------------+
      |                  |
packages/policy-engine  packages/data-provenance
      |                  |
packages/drl-ai-core ----+---- packages/observability
      |                  |
atticus-sdk         evalforge-sdk
      |                  |
services/atticus     services/evalforge
      |
      +------ specialist client contracts ------+
      |                 |                       |
 services/atlas   services/fedlens     services/balancelab-ai
      |
apps/lab-web + apps/atticus-console + apps/local-runner
```

## Forbidden dependency examples

- BalanceLab importing the Atticus planner.
- Atlas reading FedLens tables directly.
- Public web querying production databases without service APIs.
- Policy engine calling an LLM to decide whether policy applies.
- EvalForge modifying production traces under evaluation.
- Local runner trusting cloud-supplied shell strings without local policy validation.
