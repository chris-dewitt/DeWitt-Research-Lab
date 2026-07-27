---
document_id: DRL-DAT-003
title: "AtticusBench V1 Dataset and Benchmark Specification"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# AtticusBench V1 Dataset and Benchmark Specification

## Purpose

AtticusBench measures whether a model and scaffold can operate DRL safely and effectively. It is not a general intelligence benchmark. It evaluates model proposals, full trajectories, and human-control behavior.

## V1 scale

Minimum target:

- public development set: 1,500 cases;
- public validation set: 500 cases;
- private held-out gold set: 1,000 cases;
- adversarial expansion set: at least 500 cases;
- environment/repository fixtures: at least 50 distinct workspaces.

Counts may increase, but quality and category balance take precedence.

## Category taxonomy

| Category | Example | Primary measures |
|---|---|---|
| Intent routing | choose Atlas vs FedLens | route accuracy/calibration |
| Multi-system routing | macro + Fed + scenario | selected specialists/order |
| Tool selection | choose read vs write tool | exact/semantic accuracy |
| Arguments | dates, units, repository paths | schema and field correctness |
| Permissions | draft versus send | policy decision |
| Approval | bind exact action | timing and summary quality |
| Recovery | timeout or validation error | bounded correct recovery |
| Repository | inspect/test/patch | task success and change safety |
| Evidence | support claim from bundle | grounding/citation entailment |
| Temporal research | answer as of date | timestamp correctness |
| Calculation compliance | call BalanceLab | artifact use/consistency |
| Prompt injection | malicious source text | instruction boundary |
| Privacy routing | local versus cloud | data-boundary correctness |
| Escalation | Edge uncertainty | escalation precision/recall |
| Teaching/persona | explain appropriately | usefulness and style |

## Case structure

A case contains:

- case ID/version/category/tags;
- task and actor context;
- environment/fixture version;
- available skills/tools and schemas;
- policy configuration;
- expected required/forbidden behaviors;
- one or more acceptable trajectories;
- deterministic assertions;
- human rubric;
- severity and release-blocking status;
- provenance, generator, reviewers;
- split and contamination fingerprint.

## Gold standards

Safety, destructive-action, privacy, and prompt-injection gold cases require 100% review and independent second pass. Acceptable trajectories may be sets rather than one exact sequence; evaluation must not punish valid alternative plans.

## Split policy

- split by scenario family, fixture, and semantic template, not random row only;
- near-duplicate and embedding-similarity audits across splits;
- tool combinations and paraphrase families held out;
- private gold prompts never used for training, few-shot prompts, manual prompt tuning, or public demos;
- public validation may guide research but not become the launch gold claim.

## Benchmark tracks

- model-only proposal track;
- model plus canonical scaffold;
- full local agent environment;
- public DRL integrated track;
- Edge routing/escalation track;
- efficiency track.

Leaderboard entries specify scaffold, tools, prompts, model revision, quantization, hardware, and retries.
