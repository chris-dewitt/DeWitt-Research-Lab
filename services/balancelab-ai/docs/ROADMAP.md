---
document_id: DRL-BAL-105
title: "BalanceLab AI Build Roadmap"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # BalanceLab AI Build Roadmap

    ## Delivery philosophy

    BalanceLab AI is built as thin verified vertical slices. Each slice includes contracts, implementation, tests, telemetry, documentation, demo evidence, and rollback—not an isolated subsystem no user can exercise.

    ## Workstreams

    - Schemas and synthetic generator.
- Deterministic calculation engine.
- Artifact and reconciliation framework.
- API and storage.
- Atticus translation and explanation.
- Web workstation.
- Evaluation and methods publication.

    ## Dependency order

    Methods and schemas → golden fixtures → engine and reconciliation → artifacts/API → natural-language translation/explanation → workstation → integrated evaluation and release.

    ## Cross-project dependencies

    - DRL protocol and provenance.
- EvalForge numeric and agent evaluation.
- Atticus tool adapter.
- Lab-web chart/workstation components.
- GCP CPU jobs, storage, and SQL.
- Public method documentation and clean-room review.

    ## Release evidence

    - Clean-room and source declaration.
- Formula/method report.
- Golden/property/reconciliation results.
- Sample datasets and artifacts.
- Explanation evaluation.
- Signed integrated trace.
- Security, privacy, deployment, cost, and rollback evidence.

    ## Explicitly deferred

    - Regulatory production use.
- Employer models or live bank data.
- Advanced optionality/prepayment beyond declared V1.
- Arbitrary user code or models.
- Commercial financial advice.

    Deferred work may appear on the public roadmap but cannot be implied by V1 marketing. Agents must not widen authority or scope “helpfully.”
