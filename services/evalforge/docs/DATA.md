---
document_id: DRL-EVL-102
title: "EvalForge Data and Persistence Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # EvalForge Data and Persistence Specification

    ## Principles

    EvalForge stores only state required for declared purposes. Storage location, classification, retention, deletion, telemetry eligibility, training eligibility, and rights are explicit fields or policies—not conventions inferred from code.

    ## Canonical entities

    - Suite, case, dataset version, slice, and access tier.
- Target, runtime, prompt, tool, model, and environment snapshot.
- Run, sample, trace, output, and artifact.
- Score, judge, human review, and adjudication.
- Comparison, statistics, baseline, gate, exception, report, and leaderboard.

    ## Classification and handling

    - Public benchmarks and approved public results.
- DRL-private holdouts and results.
- Local-personal evaluation data.
- Online traces only with consent and privacy filtering.
- Provider prompts/responses classified by source rights and diagnostic mode.
- Hidden labels are restricted.

    ## Persistence services

    - PostgreSQL for registry, run, score, gate, and metadata.
- Object storage for immutable datasets, outputs, traces, and signed reports.
- Local filesystem backend for offline contributors.
- Cloud job runner for full suites.
- Training systems have no default access to held-out data.

    ## Retention and deletion

    - Public releases remain available and versioned.
- Holdout access logs retain under research-integrity policy.
- Raw online trace content retains less time than aggregate metrics.
- Temporary failed outputs expire after the diagnostic window.
- User deletion applies unless content was explicitly donated and irreversibly published under disclosed terms.

    Deletion is a traceable workflow with an identifier and terminal outcome. Backup expiration is described honestly. Legal/security holds, if any, are explicit and restricted.

    ## Provenance and lineage

    - Git revision, environment lock/container digest, hardware, runtime, and seed.
- Target model/provider revision, prompts/templates, tool versions, and configs.
- Dataset, suite, scorer, and judge versions.
- Sample exclusions, failures, human reviewers, and adjudication.
- Report signature and artifact digests.

    Every derived artifact records source identifiers, acquisition time, effective/as-of time where applicable, transformation version, code/model/configuration revisions, rights decision, and content digest. Untraceable artifacts cannot support public claims.

    ## Migration policy

    - Results are immutable; corrections append superseding analysis/reports.
- Dataset updates create new versions.
- Scorer migrations produce new result sets while preserving originals.
- Comparison-code revisions are recorded and can reproduce prior decisions.

    Migrations are versioned and tested on representative data. Destructive migrations require backup, rehearsal, verification, and director approval. Protocol-facing changes coordinate schema/API versions.

    ## Required tests

    - required fields, uniqueness, referential integrity, enum and unit domains;
    - timezone and historical/as-of semantics;
    - idempotent ingestion and partial-write recovery;
    - tenant/session/access isolation;
    - retention and deletion;
    - lineage completeness and artifact digest;
    - representative scale and recovery behavior.
