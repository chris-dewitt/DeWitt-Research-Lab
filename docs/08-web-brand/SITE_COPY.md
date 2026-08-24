---
document_id: DRL-WEB-022
title: "Personal Academic Portfolio Site Copy"
version: 3.2.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-24
---

# Personal academic portfolio site copy

Paste-ready copy for manual Wix use. This does not authorize a Wix write; nothing
here is applied to the live site by any tool in this repository.

Version 3.2.0 points the recorded-run buttons at the live GitHub Pages viewer
`https://chris-dewitt.github.io/DeWitt-Research-Lab/`. Wix remains the
portfolio; Pages hosts the signed fixture recordings. Version 3.1.0 replaced
the outline in 2.0.0 with finished text for all four approved pages.

## Page tree

Four pages, as RES-016 approves them: Home, Research, Projects, About.

An earlier draft of this document proposed three, folding Research into Projects
on the grounds that a Research page holding one report next to a Projects page
describing the same work splits thin material across two thin pages. That
reasoning rested on there being one report. There are two — TR-2026-001 and
TR-2026-002 — and the second is the stronger of them, because its result is a
null one. The premise was wrong, so the deviation is withdrawn and the approved
tree stands unchanged.

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

**Dead buttons.** *View my research*, *About me*, *View All Questions*,
*Inspect deterministic logs*, and *Source code* have no destinations. A button
that does nothing reads worse than no button: either point it somewhere or
delete it. *Watch prototype run* and *Recorded run* now have a destination:
`https://chris-dewitt.github.io/DeWitt-Research-Lab/`.

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
*View my research* goes to `/research`, *Explore my projects* to `/projects`.
Neither resolves today — both are dead buttons on the live site.

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

A summary and a link. Report detail lives on `/research`, once — spreading
abstracts, limitations, and figures across pages is how the fabricated block
came to sit on three pages at the same time.

```text
Research

Two working papers: one documenting a traceable evidence-to-scenario workflow,
one describing a model-selection harness whose evidence gate currently refuses to
name a winner — and why that is the correct outcome.

[ Read the research ]

Recorded runs

Two signed recordings of the evidence-to-scenario workflow, including one that
fails partway through and keeps going. They replay in the browser with no model,
GPU, or API key.

[ Watch a recorded run ]
```

Point *Watch a recorded run* at
`https://chris-dewitt.github.io/DeWitt-Research-Lab/`. Those pages are fixture
recordings with a demo signature, not live market data and not a local model
run. The portfolio stays on this Wix site.

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

# Page 2 — Research

The whole page, as markdown. This is where report detail lives; Home summarizes
it and Projects points at it.

```markdown
# Research

Independent technical reports from my own work. Each says what was done, what the
evidence supports, and where it stops. Both are prototype-maturity working papers,
not peer-reviewed publications, and neither is coursework for my degree program.

---

## TR-2026-001 — Local Integrated Evidence-to-Scenario Workflow

**Working paper · prototype · v1.0.0 · August 2026**

Can specialist components be coordinated so that every claim at the end is
traceable to the evidence or calculation that produced it?

This report documents one reproducible workflow. A local runtime gathers synthetic
macroeconomic evidence, compares synthetic Federal Reserve communications with
passage-level citations, projects a bear-steepener scenario against an educational
bank balance sheet, evaluates the resulting trajectory, and links all five
artifacts under a single task digest. Every step emits a typed envelope and every
policy decision is recorded, so the path from a final statement back to its source
is inspectable rather than asserted.

**Limitations.** Fixture data throughout — no live economic APIs, no production
bank data. No trained model weights. Signatures in the recorded runs are valid
only inside the local laboratory context and are not intended for verification by
anyone else.

[Read the report] · [Source]

---

## TR-2026-002 — Evidence-Gated Model Selection

**Working paper · prototype · draft · v1.1.0 · August 2026**

Model selection is usually reported as a ranking: score the candidates, take the
highest. That framing hides the question that comes first — whether the
measurement was good enough to support choosing at all.

This report describes a harness that separates the two. Candidates run against a
fixed task suite and are graded deterministically, which produces a ranking. The
ranking then passes through an evidence gate of nine blocking conditions:
measurement provenance, revision pinning, license clearance, suite coverage,
execution completeness, a quality floor, zero safety-critical failures, a minimum
field of candidates, and a minimum margin over the runner-up. A failure on any one
returns "no selection" together with its reasons. No score overrides a blocked
gate.

**Result: no winner.** Run against the current candidate register, the gate
refuses to select for either role. The core role is blocked by six reasons at
once — quality below the floor, safety-critical failures on citation refusal and
credential refusal, an unpinned revision, an uncleared license, fixture rather
than hardware measurement, and a margin of zero over the runner-up. The edge role
falls below the eight-task coverage minimum with a safety-critical failure
recorded. That null result is the report's only empirical claim.

**Limitations.** The candidates here are scripted fixtures that perform no
inference; they exercise the harness, not any model. Three of them tied exactly,
an artifact of their sharing one script, reported rather than suppressed. The
suite is twelve tasks — a starting instrument, not a decisive one. The thresholds
are asserted from judgment rather than derived from a power analysis, and no claim
is made that the gate conditions are complete.

[Read the report] · [Source]

---

## What is not settled

No base model has been selected. The gate above is the reason, and it is working
as intended: a selection made on one candidate, against no alternative, on a
license that has not been confirmed, is the premature result the gate exists to
refuse.

Two things have to happen before that changes. A second candidate has to be
served, because a field of one is a measurement and not a comparison. And the
license status of the leading candidate has to be confirmed against the publisher
rather than the packaged model card, because a hedged status is not a cleared one.

## Recorded runs

Wix editor: add this block on **Home** and on **/projects** (the live
`/research` route currently 404s). The button must be a real HTTPS link, not
plain text.

```text
Recorded runs

