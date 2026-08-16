---
document_id: DRL-AGT-904
title: "Agent Mission Index"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-16
---

# Agent Mission Index

## What these files are

Instruction files for AI coding agents. Not job descriptions, and not an
org chart.

Each numbered file is a prompt: the scope an agent is given when it works on
that part of the repository, the constraints it has to hold to, and the evidence
it must produce before the work counts as done. "Program Director", "Document
Control", and "Release QA" name *missions* in that sense — a slice of work with
its own rules — rather than roles held by people.

One person operates all sixteen: Christopher Noxon DeWitt. There is no staff and
no department behind the numbering. It exists because sixteen narrow prompts
produce better work than one broad one, and because constraints written down in
advance can be checked afterwards against what was actually done.

The "director decisions" referenced throughout are his own. They are recorded in
`DECISION_REGISTER.md` and `DIRECTORS_MEMO.md` so that a decision and its
reasoning outlive the conversation that produced it — including the ones that
were later reversed, which are kept rather than deleted.

## Mission order

| Mission | Primary outcome |
|---|---|
| 00 | program graph, issues, evidence ownership |
| 01 | document control, IDs, traceability, validation |
| 02 | architecture and protocol contracts |
| 03 | security, privacy, permission, abuse policy |
| 04 | EvalForge evaluation substrate |
| 05 | Google Cloud platform and delivery pipelines |
| 06 | brand, website, Atticus public experience |
| 07 | Atticus control plane and orchestration |
| 08 | Atticus Core/Edge models and AtticusBench |
| 09 | private local runner, voice, edge runtime |
| 10 | Atlas |
| 11 | FedLens |
| 12 | BalanceLab AI |
| 13 | cross-system integration and reference demo |
| 14 | independent release QA and V1 dossier |
| 15 | research publications and open-source community |

Read `SEQUENTIAL_EXECUTION_PLAN.md` before selecting a mission. Numeric order is the default because agents run sequentially, but dependency gates—not convenience—are authoritative.

## Source of truth hierarchy

1. `LABORATORY_BIBLE.md`
2. approved ADRs and director decisions
3. laboratory-wide controlled specifications
4. component specifications
5. machine-readable schemas/configuration
6. mission files and current worklog
7. implementation and tests
8. issues, PRs, conversation, and tool memory

A lower layer cannot silently contradict a higher layer. When implementation proves a specification wrong, update the specification through controlled review rather than treating stale prose as sacred.
