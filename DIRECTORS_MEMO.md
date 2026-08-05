---
document_id: DRL-DIR-001
title: "Director's Decision and Escalation Ledger"
version: 1.9.0
status: APPROVED OPERATING PROCEDURE
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Director's Decision and Escalation Ledger

This is the mandatory living decision ledger for DeWitt Research Workshop.
It is not promotional copy. Every human or coding agent must read it before
making a material change and update it when work exposes an inconsistency,
blocker, risk, missing assumption, cost commitment, or decision requiring
the Director's approval.

## Director's standing context

- The public identity is **DeWitt Research Workshop** (RES-014, superseding RES-003).
  `DRL` is retired as a public mark and survives only as the internal identifier
  prefix in document, requirement, and code IDs.
- The workshop is an independent initiative: one founder tinkering, researching, and
  building applied AI in public. It must never imply nonexistent staff,
  accreditation, institutional history, scale, or employer affiliation.
- The canonical public domain is `https://www.dewitt-labs.com`.
- Wix is the public and editorial front door.
- The public website is **Christopher Noxon DeWitt's personal academic
  portfolio**, not the website of a research laboratory, institute, or workshop.
  It centers his current Master of Applied Data Science study at the University
  of North Carolina at Chapel Hill, the complex systems he engineers and studies,
  and his goal of moving toward graduate work in computer science. Projects and
  reports are evidence inside that story, not the identity of the site.
- Atticus and the computational projects remain independently deployable,
  open-source applications under workshop subdomains.
- Atticus is the deepest initial implementation and the operator of the
  workshop.
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
5. When the Director decides, record the resolution, date, and affected ADR or issue.
6. Preserve closed entries; do not erase institutional memory.

## Active decision queue

| ID | Area | Question | Options and consequence | Agent recommendation | Status |
|---|---|---|---|---|---|
| DIR-001 | Repository | What GitHub owner and repository slug will host DRL? | Personal account is simplest; an organization provides cleaner long-term governance. Observed push redirect to `chris-dewitt/DeWitt-Research-Lab-Foundation` (legacy lowercase remote still resolves). | Confirm personal slug casing/org as canonical or schedule org transfer; preserve transferability. | Director confirmation required (remote exists; identity not finalized) |
| DIR-002 | GCP | What projects, billing account, and primary US region will be used? | Separate dev/stage/prod/research projects reduce blast radius but require more setup. | Begin with one budget-capped development project, then create isolated production and research projects before public beta. | Director input required before deployment |
| DIR-003 | Security | What public address receives vulnerability reports? | A dedicated alias protects personal workflow and supports policy publication. | Create `security@dewitt-labs.com` before public launch. | Director input required |
| DIR-004 | Models | Which upstream models become Atticus Core and Edge? | License, tool reliability, local performance, quantization, and cost differ materially. | Run the documented bake-off; do not select by brand preference. Scaffold register + fixture report landed (DRL-012); no winner declared. | Evidence gate — scaffold only |
| DIR-005 | Public access | What anonymous and authenticated quotas apply? | Higher limits improve exploration but increase abuse and cost. | Use fixture/replay mode by default; open bounded inference only after load and abuse testing. | Evidence gate |
| DIR-006 | Legal | When should DRL form a legal entity or register marks? | Formation adds cost and administration but may help contracts and liability separation. | Continue truthful independent-initiative language; obtain professional advice before contracts or material revenue. | Deferred Director/legal decision |
| DIR-007 | Legal/brand | Does the RES-014 rename extend to the claimed trademarks? | `NOTICE`, `TRADEMARK_POLICY.md`, and `LICENSE-STRATEGY.md` still claim "DeWitt Research Laboratory" and `DRL` as marks. Renaming a claimed mark is not a copy edit: it abandons accrued use of the old name and restarts it under the new one. Retaining both is also valid — the old name can stay as a prior mark while the public identity moves. | Do not rewrite the legal documents on brand grounds alone. Either retain "DeWitt Research Laboratory" as a prior/legacy mark and add "DeWitt Research Workshop" alongside it, or take advice before consolidating. Ties to DIR-006. | Director decision required — legal documents deliberately left unrenamed |

## Approved resolutions

