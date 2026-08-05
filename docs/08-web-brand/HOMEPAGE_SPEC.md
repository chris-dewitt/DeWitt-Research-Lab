---
document_id: DRL-WEB-004
title: "Homepage Detailed Specification"
version: 4.2.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Homepage Detailed Specification

## Canonical implementation

The homepage is implemented at **`https://www.dewitt-labs.com`** in Wix. It is
complete without a live Atticus service. A bounded custom element may enhance a
recorded replay, but a transcript and ordinary link are always available.

## Hero

```text
DEWITT RESEARCH WORKSHOP
Engineering complex systems for open, inspectable intelligence.

I build agents, evidence pipelines, deterministic models, and the evaluations
that keep them honest. This is the public record of that work.

[Watch a recorded run] [Read TR-2026-001]
```

The approved mission line, **Intelligence for Good. Intelligence for All.**,
appears as a quiet mission statement below the research thesis or in the first
evidence transition. It is not the only explanation of the work.

The first action opens the success replay with an obvious switch to the degraded
case. The second opens the report reading experience. Both have ordinary-link
fallbacks. No project catalog, code link, status badge, or contact action outranks
them.

Optional visual: an accessible, low-motion trace fragment from the real replay.
Do not use a generic AI image, fictional terminal text, fake node/status strip,
or animation required for comprehension.

## Evidence block 1: Recorded run

Heading: **A run you can inspect**

Show:

- recorded/prototype/fixture labels;
- artifact ID, version, and verification date;
- the research question and plain-language outcome;
- task -> evidence -> scenario -> evaluation -> report sequence;
- controls for **Success** and **Degraded**;
- transcript, manifest, verification method, and source links;
- plain warning that the demo HMAC proves packaging structure, not production
  signing identity.

The degraded case is visible without an easter egg or separate failure page.

## Evidence block 2: Technical report

Heading: **Read the method, not just the result**

Feature `TR-2026-001: Local Integrated Evidence-to-Scenario Workflow` with its
abstract opening, prototype status, date, methods, limitations, citation, code,
and reproduce links. This is a substantive reading surface, not a decorative
card.

## Research agenda and negative result

Heading: **Questions on the bench**

State two to four current research questions from controlled documents. Directly
below them, feature the current model bake-off:

```text
STAGE-B MODEL BAKE-OFF
Result: no winner.
```

List the six documented reasons no candidate was selected and link the board,
protocol, and next experiment. “No winner” is evidence of the release gate
working, not a suspense hook.

## Projects

List Atticus, Atlas, FedLens, BalanceLab AI, and EvalForge compactly. Each entry
has one sentence, maturity, last verified date, strongest evidence, and a link.
Atticus is the guide/operator research artifact, not a public service claim.

## Writing, methods, and teaching

Link technical reports, notes, the integrated workflow lab, and failure records.
Teaching stays a Writing/Methods collection until enough maintained material
exists for a standalone page.

## Founder and contact

One short paragraph:

> Christopher Noxon DeWitt is an applied AI researcher in Charlotte engineering
> complex systems across agents, evaluation, evidence, and deterministic
> quantitative modeling.

Quantitative financial analysis may appear in the expanded profile. Do not name
an employer. Invite serious research, mentorship, PhD, grant, and relevant
employment conversations; do not publish an open call to join a team.

## Open identity

Open weights, open-source software, public evaluation, local operation, and
reproducible research are visible before the footer. Link licenses, upstream
lineage, source, and reproduction evidence without turning contribution into the
homepage's primary conversion goal. A visible **Open Source portal** link leads
to the local-run and artifact catalog.

## Wix launch requirements

- domain, HTTPS, canonical URL, apex redirect, social cards, favicon, robots,
  and sitemap verified;
- evidence buttons resolve to real public artifacts or explicit fallbacks;
- no `Launch Atticus` action while the public application is only planned;
- maturity and verification dates come from controlled metadata;
- phone, tablet, laptop, keyboard, screen-reader, reduced-motion, zoom, and
  unavailable-backend states pass review;
- no fabricated uptime, system count, release status, or institutional chrome.
