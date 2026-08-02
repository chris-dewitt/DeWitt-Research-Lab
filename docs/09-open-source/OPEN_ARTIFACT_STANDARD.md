---
document_id: DRL-OSS-007
title: "DRL Open Artifact and Modification-Surface Standard"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# DRL Open Artifact and Modification-Surface Standard

## Purpose

A repository URL is not sufficient evidence that an AI system is meaningfully open. This standard defines the minimum modification surface DRL must publish for each artifact class so another person can understand what was released, alter it, evaluate the alteration, and run it in a supported environment.

## Artifact classes

DRL recognizes six primary artifact classes:

1. **Software:** applications, libraries, CLIs, SDKs, infrastructure modules, schemas, and plugins.
2. **Models:** base references, adapters, merged weights, quantizations, tokenizers, templates, parsers, and serving images.
3. **Datasets:** raw-source manifests, normalized records, labels, synthetic records, benchmark cases, and hidden evaluation sets.
4. **Research:** papers, working papers, notebooks, experiment bundles, statistical analyses, and failure reports.
5. **Deployments:** local profiles, containers, cloud templates, migration scripts, observability configuration, and runbooks.
6. **Teaching:** tutorials, assignments, guided labs, lecture notes, example projects, and instructor materials.

## Universal release envelope

Every public release must provide a machine-readable release manifest containing:

- artifact identifier and semantic version;
- repository and immutable source revision;
- authors and recognized contributors;
- license expression for every artifact class;
- upstream dependencies, models, datasets, and notices;
- build or generation command;
- checksums for distributable artifacts;
- supported environments and resource assumptions;
- evaluation or verification report;
- known limitations and unsupported use;
- security contact and reporting instructions;
- lifecycle state: experimental, alpha, beta, stable, deprecated, or archived;
- evidence of the achieved DRL openness and reproducibility level.

## Software modification surface

A DRL software release is complete only when it includes:

- human-readable source in the preferred form for modification;
- dependency lockfiles and minimum supported versions;
- build, test, lint, type-check, and package commands;
- local mock or fixture profile without paid APIs;
- public interfaces and compatibility policy;
- sample configuration with no secrets;
- migrations and rollback notes when stateful;
- security and threat-boundary documentation;
- architecture decision links;
- SBOM and dependency-license inventory;
- CI-generated package provenance when feasible;
- at least one runnable example and one failure example.

Generated code is not the preferred form when the generator templates or source definitions are missing. Minified bundles do not replace source.

## Model modification surface

A DRL model release must include, to the extent permitted by upstream rights:

- exact upstream model repository, revision, license, and terms snapshot;
- DRL training and evaluation code;
- tokenizer, chat template, tool-call format, and parser configuration;
- data manifest and mixture summary;
- training configuration, seeds, precision, optimizer, scheduler, hardware profile, and checkpoint policy;
- adapters and merged weights when permitted;
- at least one broadly usable quantized distribution for local inference;
- vLLM or equivalent cloud-serving profile and llama.cpp/GGUF or equivalent local profile where supported;
- AtticusBench results and category-level failures;
- model card, safety report, license review, and intended-use boundaries;
- comparison against the unmodified base and at least one alternative candidate;
- reproduction notebook or job specification.

If the upstream model's training data or source is not available, the release must be labeled **open-weight derivative**, not fully Open Source AI.

## Dataset modification surface

A public dataset or benchmark release must include:

- dataset card and exact license;
- source, rights, and provenance register;
- acquisition and transformation code when lawful;
- schema, data dictionary, versioning, and split logic;
- filtering, de-identification, deduplication, and quality-review methods;
- known exclusions, bias, and coverage limitations;
- contamination analysis for evaluation sets;
- record-level or batch-level lineage sufficient to audit origin;
- checksums and immutable release snapshot;
- a small inspectable sample where full redistribution is restricted;
- instructions to reconstruct from source when DRL may publish code but not source content.

## Research modification surface

A research result must distinguish hypothesis, method, evidence, interpretation, and recommendation. A replication bundle includes:

- preregistration or dated analysis plan when appropriate;
- code and environment;
- input artifact references;
- exact model and prompt/template revisions;
- output data used in figures and tables;
- statistical method and uncertainty treatment;
- negative and null results relevant to the conclusion;
- known deviations from plan;
- cost and hardware profile;
- citation and correction path.

## Deployment modification surface

Hosted DRL services may use managed Google Cloud components, but the open distribution must document:

- the portable component boundary;
- self-hosted development profile;
- container images or build recipes;
- database schema and migration path;
- environment configuration;
- local or community-supported substitutes for managed dependencies;
- data export and deletion procedures;
- operational limitations that differ from hosted DRL.

## Open exception register

An artifact may fall below the standard only through a recorded exception with:

- affected artifact and requirement;
- legal, security, privacy, cost, or technical reason;
- rejected alternatives;
- public substitute, interface, or reconstruction path;
- owner and approving authority;
- review date and expiration where possible;
- public disclosure wording.

Exceptions may not be used to describe a closed system as open. The release badge must reflect the actual achieved level.
