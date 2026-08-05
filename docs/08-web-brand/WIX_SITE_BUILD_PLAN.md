---
document_id: DRL-WEB-019
title: "Wix Site Build Plan and Page Blueprint"
version: 2.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Wix Site Build Plan and Page Blueprint

## Objective

Rework `www.dewitt-labs.com` into an evidence-first academic workshop and
portfolio. A visitor should quickly understand the research thesis, inspect a
real run, read a real report, see honest failure evidence, and decide whether a
serious research or professional conversation is warranted.

The site keeps the cream-on-black research-workstation language and the approved
mission, but removes institutional theater. Atticus appears as a documented
research artifact until a public application exists.

## Success hierarchy

1. **Watch a recorded run.**
2. **Read TR-2026-001.**
3. Understand the research agenda, including the degraded case and Stage-B
   no-winner result.
4. Inspect projects, code, methods, and the Director's background.
5. Contact the Director about research, mentorship, PhD, grant, or relevant
   employment opportunities.

Contributor discovery remains available under Open Source but is not a primary
homepage conversion.

## Wix page tree

```text
Home            /            thesis, run, report, questions, projects, founder
Projects        /projects    five artifacts with maturity and evidence
Writing         /writing     TR-2026-001, notes, methods, teaching, failures
Open Source     /open-source local run, source, licenses, lineage, contribution
About           /about       person, interests, background, contact, disclosure
```

Teaching remains a Writing/Methods collection even though a real integrated
workflow lab now exists. It receives a standalone page only after the collection
has enough maintained material to make that route honest. Failure records also
remain under Writing so negative results stay beside the research they qualify.

### Redirects

```text
/laboratory      -> /
/systems         -> /projects
/research        -> /writing
/failure-museum  -> /writing#what-broke
/teaching        -> /writing#methods
/status          -> /projects
```

Existing project paths may remain and should be linked from `/projects`.

## As-built snapshot recorded 2026-08-03

This is a dated audit, not a claim about current live state.

Already present:

- live Wix origin and canonical `www` domain;
- near-black canvas, mono metadata, five project pages, and independent-initiative
  disclosure;
- CMS with a populated `Systems` collection and seven empty collections;
- broad 14-page institutional tree.

Known cleanup items:

- collapse the broad tree into the five-page workshop structure;
- replace project/status-first homepage hierarchy with the recorded run and
  `TR-2026-001`;
- remove fabricated `UPTIME: 99.9%` and any operations-center framing;
- bind visible maturity values to controlled metadata;
- populate evidence surfaces from repository artifacts rather than placeholder
  copy;
- fix footer labels that are not working links;
- restore warm cream as the primary foreground and reserve amber for function;
- label unresolved subdomains, including `atticus.dewitt-labs.com`, as planned.

## Global shell

### Header

- compact wordmark;
- Projects, Writing, Open Source, About;
- optional search;
- visible keyboard focus and a compact mobile menu;
- no Launch, Status, Join, or Apply action.

### Footer

- canonical address and independent-initiative disclosure;
- working GitHub, contact, governance, security, privacy, and license links;
- updated date and truthful prototype/release state from controlled metadata;
- optional `Charlotte, North Carolina` location line;
- no uptime, node count, SLA, or invented activity indicator.

## Homepage build order

### 1. Hero

```text
DEWITT RESEARCH WORKSHOP
Engineering complex systems for open, inspectable intelligence.

I build agents, evidence pipelines, deterministic models, and the evaluations
that keep them honest. This is the public record of that work.

[Watch a recorded run] [Read TR-2026-001]
```

Place the approved mission, **Intelligence for Good. Intelligence for All.**, as
a secondary mission statement.

### 2. Recorded run

Show success and degraded recorded replays side by side or with an obvious
switch. Include artifact ID, recorded/prototype/fixture labels, last verification,
transcript, manifest, source, and the demo-HMAC limitation. Provide a static link
fallback if an embedded viewer fails.

### 3. TR-2026-001

Show title, date, prototype status, abstract opening, methods, limitations,
citation, code, and a clear route to the full reading experience.

### 4. Questions and negative result

List current research questions. Feature the Stage-B bake-off as **No winner**
and expose the six documented blocking reasons. Link the board and protocol.

### 5. Projects

Compact project index with one sentence, maturity, last verified date, strongest
artifact, and project page. Do not use a fictional control-center systems map.

### 6. Writing/methods

Link `TR-2026-001`, the integrated workflow lab, current notes, degraded replay,
and bake-off record.

### 7. Founder/contact

Identify Christopher Noxon DeWitt as an applied AI researcher in Charlotte.
Mention quantitative financial analysis as supporting background. Invite serious
academic and relevant professional inquiries without naming an employer or
recruiting collaborators.

## Project page template

1. Research question and intended user.
2. Current maturity and last verified date from controlled metadata.
3. Concrete workflow and interfaces.
4. Architecture and trust boundary.
5. Replay, read, run, or planned actions with explicit state.
6. Evaluation, failures, and limitations.
7. Source, license, local path, and upstream lineage.
8. Related writing and return path.

## Writing page template

- controlled title, author, status, version, and date;
- abstract and plain-language summary;
- methods and limitations;
- code/data/model/benchmark links;
- citation, license, reproduction, and correction history;
- related failure or negative result;
- integrated workflow lab under Methods/Teaching.

## Open Source page

Lead with what a visitor can run or inspect today: verified commands, packages,
applications, research artifacts, licenses, hardware assumptions, upstream
lineage, and open exceptions. Put contributor guidance and good-first issues
after the local-run and reproduction paths.

## CMS/content model

Preferred collections:

- `Systems`
- `ResearchArtifacts`
- `OpenArtifacts`
- `TeachingResources`
- `FailureRecords`
- `PeopleAndContributors`
- `Announcements`
- `ExternalLaunchTargets`

Every item records canonical ID, title, summary, maturity, publication status,
version, updated/verified date, source URL, canonical URL, license/classification,
tags, public eligibility, evidence reference, and live/replay/planned state.
Imports are idempotent and never elevate drafts automatically.

## Application and Velo boundary

- future app launches use first-class HTTPS subdomains and include `Return to
  Workshop`;
- Wix displays live/replay/planned state before an external launch;
- unavailable services fall back to documentation, transcript, or signed replay;
- no privileged token appears in Wix, browser code, or query parameters;
- custom code requires an owner, source, threat review, data classification,
  fallback, and removal path;
- no primary application depends exclusively on an iframe.

## Afternoon implementation sequence

1. Save a Wix revision and capture current desktop/mobile references.
2. Replace header/footer and remove fabricated metrics.
3. Rebuild the homepage in the seven-block order above.
4. Collapse navigation and add redirects without deleting project pages.
5. Build the full report and replay links, including static fallbacks.
6. Update Projects, Writing, Open Source, and About from `SITE_COPY.md`.
7. Verify every state label, date, link, disclosure, and planned-service label.
8. Test phone, tablet, laptop, keyboard, focus, zoom, reduced motion, and
   unavailable embeds.
9. Capture evidence and preserve rollback instructions.

## Acceptance evidence

- exported page and redirect map;
- desktop and mobile captures of the seven homepage blocks;
- working success/degraded replay and `TR-2026-001` links;
- capture of the no-winner board and six reasons;
- link checker and controlled-content reconciliation;
- keyboard, screen-reader, contrast, zoom, reduced-motion, and responsive notes;
- custom-code and data-collection inventory;
- domain, SEO, canonical, and fallback checklist;
- Wix revision/rollback reference and Director handoff.
