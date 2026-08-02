---
document_id: DRL-EVL-105
title: "EvalForge Build Roadmap"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # EvalForge Build Roadmap

    ## Delivery philosophy

    EvalForge is built as thin verified vertical slices. Each slice includes contracts, implementation, tests, telemetry, documentation, demo evidence, and rollback—not an isolated subsystem no user can exercise.

    ## Workstreams

    - Manifest, schema, SDK, and CLI.
- Runner and target adapters.
- Scorers, statistics, and slices.
- Result store and reports.
- Judges and human review.
- CI and release gates.
- Public comparison and leaderboard.

    ## Dependency order

    Schemas and self-tests → local runner/scorers → result store/report → target adapters → statistics/judges → security and CI gates → public experience and release.

    ## Cross-project dependencies

    - DRL protocol and trace schemas.
- AtticusBench and project datasets.
- Every project claim map.
- GCP jobs, storage, and SQL.
- Lab-web report visualizations.
- Signing and release process.

    ## Release evidence

    - Self-test and statistical validation.
- Access and privacy audit.
- Judge calibration report.
- Seeded CI regression proof.
- Signed project reports.
- Public methods and limitations.
- Load, cost, incident, and operator evidence.

    ## Explicitly deferred

    - One universal safety score.
- Uncontrolled public code execution.
- Large commercial evaluation service.
- Automatic baseline promotion.
- Proprietary undisclosed leaderboard claims.

    Deferred work may appear on the public roadmap but cannot be implied by V1 marketing. Agents must not widen authority or scope “helpfully.”
