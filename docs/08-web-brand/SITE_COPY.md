---
document_id: DRL-WEB-022
title: "Personal Academic Portfolio Site Copy"
version: 3.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-16
---

# Personal academic portfolio site copy

Paste-ready copy for manual Wix use. This does not authorize a Wix write; nothing
here is applied to the live site by any tool in this repository.

Version 3.0.0 replaces the outline in 2.0.0 with finished text, and reduces the
tree from four pages to three. It is written against the live site as audited on
2026-08-16, so it says what to remove as well as what to write.

## The one deviation from RES-016

RES-016 approves four pages: Home, Research, Projects, About. This draft writes
**three** — Home, Projects, About — and puts TR-2026-001 on Projects.

The reason is that there is one report. A Research page holding a single item,
next to a Projects page describing the same work, splits thin material across two
thin pages. When a second report exists, Research earns its own page and the
TR-2026-001 block moves there unchanged.

This is a deviation to accept or reject, not a decision already made. The
auditor still expects `/research`, and will report it missing until either the
page exists or this deviation is approved into RES-016.

## Before you paste: what comes off the site

These are the live findings, in the order they matter. The first group is not
stylistic.

**Claims with nothing behind them.** None of these strings appear anywhere in
the repository, and the work they describe has not happened:

| On the site now | Reality |
| --- | --- |
| TR-2026-001 "Coordinating Language Models, Deterministic Analysis, and Human Approval for Specialist Systems" | The real TR-2026-001 is *Local Integrated Evidence-to-Scenario Workflow* |
| "We utilized Llama-3-70B and Mistral-Large-2 as core inference engines" | No model has been run live. Model selection (DIR-004) is still open |
| "across 500+ distinct research trajectories" | No such runs exist |
| "Deterministic pass rate achieved 94.2% on source verification tasks" | Not produced by anything in the repository |
| "Strongest trajectories documented in run 084x" | No such run |
| Citation: "Intelligence as Agency: Coordinating Multi-Agent Multi-Layer Systems" | A third title, inconsistent with the heading above it |
| "RUN DOCUMENTED: CHARLOTTE, NC // OCT 2026" | Future-dated |

**Institutional chrome.** `NODE: 01 // UPTIME: 99.9%` in the footer of all three
pages — `BRAND_SYSTEM.md` names that exact string as its example of a fabricated
metric. "Specialist research nodes" on the Systems page is prohibited by the same
section. So is the six-row TECHNICAL SPECIFICATIONS table, which asserts
completeness ("FULLY DEPLOYABLE", "FULL TRACEABILITY") for prototypes.

**A wrong link.** The footer links to `http://www.git-hub.com/chris-dewitt`. That
is not GitHub. The correct link is `https://github.com/chris-dewitt`.

**Dead buttons.** *View my research*, *About me*, *View All Questions*, *Watch
prototype run*, *Inspect deterministic logs*, *Source code*, and *Recorded run*
have no destinations. A button that does nothing reads worse than no button:
either point it somewhere or delete it.

**Duplication.** The homepage lists the same five research questions twice, once
as INTEREST_01–05 and again as Q-2026-001–005 with invented pipeline states
(`[ACTIVE_INVESTIGATION]`, `[DEGRADED_STATE]`). Keep one list, without the states.

**An empty page.** `/projects` has 133 characters of visible text — nav and
footer only — and the homepage links to it.

---

# Page 1 — Home

## Hero

```text
CHRISTOPHER NOXON DEWITT
Academic Portfolio

I am a student in the Master of Applied Data Science program at the University of
North Carolina at Chapel Hill. I engineer complex systems at work and study them
part time, with the goal of moving from applied data science toward graduate work
in computer science.

[ View my research ]  [ Explore my projects ]
```

RES-016 fixes both the labels and their order: research first, projects second.
Both must resolve. While `/research` is deferred, *View my research* goes to the
TR-2026-001 section on `/projects` and *Explore my projects* to the top of the
same page. Neither resolves today.

## Opening statement

```text
On deterministic agency

My academic interest sits on the divide between language models, deterministic
policy, and human approval — which decisions a probabilistic model should be
allowed to make, which belong to code that behaves the same way every time, and
which require a person to agree before anything happens.

I am documenting the failures as well as the results. This portfolio is one
person's trajectory through these systems, not a laboratory and not an
organization.
```

## Open questions

One list. No status tags — an open question is open, and labelling five of them
with different pipeline states implies a machine that is processing them.

```text
Open questions

01  Can small and mid-sized open-weight models reliably operate specialist
    systems?

02  How should language models, deterministic policy, and human approval divide
    authority?

03  How can research agents preserve temporal truth, source lineage, calculation
    lineage, and uncertainty?

04  How should complete agent trajectories be evaluated, rather than only final
    answers?

05  How can deterministic fixtures verify the reliability of stochastic model
    outputs in a research workflow?
```

## Selected work

```text
TR-2026-001 — Local Integrated Evidence-to-Scenario Workflow

An independent technical report documenting one reproducible workflow: a local
runtime gathers synthetic macroeconomic evidence, compares synthetic Federal
Reserve communications with passage-level citations, projects a bear-steepener
scenario against an educational bank balance sheet, evaluates the resulting
trajectory, and links all five artifacts under a single task digest.

The report is prototype maturity and says so: fixture data only, no trained
model weights, no production signing identity, and no live public deployment.
It includes the method, the limitations, and the source.

[ Read the report ]
```

## What I am working on

