---
document_id: DRL-OSS-020
title: "V1 Open Source Showcase and Public Demonstration"
version: 3.2.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# V1 Open Source Showcase and Public Demonstration

## Objective

The V1 launch must demonstrate the open-source identity as a working system. A visitor should not need to trust a slogan or inspect hundreds of documents to understand what is open and how it works.

## Signature demonstration

Atticus receives a public research question and performs the following traceable workflow:

1. identifies the relevant DRL skill;
2. uses Atlas and FedLens to retrieve public evidence;
3. asks BalanceLab AI to run a deterministic synthetic scenario;
4. sends the execution trace and claims to EvalForge;
5. produces a cited report with model identity, artifact digests, limitations, and evaluation status;
6. exposes a **Reproduce this run** bundle;
7. offers a local command using the supported open-weight Atticus profile;
8. links to source, schemas, model card, benchmark cases, and contribution issues.

## Website presentation

The demonstration page includes:

- live or replay mode, clearly labeled;
- system and open-stack lineage diagram;
- exact model/runtime identity;
- tool calls and permission decisions;
- source evidence and deterministic calculation artifacts;
- EvalForge results;
- cost/latency/resource profile;
- license and maturity labels;
- download or clone commands;
- "change one thing" experiments for learners;
- known failure example and regression test;
- contributor credits and upstream acknowledgments.

## Clean-room companion test

An independent tester follows only public documentation to:

- clone the monorepo;
- start the local research profile;
- obtain a supported Atticus model artifact;
- run a reduced version of the signature workflow with public fixtures;
- execute the mini evaluation suite;
- modify one skill or specialist adapter;
- export a reproduction report.

A successful hosted demo without a successful clean-room test does not satisfy V1.

## Audience tours

Atticus provides tailored tours for:

- **Learner:** understand the system and modify a small skill.
- **Researcher:** inspect model/data/evaluation lineage and reproduce a claim.
- **Developer:** run locally, read interfaces, and pick up a scoped issue.
- **Teacher:** find lesson plans and reproducible exercises.
- **Hiring manager:** inspect architecture, security boundaries, operational evidence, and decisions.
- **Maintainer:** review upstream dependencies and contribution opportunities.

## Failure museum integration

At least one failed open-model route, one retrieval failure, one permission failure, and one reproducibility failure are presented with cause, detection, fix, and test. Openness includes the record of what did not work.
