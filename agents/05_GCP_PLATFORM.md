---
document_id: DRL-AGT-005
title: "Agent Mission 05: Google Cloud Platform and Infrastructure"
version: 4.0.0
status: APPROVED EXECUTION MISSION
owner: DeWitt
last_updated: 2026-07-26
---

# Agent Mission 05: Google Cloud Platform and Infrastructure

## Mission objective

Build the reproducible Google-first platform foundation for development, staging, and production: Terraform, identity, networking, data services, CI/CD, observability, cost controls, backup/recovery, and a documented path from Colab experiments to Vertex AI training and Cloud Run inference.


## Operating contract

This mission is executed on a dedicated feature branch and ends in a reviewable pull request. Before changing files, the agent must read `LABORATORY_BIBLE.md`, root `AGENTS.md`, `docs/00-program/SPECIFICATION_MAP.md`, `docs/00-program/DECISION_REGISTER.md`, the current `WORKLOG.md`, this mission, and every listed prerequisite.

The agent must not silently reinterpret the laboratory. Missing or contradictory decisions become a documented blocker or an ADR proposal. All external factual or technical assumptions that could have changed must be revalidated against authoritative primary documentation and entered in the technical reference register.

## Branch, commit, and pull-request protocol

- Create a branch named `agent/<mission-number>-<short-scope>` from the latest approved integration branch.
- Reserve the mission in `WORKLOG.md` before modifying controlled files.
- Commit after coherent work packages; avoid one giant undifferentiated commit.
- Rebase or merge the latest integration branch before final verification.
- Open a pull request containing requirement IDs, changed contracts, ADRs, test evidence, security/privacy impact, documentation impact, known limitations, and exact handoff state.
- Never merge the pull request yourself unless DeWitt has explicitly delegated that authority for the specific PR.

## Universal constraints

- No credentials, personal/private content, employer material, unlicensed corpora, or generated secrets may be committed.
- Do not weaken security, privacy, evaluation, accessibility, open-weight, provenance, or deterministic-computation requirements to make a demo pass.
- Do not claim completion without verifiable evidence.
- Do not alter another component's public contract without coordination and, when material, an approved ADR.
- Public write actions and unrestricted shell execution remain outside the public Atticus trust boundary.
- LLM output never becomes an authoritative numerical financial result; BalanceLab calculations must be deterministic and auditable.

## Required artifacts in every mission PR

1. Implemented or revised artifacts owned by the mission.
2. Automated tests or executable validation for every material behavior.
3. Updated controlled documentation and requirement traceability.
4. A completed handoff ledger entry using `agents/HANDOFF_TEMPLATE.md`.
5. A list of decisions made, assumptions retained, unresolved blockers, and follow-on issues.
6. Evidence that relevant local and CI commands pass.

## Stop conditions

Stop rather than improvise when a change would expose private data, expand write authority, change a public protocol, add a new upstream model/license, materially change cloud cost, undermine reproducibility, or contradict an approved foundation decision. Draft an ADR or blocker with alternatives and impact.



## Open Research Charter obligations

This mission must preserve DRL's open-by-construction identity. Read `OPEN_RESEARCH_CHARTER.md` and the relevant `docs/09-open-source/` standards. For every material feature, record the public artifact, license, modification surface, self-hosted path, upstream dependencies, reproducibility evidence, and any open exception. Prefer upstream contribution over permanent private forks. Use “open source,” “open weight,” and “source available” precisely.

## Entry prerequisites

- Missions 00–03 merged.
- Core protocol and security boundaries approved.
- Google Cloud billing account and target organization/project arrangement identified by DeWitt; no credentials are committed.
- Cost envelope and environment policy approved.

## Owned paths

- `infra/**`
- `.github/workflows/**` for build/deploy/release infrastructure
- `docs/07-platform-gcp/**`
- `configs/environments/**`
- infrastructure-related sections of `.env.example` and `Makefile`

## Protected or coordinated paths