The workflow in TR-2026-001 has signed recordings, including a deliberately
degraded one. A run that fails is evidence about the system, not an outcome to
hide.

Watch them here — no model, GPU, or API key required:
https://chris-dewitt.github.io/DeWitt-Research-Lab/

These are fixture recordings signed with a demo key so the files cannot be
silently swapped. That is integrity checking, not a production signature, and
the numbers are not live market data. This Wix site is the academic portfolio;
the recordings live on GitHub Pages.

[ Watch a recorded run ]
```

### Link targets

| Placeholder | Target |
| --- | --- |
| TR-2026-001 → Read the report | `blob/main/docs/10-research/reports/TR-2026-001-integrated-workflow.md` |
| TR-2026-002 → Read the report | `blob/main/docs/10-research/reports/TR-2026-002-evidence-gated-model-selection.md` |
| Both → Source | repository root |
| Watch a recorded run | `https://chris-dewitt.github.io/DeWitt-Research-Lab/` |

Confirm the repository name before pasting: GitHub reports the project as moved
from `DeWitt-Research-Lab-Foundation` to `DeWitt-Research-Lab`. The old address
redirects, so both work today; pick the canonical one deliberately rather than
inheriting it from an old link.

---

# Page 3 — Projects

## Intro

```text
Projects

Software I have built to learn how complex systems are designed, connected,
tested, and explained. All of it is prototype work. Each entry says what exists,
what it runs on, and where it stops.
```

## Pointing at the research

Projects does not restate a report. Each entry names the report that used it, and
the link does the rest:

```text
Used in TR-2026-001 · Read the research
```

Atticus carries a second line, because the selection harness evaluates it:

```text
Evaluated by the harness in TR-2026-002
```

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

# Page 4 — About

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
| TR-2026-002 nine gate conditions, no-winner result, six blockers, twelve tasks, tied candidates | `docs/10-research/reports/TR-2026-002-evidence-gated-model-selection.md` §§2–6 |
| All five projects are `prototype` | `docs/00-program/CURRENT_STATE_BASELINE.md` |
| Model weights are `specified`, selection open | `docs/00-program/CURRENT_STATE_BASELINE.md`, DIR-004 / G-001 |
| Selection cannot rest on one candidate or an unconfirmed license | `packages/drl-ai-core/src/drl_ai_core/bakeoff_harness.py` (`EvidenceGate`) |
| Fixture/synthetic data throughout | TR-2026-001 §1 scope |
| Local execution, no cloud dependency | `docs/02-architecture/DEPLOYMENT_AND_ENVIRONMENTS.md` |
| Independent-initiative disclosure | `BRAND_SYSTEM.md`, required content |
