---
document_id: DRL-OSS-009
title: "Open Stack Selection, Upstream Contribution, and Lock-In Policy"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Open Stack Selection, Upstream Contribution, and Lock-In Policy

## Principle

DRL is built on an open technology stack and should be a visible participant in the ecosystems it relies upon. The laboratory prefers mature open-source components that preserve portability, inspection, self-hosting, and community knowledge. Managed services are allowed where they improve operations, but they must not become undocumented prisons around the core research system.

## Selection hierarchy

For a foundational dependency, agents evaluate candidates in this order:

1. Technical fitness and security for the required behavior.
2. License compatibility and freedom to use, inspect, modify, distribute, and operate.
3. Reproducibility and ability to pin an exact version.
4. Community health, maintenance, governance, and security response.
5. Portability across local, cloud, and contributor environments.
6. Standards compatibility and data-export quality.
7. Performance, total operating cost, and developer experience.
8. Availability of maintained managed services, not vendor exclusivity.

Open-source status does not excuse poor security or abandonment. A closed or source-available dependency can be used when it is materially superior or required, but the choice needs an ADR, an exit plan, and truthful labeling.

## Foundation stack identity

The planned DRL V1 stack should prominently acknowledge these open-source foundations, subject to version and license revalidation:

| Layer | Preferred open technology | DRL role |
|---|---|---|
| Model ecosystem | Hugging Face Transformers, Datasets, TRL, PEFT | model loading, data, post-training, release |
| Cloud inference | vLLM, with SGLang evaluated where useful | open-weight model serving and tool calls |
| Local inference | llama.cpp/GGUF and compatible local runners | offline and low-resource Atticus |
| APIs | FastAPI, Pydantic, OpenAPI, JSON Schema | typed public and internal contracts |
| Data | PostgreSQL and pgvector; Parquet/DuckDB for research | relational, vector, and analytical storage |
| Web | Next.js/React/TypeScript and DRL-authored terminal UI | public laboratory and console |
| Observability | OpenTelemetry with exportable traces/metrics/logs | vendor-neutral execution evidence |
| Evaluation | EvalForge plus open adapters to MLflow or other tools | reproducible agent/model evaluation |
| Containers | OCI/Docker-compatible images | portable execution artifacts |
| IaC | OpenTofu-first evaluation with Terraform-language compatibility | open infrastructure-as-code path |
| Supply chain | SPDX SBOM, SLSA provenance, OpenSSF Scorecard, REUSE | trusted and inspectable releases |

The final lock for each dependency remains versioned and subject to security and license review.

## OpenTofu and Terraform decision gate

DRL initially planned Terraform. Because Terraform's current license is not an OSI-approved open-source license, the implementation mission must evaluate OpenTofu as the preferred CLI while retaining compatible configuration where practical. This is a director-approved ADR decision point, not a silent substitution. The repository path may remain `infra/terraform` for ecosystem familiarity, but documentation and CI must state the actual tool and license.

## Managed service equivalence

For each managed Google Cloud service in the production design, the documentation records:

- portable application boundary;
- export format and data ownership;
- development/self-hosted substitute;
- migration and exit procedure;
- features available only in managed DRL;
- cost and reliability rationale;
- identity, security, and privacy differences.

A local profile need not reproduce planetary scale. It must reproduce the research and functional core.

## Upstream-first engineering

When DRL finds a generally useful defect or missing feature in an upstream dependency, the preferred sequence is:

1. confirm the issue against a supported upstream version;
2. open a minimal reproducible issue when appropriate;
3. prepare an upstream patch or documentation improvement;
4. keep DRL-specific behavior in an extension rather than a permanent fork;
5. maintain a temporary patch only with an owner, upstream link, rebase procedure, and removal condition;
6. record the contribution in the DRL upstream ledger.

DRL should not build a private replacement merely to claim ownership when a healthy open project can be improved.

## Dependency health review

Critical dependencies receive a quarterly or pre-release review covering:

- license and governance changes;
- release cadence and maintainer activity;
- security advisories and response;
- bus factor and archival risk;
- reproducible build and package integrity;
- API compatibility and deprecations;
- availability of alternatives;
- DRL patches or forks awaiting upstream resolution.

The result feeds a dependency risk register and migration backlog.

## Fork policy

Temporary forks are permitted for security patches, unblockers, or research experiments. Every fork must declare:

- upstream repository and commit;
- reason for fork;
- exact patch set;
- license and notice preservation;
- owner;
- sync cadence;
- upstream issue or PR;
- sunset condition.

An untracked fork is a release blocker.

## Upstream contribution goals

By V1 public launch, DRL should target meaningful upstream participation rather than an arbitrary contribution count. Candidate contributions include:

- tool-call parser or template fixes;
- model card and deployment documentation;
- runtime compatibility tests;
- OpenTelemetry semantic-convention feedback;
- pgvector/query examples;
- evaluation adapters;
- accessibility fixes in open UI dependencies;
- reproducible Colab and Vertex recipes;
- security tests or documentation.

Contributions are listed on the public Open Stack page with links and attribution after acceptance or public submission.
