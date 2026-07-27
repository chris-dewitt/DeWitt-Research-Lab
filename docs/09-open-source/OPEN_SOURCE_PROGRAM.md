---
document_id: DRL-OSS-001
title: "Open-Source Program and Repository Strategy"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Open-Source Program and Repository Strategy

## Goal

Make DeWitt Research Laboratory useful to people who never use the official hosted website. The monorepo is a public research instrument containing applications, standalone packages, models, datasets, benchmarks, deployment profiles, teaching material, and reproducible experiments. Open-source work is not a separate outreach lane; it is the method by which DRL builds credibility and distributes capability.

The program operates under the root `OPEN_RESEARCH_CHARTER.md` and the artifact-specific standards in this directory.

## Institutional outcomes

DRL seeks to produce:

- an open-weight Atticus model family specialized for safe tool use and laboratory orchestration;
- a public benchmark and evaluation ecosystem for agent trajectories, permission behavior, and specialist routing;
- reusable open-source libraries for typed agent protocols, policy, provenance, evaluation, and local/cloud operation;
- specialist research systems whose calculations, sources, and limits are inspectable;
- public datasets and reconstruction pipelines where rights allow;
- self-hosted profiles that preserve user agency and research independence;
- teaching and research materials that convert implementation into shared knowledge;
- meaningful upstream contributions to the projects DRL relies upon.

## Open-source layers

### Flagship applications

- Atticus public console and local runner;
- Atlas macro and market research;
- FedLens policy-document research;
- BalanceLab AI scenario system;
- EvalForge evaluation platform;
- DRL laboratory website and research archive.

### Stable libraries and contracts

- DRL protocol schemas;
- policy and approval engine;
- provenance and evidence models;
- Atticus and specialist SDKs;
- evaluation runner and report formats;
- terminal UI/design-system components;
- data connector interfaces;
- skill/plugin manifests;
- local runner transport and capability contracts.

### Models and data

- Atticus Core and Edge;
- AtticusBench public and protected evaluation program;
- public training and preference datasets;
- synthetic-data generation and review recipes;
- quantized and runtime-specific distributions;
- model/data cards, safety reports, and replication bundles.

### Research and teaching

- architecture and methodology reports;
- experiments and negative results;
- Colab/Vertex notebooks;
- guided labs and courses;
- seminars and contributor sprints;
- public failure museum and correction record.

## Extraction rule

Do not create a package merely for branding. Extract a standalone package when at least two real consumers require the boundary, when a stable protocol benefits external adopters, or when the package has clear independent use. Every extraction needs ownership, versioning, test, documentation, and compatibility policy. A package with no maintainer or user is a liability.

## Open-by-default workflow

Every new work package answers before implementation:

1. What public artifact should result?
2. What upstream open projects does it depend on?
3. What rights and notices apply?
4. What is the preferred modification surface?
5. Can the feature run without the official hosted service?
6. What data or security boundary prevents full publication?
7. What generally useful change should be contributed upstream?
8. How will a learner or contributor reproduce the result?

The PR template and release checklist capture these answers.

## Contributor experience

The expected path is:

```text
clone -> make doctor -> make dev -> run fixture workflow -> choose issue -> test -> PR -> evidence -> recognition
```

Requirements include:

- clean checkout and one-command diagnosis;
- Python `uv`, TypeScript `pnpm`, container, and documented Windows paths;
- local mock and small open-model profiles without paid APIs;
- fixture datasets and deterministic replay;
- issue ladder from docs/tests through models/security/research;
- architecture maps and ADRs;
- consistent quality gates;
- maintainer response and support boundaries;
- public roadmap, release notes, and correction history;
- contribution recognition beyond code.

## Official distribution versus ecosystem

DRL maintains an official distribution and compatibility matrix. Community forks and extensions are welcomed but cannot imply official status. “Official,” “verified,” “reviewed,” and “community” have explicit criteria. The trademark policy protects identity; it does not restrict lawful technical forks.

## Release trains

DRL uses coordinated release trains:

- **Platform train:** runtime, schemas, SDKs, specialists, and website;
- **Model train:** Core/Edge weights, recipes, quantizations, and cards;
- **Data/eval train:** AtticusBench, public data, scorers, and reports;
- **Research train:** papers, notebooks, replications, and teaching materials.

V1 launches together, but internal candidates can move at different rates. Compatibility manifests identify known-good combinations.

## Compatibility and lifecycle

Stable packages follow semantic versioning and published support windows. Experimental interfaces are namespaced and labeled. Deprecations include replacement, migration, timeline, and security support. Model, application, dataset, and benchmark versions remain distinct.

## Open-source health dashboard

The public program dashboard should include:

- active releases by maturity;
- local installation verification;
- open issues and review age;
- contributor and maintainer coverage;
- upstream contribution ledger;
- open exceptions;
- security advisories and supported versions;
- independent evaluations and replications;
- documentation/setup failures;
- current research sprints.

The dashboard must never fabricate activity or convert people into vanity metrics.
