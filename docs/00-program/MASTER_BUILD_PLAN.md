---
document_id: DRL-PRG-003
title: "Master Dependency-Ordered Build Plan"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Master Dependency-Ordered Build Plan

## Strategy

Build the platform through dependency-complete vertical slices. Do not ask each project agent to build an isolated application and attempt integration at the end. Shared contracts, policy, evaluation, observability, and mock specialists come first; real specialist services replace mocks incrementally.

## Phase 0 — Repository control and evidence system

**Outcome:** Agents can work without ambiguity.

Deliver:

- validated document-control tooling;
- requirement IDs and traceability matrix;
- issue/PR templates;
- ADR workflow;
- branch protection plan;
- workspace commands and toolchain locks;
- manifest and reproducible archive;
- sequential handoff ledger.

Exit gate: a fresh agent can identify current scope, approved decisions, owned files, commands, and next task without external conversation.

## Phase 1 — Protocol, policy, and local mock spine

**Outcome:** A minimal Atticus request can pass through typed contracts and a deterministic policy engine using mock models and tools.

Deliver:

- versioned task, tool, evidence, approval, trace, error, and evaluation schemas;
- generated Python/TypeScript types or contract validators;
- policy engine with Tier 0–4 rules;
- approval binding and expiration;
- trace/event collector;
- in-memory/mock service adapters;
- local Docker dependencies;
- contract and negative tests.

Exit gate: mock Atticus receives a task, proposes a tool call, policy allows or denies it, approval is bound when needed, and a complete trace is evaluated.

## Phase 2 — EvalForge minimum viable foundation

**Outcome:** Every later project can be measured.

Deliver:

- dataset and case format;
- evaluator plugin interface;
- deterministic schema/tool/policy evaluators;
- trajectory replay;
- baseline/candidate comparison;
- CLI and HTML/JSON report;
- CI regression gate;
- initial AtticusBench development set.

Exit gate: protocol/policy changes cannot merge if they regress the published safety suite.

## Phase 3 — Atticus control plane and public laboratory guide

**Outcome:** Public Atticus can explain DRL and operate bounded mock specialist workflows.

Deliver:

- session and identity model;
- model gateway with open-weight adapter and deterministic mock;
- planner/router/skill runtime;
- public allowlisted tool registry;
- documentation retrieval with citation objects;
- streaming trace and approval UI API;
- anonymous quota controls;
- laboratory-guide and integrated-demo skills using mocks.

Exit gate: website console can run a complete sandbox workflow and expose trace, policy, sources, and evaluation.

## Phase 4 — Website and public experience

**Outcome:** The laboratory exists as a polished public institution independent of specialist maturity.

Deliver:

- design tokens and accessible component system;
- homepage, systems map, research, open-source, models/data, benchmark, teaching, failure museum, console, about, and docs pages;
- Atticus dock and command palette;
- replay engine for curated traces;
- mobile and reduced-motion designs;
- privacy and telemetry controls;
- content pipeline from repository Markdown.

Exit gate: static and replay experiences remain compelling and accurate even when GPU services are scaled to zero.

## Phase 5 — Specialist vertical slices

Develop in an integration-friendly order:

1. **FedLens:** bounded official corpus and document diff; easiest evidence-rich vertical slice.
2. **BalanceLab:** deterministic engine and synthetic institution; establishes calculator contract.
3. **Atlas:** broader data ingestion and temporal research; largest data-engineering scope.

Each must expose canonical tools, evidence, tests, a public demo, and EvalForge suites.

Exit gate: Atticus can replace each mock with the real service without changing the user-facing skill contract.

## Phase 6 — Model and dataset program

This phase begins earlier for data design but promotes models only after the runtime and evaluation contracts stabilize.

Deliver:

- candidate model bake-off;
- AtticusBench v1 development and held-out sets;
- SFT and preference datasets;
- Core and Edge training runs;
- ablations and error analysis;
- quantized artifacts;
- serving images;
- model/data/safety cards;
- public release repositories.

Exit gate: selected Atticus models beat their bases on DRL tasks without unacceptable general-capability or safety regression and meet runtime budgets.

## Phase 7 — Private local runner

**Outcome:** DeWitt can use Atticus locally without exposing the machine publicly.

Deliver:

- device pairing and revocation;
- outbound-only task channel;
- approved-directory file search;
- repository read/test/patch workflows;
- local voice input/output adapter;
- OS credential storage;
- local approval UI;
- sandbox and audit log;
- fully local model option.

Exit gate: public accounts cannot discover or invoke the runner; security test demonstrates replay protection and scope enforcement.

## Phase 8 — Integrated hardening and release candidates

Deliver:

- real integrated reference workflow;
- load, cold-start, fault-injection, security, and cost tests;
- data and model release review;
- migration and backup drills;
- accessibility and user testing;
- documentation freeze and link validation;
- release candidate deployments;
- public demonstration recordings and replays.

## Phase 9 — Coordinated V1 launch

Launch only after the V1 evidence matrix is complete. Publish:

- website and public services;
- source release and signed tags;
- model and dataset artifacts;
- evaluation and security reports;
- technical paper or system report;
- tutorials and contribution calls;
- roadmap for V1.x and next research questions.

## Critical path

```text
Document control
   -> protocol + policy
      -> EvalForge core
         -> Atticus runtime + public guide
            -> specialist contracts and real services
               -> Atticus training against stable tools
                  -> integrated workflow
                     -> security/reliability release gates
                        -> V1 launch
```

Website work, corpus acquisition, BalanceLab model design, and model-candidate baseline experiments can proceed in parallel only when they do not change shared contracts without approval.
