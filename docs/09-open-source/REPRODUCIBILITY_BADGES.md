---
document_id: DRL-OSS-010
title: "DRL Openness, Reproducibility, and Forkability Badges"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# DRL Openness, Reproducibility, and Forkability Badges

## Purpose

Badges convert broad claims into inspectable release evidence. They are not decorative awards. Each badge links to a signed or immutable report and expires when the underlying artifact is superseded, withdrawn, or found not to satisfy its criteria.

## Badge families

### Open Software

Requirements:

- OSI-approved license;
- preferred source form;
- build and test instructions;
- lockfiles;
- public issue/security path;
- dependency and notice inventory.

Levels:

- **OS-1 Source:** source and license published.
- **OS-2 Buildable:** clean build and test verified.
- **OS-3 Forkable:** local profile, extension example, migration/export path, and compatibility policy verified.

### Open Model

Because AI openness has multiple dimensions, the badge states terminology rather than collapsing everything into “open source.”

- **OM-W Open Weights:** weights downloadable with explicit terms.
- **OM-D Derivative Reproducible:** post-training code, data manifest, config, and evaluation published.
- **OM-S Open System Candidate:** release has the preferred modification materials required by DRL's interpretation of the current Open Source AI Definition; legal and community review still recorded.

A release using a custom license can qualify for OM-W and possibly OM-D but is not automatically Open Source AI.

### Reproducible Research

- **RR-1 Inspectable:** methods and evidence published.
- **RR-2 Runnable:** evaluation or analysis reruns from public artifacts.
- **RR-3 Retrainable:** public recipe and eligible data reconstruct the adapter/model result within defined tolerance.
- **RR-4 Independently Replicated:** at least one external replication bundle passes verification.

### Local Sovereignty

- **LS-1 Offline Demo:** core demonstration works without external model API.
- **LS-2 Local Operator:** Atticus runs approved read-only/local workflows on supported consumer hardware.
- **LS-3 Portable Lab:** full reference workflow runs on a documented self-hosted profile with substituteable models and storage.

### Supply-Chain Transparency

- **SC-1 Inventory:** SBOM, licenses, and checksums published.
- **SC-2 Provenance:** CI-generated build provenance and signed release attestations published.
- **SC-3 Hardened:** approved SLSA/OpenSSF-oriented controls and independent release review passed.

## Evidence contract

A badge report includes:

- badge and level;
- artifact and version;
- evidence URLs and digests;
- validation commands;
- environment and date;
- validator identity;
- exceptions and limitations;
- expiration or next review;
- pass/fail status by criterion.

The website and READMEs consume badge data from the release manifest. Humans may not manually type a badge into marketing copy.

## Community verification

External users can submit verification bundles. EvalForge validates structure, while maintainers review environment differences and claims. Community-verified badges are visually distinct from DRL-verified badges until independent-maintainer rules are established.

## Removal and correction

A badge is removed or marked disputed when:

- a required artifact disappears;
- a security incident invalidates provenance;
- the published command no longer works in a supported environment;
- license terms were misstated;
- independent evidence reveals material non-reproducibility;
- the artifact is superseded and no longer supported.

Corrections remain visible in release history.
