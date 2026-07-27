---
document_id: DRL-PRD-002
title: "User Personas and End-to-End Journeys"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# User Personas and End-to-End Journeys

## Persona: The collaborator

**Goal:** determine whether DRL is worth contributing to and find a tractable issue.  
**Needs:** architecture clarity, setup instructions, roadmap, governance, issue quality, maintainer responsiveness.  
**Journey:** homepage → open-source portal → system architecture → contributor tour with Atticus → good-first issue → local mock setup → PR.

Success means the collaborator can identify the purpose of the work, run tests without paid APIs, understand ownership, and submit a change without asking DeWitt to explain the entire repository.

## Persona: The tinkerer

**Goal:** install a reusable component or run a demo.  
**Needs:** simple commands, examples, transparent dependencies, small packages, API stability.  
**Journey:** package catalog → EvalForge or policy-engine page → install command → example notebook/CLI → API reference.

## Persona: The student or learner

**Goal:** understand agents, RAG, evaluation, post-training, or quantitative AI by seeing it work.  
**Needs:** plain-language explanations, diagrams, guided tours, glossary, reproducible notebooks, visible failure cases.  
**Journey:** teaching portal → “How Atticus uses tools” tour → trace replay → short lesson → notebook exercise.

## Persona: The academic or applied researcher

**Goal:** assess methodology, reproduce results, or extend a benchmark.  
**Needs:** dataset/version details, statistical analysis, baseline definitions, ablations, code and environment locks, limitations.  
**Journey:** research archive → AtticusBench paper/report → dataset card → replication package → issue/discussion.

## Persona: The teacher

**Goal:** use DRL material in a class.  
**Needs:** stable lesson pages, learning objectives, estimated time, prerequisites, datasets, licenses, answer guidance, accessible alternatives.  
**Journey:** teaching portal → module → instructor notes → student exercise → citation/license guidance.

## Persona: The hiring manager

**Goal:** quickly judge DeWitt's ability to design and operate AI systems.  
**Needs:** concise value proposition, three strong workflows, architecture, measurable evidence, code quality, résumé.  
**Journey:** homepage → two-minute systems tour → Atticus trace → EvalForge report → founder profile/résumé → GitHub.

## Persona: DeWitt, private operator

**Goal:** use Atticus as a trusted local copilot and operate DRL.  
**Needs:** voice, repository workflows, private files, model selection, approvals, local logs, cloud/local control.  
**Journey:** local runner starts → voice request → local intent/permission → repository/file action → approval → result and audit.

## Cross-cutting journey requirements

Every journey must specify:

- entry and exit;
- anonymous/authenticated/local identity;
- required services;
- cold-start/offline behavior;
- data collected and retained;
- errors and recovery;
- accessibility alternatives;
- evaluation events;
- cost guardrails.
