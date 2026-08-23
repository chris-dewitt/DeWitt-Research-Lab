---
document_id: DRL-DIR-001
title: "Director's Decision and Escalation Ledger"
version: 1.15.0
status: APPROVED OPERATING PROCEDURE
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
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
- The canonical GitHub repository is the Director-owned private repository
  `chris-dewitt/DeWitt-Research-Lab`. It remains private through the end of
  September 2026 while public-ready evidence is prepared. GitHub branch
  protection and rulesets are intentionally not enabled; repository process,
  review, and validation remain mandatory operating policy.
- `director@dewitt-labs.com` is the only public contact address used by the
  portfolio and repository, including responsible security reports.

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
| DIR-001 | Repository | What GitHub owner and repository slug will host DRL? | Personal account is simplest; an organization provides cleaner long-term governance. Observed push redirect to `chris-dewitt/DeWitt-Research-Lab-Foundation` (legacy lowercase remote still resolves). | Confirm personal slug casing/org as canonical or schedule org transfer; preserve transferability. | RESOLVED — RES-018 |
| DIR-002 | GCP | What projects, billing account, and primary US region will be used? | Separate dev/stage/prod/research projects reduce blast radius but require more setup. | Begin with one budget-capped development project, then create isolated production and research projects before public beta. | Director input required before deployment |
| DIR-003 | Security | What public address receives vulnerability reports? | A dedicated alias protects personal workflow and supports policy publication. | Create `security@dewitt-labs.com` before public launch. | RESOLVED — RES-019; use `director@dewitt-labs.com` only |
| DIR-004 | Models | Which upstream models become Atticus Core and Edge? | License, tool reliability, local performance, quantization, and cost differ materially. A local Qwen/SmolLM3 demo that completes omitted catalog specialists is not a bake-off result. | Run the documented bake-off; do not select by brand preference. Scaffold register + fixture report landed (DRL-012); no winner declared. | Evidence gate — scaffold only |
| DIR-005 | Public access | What anonymous and authenticated quotas apply? | Higher limits improve exploration but increase abuse and cost. | Use fixture/replay mode by default; open bounded inference only after load and abuse testing. | Evidence gate |
| DIR-006 | Legal | When should DRL form a legal entity or register marks? | Formation adds cost and administration but may help contracts and liability separation. | Continue truthful independent-initiative language; obtain professional advice before contracts or material revenue. | Deferred Director/legal decision |
| DIR-007 | Legal/brand | Does the RES-014 rename extend to the claimed trademarks? | `NOTICE`, `TRADEMARK_POLICY.md`, and `LICENSE-STRATEGY.md` still claim "DeWitt Research Laboratory" and `DRL` as marks. Renaming a claimed mark is not a copy edit: it abandons accrued use of the old name and restarts it under the new one. Retaining both is also valid — the old name can stay as a prior mark while the public identity moves. | Do not rewrite the legal documents on brand grounds alone. Either retain "DeWitt Research Laboratory" as a prior/legacy mark and add "DeWitt Research Workshop" alongside it, or take advice before consolidating. Ties to DIR-006. | Director decision required — legal documents deliberately left unrenamed |
| DIR-008 | CFI research | How should the CFI program respond to 2026 primary work that substantially overlaps Papers I and III and the repair component of Paper II? | A: preserve the program, make narrowed Paper II the flagship, and authorize new scoping for active information acquisition and identifiable coupled dynamics; B: retain all three as explicit replication/extension papers; C: retain Paper II and replace Papers I and III. Experiments under the original claims risk producing technically sound but non-novel work. | Choose A. Do not change the approved questions yet; authorize a bounded follow-up novelty packet for the two redesigns and independent G1 review of Paper II. | RESOLVED — RES-020; independent G1 review remains required |
| DIR-009 | Repository privacy | Should 16 commits whose author metadata exposes a UNC email address be rewritten before the repository becomes public? | A: rewrite all affected reachable history to the GitHub no-reply address, coordinate every open branch, and force-push; this removes the address but changes commit SHAs. B: accept the historical disclosure and preserve commit identity; future commits already use the no-reply address. | Choose A before changing visibility because RES-019 establishes one public contact, but do not rewrite history without the Director's explicit approval. | RESOLVED — RES-022; Option B chosen against the recommendation |

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
| RES-017 | Establish **Computational Finance of Intelligence** as the Director's three-paper academic research program, with Belief Diffusion as the shared methods bridge. | The Director | 2026-08-05 | The approved tracks are: optimal stopping and the option value of thinking; linguistic framing plus no-arbitrage belief repair; and market-based aggregation of human and machine beliefs. The program is portfolio research, not a separate institution or a claim of completed results. Agents may execute bounded task packets, but the Director retains authority over hypotheses, data eligibility, confirmatory protocols, claims, authorship, and publication. |
| RES-018 | Use `chris-dewitt/DeWitt-Research-Lab` as the permanent Director-owned repository; keep it private through 2026-09-30 and do not enable GitHub branch protection or rulesets. | The Director | 2026-08-05 | **The private-through-2026-09-30 clause is superseded by RES-024.** The rest stands: the former `DeWitt-Research-Lab-Foundation` slug is retired, branch protection and rulesets remain off, and feature branches, review, tests, and handoffs remain policy requirements even though GitHub does not technically enforce them. |
| RES-019 | Use `director@dewitt-labs.com` as the only public contact address. | The Director | 2026-08-05 | Portfolio contact, research inquiries, employment or academic inquiries, and responsible security reports all route to the same address. Agents must not invent or recommend additional public aliases unless the Director reopens the decision. |
| RES-020 | Approve DIR-008 Option A for the CFI program. | The Director | 2026-08-05 | Narrow Paper II into the first flagship; treat Dutch-book repair as a baseline rather than the contribution; authorize bounded re-scoping of Paper I around active information acquisition and Paper III around identifiable coupled belief dynamics or registered replication. No experiment bypasses independent G1 review. |
| RES-021 | ~~Publish sanitized display artifacts from a separate public repository while the authoritative research repository remains private.~~ **Superseded by RES-024.** | The Director | 2026-08-05 | `chris-dewitt/dewitt-research-artifacts` is the approved public deployment mirror (live GitHub slug; GitHub equates earlier Title-Case references). Only generated files admitted by the publication allowlist may be exported. The first artifact is the experimental replay viewer; papers require separate release approval and allowlist changes. ADR-0009 governs the boundary. |
| RES-022 | Accept the historical UNC email address in Git author metadata; do not rewrite history. | The Director | 2026-08-19 | **Resolves DIR-009 as Option B, against the recommendation recorded there.** The commits carrying the UNC address in author metadata keep it, and their SHAs are preserved. The count is ref-dependent and drifts as branches merge and are deleted — DIR-009 recorded 16, and 15 are reachable from the current ref set — so the audit reports a measured count rather than a fixed one. The disclosure is a personal academic address already associated with the Director's public identity under RES-016, and the Director judges it not worth invalidating every published SHA, coordinating open branches, and force-pushing shared history. New commits continue to use the GitHub no-reply address, so the exposure does not grow. RES-019 is unaffected: `director@dewitt-labs.com` remains the only *published* contact, and no document, site page, or artifact may present the UNC address as a contact route. DIR-009 no longer blocks public visibility. |
| RES-023 | Ratify the `research/cfi` package created ahead of the CFI-004 layout gate. | The Director | 2026-08-19 | `COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md` §11 permits an implementation agent to create the `research/cfi/` tree "in a focused issue after CFI-004 is approved." The package was built at the Director's direct instruction before that gate. The Director ratifies the deviation: the package stays where it is, and CFI-004 approval is no longer a precondition for its existence. The gate still governs the *belief-event schema* work it was written for; this ratification is scoped to the directory and package layout only, and does not approve CFI-004, unblock any experimental packet, or relax G2/G3. |
| RES-024 | Make `chris-dewitt/DeWitt-Research-Lab` public now, and retire the separate artifact mirror. | The Director | 2026-08-22 | **Supersedes the private-through-2026-09-30 clause of RES-018 and supersedes RES-021 in full.** The Director elects to publish the authoritative source rather than a sanitized derivative. The mirror existed for one reason — GitHub Pages will not deploy from a private personal repository on the current plan — and a public source removes that reason, so `ADR-0009` is superseded, `DRL-OEX-0001` is closed, and the export policy, publication workflow, preparation script, and their tests are deleted. The Director accepts, deliberately, that this publishes material the allowlist previously withheld: the Directors Memo including the open DIR-006 and DIR-007 deliberations, `LICENSE-STRATEGY.md`, `COMMERCIAL_SUSTAINABILITY.md`, the worklog, 24 agent handoffs, and every `DRAFT` or `IN REVIEW` controlled document — among them `TR-2026-002` and its preliminary novelty scan. Each remains labelled with its real status; publishing unfinished work as unfinished work is the intent, not a lapse. Visibility is changed in the Director's GitHub account; this resolution authorizes it and no agent performs it. |
| RES-025 | Replace the independent-reviewer requirement at the G1 novelty gate with a stratum-coverage rule. | The Director | 2026-08-23 | **Amends RES-020 and the G1 row of the CFI lifecycle.** Blocking the research program on recruiting a volunteer reviewer stopped it for three weeks and was never realistic for a one-person workshop. The requirement is withdrawn. What replaces it is the function the reviewer served, not nothing: before any novelty claim is made public, the question must be searched in **a literature stratum the original review did not cover**, and the coverage of each pass must be stated. The rule exists because the gap is demonstrated rather than theoretical — the 2026-08-05 review searched arXiv and OpenReview almost exclusively, and the first two searches of a published-journal corpus surfaced close neighbours it had never seen, including experimental valuation work in the *Journal of Finance*. A single-stratum search is now treated as an incomplete search, and saying which strata were covered is mandatory in any novelty record. The Director may still seek outside review; it is no longer a precondition for proceeding. |

