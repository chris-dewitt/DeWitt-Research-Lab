---
document_id: DRL-ROOT-ROADMAP
title: "V1 Coordinated Roadmap"
version: 4.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# V1 Coordinated Roadmap

**Canonical public destination:** `https://www.dwit-labs.com` (registered domain; Wix institutional site).

## Release philosophy

DRL V1 launches publicly as one coherent platform. Internal milestones and release candidates reduce risk; they are not marketed as completed V1. Dates are estimates only after resource and dependency evidence exists. Quality, safety, license, and truthfulness gates are not silently traded for schedule.

## Milestone sequence

| Milestone | Exit evidence |
|---|---|
| M0 Foundation freeze | Bible/spec map/ADRs/requirements/agent missions validated |
| M1 Contracts and policy | protocol schemas/examples, identity, permissions, threat model, EvalForge skeleton |
| M2 Platform and web shell | reproducible dev/staging, CI/CD, design system, content engine, mock console |
| M3 Atticus runtime alpha | bounded orchestration with open-weight/mock model, policy, traces, specialist mocks |
| M4 Model/data release candidates | Core/Edge bakeoff, AtticusBench, training artifacts, evaluation/safety/license reports |
| M5 Local runner and specialists | private runner plus Atlas/FedLens/BalanceLab vertical slices and project demos |
| M6 Integrated release candidate | canonical workflow, signed replay, failure drills, staging endurance, frozen versions |
| M7 Independent V1 verification | clean-room, security/privacy/license/accessibility/operations evidence and go/no-go |
| M8 Public V1 | coordinated website, repos, weights, benchmark, reports, demos, release notes |
| M9 Stabilization | incident/feedback triage, corrections, contributor onboarding, first maintenance release |

## Critical-path principles

Protocol/security/evaluation precede broad implementation. Model/data work begins after task and evaluation contracts stabilize. Specialist services implement against mock Atticus clients before integration. Web work uses versioned mocks/replays before live backends. Independent release QA does not own implementation and cannot self-certify upstream defects.

## V1 exclusions unless an approved scope change occurs

- unrestricted autonomous computer control;
- public external-write tools;
- production financial advice or proprietary bank modeling;
- generalized commercial multi-tenant enterprise platform promises;
- always-on expensive GPU fleet without measured demand;
- training a foundation model from random initialization;
- mobile-native applications beyond responsive web and optional local companion research;
- a broad plugin marketplace without security/review maturity.

## Post-V1 research directions

Multilingual Atticus, additional specialist laboratories, stronger local multimodality, privacy-preserving personalization, distributed evaluation, third-party plugin registry, formal policy verification, community benchmark challenges, and managed hosting may follow through evidence-backed roadmap decisions.

## Open research alignment

This document is interpreted with the root `OPEN_RESEARCH_CHARTER.md` and the controlled standards in `docs/09-open-source/`.

## Open Model and Commons Program

- publish Atticus Core and Edge candidate bakeoff and precise license classification;
- release model/data/evaluation cards and replication bundles;
- open the DRL Open Source portal and Open Stack ledger;
- pass clean-room self-hosting and no-paid-API verification;
- establish upstream contribution and community research sprints;
- publish evidence-derived openness, reproducibility, forkability, and supply-chain badges.

## Open commons launch thread

The V1 program includes one coordinated open-commons thread: Atticus Core and Edge release artifacts, AtticusBench, public protocols, Open Stack catalog, self-host profile, signature reproduction workflow, contributor network, upstream ledger, health baseline, and annual accountability template. These are release gates, not post-launch aspirations.


## Domain and Wix launch track

- Connect and verify `www.dwit-labs.com`; establish apex redirect and HTTPS.
- Implement the institute-first Wix shell, mission, systems overview, research, open-source, teaching, About, Contact, and truthful status/launch pages.
- Establish application subdomains and shared navigation/design/consent contracts.
- Publish Atticus and specialist applications as independent open-source experiences, not iframe-only demos.
- Add validated repository-to-Wix publishing, bounded custom elements, and community/editorial features only after the core launch is stable.