```text
Current direction

Right now I am choosing a base model. An open-weight model has to run specialist
systems on hardware I actually own, and the selection is gated on evidence rather
than preference: a candidate cannot be chosen on a single measurement, against no
alternative, or on a license that has not been confirmed.

No model has been selected yet. That gate is the current work.
```

This section is optional, and it is the most honest thing the site could say. An
open question in progress reads as research; a finished claim would not be true.

## Footer

```text
Local prototype runs · deterministic fixtures · not a production environment

This is an independent initiative. Not a government, university, or accredited
institution.

GitHub · Contact · Privacy
```

Delete `NODE: 01 // UPTIME: 99.9%`. Fix the GitHub URL to
`https://github.com/chris-dewitt`.

---

# Page 2 — Projects

## Intro

```text
Projects

Software I have built to learn how complex systems are designed, connected,
tested, and explained. All of it is prototype work. Each entry says what exists,
what it runs on, and where it stops.
```

## The report

Place the TR-2026-001 block from the homepage here in full, followed by:

```text
Method

A deterministic local runtime composes five components behind one orchestrator.
Every step emits a typed envelope, every policy decision is recorded, and the
artifacts are linked under one digest so a claim can be traced back to the
evidence or calculation that produced it.

Limitations

Fixture data throughout — no live economic APIs and no production bank data.
No trained model weights: the open-weight selection is still open. Signatures in
the recorded runs are valid inside the local laboratory context only, and are not
intended for verification by anyone else.

Source · Recorded run
```

Point *Source* at the repository. Do not add *Recorded run* until a page exists
to receive it: the replay site is generated into `site/replays` and is not
published anywhere yet.

## The five projects

Written as five short entries. No capability table, no completeness claims, no
"nodes".

```text
Atticus — orchestration and agent-system research
The control plane: planning, policy, approvals, and tool calls under one
protocol. Prototype. Runs locally against a deterministic planner today; the
open-weight planner is wired and gated on model selection.

Atlas — macroeconomic evidence gathering
Collects macro evidence with provenance attached to every figure. Prototype,
running on synthetic fixture data, not live economic APIs.

FedLens — cited analysis of Federal Reserve material
Compares communications passage by passage and cites what it used. Prototype,
running on a bounded fixture corpus of synthetic material.

BalanceLab — deterministic scenario modeling
Projects rate scenarios against an educational bank balance sheet with fixed
seeds, so the same inputs give the same output. Prototype. The worked example is
a bear-steepener.

EvalForge — evaluation and permission testing
Grades whole agent trajectories rather than final answers, and tests what a run
was allowed to do. Prototype.
```

The words "prototype", "synthetic", and "fixture" are doing necessary work in
every one of those. They are the difference between describing a workbench and
implying a product.

## Replacing the Systems page

The Systems page becomes this page. Its five cards carry over as the entries
above; its TECHNICAL SPECIFICATIONS table does not. Two of that table's six rows
are worth keeping as ordinary sentences, because they are true and load-bearing:

```text
Everything runs locally, on hardware I own, without a cloud dependency. The code
is open source. This is an independent initiative — not a government, university,
or accredited institution.
```

Then remove `/systems` from the navigation.

---

# Page 3 — About

```text
About

I am Christopher Noxon DeWitt, a student in the Master of Applied Data Science
program at the University of North Carolina at Chapel Hill.

I work with complex systems professionally and study them part time. My
background includes quantitative financial analysis, statistics, economics,
applied data science, software development, Python, SQL, and technical
automation. I am especially interested in agent systems, evaluation,
reproducibility, and the boundary between data science and computer science.

After my current studies, I hope to continue toward graduate work in computer
science.

GitHub · Email
```

Add CV and LinkedIn when they are ready. Do not name an employer, and do not
imply that the university endorses the independent projects — the degree program
is the whole of the affiliation.

The homepage "About me" button points here. Currently it points nowhere.

---

## Copy rules

1. The site is Christopher's academic portfolio.
2. Lead with current study and direction, not a lab name or a slogan.
3. Use "I", not "we". There is no team, and "we" invents one.
4. Projects are evidence, not departments. Not "nodes", not "our systems".
5. Keep the UNC-Chapel Hill affiliation exact and limited to the degree program.
6. Never expose employer identity or confidential work.
7. **Every number is a claim.** A figure on the site must be reproducible from
   the repository and linked to what produced it. If it cannot be, it does not go
   on the site — including uptime, pass rates, run counts, and dates.
8. **Name the maturity.** Prototype work says "prototype"; fixture data says
   "fixture" or "synthetic". Omitting the qualifier is itself a claim.
9. A button either resolves or does not exist.

## Where each claim comes from

Every factual statement in this copy traces to a repository source. Nothing here
requires new evidence to be true.

| Claim in the copy | Source |
| --- | --- |
| TR-2026-001 title, scope, method, limitations | `docs/10-research/reports/TR-2026-001-integrated-workflow.md` |
| All five projects are `prototype` | `docs/00-program/CURRENT_STATE_BASELINE.md` |
| Model weights are `specified`, selection open | `docs/00-program/CURRENT_STATE_BASELINE.md`, DIR-004 / G-001 |
| Selection cannot rest on one candidate or an unconfirmed license | `packages/drl-ai-core/src/drl_ai_core/bakeoff_harness.py` (`EvidenceGate`) |
| Fixture/synthetic data throughout | TR-2026-001 §1 scope |
| Local execution, no cloud dependency | `docs/02-architecture/DEPLOYMENT_AND_ENVIRONMENTS.md` |
| Independent-initiative disclosure | `BRAND_SYSTEM.md`, required content |