| ID | Resolution | Approved by | Date | Consequence |
|---|---|---|---|---|
| RES-001 | Use the recovered Wix/domain build-bible archive as the repository foundation and upgrade it. | The Director | 2026-07-27 | Preserve specifications and add runnable implementation. |
| RES-002 | Use `dewitt-labs.com` as the canonical domain. | The Director | 2026-07-27 | Wix, DNS, documentation, and subdomains use this spelling. |
| RES-003 | Keep the formal name singular: DeWitt Research Laboratory. | The Director | 2026-07-27 | Brand, metadata, and legal disclaimers use the singular name. |
| RES-004 | Describe DRL as an independent initiative run by one person tinkering and researching AI. | The Director | 2026-07-27 | No fictional team, institution, or corporate status. |
| RES-005 | Make this file a living agent decision ledger. | The Director | 2026-07-27 | Root instructions, PRs, handoffs, and releases must check it. |
| RES-006 | Deliver both controlled documentation and runnable code. | The Director | 2026-07-27 | A documentation-only skeleton is no longer sufficient. |
| RES-007 | Retain Wix as the institutional front door and independently deploy applications. | The Director | 2026-07-27 | Public editorial and computational trust boundaries remain separate. |
| RES-008 | Deeply implement Atticus and provide working specialist starters. | The Director | 2026-07-27 | Initial engineering prioritizes the control plane and integrated workflow. |
| RES-009 | Use Google Cloud as primary deployment and Azure as an option. | The Director | 2026-07-27 | GCP is reference architecture; Azure portability must be documented. |
| RES-010 | Include GitHub milestones, issues, CI, agent sequencing, and a 90-day plan. | The Director | 2026-07-27 | Repository is execution-ready after upload. |
| RES-011 | Correct the canonical domain spelling to `dewitt-labs.com`; the public Wix site is live at `https://www.dewitt-labs.com`. | The Director | 2026-08-02 | All documentation, DNS, and subdomains use the corrected spelling; earlier `dwit-labs.com` references were typos. |
| RES-012 | Record the founder's full name as Christopher Noxon DeWitt; operational documents refer to "the Director." | The Director | 2026-08-02 | Founder-identity lines use the full name; governance and process text uses the Director. |
| RES-013 | Change the mission line to "Intelligence for Good. Intelligence for All." | The Director | 2026-08-03 | Replaces "AI for Good. AI for all. Intelligence of the people and for the people."; the second sentence is retired entirely. `BRAND_SYSTEM.md` remains the canonical owner; all documents and code quoting the line were updated and a test now enforces agreement. |
| RES-014 | Rename the public identity to **DeWitt Research Workshop** and drop "Laboratory" from public framing. | The Director | 2026-08-03 | **Supersedes RES-003.** Positioning is one person's workshop, not a research institute — this enforces RES-004 rather than changing it. Register is understated academic. `DRL` is retired as a public mark but retained as the internal identifier prefix (`DRL-WEB-002`) and code namespace. The canonical domain `dewitt-labs.com` is unchanged (RES-002/RES-011 stand); the name/domain mismatch is accepted and must not be explained in copy. Palette, typography, and terminal grammar are unchanged; institutional chrome is now a prohibited motif. Legal and trademark documents (`NOTICE`, `TRADEMARK_POLICY.md`, `LICENSE-STRATEGY.md`) were deliberately **not** renamed — see DIR-007. |
| RES-015 | Position the public website as an evidence-first academic workshop and public research record. | The Director | 2026-08-04 | Retains the RES-013 mission and RES-014 name. The research thesis is "Engineering complex systems for open, inspectable intelligence." The homepage leads to a signed recorded run and `TR-2026-001`, makes degraded evidence and the Stage-B no-winner result visible, and treats contributor routes as secondary. Atticus is a documented research artifact; `atticus.dewitt-labs.com` remains planned until a service is actually deployed. Quantitative-finance experience and Charlotte provide supporting context without employer identification or institutional overstatement. |
| RES-016 | Make `www.dewitt-labs.com` Christopher Noxon DeWitt's personal academic portfolio. | The Director | 2026-08-04 | **Supersedes the public-website positioning in RES-014 and RES-015.** The site title is the Director's name with the descriptor "Academic Portfolio," not DeWitt Research Workshop/Laboratory. It states that he is a student in the Master of Applied Data Science program at the University of North Carolina at Chapel Hill, engineers complex systems at work, studies them part time, and hopes to move toward graduate work in computer science. Research reports, replays, software, and Atticus are portfolio evidence. The RES-013 line may remain a repository/project mission but is not the website headline. No employer is named. |

## Current blockers

- DIR-001 remains open for Director confirmation even though a GitHub remote
  currently resolves to `chris-dewitt/dewitt-research-lab-foundation`. Agents
  must not treat that remote as a final org/governance decision until confirmed.
- No Google Cloud project or billing identity is configured.
- No production secrets or credentials belong in this archive.
- Core and Edge upstream models remain an evidence-based selection gate.
- The public Wix site is live at `https://www.dewitt-labs.com`; ongoing content and DNS changes remain actions in the Director's accounts.
- GitHub milestones/issues from the Mission 00 register are ready to file but
  not yet created on the remote (gh write is operator-owned).

## Current implementation truth

The repository contains a runnable local research vertical slice using
deterministic fixture specialists and a rule-based Atticus planning path. M3
specialists (Atlas public adapter, bounded FedLens corpus with passage
citations, BalanceLab scenario catalog) are composed into one prototype
evidence-to-scenario workflow with a five-way `linked_workflow` artifact
(DRL-018). This proves component contracts, policy behavior, approval binding,
evidence lineage, integrated orchestration, and evaluation plumbing. It is not
yet a public production service, a trained Atticus model release, or a deployed
Wix site. Signed success/degraded replay fixtures exist as prototype packages
(DRL-019) using a demo HMAC key — not production signing identity.

## Release check

A release is blocked when:

- this memo contains a blocker affecting the release;
- an active decision was silently assumed;
- implementation maturity is overstated;
- tests or validators were not run;
- secrets or private/employer data are present;
- required security, rights, cost, or approval evidence is missing.
