---
document_id: DRL-OSS-021
title: "Open Source Identity Upgrade and Coverage Audit"
version: 3.2.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Open Source Identity Upgrade and Coverage Audit

## Purpose

This document records the third foundation iteration of DeWitt Research Laboratory. The iteration makes open models, open-source software, public evaluation, self-hosting, reproducible research, and reciprocal community participation visible across the laboratory's identity, architecture, release system, website, model program, contributor experience, and acceptance gates.

The change is not a cosmetic addition of badges or license files. It changes what counts as a complete DRL product. A system cannot represent the laboratory merely because its code is public. It must expose a meaningful modification surface, identify upstream work accurately, publish evidence, provide a local or self-hosted path, and invite inspection and contribution.

## Identity coverage matrix

| Surface | Required open-source identity signal | Enforcing artifact |
|---|---|---|
| Institutional story | open by construction; public-interest AI; community reciprocity | `OPEN_RESEARCH_CHARTER.md` |
| Homepage | open models/software/research visible before project detail | `docs/08-web-brand/OPEN_SOURCE_VISUAL_IDENTITY.md` |
| Portfolio projects | lineage, license, local run, reproduce, contribute, limitations | `docs/08-web-brand/OPEN_SOURCE_PORTAL_AND_COMMONS.md` |
| Atticus | public weights where lawful, adapters, recipes, benchmarks, runtimes | `docs/03-model/ATTICUS_OPEN_MODEL_COMMONS_RELEASE_TRAIN.md` |
| Specialist systems | public protocols, SDKs, fixtures, evals, self-host profile | `docs/09-open-source/OPEN_ARTIFACT_STANDARD.md` |
| Research | methods, manifests, notebooks, negative results, replication bundles | `docs/10-research/OPEN_RESEARCH_PUBLICATION_AND_REPLICATION.md` |
| Dependencies | precise license labels, ownership, upstream contribution, exit plans | `docs/09-open-source/OPEN_TECHNOLOGY_CATALOG.md` |
| Community | beginner-to-maintainer paths, credit, mentorship, research participation | `docs/09-open-source/CONTRIBUTOR_CREDIT_AND_AUTHORSHIP.md` |
| Operations | signed/hashed artifacts, SBOMs, cards, release manifests, clean-room test | `docs/11-operations/OPEN_SOURCE_RELEASE_OPERATIONS.md` |
| Sustainability | managed services and teaching fund the commons without withholding essentials | `docs/09-open-source/OPEN_SOURCE_SUSTAINABILITY.md` |
| Governance | exceptions and major tool substitutions require records and approval | `GOVERNANCE.md`, ADRs, exception schema |
| Quality | machine validator rejects missing open identity surfaces | `scripts/validate_open_identity.py` |

## Major improvements over the prior Build Bible

1. Added an explicit institutional open-research charter and terminology policy.
2. Defined a modification-surface standard for software, models, data, research, deployment, and teaching artifacts.
3. Elevated Atticus from a released model to a maintained Open Model Commons with Core, Edge, adapters, quantizations, recipes, evaluation suites, and community submissions.
4. Added a public Open Stack and upstream lineage experience instead of an uncurated logo wall.
5. Added evidence-derived reproducibility, forkability, provenance, and maturity badges.
6. Added machine-readable artifact, exception, and upstream-dependency contracts.
7. Added open-source health metrics that reward maintainability, replication, upstream work, and contributor experience rather than stars alone.
8. Added public credit and authorship rules for code, data, models, evaluations, teaching, and research.
9. Added sustainability boundaries preserving consulting, managed hosting, paid education, and support without turning the public code into a crippled demo.
10. Added a clean-room V1 showcase in which an outsider can install the stack, run Atticus on open weights, invoke specialist systems, evaluate the trace, and inspect every material artifact.
11. Added a formal OpenTofu/Terraform decision proposal and a Valkey adoption proposal rather than allowing hidden license drift in infrastructure dependencies.
12. Added dedicated validation and test coverage for the open-source identity itself.

## Remaining director decisions

This iteration deliberately does not silently approve two material substitutions:

- **Infrastructure as code:** OpenTofu is recommended for evaluation as the open-source-first CLI while retaining Terraform-language compatibility where practical. The existing Terraform decision remains operative until ADR-0006 is approved.
- **Cache and ephemeral coordination:** Valkey is recommended over a floating Redis image because it provides a clear BSD open-source path and a managed Google Cloud option. The existing generic Redis reference remains until ADR-0007 is approved.

Agents must treat both as approval gates, not as implementation freedom.

## Definition of success

Open-source technology is a strong contributor to DRL's identity when a visitor can answer, without hunting through legal files:

- Which models power Atticus?
- What rights attach to them?
- What open software makes the systems work?
- What did DRL modify?
- How can I run it locally?
- How can I reproduce the claim?
- How can I contribute?
- How does DRL contribute upstream?
- What remains closed, and why?
- How does the laboratory sustain the work without compromising the public commons?

The website, repositories, release manifests, and live demonstrations must provide those answers with evidence.
