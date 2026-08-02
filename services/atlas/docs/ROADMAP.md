---
document_id: DRL-ATL-105
title: "Atlas Build Roadmap"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atlas Build Roadmap

    ## Delivery philosophy

    Atlas is built as thin verified vertical slices. Each slice includes contracts, implementation, tests, telemetry, documentation, demo evidence, and rollback—not an isolated subsystem no user can exercise.

    ## Workstreams

    - Source governance and connectors.
- Bitemporal data and snapshots.
- Retrieval and indexing.
- Deterministic analytics.
- Evidence/report API.
- Atticus integration.
- Web demo and research publication.

    ## Dependency order

    Schemas and source registry → fixture connectors → storage/time ledger → retrieval → analytics/evidence bundles → evaluation → public API/demo → scale and release.

    ## Cross-project dependencies

    - DRL protocol and provenance.
- EvalForge RAG/temporal evaluation.
- Atticus adapter.
- Lab-web charts and artifact views.
- GCP jobs, storage, and SQL.
- FedLens may reuse document primitives without losing domain ownership.

    ## Release evidence

    - Signed source/rights register.
- Data-quality and temporal reports.
- Retrieval/citation benchmark.
- Reproducible snapshot.
- Integrated Atticus trace.
- Runbooks, budget, SLO, and rollback evidence.

    ## Explicitly deferred

    - Commercial real-time feeds.
- Personalized investment advice.
- Broad web crawling.
- Automated trading.
- Causal claims without a research design.
- Proprietary source redistribution.

    Deferred work may appear on the public roadmap but cannot be implied by V1 marketing. Agents must not widen authority or scope “helpfully.”
