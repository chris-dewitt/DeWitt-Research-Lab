---
document_id: DRL-ROOT-001
title: "DeWitt Research Workshop Monorepo"
version: 4.3.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---


# DeWitt Research Workshop

**Canonical website:** [www.dewitt-labs.com](https://www.dewitt-labs.com)  
**Intelligence for Good. Intelligence for All.**

> **Engineering complex systems for open, inspectable intelligence.**

This is one person's workshop. Christopher Noxon DeWitt builds and tests
open-weight AI systems in the open. The workshop is **open by construction**:
the models are open-weight, the code is open-source, the evaluation is public,
and everything runs locally — not as an afterthought, but as the reason the rest
of it is arranged the way it is. Governed by the
[Open Research and Open Technology Charter](OPEN_RESEARCH_CHARTER.md).

**Atticus** is the operator: it plans a piece of work and routes it across four
specialist projects — Atlas (macro evidence), FedLens (Fed policy with
passage-level citations), BalanceLab AI (deterministic scenario modelling), and
EvalForge (evaluation and permission testing).

Everything here is **prototype** maturity. That label is accurate, not modest.

## Quickstart

The whole workflow runs on one machine with deterministic fixtures. No cloud
account, no API key, no inference bill.

```bash
make bootstrap   # uv sync + pnpm install
make doctor      # check your toolchain
make demo        # run the integrated workflow end to end
```

`make demo` runs a real evidence-to-scenario pass: Atlas supplies macro
evidence, FedLens reads an FOMC communication and cites it, BalanceLab applies a
rate shock, and EvalForge scores the result. It prints the evidence count, the
score, and — deliberately — its own limitations.

Expect roughly this:

```text
DEWITT RESEARCH WORKSHOP // ATTICUS LOCAL FOUNDATION
STATE: completed
...
EVIDENCE: 5 items
EVALFORGE: 1.0
LIMITATIONS:
- Macro, market, and Fed inputs are synthetic fixtures for local development.
- BalanceLab uses a simplified educational repricing model, not production bank data.
```

Those limitations are the point. The inputs are synthetic fixtures, and the
planner driving Atticus is rule-based — it stands in for Atticus Core until the
model bake-off picks a real one. What the demo proves is that the contracts,
policy boundaries, evidence lineage, and evaluation plumbing compose correctly,
not that the numbers mean anything about the world.

### Other useful targets

```bash
make verify      # all validators + tests, the same gate CI runs
make test        # pytest only
make serve       # run the Atticus control-plane server locally
```

## Read this first

1. [`LABORATORY_BIBLE.md`](LABORATORY_BIBLE.md) — highest-level product, research, architecture, governance, and delivery authority.
2. [`DIRECTORS_MEMO.md`](DIRECTORS_MEMO.md) — active decisions, blockers, risks, and questions requiring the Director.
3. [`AGENTS.md`](AGENTS.md) — mandatory operating rules for every coding agent.
4. [`docs/00-program/SPECIFICATION_MAP.md`](docs/00-program/SPECIFICATION_MAP.md) — map of every controlled document and its authority.
5. [`docs/00-program/90_DAY_EXECUTION_PLAN.md`](docs/00-program/90_DAY_EXECUTION_PLAN.md) — first execution program after repository upload.
6. [`docs/00-program/MASTER_BUILD_PLAN.md`](docs/00-program/MASTER_BUILD_PLAN.md) — dependency-ordered implementation program.
7. [`docs/12-acceptance/V1_RELEASE_CRITERIA.md`](docs/12-acceptance/V1_RELEASE_CRITERIA.md) — evidence required before the platform may be called V1.0.
8. [`agents/SEQUENTIAL_EXECUTION_PLAN.md`](agents/SEQUENTIAL_EXECUTION_PLAN.md) — exact order and handoff protocol for agentic developers.

## Platform at a glance

```text
                                PUBLIC / PRIVATE USERS
                                          |
                                  DeWitt Lab Web
                                  Atticus Console
                                          |
                               ATTICUS CONTROL PLANE
                     plan | route | policy | approvals | memory
                       /             |              |             \
                  ATLAS          FEDLENS      BALANCELAB AI      TOOLS
             macro research    Fed policy       deterministic   local/MCP
                       \             |              /
                              EVALFORGE
                offline evals | online monitoring | CI gates
```

### Atticus

Atticus is the workshop's documented research artifact, planned open-weight model
family, agent runtime, and permissioned orchestration layer. The program studies
two model sizes from the beginning:

- **Atticus Core:** approximately 8–10B class, optimized for multi-step routing, tool use, research synthesis, coding assistance, and laboratory operation.
- **Atticus Edge:** approximately 2–4B class, optimized for local intent routing, voice responsiveness, constrained tool use, offline guidance, and escalation to Core.

The final upstream models are selected through a documented bake-off; no brand or model is hard-coded before benchmark, license, hardware, and reproducibility review.

### Specialist systems

- **Atlas:** time-aware macroeconomic and market research.
- **FedLens:** Federal Reserve documents, policy language, and event-study research.
- **BalanceLab AI:** synthetic balance-sheet scenarios and deterministic quantitative analysis.
- **EvalForge:** benchmark, regression, security, RAG, tool-use, and trajectory evaluation.

## Monorepo structure

```text
apps/                  open-source interactive web, Atticus console, local runner
services/              Atticus, Atlas, FedLens, BalanceLab, EvalForge
packages/              protocol, policy, provenance, SDKs, UI, observability
models/                Atticus Core and Edge release programs
datasets/              AtticusBench and public trace assets
research/               papers, notebooks, experiments, replication packages
infra/                  Terraform, Cloud Run, Vertex AI, Firebase, Wix/domain integration, observability
configs/                risk tiers, routing, retention, telemetry, permissions
schemas/                canonical JSON Schemas and API contracts
docs/                   laboratory-wide controlled specifications
agents/                 sequential agent missions and handoff records
```

## Technology baseline

- **Python:** services, training, evaluation, data engineering, deterministic models.
- **TypeScript:** Next.js applications, console, SDKs, interactive visualizations.
- **SQL:** PostgreSQL schemas, provenance, evaluation, and analytical queries.
- **Bash:** local automation, CI helpers, release and environment scripts.
- **Terraform:** Google Cloud infrastructure as code.
- **Python environment:** `uv` workspaces and locked dependencies.
- **JavaScript environment:** `pnpm` workspaces.
- **Local integration:** Docker Compose.
- **Public workshop:** Wix at `https://www.dewitt-labs.com`, using the registered `dewitt-labs.com` domain.
- **Interactive applications and cloud:** Firebase/App Hosting or other approved Google-hosted frontends, Cloud Run, Cloud Run GPU, Vertex AI custom jobs, Cloud SQL PostgreSQL, Cloud Storage, Pub/Sub or Cloud Tasks, Secret Manager, Artifact Registry, Cloud Logging and Monitoring.
- **Canonical integration plan:** [`docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md`](docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md).

## Non-negotiable engineering properties

1. Models request actions; deterministic policy code authorizes them.
2. Authoritative financial and statistical calculations run in deterministic tools, not free-form model text.
3. Every material answer can expose sources, calculation lineage, model identity, tool calls, and uncertainty.
4. Consequential actions require explicit approval under a published risk-tier model.
5. Public demos are isolated from the Director's private runner and private data.
6. The system is usable without paid commercial model APIs in its core path.
7. Every release includes evaluation evidence, limitations, security notes, and reproducibility materials.
8. Major decisions require an approved ADR.
9. Agents never merge their own work, claim unrun tests, or silently weaken requirements.
10. The workshop does not pretend to be larger, older, accredited, governmental, or staffed in a way that is false.

## Development entry points

The repository includes specifications, interface contracts, and a tested local
prototype. It deliberately uses fixture evidence and synthetic financial data;
it does not pretend to be a production service or trained model release.

```bash
make bootstrap       # install Python and JavaScript workspaces
make demo            # run the integrated Atticus research workflow
make doctor          # verify local toolchain
make docs-check      # validate controlled documents and links
make program-check   # validate issue/work-package registers and dependency graph
make schema-check    # validate JSON Schemas and examples
make test            # run available tests across workspaces
make dev             # start local dependency stack as implementation matures
```

## Release philosophy

V1 is one coordinated public launch, but development is completed through internal release candidates. DRL may not publicly call the platform V1.0 until the integrated demonstration works end to end using open weights:

> Atticus receives a research question, routes evidence collection to Atlas and FedLens, constructs a synthetic scenario, invokes BalanceLab's deterministic engine, submits the full trace to EvalForge, and returns a cited report with visible calculation and evaluation evidence.

## Licensing and monetization

The recommended default is Apache License 2.0 for original software, with a mixed strategy for documentation, datasets, model artifacts, and third-party material. Open-source licensing does not prevent DRL from charging for managed hosting, consulting, training, private deployments, custom adapters, support, certification, or premium data services. The DRL name, logos, and marks should be governed separately by a trademark-use policy.

See [`LICENSE-STRATEGY.md`](LICENSE-STRATEGY.md). This repository does not provide legal advice; formal releases require license review.

## Current repository status

**Status:** Runnable foundation. Atticus and every specialist have a deterministic
local vertical slice with executable tests. The canonical public Wix site is live
at [www.dewitt-labs.com](https://www.dewitt-labs.com). Public inference, trained
Core/Edge weights, private-device pairing, and production cloud services
remain planned work. Every feature must report its actual maturity honestly:
`specified`, `prototype`, `alpha`, `beta`, `release candidate`, or `stable`.

## Open-source identity, not an appendix

The workshop's open identity is implemented through the [Open Research Charter](OPEN_RESEARCH_CHARTER.md), [Open Source Identity System](docs/09-open-source/OPEN_SOURCE_IDENTITY_SYSTEM.md), [Atticus Open Model Commons](docs/03-model/ATTICUS_OPEN_MODEL_COMMONS_RELEASE_TRAIN.md), and [Open Technology Catalog](docs/09-open-source/OPEN_TECHNOLOGY_CATALOG.md). Public releases must expose the modification surface, self-host path, evidence, upstream lineage, and contributor routes. Run `make open-check` to validate these promises.
