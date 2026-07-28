---
document_id: DRL-EVL-104
title: "EvalForge Evaluation and Acceptance Specification"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-28
---


    # EvalForge Evaluation and Acceptance Specification

    ## Evaluation contract

    Evaluations test actual product/research claims. Each claim has population, threat model, metric, uncertainty treatment, slices, failure examples, owner, and release threshold. A single aggregate score is never sufficient.

    ## Claims

    - Framework scores and gates are reproducible and scoped.
- Baseline comparisons are statistically defensible.
- Critical gates block seeded regressions.
- Judge output is sufficiently calibrated for its declared use.
- Private and held-out data remain protected.
- Public reports accurately reflect run evidence.

    ## Required suites

    - Framework self-tests with synthetic known scores.
- Target and scorer adapter contract tests.
- Statistical golden simulations.
- Judge calibration fixtures.
- Access, contamination, and tenant/session tests.
- CI gate injection tests.
- Signed report and manifest verification.
- **Prototype (DRL-011):** held-out permission/trajectory suite covering allow,
  deny, approval, and injection slices with separate terminal and trajectory
  scores and a hard unauthorized-action gate.

    ## Metrics and analysis

    - Framework exact correctness and run reproducibility.
- Scorer and human agreement.
- Judge-human correlation, calibration, and error slices.
- Confidence-interval coverage and paired-test behavior.
- False pass/fail rate on seeded gates.
- Runtime, cost, throughput, and failed-sample rate.
- Access or contamination events.

    Paired tests or bootstrap intervals are used where appropriate. Repeated tuning against a benchmark is tracked. Human and model judges include calibration, disagreement, and limitations; model-judge output is not objective truth.

    ## Release gates

    - Deterministic framework and schema tests pass.
- Known statistical simulations produce expected decisions.
- Private dataset access and report redaction tests pass.
- CI rejects seeded critical regressions.
- Judge use is permitted only after calibration thresholds and fallback policy pass.
- Report signature and manifest validate.

    A noncritical regression needs a time-bounded exception with user value, affected slices, mitigation, owner, expiry, and director approval. Security/privacy boundary and deterministic-correctness failures cannot be averaged away.

    ## Adversarial program

    - Malicious target output and recursive traces.
- Prompt injection against judges.
- Poisoned evaluator plugins.
- Held-out label leakage and canary detection.
- Multiple-comparison and p-hacking scenarios.
- Cherry-picked slices and baseline overwrite.
- Forged report or leaderboard entry.
- Denial-of-wallet evaluation jobs.

    ## Required evidence

    - Framework self-evaluation.
- Adapter compatibility matrix.
- Statistical validation notebook/report.
- Judge calibration report.
- Contamination and access audit.
- CI seeded-regression proof.
- Signature verification and operator runbooks.

    Reports pin code, data, model/provider, prompt/template, tool, configuration, environment, sample counts, exclusions, costs, failures, and reproduction commands. Public metrics link to signed reports.
