---
document_id: DRL-PRG-004
title: "V1 Work Breakdown Structure"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# V1 Work Breakdown Structure

Each work package has an owner, prerequisites, outputs, verification, and handoff. Issue IDs should use the package code.

| Code | Work package | Primary owner | Prerequisites | Exit evidence |
|---|---|---|---|---|
| PRG-01 | Document control and traceability | Program Director | none | validation report, requirement index |
| ARC-01 | Canonical schemas and compatibility | Architecture/Protocol | PRG-01 | schema tests, generated types |
| SEC-01 | Risk tiers, permissions, approvals | Security | ARC-01 | negative tests, threat model |
| OBS-01 | Trace and observability contract | Architecture/Observability | ARC-01 | trace examples, OTel mapping |
| EVA-01 | EvalForge case format and CLI | EvalForge | ARC-01, SEC-01 | reproducible report |
| ATT-01 | Atticus session/control-plane spine | Atticus Runtime | ARC-01, SEC-01, OBS-01 | end-to-end mock trace |
| WEB-01 | DRL design system and shell | Brand/Web | PRG-01 | accessible component catalog |
| WEB-02 | Atticus console and replay | Brand/Web + Atticus | ATT-01, WEB-01 | guided workflow demo |
| FED-01 | Fed corpus and document diff | FedLens | ARC-01, EVA-01 | public bounded corpus demo |
| BAL-01 | Synthetic institution and deterministic engine | BalanceLab | ARC-01, EVA-01 | calculation report and tests |
| ATL-01 | Temporal source ingestion and retrieval | Atlas | ARC-01, EVA-01 | cited research workflow |
| MOD-01 | Candidate bake-off | Model/Data | EVA-01, ATT-01 | selection report |
| DAT-01 | AtticusBench development set | Model/Data + EvalForge | ARC-01, SEC-01 | reviewed dataset manifest |
| MOD-02 | Atticus Core post-training | Model/Data | MOD-01, DAT-01 | model candidate report |
| MOD-03 | Atticus Edge distillation/post-training | Model/Data | MOD-02 or approved teacher | edge report |
| LOC-01 | Local runner pairing and policy | Atticus Runtime + Security | ATT-01, SEC-01 | penetration/abuse test evidence |
| GCP-01 | Dev/stage/prod infrastructure | Infrastructure | architecture ADRs | Terraform plan/apply evidence |
| INT-01 | Integrated specialist workflow | Integration | FED-01, BAL-01, ATL-01, ATT-01 | live trace and EvalForge report |
| REL-01 | Release candidate hardening | Release | all critical packages | evidence matrix |
| REL-02 | Public V1 launch | DeWitt | REL-01 signoff | signed release, public artifacts |

No issue may claim a package complete without attaching its exit evidence.
