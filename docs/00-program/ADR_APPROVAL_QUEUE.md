---
document_id: DRL-PRG-094
title: "ADR and Director Approval Queue"
version: 1.3.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---

# ADR and Director Approval Queue

Agents may prepare proposals and evidence. They may not treat silence as
approval. Source of living decisions: `DIRECTORS_MEMO.md`. ADR process:
`docs/11-operations/ADR_PROCESS.md`.

## Priority queue

| Priority | ID | Question | Status | Blocking | Recommended next evidence |
|---:|---|---|---|---|---|
| — | DIR-009 | Rewrite Git history or accept institutional author-address exposure | RESOLVED — RES-022 | Public repository visibility | Closed: explicit risk acceptance recorded; no rewrite authorized |
| P1 | DIR-002 | GCP projects, billing, primary US region | Director input | Any cloud apply | One budget-capped dev project first |
| P1 | ADR-0006 | OpenTofu-first IaC CLI | IN REVIEW | Mission 05 toolchain lock | Disposable init/plan/apply/destroy spike |
| P1 | ADR-0007 | Valkey as default cache/coordination | IN REVIEW | Compose + platform defaults | Compatibility tests for sessions/rate limits |
| P2 | ADR-0010 / DIR-010 | Official public feeds versus Yahoo | IN REVIEW | Live Atlas/FedLens ingest | Accept official-only opt-in store; fixtures stay default |
| P2 | DIR-004 / G-001 | Atticus Core upstream model | Evidence gate | Core SFT | Bake-off per `docs/03-model/BASE_MODEL_BAKEOFF.md` |
| P2 | G-002 | Edge upstream / teacher | Evidence gate | Edge training | Edge bake-off + distillation study |
| P2 | DIR-005 / G-005 | Anonymous/auth quotas and pricing | Evidence gate | Public beta | Load/abuse/cost experiment |
| P3 | DIR-006 | Legal entity / marks | Deferred | Contracts/revenue | Professional advice before material revenue |
| P3 | G-003 | DCO vs CLA | Open | External contribution scale | Legal/strategy review |
| P3 | G-004 | Public trace retention duration | Open | Public beta retention | Privacy/research/cost study |
| P3 | G-006 | Cloud Run GPU serving profile | Open | Production GPU | Cold-start/throughput/cost benchmark |
| P3 | G-007 | Plugin registry launch | Open | Post-API-stability | Compatibility + security review |
| P3 | G-008 | Formal trademark registration | Open | Major marketing spend | Name/domain/legal search |

## Already approved (do not re-litigate without ADR)

ADR-0001 monorepo · ADR-0002 Google Cloud primary · ADR-0003 Atticus model family
program · ADR-0004 permission engine · ADR-0005 mixed licensing · ADR-0008 Wix
canonical public site · RES-001–RES-010 in `DIRECTORS_MEMO.md`.

ADR-0009 and RES-018 through RES-021 were approved on 2026-08-05. DIR-001,
DIR-003, and DIR-008 were resolved by RES-018, RES-019, and RES-020
respectively. DIR-009 was resolved by RES-022 on 2026-08-19. Preserve their full
history in `DIRECTORS_MEMO.md`; they are no longer approval-queue items.

DIR-009 no longer gates the change from private to public. RES-022 records the
Director's explicit acceptance of the historical institutional author address in
place of a history rewrite.

## Agent rules for this queue

1. File or update an ADR row before implementing a material unresolved choice.
2. Mark affected issues `blocked` when a P0/P1 item gates them.
3. Record the Director’s resolution date and linked ADR/issue; never delete history.
4. Spikes allowed only in isolated paths labeled experimental until approval.