## Current blockers

- No Google Cloud project or billing identity is configured.
- No production secrets or credentials belong in this archive.
- Core and Edge upstream models remain an evidence-based selection gate.
- The public Wix site is live at `https://www.dewitt-labs.com`; ongoing content and DNS changes remain actions in the Director's accounts.
- GitHub milestones/issues from the Mission 00 register are ready to file but
  not yet created on the remote.
- CFI-002 found contribution-level collisions with current primary work.
  RES-020 resolves the Director disposition. RES-025 withdraws the
  independent-reviewer precondition and replaces it with stratum coverage, so
  what remains before experiments proceed is the bounded re-scoping of Papers I
  and III and a completed multi-stratum revalidation.
- The separate artifact mirror is retired by RES-024 and is no longer a
  blocker. `chris-dewitt/dewitt-research-artifacts` may be deleted or left
  dormant at the Director's discretion; nothing in this repository targets it.
  Once `DeWitt-Research-Lab` is public, GitHub Pages can serve the replay
  viewer directly from it — `make replay-site` still builds those files — but
  no Pages workflow is configured yet.
- Some reachable commits expose a UNC email address in Git author metadata
  (16 when DIR-009 was raised; 15 reachable today — the figure moves with the
  ref set). Accepted by RES-022 as a known, deliberate disclosure; no history
  rewrite is authorized and none is planned. New commits use the GitHub
  no-reply address. This no longer blocks public visibility.

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

The original same-repository GitHub Pages build succeeded at `1feda7f`, but
deployment was rejected because the canonical repository is private on a plan
without private-repository Pages. RES-021 approves a separate allowlisted public
deployment mirror; the public repository now exists, but Pages and the publish
token are still outstanding, so no artifact is live.

## Release check

A release is blocked when:

- this memo contains a blocker affecting the release;
- an active decision was silently assumed;
- implementation maturity is overstated;
- tests or validators were not run;
- secrets or private/employer data are present;
- required security, rights, cost, or approval evidence is missing.
