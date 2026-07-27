---
document_id: DRL-EVA-003
title: "Metrics, Scoring, and Aggregation"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Metrics, Scoring, and Aggregation

## Core metrics

### Routing/tool

- exact and semantic route accuracy;
- top-k route accuracy;
- tool selection precision/recall;
- argument schema validity;
- field-level accuracy;
- unnecessary tool rate;
- invented tool rate.

### Policy

- unsafe allow rate;
- incorrect denial rate;
- approval-required recall;
- approval summary completeness;
- approval binding correctness;
- private/cloud route correctness.

### Trajectory

- task success;
- valid step sequence;
- side-effect violations;
- recovery success;
- retry efficiency;
- step/tool count;
- human intervention rate;
- trace completeness.

### Evidence/RAG

- retrieval recall/precision at k;
- MRR/nDCG where labels support them;
- context relevance;
- claim support/entailment;
- citation correctness and completeness;
- temporal correctness;
- contradictory-evidence handling.

### Operations

- latency and time to first token;
- throughput;
- memory;
- token and dollar cost;
- cold-start rate;
- error/fallback rate;
- cost per successful task.

## Aggregation

Report macro and weighted averages, category tables, critical-case counts, distributions, and worst-case examples. Safety-critical failures are not diluted by averaging. Missing/failed runs are counted explicitly, not dropped.
