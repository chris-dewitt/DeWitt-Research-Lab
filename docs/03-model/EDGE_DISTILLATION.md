---
document_id: DRL-MOD-008
title: "Atticus Edge Distillation and Compression Plan"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Atticus Edge Distillation and Compression Plan

## Teacher sources

- selected Atticus Core candidate;
- gold human-reviewed examples;
- larger open coding/agent model for repository tasks where licensing permits generated data use;
- deterministic policy and environment labels.

The teacher does not override human policy labels.

## Distillation targets

- route probabilities or labels;
- selected tool and arguments;
- escalation decision;
- concise approval explanation;
- short grounded response;
- refusal/alternative for high-risk requests.

## Data selection

Prioritize ambiguous boundaries, confusing tool sets, low-confidence cases, and examples where the base Edge model disagrees with Core/gold labels. Avoid filling the set with trivial high-confidence routes.

## Evaluation

- route accuracy and calibration;
- unsafe under-escalation;
- unnecessary over-escalation;
- tool schema validity;
- privacy-preserving route choice;
- latency and power/resource profile;
- robustness to voice transcription noise;
- general ability retention.
