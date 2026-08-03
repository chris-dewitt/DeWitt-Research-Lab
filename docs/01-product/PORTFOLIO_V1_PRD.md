---
document_id: DRL-PRD-001
title: "DeWitt Research Workshop V1 Product Requirements"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# DeWitt Research Workshop V1 Product Requirements

## Product vision

DRL V1 is a public, open-source research laboratory operated by Atticus. It gives visitors a compelling way to explore real AI systems, gives contributors usable software and documentation, gives learners transparent examples, and gives the Director a credible body of applied-AI research.

## Primary audiences

1. **Collaborators and maintainers** seeking a serious open-source project with clear contribution boundaries.
2. **Tinkerers and builders** wanting reusable agent, evaluation, retrieval, and quantitative components.
3. **Students and learners** wanting transparent demonstrations and teaching materials.
4. **Academics and applied researchers** interested in benchmarks, datasets, model post-training, and reproducibility.
5. **Teachers** seeking examples and course-ready material.
6. **Hiring managers and technical leaders** evaluating the Director's engineering and research judgment.
7. **Potential sponsors, consulting clients, or training partners** seeking credible expertise without roadmap control.

## Product promise

A visitor can understand the laboratory without chat, ask Atticus to guide them, inspect live or replayed workflows, see the evidence and evaluation behind claims, run bounded public demonstrations, navigate code and documentation, and learn how to contribute.

## Required V1 capabilities

### Laboratory platform

- institutional website with mission, systems map, research archive, open-source portal, models/data, benchmarks, teaching, failure museum, console, about, and documentation;
- repository-backed content publishing;
- public status and release manifests;
- command palette and guided tours;
- accessible responsive design.

### Public Atticus

- anonymous sessions with strict quotas and allowlisted tools;
- authenticated sessions with saved public projects/history and transparent retention;
- laboratory documentation Q&A with citations;
- guided tours;
- specialist routing;
- live and replayed demonstrations;
- visible plan, tool calls, policy checks, sources, costs, and evaluation summary;
- open-weight inference path.

### Private Atticus

- Windows-first local runner;
- device pairing/revocation;
- outbound-only communication;
- local voice adapter;
- approved-directory file search;
- repository inspection, test, and patch preparation;
- local approval and audit;
- fully local inference option for supported tasks.

### Models and research

- Atticus Core and Edge research programs;
- published model artifacts when licensing permits;
- AtticusBench development and held-out evaluation sets;
- training and evaluation recipes;
- model, data, safety, and reproducibility reports.

### Specialist systems

- Atlas public macro research vertical slice;
- FedLens official-document comparison and timeline vertical slice;
- BalanceLab deterministic synthetic scenario vertical slice;
- EvalForge standalone SDK, CLI, report, and CI gate.

## Product principles

- Real capability over simulated capability; replays are clearly labeled.
- Progressive disclosure: useful in 60 seconds, inspectable for hours.
- Public data and synthetic financial models only.
- Open-weight core; provider fallback is disclosed and optional.
- A model does not receive more authority because the interface is conversational.
- The interface teaches how the system works.
- Failure and uncertainty are product features, not hidden embarrassment.

## V1 non-goals

- unrestricted public general-purpose agent;
- real-world financial advice or production bank modeling;
- public access to the Director's local runner;
- training a foundation model from scratch;
- full enterprise organization administration;
- an unreviewed community plugin marketplace;
- supporting all clouds and runtimes;
- persistent GPU capacity solely for visual smoothness.

## Product metrics

### Engagement

- completion of guided tours and demos;
- documentation and repository navigation;
- contribution funnel from issue view to accepted PR;
- teaching-material usage;
- repeat authenticated use.

### Quality

- public workflow task success;
- route/tool accuracy;
- citation support;
- trace completeness;
- deterministic calculation consistency;
- accessibility audit score;
- setup success from clean checkout.

### Safety and operations

- unauthorized actions: target zero;
- cross-tenant leakage: target zero;
- abuse-block efficacy;
- cost per completed public workflow;
- p50/p95 time to first useful output;
- cold-start fallback success;
- incident count and recovery time.

Metrics are not silently collected. Analytics and research donation use separate consent and data paths.
