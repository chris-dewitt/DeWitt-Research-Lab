---
document_id: DRL-EVA-009
title: "CI Regression and Release Evaluation Gates"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# CI Regression and Release Evaluation Gates

## PR tier

Fast deterministic and sampled suites:

- schemas/contracts;
- policy/approval;
- unit tool cases;
- prompt-injection smoke;
- small baseline comparison for model/prompt changes.

## Nightly tier

- larger AtticusBench development set;
- RAG/citation tests;
- integration fixtures;
- dependency/runtime matrix;
- performance trend.

## Release-candidate tier

- complete private gold;
- adversarial/security suite;
- repeated stochastic subset;
- human/judge review;
- quantization/runtime matrix;
- live integrated workflow;
- load/cost/cold-start;
- accessibility and usability evidence.

## Gate logic

- zero critical regressions;
- absolute threshold on critical categories;
- candidate not materially worse than prior stable release;
- declared budget and latency targets;
- director approval for accepted noncritical regressions with explanation.
