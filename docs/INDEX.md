---
document_id: DRL-DOC-002
title: "Controlled Documentation Index"
version: 3.5.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-05
---

# Controlled Documentation Index

## Start here

1. Root `README.md` — orientation and commands.
2. `LABORATORY_BIBLE.md` — constitutional product/system vision.
3. Root `OPEN_RESEARCH_CHARTER.md` — open models, open-source systems, artifact and community commitments.
4. `docs/00-program/SPECIFICATION_MAP.md` — document authority and reading order.
5. `docs/00-program/REQUIREMENT_CATALOG.md` — approved V1 requirements.
6. `agents/SEQUENTIAL_EXECUTION_PLAN.md` — implementation order.

## Controlled domains

- `00-program` — charter, scope, requirements, risks, decisions, quality, traceability, backlog.
- `01-product` — users, public/private Atticus, portfolio, reference workflow.
- `02-architecture` — protocols, state, identity, policy, data, events, provenance, errors, SLOs.
- `03-model` — Core/Edge selection, training, distillation, quantization, serving, release.
- `04-data` — governance, AtticusBench, review, contamination, donation, lineage.
- `05-evaluation` — EvalForge, metrics, graders, statistics, CI/release gates.
- `06-security` — threat, permission, sandbox, privacy, MCP, local runner, incidents.
- `07-platform-gcp` — Terraform, IAM, Cloud Run, Vertex, Colab, Cloud SQL, operations.
- `08-web-brand` — brand, website, console, replay, accessibility, analytics.
- `09-open-source` — open research charter implementation, artifact standards, models, stack/upstream policy, reproducibility, forkability, licensing, contributors, governance, and plugins.
- `10-research` — ethics, publications, teaching/research program.
- `11-operations` — agents, ADRs, releases, cost, document control, and the
  local/edge model measurement runbooks (DRL-OPS-007, DRL-OPS-008).
- `12-acceptance` — Definition of Ready/Done and V1 release gates.

## Component authority

Each app, service, model, package, and dataset has a README plus component docs. Component specifications may add detail but cannot contradict laboratory-wide requirements. Machine-readable schemas/configuration are under `schemas/`, `configs/`, `requirements/`, and `sql/`.

## Duplicate legacy paths

Some older seed documents may remain under unnumbered domain paths for history. Numbered controlled domains and component `docs/` are authoritative. Mission 01 should either migrate useful unique content or mark/delete superseded duplicates before implementation begins.

## Open-source identity and commons

- `../OPEN_RESEARCH_CHARTER.md` — constitutional open-research commitments and precise terminology.
- `09-open-source/OPEN_SOURCE_IDENTITY_SYSTEM.md` — institutional narrative and website behaviors.
- `09-open-source/OPEN_ARTIFACT_STANDARD.md` — modification surfaces for software, models, data, research, deployments, and teaching.
- `09-open-source/OPEN_TECHNOLOGY_CATALOG.md` — adoption scorecard and upstream stewardship.
- `03-model/ATTICUS_OPEN_MODEL_COMMONS_RELEASE_TRAIN.md` — Core/Edge public model program.
- `08-web-brand/OPEN_SOURCE_PORTAL_AND_COMMONS.md` — public portal and model commons experience.
- `09-open-source/V1_OPEN_SOURCE_SHOWCASE.md` — signature end-to-end demonstration and clean-room companion test.

## Current academic research program

- `10-research/COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md` — approved
  three-paper plan, Belief Diffusion methods bridge, research gates, and
  sequential agent task graph.
- `10-research/RESEARCH_PROGRAM.md` — publication forms, standards, and
  relationship to the broader Atticus research lines.
- `10-research/CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md` — dated G1 scoping review
  that narrowed the program; still `IN REVIEW` pending independent G1.
- `10-research/CFI_CANDIDATE_DATA_RIGHTS_REGISTER.md` — opening CFI-003 record
  of candidate human datasets. No data acquired; G2 remains closed.
- `10-research/TR-2026-002_NOVELTY_SCAN.md` — preliminary novelty scan for the
  evidence-gate report.
- `10-research/CFI_REVALIDATION_2026-08-23.md` — first revalidation pass against
  the 2026-09-05 boundary, covering the published-journal stratum the original
  review missed. Companion to the 2026-08-05 review, not an edit to it.
- `research/cfi/` — Paper II machine instrument (payoff equivalence, pricing
  oracle, coherence repair). Contains no experiment, dataset, or result.
