---
document_id: DRL-AGT-904
title: "Agent Mission Index"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Agent Mission Index

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
