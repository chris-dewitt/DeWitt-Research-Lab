---
document_id: DRL-MOD-012
title: "Model Reproducibility and Experiment Tracking"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Model Reproducibility and Experiment Tracking

## Reproduction levels

- **L1:** inference can be reproduced from public artifact and config.
- **L2:** evaluation can be reproduced from public cases and runner.
- **L3:** adapter training can be reproduced from public dataset and recipe.
- **L4:** merged/quantized release can be reconstructed and hashes matched where deterministic.

Each release states achieved level and exclusions.

## Experiment repository

`research/experiments/<experiment-id>/` contains:

- hypothesis;
- preregistered primary metrics where appropriate;
- config;
- data/model manifests;
- launch command;
- environment/container;
- results and plots;
- error analysis;
- cost;
- conclusion and follow-up;
- link to immutable artifacts.

Failed experiments are retained when informative and sanitized for release.
