---
document_id: DRL-WEB-001
title: "Workshop Website Product and Design Specification"
version: 4.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Workshop Website Product and Design Specification

## Canonical site and role

The canonical public site is **`https://www.dewitt-labs.com`**, hosted on Wix
for V1. It is an evidence-first academic portfolio, public workshop, and
research record for Christopher Noxon DeWitt. It is not a startup funnel, a
staffed institute, or a claim that every specified system is deployed.

Repository-backed documents, replay viewers, and future interactive
applications may use first-class subdomains. Wix remains the editorial front
door; application identity, security, consent, and service availability remain
separate contracts. See
[`DOMAIN_AND_WIX_INTEGRATION.md`](DOMAIN_AND_WIX_INTEGRATION.md).

## Product outcome

Within one minute, a research peer, prospective mentor or PhD adviser, grant
reviewer, or research-oriented employer can answer:

1. What does the Director investigate?
2. What has he actually built?
3. What evidence can I inspect now?
4. What failed or remains unresolved?
5. How do I read more or contact him?

The shortest answer to the first question is:

> **Engineering complex systems for open, inspectable intelligence.**

## Experience principles

- evidence before capability claims;
- a recorded run and a technical report before a project catalog;
- methods, limitations, degraded behavior, and negative results stay visible;
- the workshop is understandable without chat, sign-in, or a warm backend;
- first-person, understated academic voice with no invented staff;
- traditional navigation and readable documents before terminal effects;
- keyboard, screen-reader, reduced-motion, and mobile use are designed modes;
- every live, replayed, cached, illustrative, and planned state is distinct.

## Creative direction

One researcher's workshop rendered as a modern financial research workstation
and scholar's study on a restored computing bench. The atmosphere references
`tmux`, academic working papers, UNIX terminals, archival technical reports,
and quantitative analysis without becoming costume.

The palette is warm cream on near-black. Amber, muted red, and phosphor green
are functional accents for links, state, focus, and project family. Mono type is
for metadata, commands, and data; readable serif or sans type carries long-form
research prose. No fake uptime, node count, seal, classification, or operations
center chrome is permitted.

## Audience hierarchy

1. Academic evaluator: research peer, mentor, PhD adviser, or grant reviewer.
2. Research-oriented employer or technical leader.
3. Curious developer, tinkerer, learner, or teacher.
4. Future contributor.

The public posture is read-mostly. The site may welcome mentorship, academic
conversation, PhD opportunities, grants, and relevant work. Contributor routes
live under Open Source and do not control the homepage.

## Top-level Wix routes

```text
/             Home        thesis and strongest evidence
/projects     Projects    five connected research artifacts
/writing      Writing     reports, notes, methods, teaching, failures
/open-source  Open Source code, licenses, lineage, local operation
/about        About       person, interests, background, contact
```

Existing project paths may remain. Empty department-shaped pages are redirected
into this tree until real content justifies a separate destination.

## Homepage sequence

1. **Research thesis:** workshop name, thesis, mission, and first-person
   orientation.
2. **Watch a recorded run:** success and degraded replays with state, signature,
   artifact identity, and a plain fallback link.
3. **Read TR-2026-001:** abstract, methods, limitations, citation, and source.
4. **Current questions and negative results:** the Stage-B bake-off declares no
   winner and states the six blocking reasons.
5. **Projects:** compact index with maturity and last verification.
6. **Writing and methods:** technical notes, integrated workflow lab, and the
   current failure record.
7. **About/contact:** concise founder context and serious inquiry route.

The first two actions are exactly **Watch a recorded run** and **Read
TR-2026-001**, in that order.

## Evidence surfaces

### Recorded-run viewer

- exposes signed success and degraded fixture replays;
- labels output as recorded, prototype, and fixture-backed;
- identifies the demo HMAC key as structural rather than production trust;
- shows task, policy, tools, sources, calculations, evaluation, and result;
- works by keyboard and with a noninteractive transcript fallback.

### Technical report

`TR-2026-001` receives a full reading surface: controlled title, author, status,
version, date, abstract, plain-language summary, methods, limitations, code and
artifact links, citation, license, and correction history.

### Negative results

The degraded replay and Stage-B bake-off no-winner result are not buried in a
failure museum. They appear as first-class evidence with the question tested,
failure or exclusion reason, consequence, and next experiment.

## Project pages

Each project page contains:

1. research question and intended user;
2. current maturity and last verified date;
3. concrete workflow and interfaces;
4. architecture and trust boundary;
5. available replay, read, run, or planned actions;
6. methods, evidence, limitations, and failures;
7. open artifacts, licenses, upstream lineage, and local path;
8. related writing and a route back to the workshop.

Atticus is a documented research artifact. `atticus.dewitt-labs.com` is a
planned application target, not a live-service claim. No `Launch Atticus`
action appears until separate deployment and safety acceptance evidence exists.

## About page

The profile identifies Christopher Noxon DeWitt as an applied AI researcher in
Charlotte who engineers complex systems. Quantitative financial analysis is
supporting background. The page names research interests and welcomes serious
academic, mentorship, PhD, grant, and relevant employment inquiries without
naming an employer or soliciting a team.

## Cross-host product architecture

- Wix owns the five-page editorial tree and evidence launch links.
- `apps/lab-web` can supply self-hostable replay and research-document viewers.
- Future application subdomains expose a visible return path to the workshop.
- Primary applications never depend solely on a Wix iframe.
- Cross-host canonical metadata, state labels, consent, CORS/CSP, cookie scope,
  analytics, and unavailable-service fallbacks are validated before launch.

## Quality and acceptance

- the thesis and primary actions are visible without scrolling on representative
  laptop and phone layouts;
- the site remains complete when scripts or application backends are absent;
- all claims resolve to a dated artifact, method, or clearly labeled plan;
- keyboard order, focus, headings, landmarks, contrast, zoom, screen-reader
  names, reduced motion, and responsive layouts pass review;
- empty, loading, error, replay, planned, and unavailable states are explicit;
- no credentials, private analytics capture, employer material, or fabricated
  metrics enter Wix or browser code.
