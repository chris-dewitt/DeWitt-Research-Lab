---
document_id: DRL-EVA-001
title: "EvalForge System Specification"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# EvalForge System Specification

## Mission

Provide an independent, open-source evaluation platform for model responses, retrieval systems, tool-using agents, full trajectories, policy compliance, and DRL release gates.

## Standalone value

A developer can install EvalForge without running DRL:

```bash
uv add evalforge
# or
pip install evalforge

evalforge init
evalforge run evals/
evalforge compare baseline.json candidate.json
evalforge report --format html
```

## Components

- case/dataset loader;
- environment/fixture interface;
- run adapter for model, RAG, agent, or trace;
- evaluator registry;
- deterministic and judge evaluators;
- human-review queue/export;
- metric aggregation and statistical comparison;
- report generator;
- baseline store;
- CI gate;
- red-team runner;
- web report/leaderboard API.

## Design principles

- evaluator definitions are versioned and inspectable;
- raw item results retained for error analysis;
- no single composite hides critical failures;
- deterministic evaluators preferred where possible;
- judge models calibrated and replaceable;
- trajectory and output evaluated separately;
- thresholds can be absolute, relative, and critical-case zero-tolerance;
- reports contain environment and cost metadata.

## V1 interfaces

- Python SDK;
- CLI;
- JSON/YAML case format;
- JSON result/report schema;
- HTML report;
- GitHub Actions summary/annotation;
- DRL trace adapter;
- provider adapters behind stable interface.
