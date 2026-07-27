---
document_id: DRL-MOD-001
title: "Atticus Open-Weight Model Research Program"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Atticus Open-Weight Model Research Program


## Open-model identity

Atticus is the flagship public research artifact of DRL. The model family must be usable outside the official website and must ship as part of an open commons containing weights or lawful derivatives, recipes, data manifests, evaluation code, local/cloud runtime profiles, cards, and failure evidence. The runtime is deliberately model-pluralistic: DRL selects an official Core and Edge through evidence, while preserving adapters so researchers can compare compatible open models.

The laboratory distinguishes open-source software, Open Source AI, open-weight models, and source-available artifacts according to the root Open Research Charter. If an upstream license or missing training materials prevent Atticus from meeting the Open Source AI definition, the release is labeled an open-weight derivative without embarrassment or marketing ambiguity.

Success is measured partly by external use: clean-room installs, independent evaluations, community adapters, research replications, teaching use, and useful upstream contributions. Download count alone is not a research outcome.

## Research objective

Create publicly released, locally runnable model variants specialized for operating DRL through reliable routing, typed tool calls, permission awareness, evidence synthesis, repository assistance, and recovery from execution failure.

The project is post-training, evaluation, and systems research. It does not claim to train a frontier foundation model from random initialization.

## Hypotheses

1. Focused post-training and a disciplined scaffold can improve agent reliability more efficiently than scaling parameters alone.
2. Explicit training on permission and approval boundaries can reduce unsafe proposals, but deterministic policy remains necessary.
3. Trajectory-level evaluation will reveal regressions hidden by final-answer metrics.
4. Edge can be distilled to handle intent, simple tools, and escalation while Core handles complex synthesis.
5. High-quality reviewed examples, counterexamples, and environment feedback matter more than a very large low-quality synthetic corpus.
6. Model behavior improves when tools have clear schemas, discriminative descriptions, and stable error messages.

## Product family

### Atticus Core

- target: approximately 8–10B deployable class;
- public Cloud Run GPU and stronger local hardware;
- complex routing, multi-tool workflows, coding, research synthesis;
- primary model for public laboratory operator.

### Atticus Edge

- target: approximately 2–4B deployable class;
- laptops and low-latency local voice paths;
- intent, simple tools, approval presentation, offline docs, escalation;
- may use distillation from Core/teacher models.

### Optional micro-router

A sub-billion function-calling model may be evaluated for wake-to-intent and deterministic tool selection, but it does not replace Edge's conversational role. It becomes a component only if measured latency/quality justifies complexity.

## Research workstreams

- base-model bake-off;
- tool and policy dataset creation;
- SFT recipe and data-mixture ablations;
- preference optimization;
- environment/trajectory optimization if justified;
- safety and prompt-injection training;
- Core-to-Edge distillation;
- quantization and runtime compatibility;
- calibration and escalation;
- model cards, safety reports, and replication packages.

## Release artifact set

- exact upstream revision and license report;
- adapters and merged weights where lawful;
- safetensors and selected quantizations;
- tokenizer/chat-template/tool-parser configuration;
- inference images/configuration;
- training config and environment lock;
- data manifest and hashes;
- benchmark and ablation reports;
- safety and limitations report;
- model card;
- Colab quickstart and Vertex reproducibility job;
- signed checksums and software bill of materials for serving image.

## Model release names

Use research-style names rather than implying frontier scale:

```text
Atticus-Core-<base>-<major.minor>
Atticus-Edge-<base>-<major.minor>
```

Model releases and application releases are versioned separately. Atticus runtime must not assume every model revision supports identical tools or context behavior.
