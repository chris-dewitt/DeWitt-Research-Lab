---
document_id: DRL-PRG-007
title: "Foundation Decision Register"
version: 4.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-27
---


# Foundation Decision Register

## Approved decisions

| ID | Decision | Status | Consequence |
|---|---|---|---|
| D-001 | Formal name is DeWitt Research Laboratory | Approved | institutional brand and namespace |
| D-002 | DRL is an independent research initiative led by DeWitt | Approved | institute-first, founder-visible presentation |
| D-003 | Atticus is the laboratory's central intelligence and orchestration layer | Approved | specialist systems expose formal tools/contracts |
| D-004 | Monorepo | Approved | one dependency graph and coordinated release |
| D-005 | First-class languages: Python, TypeScript, SQL, Bash, Terraform | Approved | tooling and hiring signal |
| D-006 | Python `uv`, TypeScript `pnpm`, Docker Compose, Terraform | Approved | default developer workflow |
| D-007 | Google-first cloud; Colab for exploration, Vertex for repeatable training | Approved | infrastructure specs and cost controls |
| D-008 | Plan Atticus Core and Edge from the beginning | Approved | two deployment profiles, shared benchmark |
| D-009 | Three data layers: public, private DRL, local personalization | Approved | storage and release segregation |
| D-010 | Public model weights released when upstream terms permit | Approved | release pipeline includes weights/quantizations |
| D-011 | Limited anonymous access plus expanded authenticated public Atticus | Approved | quotas, isolation, retention controls |
| D-012 | Public users may explicitly donate traces | Approved in principle | consent, quarantine, review required |
| D-013 | Governance is benevolent-dictator-led by DeWitt | Approved | delegated maintainers but final director authority |
| D-014 | Sponsors may participate but cannot control roadmap | Approved | sponsorship disclosure and independence |
| D-015 | Mixed licensing strategy with Apache 2.0 software default | Approved | separate model/data/docs/trademark terms |
| D-016 | Major architecture decisions require recorded approval | Approved | ADR enforcement |
| D-017 | Agents work on feature branches and open pull requests | Approved | no direct-to-main work |
| D-018 | V1 launches as one coordinated public program | Approved | internal RCs, public simultaneous release |
| D-019 | Visual direction is cream on black, research terminal/workstation/tmux | Approved | design system |
| D-020 | Primary audience includes collaborators, tinkerers, students, academics, learners, teachers | Approved | educational and contribution features |
| D-021 | `www.dwit-labs.com` is the canonical institutional website and Wix is its V1 publishing platform | Approved | domain, Wix, DNS, editorial, and application integration contract |
| D-022 | Core interactive DRL applications use first-class DRL subdomains and remain independently deployable/open-source | Approved | Wix is a front door, not the sole runtime |
| D-023 | DRL remains an honest one-person independent initiative until its legal or contributor status actually changes | Approved | no fictional staff, corporate status, accreditation, or scale |
| D-024 | The repository ships controlled documentation and a runnable local vertical slice | Approved | tests and demo code accompany specifications |
| D-025 | Atticus receives the deepest initial implementation; every specialist receives a working starter | Approved | engineering sequence prioritizes orchestration and integrated evidence |
| D-026 | Google Cloud is the reference production architecture and Azure is an optional portable deployment profile | Approved | local/open contracts must not depend exclusively on either cloud |
| D-027 | `DIRECTORS_MEMO.md` is the mandatory living escalation and decision ledger | Approved | agents update it rather than silently assuming material decisions |
| D-028 | GitHub issues, milestones, CI, agent sequencing, and a 90-day plan ship with the foundation | Approved | repository can move directly from upload to execution |

## Open decision gates

| Gate | Decision deadline | Evidence required |
|---|---|---|
| G-001 | Core upstream model | before Core SFT | bake-off, license, runtime, cost |
| G-002 | Edge upstream model/teacher | before Edge training | edge bake-off and distillation study |
| G-003 | DCO versus CLA | before substantial external contribution | legal/strategy review and contributor feedback |
| G-004 | Public trace retention duration | before public beta | privacy, research value, cost, user testing |
| G-005 | Exact authenticated quota and pricing | before public beta | load/cost experiment |
| G-006 | Cloud Run GPU serving profile | before production | cold-start, throughput, cost benchmark |
| G-007 | Plugin registry launch | after API stability review | compatibility and security evidence |
| G-008 | Formal trademark registration | before major marketing spend | name/domain/legal search |

Open gates are not invitations for agents to choose silently.

## Open technology decisions awaiting Director approval

| ID | Decision | Status | Record |
|---|---|---|---|
| D-OPEN-001 | Evaluate OpenTofu as authoritative IaC CLI while retaining Terraform-language compatibility | In review | `docs/adr/ADR-0006-opentofu-first-iac.md` |
| D-OPEN-002 | Evaluate Valkey as default cache and ephemeral coordination service | In review | `docs/adr/ADR-0007-valkey-cache-coordination.md` |
