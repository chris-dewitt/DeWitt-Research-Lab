---
document_id: DRL-DAT-005
title: "Synthetic Data Generation and Validation Protocol"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Synthetic Data Generation and Validation Protocol

## Use

Commercial or open models may generate candidate tasks, paraphrases, tool errors, dialogues, and adversarial cases. Generated material is untrusted raw input.

## Generation pipeline

1. define category blueprint and target distribution;
2. generate from parameterized templates or models;
3. retain generator provider/model/version, prompt hash, seed/settings, and timestamp;
4. parse into schema;
5. run deterministic validation;
6. execute against fixture where possible;
7. deduplicate and compare against evaluation sets;
8. classify review risk;
9. human review/sample;
10. quarantine or promote.

## Automated checks

- schema and enum validity;
- tool/permission consistency;
- fixture resource existence;
- expected result from deterministic environment;
- PII/secret patterns;
- toxicity or unsafe content tagging where relevant;
- duplicate and semantic similarity;
- impossible or underspecified task detection;
- generated answer leakage into task;
- source/license metadata completeness.

## Review sampling

Routine low-risk synthetic records use stratified samples based on generator, category, tool, complexity, and validation confidence. Sampling rate increases after defects. Safety/policy cases remain 100% reviewed.

## Generator contamination

Do not ask a model to generate items using private gold examples. Prompt libraries are versioned and audited. Generated answers are not automatically used as labels when deterministic or human labels are available.
