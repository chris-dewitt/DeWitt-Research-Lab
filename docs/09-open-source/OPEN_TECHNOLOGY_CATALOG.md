---
document_id: DRL-OSS-016
title: "Open Technology Catalog and Adoption Scorecard"
version: 3.2.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Open Technology Catalog and Adoption Scorecard

## Purpose

DRL chooses technology through engineering evidence and institutional fit. Open-source status is a weighted factor because it improves inspectability, portability, contribution, teaching, and long-term sovereignty. It does not override security, reliability, accessibility, or legal obligations.

The machine-readable catalog is `configs/open-stack.yaml`. The public website renders a reviewed subset with human-readable context.

## Adoption scorecard

Each candidate receives a documented score from 0–5 for:

| Dimension | Meaning |
|---|---|
| Rights clarity | license is clear, compatible, and reviewed |
| Modification surface | preferred source and build path are available |
| Community health | maintainers, releases, issue process, governance |
| Security posture | advisory process, response history, secure defaults |
| Portability | local/cloud support, exportability, open formats |
| Interoperability | standards, APIs, ecosystem adapters |
| Reproducibility | pinned releases, deterministic setup, testability |
| Contributor opportunity | realistic upstream issues and learning value |
| Operational fit | performance, cost, reliability, observability |
| Exit cost | ability to migrate without rewriting the laboratory |

No candidate is adopted on an aggregate number alone. Security blockers, incompatible licenses, abandoned maintenance, or unacceptable data practices can disqualify a candidate.

## Preferred open stack direction

| Layer | Preferred direction | Notes |
|---|---|---|
| Language/runtime | Python, TypeScript, SQL, Bash | mature open ecosystems; versions pinned by toolchain |
| Python environment | `uv` with standards-compatible project metadata | lockfile and wheel/sdist release evidence |
| JS workspace | `pnpm` | deterministic monorepo installation |
| Web | Next.js/React or approved open equivalent | framework choice does not make hosting portable by itself |
| APIs | FastAPI/Pydantic | schema-first Python services |
| Database | PostgreSQL + pgvector | open relational and vector foundation |
| Cache/coordination | Valkey proposal | BSD open-source path; see ADR-0007 |
| Model ecosystem | Transformers, Datasets, TRL, PEFT | public training and release workflows |
| Cloud inference | vLLM; SGLang evaluated | open-weight serving; exact model parser validation |
| Local inference | llama.cpp/GGUF; compatible runners | local sovereignty and low-resource use |
| Evaluation | EvalForge with export adapters | DRL-owned core, open protocols, optional MLflow integration |
| Observability | OpenTelemetry | vendor-neutral traces, metrics, logs |
| Containers | OCI images and Compose-compatible local profiles | portable artifacts, not cloud-only scripts |
| IaC | OpenTofu proposal with Terraform-language compatibility | see ADR-0006 |
| Supply chain | SPDX, REUSE, SLSA-aligned provenance, OpenSSF Scorecard | evidence appropriate to project maturity |
| Model/data publication | Hugging Face + GitHub + OCI/object storage mirrors | immutable digests and cards |

## Upstream stewardship fields

Every critical catalog record identifies:

- canonical project and repository;
- license expression and review date;
- DRL role and owner;
- exact version or allowed range;
- security advisory source;
- health and criticality;
- DRL patches and contribution links;
- alternatives and exit strategy;
- public website attribution text;
- next review date.

## Managed-service boundary

DRL may use managed Google Cloud services around open technologies, including managed PostgreSQL or managed Valkey, when the application remains portable at the protocol and data-export layer. The public catalog must distinguish the open project from the managed service. "Powered by PostgreSQL" must not imply that Cloud SQL itself is open-source software.

## Review cadence

Critical dependencies are reviewed before each release candidate and at least quarterly. Model candidates are revalidated at bakeoff time because model cards, licenses, runtimes, and revisions can change. Floating container tags are prohibited for release evidence.
