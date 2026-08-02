---
document_id: DRL-PRG-092
title: "Critical Path, Entry Gates, and Exit Gates"
version: 1.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-27
---

# Critical Path, Entry Gates, and Exit Gates

Canonical mission order remains `agents/SEQUENTIAL_EXECUTION_PLAN.md`. This
document adds executable entry/exit gates so agents cannot skip protocol,
security, or evaluation prerequisites.

## Critical path (dependency-complete)

```text
00 Program bootstrap
 -> 01 Document control / toolchain
    -> 02 Architecture / protocol
       -> 03 Security / policy
       -> 04 EvalForge skeleton
          -> 07 Atticus runtime
             -> 09 Local runner
             -> 10 Atlas | 11 FedLens | 12 BalanceLab
                -> 13 Integration demo
                   -> 14 Release QA
                      -> 15 Research / community

Parallel-ready after contracts stabilize:
  05 GCP platform (topology/IaC; no prod secrets)
  06 Brand / Wix shell (editorial; truthful maturity labels)
  08 Model / data bake-off (provider interface required first)
```

## Mission gates

| Mission | Entry gate | Exit gate | Next unlocks |
|---:|---|---|---|
| 00 | Foundation validators pass; Director Memo read | Issue/milestone program, ADR queue, sprint plan, handoff | 01 |
| 01 | Mission 00 merged or integration-ready | One-command verify; docs/schema validators CI-gated | 02 |
| 02 | Mission 01 exit | Typed envelopes, state machine, negative contract tests | 03, 04 |
| 03 | Mission 02 exit | Deny-by-default policy + approval binding + abuse fixtures | 07, 05 |
| 04 | Mission 02 exit | Deterministic trajectory/policy suite runnable in CI | 07, 08 |
| 05 | Mission 03 contracts stable; DIR-002 decided before apply | Budget-capped IaC plan; no silent OpenTofu/Valkey swap | 06, 08, 13 |
| 06 | Design tokens/spec; no fake live claims | Wix page map + accessible shell + replay labels | 13 |
| 07 | 02+03+04 exits | Bounded orchestration with mock/open-weight provider seam | 09–12 |
| 08 | Provider interface + EvalForge suite | Bake-off report; no brand-locked selection without evidence | 09, 13 |
| 09 | Mission 07 + security suite | Pairing/approval-bound local inspect/patch proposal | 13 |
| 10–12 | Mission 07 + specialist contracts | One real public/synthetic vertical slice each | 13 |
| 13 | Specialists + Atticus + EvalForge | Signed success + degraded replays; narrative≡calculations | 14 |
| 14 | Mission 13 evidence pack | Independent clean-room / security / claim audit | 15 / launch |
| 15 | Release QA go/no-go | Public research, teaching, contributor routes | V1.x |

## Hard stop conditions

Stop and escalate via `DIRECTORS_MEMO.md` when:

- an active Director decision is assumed without resolution;
- a mission would bypass 02/03/04 before Atticus/specialist expansion;
- license, tenancy, or approval invariants would weaken;
- cloud cost or identity topology is chosen without DIR-002;
- maturity labels would overstate fixture/prototype behavior as production.

## Cycle check

Mission graph is a DAG. No mission may depend on a later mission’s exit for its
own exit. Return loops are defect-fix PRs only (`SEQUENTIAL_EXECUTION_PLAN.md`).
