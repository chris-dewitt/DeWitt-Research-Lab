---
document_id: DRL-PRG-001
title: "Specification Map and Authority Index"
version: 2.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-27
---


# Specification Map and Authority Index

## Purpose

This document tells agents where requirements live and prevents the “same rule in five files” problem. The Laboratory Bible establishes policy and intent; controlled specifications define implementable requirements; schemas define machine-verifiable contracts; ADRs record major choices; tests and release evidence prove implementation.

## Authority classes

| Class | Purpose | Examples |
|---|---|---|
| Constitution | Institutional and platform-wide non-negotiables | `LABORATORY_BIBLE.md` |
| Policy | Governance, security, privacy, licensing, agent conduct | `AGENTS.md`, `SECURITY.md`, `GOVERNANCE.md` |
| Program | Scope, dependency plan, risk, quality, release | `docs/00-program/*` |
| Product | Users, outcomes, features, non-goals, acceptance | `docs/01-product/*` |
| Architecture | Components, protocols, data, deployment, runtime | `docs/02-architecture/*` |
| Research/model/data/eval | Experimental and release methods | `docs/03-model/*`, `04-data/*`, `05-evaluation/*` |
| Project | Deeper system-specific implementation specifications | service/app `docs/` folders |
| Machine contract | Schemas, configs, API definitions | `schemas/`, `configs/` |
| Decision | Approved tradeoff or changed direction | `docs/adr/*`, decision register |
| Evidence | Tests, reports, security review, benchmark results | `tests/`, `research/`, release evidence |

## Canonical ownership

| Concern | Canonical source |
|---|---|
| Mission and platform identity | Laboratory Bible |
| V1 scope | `docs/01-product/PORTFOLIO_V1_PRD.md` |
| Cross-service protocol | `docs/02-architecture/DRL_PROTOCOL.md` and `schemas/` |
| Risk tiers and permissions | `docs/06-security/PERMISSION_AND_APPROVAL_MODEL.md` and `configs/risk-tiers.yml` |
| Model selection | `docs/03-model/BASE_MODEL_BAKEOFF.md` |
| Training data | `docs/04-data/ATTICUSBENCH_SPEC.md` and dataset manifests |
| Evaluation release gates | `docs/05-evaluation/RELEASE_EVALUATION_GATES.md` |
| GCP deployment | `docs/07-platform-gcp/PLATFORM_ARCHITECTURE.md` and Terraform |
| Website design | `docs/08-web-brand/WEBSITE_PRODUCT_AND_DESIGN_SPEC.md` |
| Open-source operations | `docs/09-open-source/OPEN_SOURCE_PROGRAM.md` |
| Agent sequence | `agents/SEQUENTIAL_EXECUTION_PLAN.md` |
| V1 acceptance | `docs/12-acceptance/V1_RELEASE_CRITERIA.md` |
| Current-state baseline | `docs/00-program/CURRENT_STATE_BASELINE.md` |
| Critical path gates | `docs/00-program/CRITICAL_PATH_AND_GATES.md` |
| First sprint plan | `docs/00-program/FIRST_SPRINT_PLAN.md` |
| ADR / Director queue | `docs/00-program/ADR_APPROVAL_QUEUE.md` |
| Weekly release dashboard | `docs/00-program/RELEASE_DASHBOARD.md` |
| Issue register | `requirements/issue-register.yaml` and `.github/ISSUE_BODIES/` |

## Change rule

Do not duplicate a canonical rule into another file as if it were independently editable. Reference the canonical file and add project-specific implications. If a schema and prose disagree, the discrepancy is a defect: neither silently overrides the other until corrected and reviewed.
