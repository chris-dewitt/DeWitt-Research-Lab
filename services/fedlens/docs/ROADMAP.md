---
document_id: DRL-FED-105
title: "FedLens Build Roadmap"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # FedLens Build Roadmap

    ## Delivery philosophy

    FedLens is built as thin verified vertical slices. Each slice includes contracts, implementation, tests, telemetry, documentation, demo evidence, and rollback—not an isolated subsystem no user can exercise.

    ## Workstreams

    - Corpus and version acquisition.
- Parsing, alignment, and exact diff.
- Search and policy timeline.
- Annotation and NLP models.
- Event-study engine.
- Atticus and Atlas integration.
- Public visual research experience.

    ## Dependency order

    Source registry and golden corpus → parser/version ledger → exact diff → search/timeline → annotation evaluation → event engine → integration/demo → release.

    ## Cross-project dependencies

    - DRL protocol and provenance.
- Atlas shared document primitives without shared domain ownership.
- EvalForge retrieval/NLP/statistical evaluation.
- Lab-web visualizations.
- GCP jobs, storage, and SQL.
- Atticus skill and evidence schema.

    ## Release evidence

    - Corpus and rights manifest.
- Golden diff report.
- Annotation and retrieval evaluation.
- Event-study replication package.
- Signed integrated trace.
- Public methods/limitations.
- Operations, budget, and rollback evidence.

    ## Explicitly deferred

    - Automated policy forecasts.
- Proprietary market feeds.
- Broad central-bank corpus.
- Causal claims beyond declared designs.
- Personalized trading conclusions.

    Deferred work may appear on the public roadmap but cannot be implied by V1 marketing. Agents must not widen authority or scope “helpfully.”
