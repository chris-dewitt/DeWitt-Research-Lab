---
document_id: DRL-PRG-002
title: "V1 Program Charter"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# V1 Program Charter

## Objective

Deliver one coordinated, public, open-source V1 of DeWitt Research Workshop in which Atticus—using open weights—operates a polished public laboratory, coordinates four functioning specialist systems, and supports an optional secure local runner.

## Business and research outcomes

- Establish Christopher Noxon DeWitt publicly as an Applied AI Researcher with a serious, reproducible body of work.
- Provide useful open-source libraries, datasets, benchmark assets, and applications rather than portfolio-only demonstrations.
- Demonstrate research quality through evaluations, citations, deterministic calculations, and failure publication.
- Attract collaborators, tinkerers, students, academics, learners, teachers, hiring managers, sponsors, and consulting/training opportunities.
- Preserve future monetization through official managed services, research/training services, custom integrations, private adapters, support, and brand trust.

## V1 scope

V1 includes:

1. laboratory website and documentation portal;
2. public Atticus with anonymous and authenticated tiers;
3. private local runner with bounded file, repository, voice, and approval flows;
4. Atticus Core and Edge model releases or launch-approved release candidates;
5. AtticusBench and EvalForge;
6. Atlas, FedLens, and BalanceLab vertical slices;
7. one integrated cross-system demonstration;
8. Google Cloud deployment and local Docker profile;
9. security, privacy, governance, licensing, contributor, research, and release systems.

## Constraints

- Open-weight core path; commercial models may assist development or synthetic-data generation but cannot be required for the V1 public Atticus claim.
- No employer-confidential data, code, methods, terminology, or samples.
- Google-first cloud architecture and Colab/Vertex model workflow.
- Monorepo using Python, TypeScript, SQL, Bash, Terraform, `uv`, `pnpm`, and Docker Compose.
- Sequential agentic development with feature branches and pull requests.
- Major decisions recorded and approved.
- Public launch is coordinated; internal release candidates are allowed.

## Program success measures

- Integrated workflow completion rate meets release threshold.
- Zero unauthorized action in the release security suite.
- Published AtticusBench, model/evaluation reports, and replication instructions.
- Website communicates the platform in under two minutes and provides deep technical evidence.
- New contributor can run the mock/local stack from clean checkout using documented commands.
- Cloud deployment remains within configured budget guardrails.
- Every public claim maps to release evidence.

## Program roles

- **Director/Product Owner:** Christopher Noxon DeWitt. Final mission, scope, ADR, release, and brand authority.
- **Program Director Agent:** maintains dependency plan, issue graph, status, and release evidence.
- **Architecture/Protocol Agent:** owns cross-service contracts and architecture coherence.
- **Security/Privacy Agent:** owns threat models, policy, abuse testing, and release security signoff.
- **Model/Data Agent:** owns model selection, training, datasets, and model releases.
- **EvalForge Agent:** owns evaluation platform and release evidence.
- **Project Agents:** own Atticus runtime, Atlas, FedLens, BalanceLab, web/brand, cloud infrastructure.
- **Integration/Release Agent:** validates end-to-end operation and packages public V1.

## Change control

V1 scope changes require an ADR or program decision record including reason, impact, alternatives, dependencies, acceptance changes, and director approval. A slipped feature is not silently reclassified as “post-V1” to preserve a date.
