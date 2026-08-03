---
document_id: DRL-WEB-022
title: "Site Copy Draft for the Five-Page Workshop Build"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-03
---

# Site copy draft

Page-by-page copy for the five-page tree in `WIX_SITE_BUILD_PLAN.md` v2.0.0.

**Status: DRAFT, not applied.** No site write is authorised. This document exists so
copy can be reviewed and edited before anything touches Wix.

Everything below is written to `BRAND_SYSTEM.md` v2.1.0: first person, understated
academic, no absolute capability claims, no invented plurals, no institutional chrome.
Bracketed `[…]` text marks a decision only the Director can make.

---

## Home — `/`

### Hero

```text
DEWITT RESEARCH WORKSHOP
Independent research in open and applied intelligence.

Intelligence for Good. Intelligence for All.
```

Orientation line beneath:

> I'm Chris DeWitt. I build and test open-weight AI systems in the open — one person,
> working in public, with the failures left in.

Actions: `See what I'm building` → `/projects` · `Read the current work` → `/writing`
· `Browse the code` → `/open-source`

### On the bench

> **On the bench**
>
> What I'm working on right now. Dates are real; so is the half-finished part.

- **The evidence-to-scenario workflow** — *last touched 3 August 2026*
  Five projects chained into one run: pull evidence, cite it, model a scenario,
  evaluate the result. It works end to end on my machine with deterministic fixtures.
  It is not a service, and the planner standing in for Atticus Core is rule-based
  until the model bake-off finishes.

- **Signed replay packaging** — *in progress*
  Recording runs so someone else can replay exactly what happened, including the
  degraded case. Currently signed with a demo key — not a production signing
  identity, so treat the signatures as structural, not trustworthy.

- **Choosing the models behind Atticus** — *open question*
  Running a documented bake-off rather than picking by brand. No winner declared.

### Featured work

> **TR-2026-001 — Local Integrated Evidence-to-Scenario Workflow**
> Technical report · prototype · 1 August 2026
>
> A working description of how the five projects compose into a single local
> workflow: what each one contributes, where the trust boundaries sit, and what the
> evaluation actually shows. Written to be reproduced, not admired.
>
> `Read the report` → `/writing#tr-2026-001`

### Projects

> **Projects**
>
> Five things I'm building. All prototypes — that label is accurate, not modest.

| | |
|---|---|
| **Atticus** | The guide and operator that runs the others. Open-weight. *Prototype.* |
| **Atlas** | Macro research and evidence gathering. *Prototype.* |
| **FedLens** | Federal Reserve policy analysis with passage-level citations. *Prototype.* |
| **BalanceLab AI** | Deterministic scenario modelling with fixed seeds. *Prototype.* |
| **EvalForge** | Evaluation and permission testing for the rest. *Prototype.* |

Maturity values bind to the `Systems` collection; do not hand-type them.

### Open source and contact

> Everything here is open source. The code is on GitHub, the packages install
> locally, and the research documents live in the same repository as the software
> that produced them.
>
> If you want to run it, start with the repository. If you want to talk, [contact
> route TBD — see DIR-003].

> This is an independent initiative. Not a government, university, or accredited
> institution.

---

## Projects — `/projects`

> **Projects**
>
> Five projects, built to work together and to run on one machine. Each is a
> prototype: the interfaces will change, and I'll say so on the page when they do.
>
> Atticus is the operator — it plans and runs work across the other four. The rest
> are specialists that do one thing each.

Then the five cards, each linking to its page, each showing maturity and last
verified date from the `Systems` collection.

Per-project one-liners:

- **Atticus** — Plans a piece of work, calls the right project, and keeps a trace of
  what it did. Open-weight, locally runnable, currently driven by a rule-based
  planner rather than a trained model.
- **Atlas** — Gathers macro evidence from public sources and hands it downstream with
  its provenance attached.
- **FedLens** — Reads Federal Reserve material and answers with passage-level
  citations, so a claim can be checked against its source.
- **BalanceLab AI** — Runs quantitative scenarios deterministically: fixed seeds, same
  inputs, same numbers.
- **EvalForge** — Tests the others: whether the answer holds up, and whether the
  permission boundaries did.

---

## Writing — `/writing`

> **Writing**
>
> Technical reports and notes. Fewer, longer, and reproducible in preference to
> frequent.

### TR-2026-001 {#tr-2026-001}

Full reading experience on the page: title, authors, status, version, date, abstract,
plain-language summary, methods, limitations, links to code and data, citation block,
and correction history. Not a teaser card.

> **TR-2026-001: Local Integrated Evidence-to-Scenario Workflow**
> Christopher Noxon DeWitt · prototype · v1.0.0 · 1 August 2026
>
> Cite as: DeWitt, Christopher Noxon. 2026. *Technical Report TR-2026-001: Local
> Integrated Evidence-to-Scenario Workflow*. DeWitt Research Workshop working paper.
> Document ID `DRL-TR-2026-001`.

### What broke {#what-broke}

> **What broke**
>
> Things that failed, and what I did about them. This shelf is not decoration — every
> entry is real, and each one has a test that keeps it fixed.
>
> [Populate from `FailureRecords`. Start with the degraded-replay case, which is
> already captured as a fixture. Do not invent entries to fill the section: if there
> is one honest record, publish one.]

---

## Open Source — `/open-source`

> **Open source**
>
> All of it. The models are open-weight, the code is open-source, and the research
> documents ship in the same repository as the software that produced them.

> **Run it locally**
>
> The workflow runs on one machine with deterministic fixtures — no cloud account, no
> API key, no inference bill.
>
> ```
> [install and run commands — pull the real ones from the repository README
> rather than writing them here]
> ```

> **What's in the repository**
>
> - **Packages** — `atticus-sdk`, `drl-ai-core`, `drl-protocol`, `evalforge-sdk`
> - **Services** — Atticus control plane, Atlas, FedLens, BalanceLab AI, EvalForge
> - **Applications** — Atticus console, local runner
> - **Research** — technical reports, in the same tree as the code
>
> Identifier prefixes like `DRL-` are internal keys, not a brand.

> **Contributing**
>
> Good-first issues are labelled in the repository. Corrections to the research
> documents are as welcome as code.

Upstream projects are credited without implying endorsement. Do not claim "full
access to all core components" or similar absolutes.

---

## About — `/about`

> **About**
>
> I'm Christopher Noxon DeWitt, an applied AI researcher. This is my workshop: one
> person building and testing open-weight AI systems in public, in Charlotte.
>
> My background is quantitative and financial, which is why the projects lean toward
> evidence, policy, and deterministic modelling. It informs the work; it isn't the
> point of it.
>
> I care about systems people can actually run, inspect, and disagree with. That's
> why the models are open-weight, why the failures are published, and why every
> maturity label says prototype until it earns otherwise.

> **Contact** — [route TBD, see DIR-003]
> **Security** — [`security@dewitt-labs.com` once created; see DIR-003]
> **Governance** · **License** · **Privacy** — link to the published documents

> This is an independent initiative. Not a government, university, or accredited
> institution.

---

## Copy rules for whoever applies this

1. No absolute capability claims. "Fully deployable", "full traceability", "full
   access to all core components" are prohibited unless measured and linked.
2. No plural that invents staff. Not "our team", "our researchers", "we deliver".
3. No fabricated metrics. `UPTIME: 99.9%` must be deleted, not restyled.
4. Maturity labels bind to the `Systems` collection. Never hand-typed, never two
   different labels on one page.
5. No button that promises an action the site cannot perform.
6. Do not repeat one sentence across five cards to fill space. Cut the cards instead.
