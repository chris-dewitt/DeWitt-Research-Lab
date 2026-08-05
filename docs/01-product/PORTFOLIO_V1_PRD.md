---
document_id: DRL-PRD-001
title: "DeWitt Research Workshop V1 Product Requirements"
version: 2.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# DeWitt Research Workshop V1 Product Requirements

## Product vision

DeWitt Research Workshop V1 is an open, evidence-first academic portfolio and
public research record. It shows what Christopher Noxon DeWitt wants to
investigate, why the questions matter, and that he can engineer the complex
systems needed to investigate them.

The public research thesis is:

> **Engineering complex systems for open, inspectable intelligence.**

The workshop publishes runnable software, signed replays, technical reports,
methods, negative results, and reproducibility evidence. Atticus and the four
specialist projects form the current research program; they do not imply a
staffed institute or a production service.

## Primary audiences

1. **Academic evaluators:** research peers, prospective mentors or PhD advisers,
   and grant reviewers assessing research direction, rigor, and potential.
2. **Research-oriented employers and technical leaders** assessing systems
   engineering, quantitative reasoning, and research judgment.
3. **Developers and tinkerers** inspecting or running open components.
4. **Students and teachers** using transparent examples and the integrated
   workflow lab.
5. **Future contributors** seeking a bounded path after they understand the work.

## Product promise

Without chatting, signing in, or waiting for a live model, a visitor can:

- understand the research thesis;
- **Watch a recorded run** in both success and degraded states;
- **Read TR-2026-001** with methods, limitations, citation, and source links;
- see why the Stage-B model bake-off declared no winner;
- inspect project maturity, architecture, code, and reproducibility evidence;
- understand the Director's background and contact him about research,
  mentorship, PhD, grant, or relevant employment opportunities.

## Public website requirements

### Five-page Wix front door

- **Home:** thesis, recorded run, technical report, research questions, negative
  results, project index, and brief founder/contact context.
- **Projects:** Atticus, Atlas, FedLens, BalanceLab AI, and EvalForge with honest
  maturity, interfaces, evidence, and limitations.
- **Writing:** `TR-2026-001`, research notes, the integrated workflow teaching
  lab, failure records, and negative results.
- **Open Source:** runnable code, licenses, upstream lineage, local setup,
  reproducibility evidence, and secondary contributor routes.
- **About:** founder profile, research interests, quantitative-finance
  background, Charlotte location, independent-initiative disclosure, and
  contact.

The page tree stays shallow until real content justifies another route.

### Evidence hierarchy

The homepage's first two actions are **Watch a recorded run** and **Read
TR-2026-001**, in that order. The signed replay viewer exposes success and
degraded runs and identifies demo-HMAC signatures as structural prototype
evidence. The report is a complete reading experience, not a teaser card.

Failures are not hidden. The degraded replay and the Stage-B no-winner result
are homepage-level evidence because they demonstrate evaluation discipline and
bounded claims.

### Atticus boundary

Atticus is currently a research artifact being documented. A public
`atticus.dewitt-labs.com` application address may be reserved, but every link is
labeled **planned** until deployment, security, consent, quota, and fallback
evidence exists. The public site contains no `Launch Atticus` promise without a
real public service.

## Platform capabilities retained for V1

- repository-backed controlled-content publishing;
- signed and versioned replay artifacts;
- traditional navigation that works without chat or client enhancement;
- accessible responsive design and truthful loading/error/replay states;
- public Atticus only after bounded tools, quotas, isolation, consent, and abuse
  controls meet their separate acceptance gates;
- a Windows-first private/local runner that remains outside the public trust
  boundary;
- open-weight Core and Edge research programs, with upstream selection governed
  by the documented bake-off rather than brand preference;
- Atlas, FedLens, BalanceLab AI, and EvalForge vertical slices;
- research, model, data, safety, license, and reproducibility reporting.

## Product principles

- Evidence before claims; real capability before simulated capability.
- Replays are clearly labeled and remain useful when live services are absent.
- Progressive disclosure: useful in 60 seconds, inspectable for hours.
- Public data and synthetic financial models only.
- Open-weight core; provider fallback is disclosed and optional.
- A model does not receive more authority because the interface is conversational.
- Failure, uncertainty, and no-winner decisions are research outputs.
- The site is read-mostly for now; mentorship and serious inquiry are welcome,
  while active collaborator recruitment is not a homepage objective.

## V1 non-goals

- unrestricted public general-purpose agent;
- claiming a hosted Atticus service before one exists;
- real-world financial advice or production bank modeling;
- public access to the Director's local runner;
- training a foundation model from scratch;
- fictional staff, departments, institutional history, or fabricated metrics;
- an unreviewed community plugin marketplace;
- persistent GPU capacity solely for visual smoothness.

## Product metrics

### Academic comprehension

- time to reach a recorded run and `TR-2026-001`;
- ability to state the research thesis, current evidence, and limitations;
- navigation from claim to method, source, code, and negative result;
- serious research, mentorship, PhD, grant, or relevant employment inquiries.

### Quality

- replay verification and workflow task success;
- citation support and trace completeness;
- deterministic calculation consistency;
- clean-checkout reproduction success;
- accessibility audit results and cold-state fallback success.

### Safety and operations

- unauthorized actions and cross-tenant leakage: target zero;
- abuse-block efficacy and cost per bounded public workflow when enabled;
- incident count, recovery time, and stale/public-claim detection.

Metrics are never fabricated or silently collected. Analytics and research-trace
donation use separate consent and data paths.
