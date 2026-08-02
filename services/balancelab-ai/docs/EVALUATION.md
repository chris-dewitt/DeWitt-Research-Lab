---
document_id: DRL-BAL-104
title: "BalanceLab AI Evaluation and Acceptance Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # BalanceLab AI Evaluation and Acceptance Specification

    ## Evaluation contract

    Evaluations test actual product/research claims. Each claim has population, threat model, metric, uncertainty treatment, slices, failure examples, owner, and release threshold. A single aggregate score is never sufficient.

    ## Claims

    - Numerical calculations are correct for declared methods.
- Reconciliation catches invalid states.
- Runs are reproducible.
- Natural-language scenario translation preserves intent and surfaces ambiguity.
- Explanations are faithful and introduce no unsupported numbers.
- Public demonstrations use synthetic data.

    ## Required suites

    - Unit and golden formula tests.
- Property-based accounting and reconciliation.
- Scenario boundary and metamorphic tests.
- Artifact reproducibility.
- Natural-language to scenario semantic validation.
- Explanation numeric and driver faithfulness.
- Upload security, privacy, and tenant isolation.

    ## Metrics and analysis

    - Exact or tolerance numeric accuracy.
- Reconciliation-failure detection.
- Artifact digest reproducibility.
- Scenario field accuracy, critical omissions, and clarification rate.
- Explanation numeric consistency and driver support.
- Task success, latency, memory, and cost by institution/horizon.

    Paired tests or bootstrap intervals are used where appropriate. Repeated tuning against a benchmark is tracked. Human and model judges include calibration, disagreement, and limitations; model-judge output is not objective truth.

    ## Release gates

    - Critical deterministic tests and identities pass 100%.
- No unsupported numeric value appears in critical explanation suite.
- Ambiguous material assumptions never execute without confirmation.
- Synthetic/private labeling and isolation tests pass.
- Reference scenarios reproduce from manifest.

    A noncritical regression needs a time-bounded exception with user value, affected slices, mitigation, owner, expiry, and director approval. Security/privacy boundary and deterministic-correctness failures cannot be averaged away.

    ## Adversarial program

    - Negative or zero rates and extreme shocks.
- Missing maturities and nonmonotonic dates.
- Unit confusion, NaN, overflow, and duplicated positions.
- CSV/spreadsheet formula injection.
- Prompt injection in labels or method documents.
- Attempt to upload employer/proprietary data.
- Artifact tampering and cross-user access.

    ## Required evidence

    - Public methods/formula report.
- Golden and property-test report.
- Independent quantitative review.
- Scenario translation evaluation.
- Explanation faithfulness report.
- Sample artifact manifests.
- Security, privacy, and clean-room reports.

    Reports pin code, data, model/provider, prompt/template, tool, configuration, environment, sample counts, exclusions, costs, failures, and reproduction commands. Public metrics link to signed reports.
