---
document_id: DRL-PRG-006
title: "Program Risk Register"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Program Risk Register

Scores use likelihood and impact from 1–5. Exposure is their product. Owners review high-exposure risks at every release-candidate checkpoint.

| ID | Risk | L | I | Exposure | Early indicators | Primary mitigation | Contingency |
|---|---|---:|---:|---:|---|---|---|
| R-01 | Scope exceeds solo-lab capacity | 5 | 5 | 25 | many shells, few vertical slices | dependency plan, strict V1 outcomes | reduce breadth inside features, not integrated claim |
| R-02 | Open model cannot meet quality | 4 | 5 | 20 | low tool/policy scores after SFT | bake-off, routing, distillation, scaffold improvements | launch candidate with limited skills; no false parity claim |
| R-03 | Benchmark leakage or synthetic feedback | 3 | 5 | 15 | suspicious score jumps, duplicate templates | held-out private set, scenario dedupe, provenance | invalidate run and rebuild affected split |
| R-04 | Prompt injection causes unsafe tool behavior | 4 | 5 | 20 | retrieved instructions influence plan | instruction/data separation, policy engine, adversarial suites | disable affected tool/connector immediately |
| R-05 | Public demo abuse or runaway cost | 4 | 4 | 16 | quota spikes, GPU idle burn | anonymous limits, cached replay, scale-to-zero, budgets | switch to replay-only mode |
| R-06 | Cloud GPU cold starts harm experience | 4 | 3 | 12 | high p95 first-token latency | visible wake state, smaller Edge route, cached demos | minimum instance only during events |
| R-07 | Documentation drifts from code | 5 | 4 | 20 | implementation PRs omit specs | docs-as-code checks, traceability, PR gates | freeze release until reconciliation |
| R-08 | License blocks model/data release | 3 | 5 | 15 | unclear upstream terms | pre-download license register and review | release recipe/adapters only or change base |
| R-09 | Local runner compromises private data | 3 | 5 | 15 | overly broad scopes or logs | outbound-only, OS vault, local approval, sandbox | revoke device and disable remote tasks |
| R-10 | Cross-tenant leakage | 2 | 5 | 10 | missing tenant filters or cache keys | tenant-aware repositories, security tests | incident response and forced session revocation |
| R-11 | Financial demo is mistaken for advice | 3 | 4 | 12 | user prompts with real portfolio | synthetic data, disclaimers, restricted use | refuse unsupported advisory requests |
| R-12 | Agent-generated code appears complete but is not verified | 5 | 4 | 20 | vague PR evidence | command/result evidence, reviewer agents | revert or quarantine branch |
| R-13 | Sponsor pressure affects research | 2 | 4 | 8 | requested conclusions or roadmap control | sponsorship policy and disclosure | reject or terminate relationship |
| R-14 | Solo founder becomes operational bottleneck | 4 | 4 | 16 | unreviewed ADR/PR queue | maintainer ladder, bounded decisions, automation | pause new features and reduce WIP |
| R-15 | Website aesthetic harms accessibility | 3 | 3 | 9 | keyboard/contrast failures | semantic components, reduced motion, testing | disable decorative effects |

## Risk acceptance

Exposure 15 or above requires a written treatment plan and director approval before V1. Critical security/privacy risks cannot be accepted solely to meet a launch date.
