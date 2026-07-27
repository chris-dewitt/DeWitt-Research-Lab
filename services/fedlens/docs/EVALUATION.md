---
document_id: DRL-FED-104
title: "FedLens Evaluation and Acceptance Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # FedLens Evaluation and Acceptance Specification

    ## Evaluation contract

    Evaluations test actual product/research claims. Each claim has population, threat model, metric, uncertainty treatment, slices, failure examples, owner, and release threshold. A single aggregate score is never sufficient.

    ## Claims

    - Corpus and source-version metadata are accurate.
- Exact and semantic diffs identify material changes.
- Search results are relevant and citations support claims.
- Topic and tone estimates are valid within declared scope.
- Event-study calculations reproduce.
- As-of queries avoid later corrections and annotations.

    ## Required suites

    - Golden document and version corpus.
- Sentence/section alignment benchmark.
- Human-annotated retrieval, topic, and tone set with disagreement.
- Temporal and correction tests.
- Event-study golden fixtures and exchange/timezone calendars.
- Prompt-injection and source-integrity tests.

    ## Metrics and analysis

    - Corpus completeness and metadata accuracy.
- Alignment span F1 and edit accuracy.
- Retrieval recall/nDCG and citation entailment.
- Annotation macro-F1, calibration, and inter-rater agreement.
- Event-study exact/tolerance accuracy.
- Temporal leakage and correction-version errors.
- Latency and cost.

    Paired tests or bootstrap intervals are used where appropriate. Repeated tuning against a benchmark is tracked. Human and model judges include calibration, disagreement, and limitations; model-judge output is not objective truth.

    ## Release gates

    - Exact source/version and event-study critical tests pass.
- No accepted future/correction leakage.
- NLP metrics meet slice thresholds and limitations are current.
- Public claims pass evidence/methods review.
- Integrated statement-comparison workflow succeeds.

    A noncritical regression needs a time-bounded exception with user value, affected slices, mitigation, owner, expiry, and director approval. Security/privacy boundary and deterministic-correctness failures cannot be averaged away.

    ## Adversarial program

    - Corrected or duplicate documents.
- PDF/HTML discrepancies.
- Timezone and DST release errors.
- Quoted language, sarcasm, or adversarial text.
- Speaker-role changes.
- Thin or cherry-picked event windows.
- Data snooping and unsupported causality.

    ## Required evidence

    - Corpus and rights manifest.
- Golden alignment report.
- Annotation protocol and agreement report.
- Retrieval/citation report.
- Event-study replication package.
- Limitations and failure cards.

    Reports pin code, data, model/provider, prompt/template, tool, configuration, environment, sample counts, exclusions, costs, failures, and reproduction commands. Public metrics link to signed reports.
