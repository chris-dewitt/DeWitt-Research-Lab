---
document_id: DRL-WEB-022
title: "Site Copy Draft for the Five-Page Workshop Build"
version: 1.1.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Site copy draft

Page-by-page copy for `WIX_SITE_BUILD_PLAN.md`. This is a repository artifact,
not authorization to edit Wix. Bracketed text is an implementation note.

## Home — `/`

### Hero

```text
DEWITT RESEARCH WORKSHOP
Engineering complex systems for open, inspectable intelligence.

I build agents, evidence pipelines, deterministic models, and the evaluations
that keep them honest. This is the public record of that work.

[Watch a recorded run] [Read TR-2026-001]
```

> Intelligence for Good. Intelligence for All.

### A run you can inspect

> **One workflow, two honest outcomes.**
>
> Watch Atticus route a research question through public evidence, cited policy
> analysis, a deterministic scenario, and evaluation. Then switch to the
> degraded run and see what happens when part of the evidence path fails.
>
> Recorded prototype · deterministic fixtures · signed with a demo HMAC key
>
> `Watch the success run` · `Watch the degraded run` · `Read the transcript`

[Bind these links to the DRL-019 public replay artifacts. Explain that the demo
key validates package structure, not production identity.]

### Read the method, not just the result

> **TR-2026-001 — Local Integrated Evidence-to-Scenario Workflow**
> Technical report · prototype · 1 August 2026
>
> A working description of how five projects compose into one local workflow:
> what each contributes, where the trust boundaries sit, what the evaluation
> shows, and what it does not show.
>
> `Read TR-2026-001` · `Methods and limitations` · `View source`

### Questions on the bench

> I am interested in the systems around intelligence: how agents earn authority,
> how evidence survives a multi-step workflow, how deterministic tools constrain
> language models, and how evaluation catches failure before a demo becomes a
> claim.

> **Stage-B model bake-off — no winner.**
>
> Six release-gate findings prevented a selection. That is the result: the
> candidates did not yet earn the role. `See the board and all six reasons`.

### Projects

- **Atticus** — a documented guide and orchestration research artifact. Prototype;
  the public hosted service is planned, not live.
- **Atlas** — macro evidence gathering with provenance attached. Prototype.
- **FedLens** — Federal Reserve analysis with passage-level citations. Prototype.
- **BalanceLab AI** — deterministic quantitative scenarios with fixed seeds.
  Prototype.
- **EvalForge** — evaluation and permission testing for the rest. Prototype.

[Maturity and last-verified dates bind to controlled metadata.]

### About the work

> I'm Christopher Noxon DeWitt, an applied AI researcher in Charlotte. My
> background includes quantitative financial analysis, which is why this work is
> unusually strict about evidence, deterministic calculations, and failure
> boundaries. It informs the research; it is not the headline.
>
> Serious conversations about research, mentorship, doctoral study, grants, or
> relevant work are welcome. [Contact route pending DIR-003.]

> Independent initiative. Not a university, company research division,
> government laboratory, or accredited institution.

## Projects — `/projects`

> **Five projects, one research program.**
>
> These prototypes study how evidence, policy, deterministic tools, agent
> orchestration, and evaluation fit together. Each page shows what exists, how it
> was tested, what failed, and what remains planned.

Each project page includes research question, workflow, architecture, trust
boundary, maturity, last verification, replay/read/run/planned actions, methods,
limitations, source, license, upstream lineage, and related writing.

Atticus copy:

> **Atticus** plans a bounded piece of work, calls the appropriate project, and
> preserves a trace of what happened. The current integrated prototype uses a
> rule-based planner while the model bake-off remains unresolved. Atticus is a
> research artifact being documented; `atticus.dewitt-labs.com` is planned.

## Writing — `/writing`

> **Technical reports, notes, methods, and things that broke.**
>
> Fewer, longer, and reproducible in preference to frequent.

`TR-2026-001` receives a full reading experience with abstract, plain-language
summary, methods, limitations, code/artifact links, citation, license, and
correction history.

### Methods and teaching

> **Integrated Workflow Lab**
>
> A reproducible guide to the fixture workflow, its evidence chain, exercises,
> and expected limitations. Teaching material stays here until there is enough
> maintained work for its own page.

### What broke

> **Degraded replay**
>
> The failure is part of the record. See where the workflow degraded, how the
> system represented uncertainty, and which regression evidence keeps that path
> visible.

> **Stage-B model bake-off: no winner**
>
> Read the six blocking reasons, candidate evidence, and next experiment. No
> candidate is promoted by brand preference.

## Open Source — `/open-source`

> **Open enough to inspect, run, and disagree with.**
>
> The code is open-source; model artifacts are described precisely as
> open-weight when that is what their terms permit; evaluations and research
> records are public; the fixture workflow runs locally without a cloud account.

Show verified install/run commands, repository structure, licenses, upstream
lineage, hardware assumptions, maturity, reproduction bundles, and open
exceptions. Contributor guidance and good-first issues appear after the local
run path as a secondary invitation.

## About — `/about`

> **Christopher Noxon DeWitt**
>
> Applied AI researcher in Charlotte, North Carolina. I engineer complex systems
> across agents, evidence, evaluation, and deterministic quantitative modeling.
>
> My background spans statistics, economics, applied data science, software
> development, and quantitative financial analysis. I built this workshop to
> make the questions, code, experiments, failures, and next steps inspectable in
> one place.
>
> I am interested in research mentorship, doctoral study, grants, and relevant
> research or engineering roles. The workshop is not currently recruiting a
> team.

`Contact` · `GitHub` · `Research interests` · `Curriculum vitae when approved`

Do not name an employer. Preserve the independent-initiative disclosure and link
working Governance, License, Privacy, and Security routes.

## Copy rules

1. Put evidence immediately after the thesis.
2. Use first person; never invent a staff, department, or institutional history.
3. No absolute capabilities, fabricated metrics, or unlabeled simulation.
4. No button promises an action that does not exist.
5. `Watch a recorded run` and `Read TR-2026-001` remain the first actions.
6. Failures, limitations, and the no-winner result remain visible.
7. Contribution is available but not the homepage's dominant invitation.
8. Employer names and confidential work never appear.
