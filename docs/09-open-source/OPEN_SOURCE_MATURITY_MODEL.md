---
document_id: DRL-OSS-012
title: "Open-Source Project and Artifact Maturity Model"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Open-Source Project and Artifact Maturity Model

## Why maturity labels matter

DRL will publish ambitious systems. Contributors and users need to know whether an interface is a research sketch, a changing alpha, or a supported stable component. Every repository area, package, model, dataset, and plugin carries a maturity state derived from evidence.

## States

### Incubator

- hypothesis and owner identified;
- no compatibility promise;
- may contain incomplete experiments;
- not recommended for consequential use;
- issue and research question are public.

### Experimental

- runnable path exists;
- basic tests and documentation exist;
- interfaces can change without deprecation;
- security and license screening completed for experiments;
- results are explicitly preliminary.

### Alpha

- core use case works;
- automated tests and evaluation exist;
- public feedback invited;
- migration support is best effort;
- known limitations and security boundaries are documented.

### Beta

- intended public interfaces identified;
- compatibility tests and release automation exist;
- threat model, cards, provenance, and local setup are complete;
- external users have reproduced the primary flow;
- deprecation notices are required for material changes.

### Stable

- semantic versioning or equivalent lifecycle policy;
- support window and maintainers named;
- release criteria, security response, and migration procedures enforced;
- reproducible artifacts and supply-chain evidence published;
- no unresolved critical safety, license, privacy, or correctness defects.

### Deprecated

- replacement and migration path published;
- security support window stated;
- no new feature development expected;
- documentation remains accessible.

### Archived

- no support promised;
- last known compatible environment recorded;
- historical artifacts and notices preserved;
- website prevents confusion with active systems.

## Promotion evidence

Promotion is a release decision, not a maintainer opinion. Evidence covers:

- user value and scope;
- interface stability;
- tests and evaluation;
- security and privacy;
- license/provenance;
- documentation and setup;
- operational reliability;
- contributor ownership;
- local/self-hosted path;
- independent feedback or replication.

## Demotion

An artifact may be demoted after a security issue, maintainer loss, broken reproduction, license change, upstream abandonment, or invalid benchmark claim. Demotion is not failure; hiding the condition would be.

## Website representation

Maturity appears on project cards, package pages, model/dataset cards, plugin listings, and release notes. Atticus must explain the label and avoid recommending an experimental component as stable.