- Application business logic and model training recipes are coordinated, not owned.
- IAM role changes, public ingress, GPU minimum replicas, data residency, new paid services, or cross-project networking require review.
- Production resources cannot be created by default from a developer workstation.

## Required work packages

### WP-05-01 — Terraform foundation and project topology
Define modules and environment composition for Firebase/App Hosting, Cloud Run services/jobs, Artifact Registry, Cloud SQL PostgreSQL/pgvector, Cloud Storage, Pub/Sub or tasking services, Secret Manager, monitoring, budgets, and service accounts. Pin providers and document state/bootstrap strategy.

### WP-05-02 — Identity and trust boundaries
Implement least-privilege service identities, workload identity federation for GitHub Actions, environment isolation, secret references, and public/private ingress policies. Produce an IAM matrix and automated policy checks.

### WP-05-03 — Deployment pipelines
Build reusable CI/CD workflows for preview, dev, staging, and production; include image provenance, migration gates, smoke tests, canary or revision rollout, rollback, and approval-controlled production promotion.

### WP-05-04 — Observability and SLO plumbing
Provision logs, traces, metrics, dashboards, alerts, correlation IDs, budget alerts, and telemetry redaction. Ensure the platform can distinguish user-visible latency, model latency, tool latency, queue delay, and cold start.

### WP-05-05 — Model training and serving substrate
Document and scaffold Colab-to-Vertex packaging, checkpoint storage, experiment identity, GPU quota requests, Cloud Run GPU deployment, model artifact verification, and scale-to-zero policy.

### WP-05-06 — Resilience and cost operations
Implement backup policies, restore drills, retention, rate limits, hard budget controls, teardown scripts, incident runbooks, and a monthly cost attribution report by component and environment.

Every work package must name the requirements it satisfies, the evidence it produces, and its failure/rollback behavior. Create focused commits at work-package boundaries.

## ADR and director-approval triggers

- Any always-on GPU, new region, or monthly hard-cap change.
- Any public ingress to an internal service.
- Any move away from Google-first architecture.
- Any state, secret, or production deployment mechanism that cannot be independently audited.
- Any data service that changes retention, residency, or encryption assumptions.

## Verification matrix

- `terraform fmt`, `validate`, and static security checks pass for all modules.
- A clean dev environment can be planned from documented inputs without hidden steps.
- IAM matrix has no wildcard administrative grants in application identities.
- Preview/development deploy and rollback are exercised with a disposable environment.
- Restore procedure is tested against non-production data.
- Budget alerts and hard-stop controls are verified.
- Public model endpoint demonstrates authentication/rate limiting and scales to zero where permitted by release SLOs.

## Handoff requirements

Provide the next agent with environment contracts, service URLs as variables rather than secrets, required cloud prerequisites, unresolved quota items, actual cost estimates from plans/tests, deployment commands, rollback commands, and any deviations from the approved topology.

## Definition of mission complete

Terraform and pipelines are reproducible, documented, least-privilege, cost-bounded, and validated in a disposable environment; downstream agents can deploy without inventing infrastructure or receiving broad credentials.

### WP-05-07 — Open infrastructure compatibility decisions

Run the director-gated OpenTofu and Valkey spikes defined in ADR-0006 and ADR-0007. Produce disposable-environment evidence, license/compatibility analysis, cost and migration consequences, and explicit approval requests. Do not silently substitute either tool.


### WP-05-08 — Domain, DNS, TLS, and Wix/cloud routing

Inventory the privately held registrar/DNS arrangement without committing secrets; implement the reviewed mapping for `www.dwit-labs.com`, the apex redirect, and DRL application subdomains. Add certificate, CORS, CSP, cookie-scope, non-indexing, monitoring, rollback, and dangling-DNS checks. Coordinate with Mission 06 so Wix and Google-hosted applications promote as one release while retaining independent failure domains. Evidence must include a redacted zone plan, HTTPS/redirect test report, link/canonical test results, and operator runbook exercise.
