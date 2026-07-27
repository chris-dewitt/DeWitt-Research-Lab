---
document_id: DRL-OPS-006
title: "Open Source Release Operations and Evidence Pipeline"
version: 3.2.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Open Source Release Operations and Evidence Pipeline

## Release pipeline

Every flagship release is assembled from immutable source and machine-readable metadata. The pipeline:

1. validates licenses, notices, and source provenance;
2. builds source and binary/model artifacts from pinned inputs;
3. runs unit, integration, contract, security, evaluation, and forkability tests;
4. generates cards, SBOMs, checksums, and release manifests;
5. signs or attests artifacts where supported;
6. publishes staged artifacts to test repositories;
7. executes clean-room installation and reproduction;
8. obtains director and independent QA approval;
9. publishes GitHub/Hugging Face/OCI/site artifacts atomically where practical;
10. verifies public links, downloads, and installation instructions;
11. opens the post-release monitoring and correction window.

## Release manifest as source of truth

Website status, badges, install commands, and artifact links are rendered from the release manifest. Manual marketing copy cannot override release state. A withdrawn artifact remains in lineage with reason and replacement path unless legal or security obligations require temporary removal.

## Repositories and mirrors

GitHub is the canonical software collaboration surface. Hugging Face is the primary model/dataset card and artifact community surface. OCI registries publish containers. Cloud Storage or another object store can provide verified mirrors. Mirrors preserve exact digests and do not become independent untracked releases.

## Supply-chain controls

The release train uses dependency locks, least-privilege CI identities, protected environments, secret scanning, SBOM generation, provenance/attestation appropriate to maturity, signed tags or releases where operationally sustainable, and reproducible commands. OpenSSF Scorecard and SLSA guidance inform controls without claiming certification that has not been achieved.

## Emergency response

A critical security or rights incident can suspend downloads or deprecate a release. The incident owner records scope, affected digests, mitigation, communication, and restoration criteria. Security embargoes temporarily supersede ordinary openness; the public receives an explanation when safe.
