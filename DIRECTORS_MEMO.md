---
document_id: DRL-DIR-001
title: "Director's Decision and Escalation Ledger"
version: 1.1.0
status: APPROVED OPERATING PROCEDURE
owner: DeWitt
last_updated: 2026-07-29
---

# Director's Decision and Escalation Ledger

This is the mandatory living decision ledger for DeWitt Research Laboratory.
It is not promotional copy. Every human or coding agent must read it before
making a material change and update it when work exposes an inconsistency,
blocker, risk, missing assumption, cost commitment, or decision requiring
DeWitt's approval.

## Director's standing context

- DRL is **DeWitt Research Laboratory**, singular.
- DRL is an independent initiative: one founder tinkering, researching, and
  building applied AI in public. It must never imply nonexistent staff,
  accreditation, institutional history, scale, or employer affiliation.
- The canonical public domain is `https://www.dwit-labs.com`.
- Wix is the institutional and editorial front door.
- Atticus and computational systems remain independently deployable,
  open-source applications under DRL subdomains.
- Atticus is the deepest initial implementation and the operator of the
  laboratory.
- Atlas, FedLens, BalanceLab AI, and EvalForge must have working vertical-slice
  implementations, honest maturity labels, and stable contracts.
- Google Cloud is the primary deployment target.
- Azure is a documented and tested portability option, not a second production
  estate required for V1.
- The repository must contain both controlled specifications and runnable code.
- Major changes move through issues, feature branches, pull requests, tests,
  handoffs, and Director review.

## How agents use this ledger

1. Add a row before implementing a material unresolved decision.
2. State concrete options, consequences, and a recommendation.
3. Mark the affected work blocked when the decision crosses a stop condition
   in `AGENTS.md`.
4. Do not interpret silence as approval.
5. When DeWitt decides, record the resolution, date, and affected ADR or issue.
6. Preserve closed entries; do not erase institutional memory.

## Active decision queue

| ID | Area | Question | Options and consequence | Agent recommendation | Status |
|---|---|---|---|---|---|
| DIR-001 | Repository | What GitHub owner and repository slug will host DRL? | Personal account is simplest; an organization provides cleaner long-term governance. Observed push redirect to `chris-dewitt/DeWitt-Research-Lab-Foundation` (legacy lowercase remote still resolves). | Confirm personal slug casing/org as canonical or schedule org transfer; preserve transferability. | Director confirmation required (remote exists; identity not finalized) |
| DIR-002 | GCP | What projects, billing account, and primary US region will be used? | Separate dev/stage/prod/research projects reduce blast radius but require more setup. | Begin with one budget-capped development project, then create isolated production and research projects before public beta. | Director input required before deployment |
| DIR-003 | Security | What public address receives vulnerability reports? | A dedicated alias protects personal workflow and supports policy publication. | Create `security@dwit-labs.com` before public launch. | Director input required |
| DIR-004 | Models | Which upstream models become Atticus Core and Edge? | License, tool reliability, local performance, quantization, and cost differ materially. | Run the documented bake-off; do not select by brand preference. Scaffold register + fixture report landed (DRL-012); no winner declared. | Evidence gate — scaffold only |
| DIR-005 | Public access | What anonymous and authenticated quotas apply? | Higher limits improve exploration but increase abuse and cost. | Use fixture/replay mode by default; open bounded inference only after load and abuse testing. | Evidence gate |
| DIR-006 | Legal | When should DRL form a legal entity or register marks? | Formation adds cost and administration but may help contracts and liability separation. | Continue truthful independent-initiative language; obtain professional advice before contracts or material revenue. | Deferred Director/legal decision |

## Approved resolutions

| ID | Resolution | Approved by | Date | Consequence |
|---|---|---|---|---|
| RES-001 | Use the recovered Wix/domain build-bible archive as the repository foundation and upgrade it. | DeWitt | 2026-07-27 | Preserve specifications and add runnable implementation. |
| RES-002 | Use `dwit-labs.com` as the canonical domain. | DeWitt | 2026-07-27 | Wix, DNS, documentation, and subdomains use this spelling. |
| RES-003 | Keep the formal name singular: DeWitt Research Laboratory. | DeWitt | 2026-07-27 | Brand, metadata, and legal disclaimers use the singular name. |
| RES-004 | Describe DRL as an independent initiative run by one person tinkering and researching AI. | DeWitt | 2026-07-27 | No fictional team, institution, or corporate status. |
| RES-005 | Make this file a living agent decision ledger. | DeWitt | 2026-07-27 | Root instructions, PRs, handoffs, and releases must check it. |
| RES-006 | Deliver both controlled documentation and runnable code. | DeWitt | 2026-07-27 | A documentation-only skeleton is no longer sufficient. |
| RES-007 | Retain Wix as the institutional front door and independently deploy applications. | DeWitt | 2026-07-27 | Public editorial and computational trust boundaries remain separate. |
| RES-008 | Deeply implement Atticus and provide working specialist starters. | DeWitt | 2026-07-27 | Initial engineering prioritizes the control plane and integrated workflow. |
| RES-009 | Use Google Cloud as primary deployment and Azure as an option. | DeWitt | 2026-07-27 | GCP is reference architecture; Azure portability must be documented. |
| RES-010 | Include GitHub milestones, issues, CI, agent sequencing, and a 90-day plan. | DeWitt | 2026-07-27 | Repository is execution-ready after upload. |

## Current blockers

- DIR-001 remains open for Director confirmation even though a GitHub remote
  currently resolves to `chris-dewitt/dewitt-research-lab-foundation`. Agents
  must not treat that remote as a final org/governance decision until confirmed.
- No Google Cloud project or billing identity is configured.
- No production secrets or credentials belong in this archive.
- Core and Edge upstream models remain an evidence-based selection gate.
- Public Wix content and DNS require action in DeWitt's accounts.
- GitHub milestones/issues from the Mission 00 register are ready to file but
  not yet created on the remote (gh write is operator-owned).

## Current implementation truth

The repository contains a runnable local research vertical slice using
deterministic fixture specialists and a rule-based Atticus planning path. This
proves component contracts, policy behavior, approval binding, evidence
lineage, integrated orchestration, and evaluation plumbing. It is not yet a
public production service, a trained Atticus model release, or a deployed Wix
site.

## Release check

A release is blocked when:

- this memo contains a blocker affecting the release;
- an active decision was silently assumed;
- implementation maturity is overstated;
- tests or validators were not run;
- secrets or private/employer data are present;
- required security, rights, cost, or approval evidence is missing.
