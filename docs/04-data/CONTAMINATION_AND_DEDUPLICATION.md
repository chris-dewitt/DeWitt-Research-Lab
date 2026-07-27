---
document_id: DRL-DAT-007
title: "Contamination, Leakage, and Deduplication Controls"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Contamination, Leakage, and Deduplication Controls

## Threats

- exact duplicates across train/test;
- paraphrase families split randomly;
- fixture or expected-output leakage;
- benchmark examples included in prompts or synthetic generation;
- model pretraining exposure to public benchmark;
- agent developers manually tuning against private gold;
- source documents repeated across multiple datasets.

## Controls

- normalized hash and near-duplicate matching;
- semantic similarity and template-family grouping;
- fixture-level splits;
- private gold access controls and audit;
- canary strings in private evaluation;
- public benchmark versioning and rotation;
- evaluation on newly generated adversarial sets;
- disclose unavoidable possible upstream pretraining exposure.

## Release report

State methods, thresholds, removed counts, remaining uncertainty, and whether benchmark is appropriate for public leaderboard comparison versus internal regression only.
