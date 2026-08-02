---
document_id: DRL-WEB-104
title: "DRL Web Information Architecture"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# DRL Web Information Architecture

## Primary navigation

- **Laboratory:** mission, principles, systems map, program, founder.
- **Systems:** Atticus, Atlas, FedLens, BalanceLab AI, EvalForge.
- **Research:** papers, technical reports, notebooks, experiments, datasets, benchmarks, model releases.
- **Open Source:** repositories, packages, starter kits, plugin registry, roadmap, contribution.
- **Learn:** guided tours, tutorials, seminars, glossaries, teaching collections.
- **Console:** Atticus, signed demonstrations, status, and methods.

## Canonical routes

```text
/
/laboratory
/laboratory/principles
/laboratory/founder
/systems
/systems/{slug}
/systems/{slug}/{architecture|security|evaluations|roadmap}
/research
/research/{type}/{slug}
/open-source
/open-source/contribute
/open-source/roadmap
/learn
/console
/console/replays/{id}
/failures
/status
/privacy
/telemetry
```

## Project-page layers

1. Identity, problem, and user.
2. Measured proof points with artifact dates.
3. Launch, replay, watch, read, and contribute actions.
4. Signature workflow and interactive architecture.
5. Engineering decisions and ADRs.
6. Evaluation, security, limitations, and failure cases.
7. Repository, install, docs, methods, research, and roadmap.

## Content states

Every public asset carries maturity (`experimental`, `alpha`, `beta`, `stable`, `archived`, `historical`), publication status (`draft`, `review`, `public`), version, owner, and last-verified date. “Stable” means a declared interface is stable, not that scientific conclusions are final.

## Search and command palette

Search covers titles, abstracts, tags, systems, methods, authors, document IDs, releases, and technologies. It excludes private drafts and user traces. Command actions are typed navigation or bounded demo commands and remain keyboard and screen-reader usable.

## Open-source identity requirements

- Open models, open-source software, public evaluation, local operation, and reproducible research must be visible without opening a footer or README.
- Every project page identifies upstream models/software, artifact licenses, maturity, local/self-hosted path, evaluation evidence, and contribution entry points.
- The public Atticus interface exposes the active model identity, version, routing mode, and whether output is live, replayed, cached, or illustrative.
- A dedicated Open Source portal presents Atticus model releases, datasets, packages, benchmarks, upstream contributions, self-hosting profiles, open exceptions, and independent replications.
- A `REPRODUCE` action is generated from tested release metadata rather than hand-authored marketing commands.
- The website credits upstream projects through a useful dependency graph, not a logo wall or implied endorsement.
