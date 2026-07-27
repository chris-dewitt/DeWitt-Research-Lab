---
document_id: DRL-EVA-002
title: "Evaluation Taxonomy and Test Strategy"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Evaluation Taxonomy and Test Strategy

## Levels

1. model response;
2. structured proposal;
3. retrieval result;
4. individual tool call;
5. trajectory;
6. final report;
7. system performance;
8. human experience;
9. operational drift.

## Methods

- exact/deterministic assertions;
- schema and constraint validation;
- reference-based scoring;
- retrieval ranking metrics;
- execution-based tests;
- property/invariant tests;
- human rubric;
- calibrated LLM judge;
- pairwise preference;
- adversarial and metamorphic tests;
- performance/cost benchmarks;
- production trace sampling.

Every metric documents what it measures, what it does not, direction, range, aggregation, missing handling, and release use.
