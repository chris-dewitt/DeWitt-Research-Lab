---
document_id: DRL-ROOT-001
title: "DeWitt Research Lab Monorepo"
version: 5.0.4
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-24
---

# DeWitt Research Lab

One person's technical workshop for studying how intelligent systems plan,
use tools, preserve evidence, and fail safely.

I am Christopher Noxon DeWitt, a student in the Master of Applied Data Science
program at the University of North Carolina at Chapel Hill. I engineer complex
systems professionally and want to continue toward graduate work in computer
science. This repository contains independent work outside UNC coursework; it
does not represent my employer or the university.

**Academic portfolio:** [www.dewitt-labs.com](https://www.dewitt-labs.com)

**Recorded runs:** [chris-dewitt.github.io/DeWitt-Research-Lab](https://chris-dewitt.github.io/DeWitt-Research-Lab/) (signed fixture replays on GitHub Pages; not a live Atticus service)

**Project mission:** Intelligence for Good. Intelligence for All.

## What this repository is

This is a working research monorepo, not a company, institution, or finished
product. It contains a runnable local prototype, technical reports, research
plans, evaluation fixtures, and the specifications used to keep implementation
claims honest.

The current prototype uses deterministic fixtures and a rule-based planner. It
does **not** include trained Atticus weights, public inference, a production
cloud deployment, or completed empirical papers. Those are planned or
evidence-gated work, and they are labeled that way throughout the repository.

Laboratory IDs always carry a prefix, and the prefixes mean different things:

| Prefix | What it is | Example |
|---|---|---|
| `DRL-NNN` | A work item / GitHub issue | `DRL-004` — prove a clean-clone bootstrap and demo |
| `DRL-XXX-NNN` | A requirement | `DRL-OPS-007` — local model runbook |
| `DIR-NNN` | A Director decision still in the ledger | `DIR-004` — which models become Atticus Core and Edge (open) |
| `RES-NNN` | An approved answer to a DIR | `RES-022` — keep historical UNC author emails |
| `ADR` | An architecture decision record | recorded in `docs/adr/` |

`DRL-004` and `DIR-004` are not the same thing.

## Start with the evidence

| Artifact | What it is | Maturity |
|---|---|---|
| [`TR-2026-001`](docs/10-research/reports/TR-2026-001-integrated-workflow.md) | Technical report for the local evidence-to-scenario workflow | `prototype report` |
| [`TR-2026-002`](docs/10-research/reports/TR-2026-002-evidence-gated-model-selection.md) | Evidence-gated account of the model-selection process and its no-winner state | `working report` |
| [Integrated workflow teaching lab](docs/10-research/teaching/INTEGRATED_WORKFLOW_LAB.md) | Guided reproduction using synthetic inputs | `prototype` |
| [Computational Finance of Intelligence](docs/10-research/COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md) | Research program connecting stochastic belief dynamics, optimal stopping, finance, cognition, and AI | `research plan; no empirical result claimed` |
| [Model bake-off](models/bakeoff/README.md) | Candidate registry, harness, license gates, and measured limitations | `prototype; no winner selected` |
| [Signed replay fixtures](services/evalforge/fixtures/signed_replays/README.md) | Success and degraded recorded runs with fixture-integrity checks | `prototype fixture` |
| [GitHub Pages replay viewer](https://chris-dewitt.github.io/DeWitt-Research-Lab/) | Hosted player for those two recordings | `prototype; live` |

## Run the local prototype

Requirements: Python 3.12 or 3.13 and
[`uv`](https://docs.astral.sh/uv/). The core demonstration does not require a
cloud account, commercial model API, or private dataset.

```bash
uv sync --all-packages --locked
uv run --package atticus-control-plane atticus-demo --public
uv run pytest
```

Equivalent Make targets are available:

```bash
make doctor
make demo
make verify
```

The demonstration runs an actual local orchestration path:

1. Atlas supplies time-aware synthetic macro evidence.
2. FedLens retrieves a fixture FOMC communication with passage citations.
3. BalanceLab applies a deterministic educational rate scenario.
4. EvalForge evaluates the completed trajectory and its permission behavior.

The reported values are fixture evidence for software behavior, not claims
about financial markets or real institutions. The planner is rule-based by
default. To point it at a local Ollama model (Qwen3 1.7B or SmolLM3-3B),
follow [`docs/11-operations/LOCAL_MODEL_RUNBOOK.md`](docs/11-operations/LOCAL_MODEL_RUNBOOK.md).
That does not select Atticus Core or Edge. A local run prints `progress:`
lines on stderr and writes an ids-only record under `runs/atticus/`.
To analyze changing official public series (FRED, Treasury yields, Fed press
RSS — not Yahoo Finance), see
[`docs/11-operations/PUBLIC_FEED_PIPELINE.md`](docs/11-operations/PUBLIC_FEED_PIPELINE.md).

## Current implementation boundary

### Runnable today

- typed protocol models and task-state transitions;
- deterministic policy and approval binding;
- Atticus local orchestration, CLI, and HTTP adapter;
- Atlas, FedLens, BalanceLab, and EvalForge prototype slices;
- local-runner path, symlink, content, and approval controls;
- model-provider, structured-output, and bake-off harnesses;
- signed success/degraded replay generation and validation;
- documentation, program, open-identity, domain, and public-repository validators.

### Specified or planned

- trained Atticus Core and Edge model artifacts;
- the TypeScript lab-web and Atticus console applications;
- public inference and authenticated user accounts;
- production Google Cloud infrastructure and application subdomains;
- empirical Computational Finance of Intelligence results;
- V1 release status.

The [`current-state baseline`](docs/00-program/CURRENT_STATE_BASELINE.md) and
[`Director's Memo`](DIRECTORS_MEMO.md) record the detailed implementation truth
and active blockers.

## System map

```text
                            LOCAL USER
                                |
                   ATTICUS CONTROL PLANE [prototype]
                 plan | route | policy | approvals
                    /          |          |          \
               ATLAS       FEDLENS   BALANCELAB   LOCAL TOOLS
             [prototype]  [prototype] [prototype] [prototype]
                    \          |          /
                         EVALFORGE
                         [prototype]

       LAB WEB / ATTICUS CONSOLE [specified; implementation pending]
       ATTICUS CORE / EDGE WEIGHTS [specified; selection gate open]
```

Atticus coordinates specialist systems; it does not replace their domain logic.
BalanceLab remains authoritative for its deterministic calculations, and policy
code—not a language model—decides whether an action is permitted.

## Repository map

```text
apps/       local runner plus specified-only TypeScript UI shells
services/   Atticus control plane and four prototype specialist services
packages/   typed protocol, AI-core utilities, and SDK scaffolds
models/     bake-off policy, candidate metadata, and future model programs
datasets/   AtticusBench specifications and controlled fixture structure
docs/       architecture, security, research, operations, and reports
schemas/    canonical JSON Schemas and examples
configs/    permissions, routing, retention, telemetry, and release policy
infra/      undeployed GCP/Azure infrastructure starters and runbooks
agents/     prompts and handoffs for sequential coding-agent work
tests/      unit, integration, security-negative, and document controls
```

The files under [`agents/`](agents/README.md) are mission prompts for coding
agents, not staff positions or an organization chart. Christopher operates the
repository and reviews the resulting evidence.

## Research direction

The broader program studies reliable agentic systems, belief diffusion and
decision-making, and the intersection of finance, cognition, mathematics, and
AI. Current research documents distinguish proposals, prior evidence, methods,
results, and unresolved questions. A plan is not presented as a paper, and a
prototype run is not presented as an empirical finding.

- [Research program](docs/10-research/RESEARCH_PROGRAM.md)
- [Computational Finance of Intelligence](docs/10-research/COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md)
- [Primary-source novelty review](docs/10-research/CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md)
- [Publication and replication standard](docs/10-research/OPEN_RESEARCH_PUBLICATION_AND_REPLICATION.md)

## Development and contribution

The repository is designed to be inspectable and reproducible without paid
APIs. Before proposing a substantial change, read
[`CONTRIBUTING.md`](CONTRIBUTING.md), the relevant component specification, and
the nearest `AGENTS.md`. Public APIs, security boundaries, data/model releases,
licensing, and cloud topology require recorded review.

Useful checks:

```bash
make verify                # validators plus Python and Node workspace checks
make lint                  # Ruff
make typecheck             # strict mypy
make security              # Bandit
make public-check          # tracked-source disclosure and metadata audit
make public-release-check  # public check plus reachable Git-author metadata
```

The TypeScript application packages are explicit scaffolds. Their current
commands validate that declared state but do not constitute an implemented UI
test suite.

## Licensing and citation

DRL-authored software defaults to Apache License 2.0. Documentation, research,
datasets, model artifacts, third-party material, and trademarks may carry
different terms; see [`LICENSE-STRATEGY.md`](LICENSE-STRATEGY.md) and release-
specific notices. Citation metadata is provided in [`CITATION.cff`](CITATION.cff).

The project is **open by construction** under the
[`Open Research and Open Technology Charter`](OPEN_RESEARCH_CHARTER.md), but it
uses terms such as *open-source software*, *open-weight model*, and *public
artifact* only when the relevant rights and modification surface actually exist.

## Contact

Research, academic, technical, employment, and responsible-security inquiries:
`director@dewitt-labs.com`.

Please use GitHub issues for reproducible, non-sensitive defects. Do not put
credentials, private data, or exploitable security details in a public issue.
