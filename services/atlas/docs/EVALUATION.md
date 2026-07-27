---
document_id: DRL-ATL-104
title: "Atlas Evaluation and Acceptance Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atlas Evaluation and Acceptance Specification

    ## Evaluation contract

    Evaluations test actual product/research claims. Each claim has population, threat model, metric, uncertainty treatment, slices, failure examples, owner, and release threshold. A single aggregate score is never sufficient.

    ## Claims

    - Point-in-time answers avoid future leakage.
- Retrieved evidence is relevant and sufficiently covers the question.
- Citations support associated claims.
- Deterministic analytics reproduce.
- Source failures and staleness are visible.
- Public outputs obey rights policy.

    ## Required suites

    - Synthetic release/revision temporal tests.
- Human-labeled macro retrieval benchmark.
- Citation entailment and coverage.
- Connector contract and data-quality fixtures.
- Golden deterministic calculations.
- Rights and export enforcement.
- End-to-end snapshot reproduction.

    ## Metrics and analysis

    - Temporal leakage and eligibility precision.
- Retrieval recall@k, nDCG, and MRR.
- Evidence and contradiction coverage.
- Citation entailment and claim coverage.
- Exact/tolerance numeric accuracy.
- Connector success, freshness, and quarantine rates.
- Artifact digest agreement, latency, and cost.

    Paired tests or bootstrap intervals are used where appropriate. Repeated tuning against a benchmark is tracked. Human and model judges include calibration, disagreement, and limitations; model-judge output is not objective truth.

    ## Release gates

    - Zero accepted future-leakage cases in critical suite.
- Golden calculations and schema tests pass.
- Retrieval/citation thresholds pass by task and source slice.
- Rights-policy tests pass.
- Reference research snapshot reproduces.

    A noncritical regression needs a time-bounded exception with user value, affected slices, mitigation, owner, expiry, and director approval. Security/privacy boundary and deterministic-correctness failures cannot be averaged away.

    ## Adversarial program

    - Misleading dates and revised or retracted releases.
- Duplicate or contradictory sources.
- Prompt injection in documents.
- Malformed units and silent source schema changes.
- Restricted-content requests.
- Unsupported causal claims and false precision.

    ## Required evidence

    - Source and rights register.
- Connector/data-quality report.
- Temporal leakage report.
- Retrieval/citation benchmark.
- Calculation audit and reproduction log.
- Rights review and failure museum cards.

    Reports pin code, data, model/provider, prompt/template, tool, configuration, environment, sample counts, exclusions, costs, failures, and reproduction commands. Public metrics link to signed reports.
