---
document_id: DRL-WEB-019
title: "Wix Site Build Plan and Page Blueprint"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-03
---

# Wix Site Build Plan and Page Blueprint

## Objective

Build `www.dewitt-labs.com` into the credible public home of DeWitt Research Workshop: one person's applied AI workshop, rendered as a research workstation and scholar's study on a restored 1980s computing bench, without sacrificing clarity, accessibility, or truthfulness.

The site introduces the workshop. Atticus guides visitors after the workshop is understood. The site sells no fictional institutional history and never implies government, university, accreditation, staff, or production maturity that does not exist.

## Wix page tree

Five pages. The tree is deliberately shallow: a section only exists when there is
real content behind it, because an empty section overstates the work exactly as a
fabricated metric does.

```text
Home            /            the bench — what is being worked on now
Projects        /projects    the five projects, each with honest maturity
Writing         /writing     technical reports, notes, and what broke
Open Source     /open-source packages, services, and how to run them
About           /about       the person, contact, disclosure
```

### Why this shape

An eight-section tree implies eight departments. One person's workshop has work,
not departments, so the navigation is organised around artifacts that exist:

- **Teaching** is retired until a real guide exists. Reinstate it as `/teaching`
  the day there is one.
- **Status** is retired. A workshop has no operations centre; that page created a
  dashboard-shaped vacuum that a fabricated uptime figure filled. Per-project state
  belongs on project cards, sourced from the `Systems` collection.
- **Failure Museum** folds into `/writing` as "what broke". A museum is a building;
  a workshop has a shelf of things that did not work. This is the most honest
  surface available and should not be hidden behind its own wing.
- **Laboratory** and **Systems** merge into `/projects`. The thesis that lived on
  the Laboratory page belongs on the homepage, in plain language.

### Redirects

Retired paths must redirect permanently so existing links and search results survive:

```text
/laboratory      -> /projects
/systems         -> /projects
/research        -> /writing
/failure-museum  -> /writing#what-broke
/teaching        -> /writing        (until reinstated)
/status          -> /projects
/atticus, /atlas, /fed-lens, /balance-lab-ai, /eval-forge  -> retained
```

Individual project pages keep their existing paths. Sections may deepen later, but
only behind real content.

## As-built state (verified 2026-08-03)

The site is live. This section records what shipped against the blueprint above; the
blueprint remains the target, and every deferred item below is open work, not a
silently accepted change.

Shipped and verified:

- 14 pages covering all eight top-level sections plus a page per specialist system:
  `/`, `/laboratory`, `/systems`, `/research`, `/open-source`, `/teaching`,
  `/failure-museum`, `/about`, `/status`, `/atticus`, `/atlas`, `/fed-lens`,
  `/balance-lab-ai`, `/eval-forge`.
- Near-black canvas `#0D0F0E`; IBM Plex Sans for body and JetBrains Mono for metadata.
- Apex `dewitt-labs.com` redirects permanently to the canonical `www` origin.
- Independent-initiative disclosure on every page.
- Footer terminal line `Node: Charlotte / Status: Prototype`, no invented classification.
- Wix CMS installed with all eight collections created; `Systems` populated with five
  items, each carrying `maturity: prototype` and a verified date.

Deferred or open:

- Page content is authored statically and does not yet bind to the CMS, so maturity
  labels shown to visitors are not read from the `Systems` collection.
- Seven collections (`ResearchArtifacts`, `OpenArtifacts`, `TeachingResources`,
  `FailureRecords`, `PeopleAndContributors`, `Announcements`, `ExternalLaunchTargets`)
  exist but hold no items, so the research, open-source, and failure surfaces are not
  yet evidence-backed.
- `atticus.dewitt-labs.com`, `docs.`, and `status.` do not resolve; launch actions
  currently route to Wix pages and do not display live/replay/planned state.
- Governance, Security, Privacy, License, Documentation, and Model Hub appear in the
  footer as text without links.
- The footer carries `NODE: 01 // UPTIME: 99.9%`. No uptime monitoring produces this
  figure, so it is a fabricated live metric — a prohibited motif under `BRAND_SYSTEM.md`.
  It must be removed or replaced with a measured value and its source.
- The site foreground is the amber accent `#D4B34F` rather than the warm cream the visual
  system specifies. `BRAND_SYSTEM.md` reserves the accent for state, selection, links, and
  system family; using it as general body colour needs either a site correction or an
  explicit Director amendment to the visual system.
- Sub-pages under Laboratory, Research, Open Source, Teaching, and About are combined
  into their section pages, as this section permits.

## Global shell

### Header

- compact wordmark;
- primary links: Projects, Writing, Open Source, About;
- utility actions: search only. No launch or status action while no
  application subdomain resolves;
- keyboard-visible focus and mobile menu;
- no oversized sticky header that consumes the workstation viewport.

### Footer

- canonical address and independent-initiative disclosure;
- GitHub, documentation, contact, governance, security, privacy, license —
  every one a working link, never plain text;
- active public release and updated date from controlled metadata;
- small terminal-style line such as `Node: Charlotte / Status: Prototype`,
  carrying only evidence-backed state. No uptime, availability, or SLA figure
  may appear unless a monitor produces it and its source is linked.

### Visual system

- near-black background and warm cream foreground;
- high-contrast functional accent only for state, selection, links, and system family;
- thin borders, data labels, tabs, evidence stamps, and research-paper metadata;
- mono font for commands, identifiers, data, and code—not long body copy;
- restrained scanline, grid, signal, or blinking effects; reduced-motion mode removes nonessential motion;
- meaningful use of asymmetry and panes rather than a generic centered startup template.

## Homepage composition

Five blocks, not nine. The homepage is a workbench, not a lobby: a visitor should
know within ten seconds that this is one person doing applied AI in the open, and
should be able to see what is on the bench this month.

### 1. Hero: what this is

Required text hierarchy:

```text
DEWITT RESEARCH WORKSHOP
Independent research in open and applied intelligence.

Intelligence for Good. Intelligence for All.
```

One line of plain first-person orientation beneath it, naming the person and the
work. Primary actions, in this order:

- See what I'm building
- Read the current work
- Browse the code

No "Launch Atticus" in the hero while Atticus has no launchable target. A button
must not promise an action the site cannot perform.

The hero may show a low-motion bench, terminal cursor, or project list. It must
load without an external application and stay useful when JavaScript or model
services fail.

### 2. On the bench

The distinguishing block. What is being worked on right now, in first person,
with a real date — not a status board. Two or three items maximum, each naming
the thing and its current state honestly, including what is unfinished.

This replaces both the institutional thesis and the "current transmission"
framing. `Last touched 3 Aug` is a workshop; `STATUS: OPERATIONAL` is an institute.

### 3. Featured work

Exactly one substantive artifact, presented properly rather than as a teaser card:
a technical report, a release, a benchmark, or a replay. It links to the full
reading experience on `/writing` and shows enough — title, abstract opening,
date, maturity — to be worth the space. Do not inflate an ordinary update into a
result.

### 4. Projects

The five projects as a compact list, each with its name, one honest sentence, and
its current maturity read from the `Systems` collection. Atticus is identified as
the guide and operator, not as the workshop itself. Every entry routes to its
project page.

No systems map with orchestration centre framing, and no capability tiles
asserting completeness.

### 5. Open source and contact

Where the code actually is, what can be installed and run today, and how to reach
the workshop. Links point at real repositories, packages, and services, or at a
truthful planned-state page. Ends with the independent-initiative disclosure.

## Project page template

Every project page contains:

1. What it does and who it is for, in plain language.
2. Current maturity and last verified date, from the `Systems` collection.
3. The signature workflow, described concretely.
4. Architecture and trust boundary.
5. Run, replay, or documentation controls — labelled live, replay, or planned.
6. Open-source artifacts and upstream lineage.
7. Evaluation results and honest limitations, including what does not work.
8. Contribution tasks.
9. Related writing.
10. Return path to the workshop and related projects.

Sections 2 and 7 are mandatory. A project page without a maturity label and a
limitations section is not publishable.

## Writing page template

Applies to technical reports and notes on `/writing`.

- controlled title, author, status, version, and date;
- abstract and plain-language summary;
- methods and limitations;
- code/data/model/benchmark links;
- citation and license;
- reproduce action;
- correction history;
- related failures or negative results.

The "what broke" shelf lives on the same page. Each entry records the failure, how
it was detected, what corrected it, and the regression test that keeps it fixed.
Do not invent an incident for visual drama, and do not hide a real one.

Wix may present the editorial page while canonical technical artifacts live in repository-backed documentation or external release hosts.

## Open Source page

The Open Source area is a primary institutional surface, not a footer link. It must present:

- Atticus Open Model Commons;
- installable DRL packages and applications;
- datasets and benchmarks;
- self-hosting profiles;
- Open Stack upstream dependency graph;
- contributor credit;
- good-first issues and research tasks;
- open exceptions and actual license classifications;
- sustainability and commercial-service boundaries.

## CMS/content collections

Where Wix CMS or collections are used, proposed collections are:

- `Systems`
- `ResearchArtifacts`
- `OpenArtifacts`
- `TeachingResources`
- `FailureRecords`
- `PeopleAndContributors`
- `Announcements`
- `ExternalLaunchTargets`

Each item records canonical ID, title, summary, maturity/status, source URL, canonical URL, release/version, updated date, license/classification, tags, public eligibility, and evidence reference. Automated import must be idempotent and may not elevate draft status.

## External application launch behavior

- launch actions open first-class HTTPS subdomains;
- same-tab is preferred for ordinary navigation; new-tab use is disclosed and reserved for external repositories or model hubs;
- external app chrome includes `Return to Workshop`;
- Wix shows live/replay/planned state before launch;
- service unavailability routes to documentation or signed replay rather than a dead screen;
- no privileged token appears in query parameters;
- cross-host referral data is minimized.

## Wix custom-code and Velo boundary

Custom code is permitted only when it has a named owner, source repository or documented snippet, threat review, data classification, fallback, and removal path. It may support:

- public release/status feed;
- artifact cards;
- bounded architecture or replay widget;
- repository publishing integration;
- validated forms or webhook/API bridge;
- privacy-respecting analytics and consent logic.

Do not put cloud credentials, service-account keys, model-provider keys, or privileged API tokens in browser or Wix code.

## Responsive and accessibility acceptance

The Wix build is tested at representative phone, tablet, laptop, and large desktop widths. Required checks include:

- keyboard order and visible focus;
- semantic headings and landmark regions;
- alt text and captions;
- contrast and zoom;
- reduced motion;
- readable line length;
- mobile embeds and fallback links;
- forms, errors, and success states;
- screen-reader announcement of system status and external launch.

## Content required before initial publication

- mission and research thesis;
- one-paragraph explanation of each system;
- truthful maturity labels;
- Open Research Charter summary;
- founder/director profile;
- contact/collaboration path;
- privacy, analytics, security-reporting, and independent-initiative disclosure;
- repository and documentation links;
- at least one real research or engineering artifact;
- launch roadmap that distinguishes available from planned systems.

## Deliverables for the Wix-building agent

- exported site/page map;
- design-token translation guide;
- component inventory;
- page copy and asset register;
- CMS/collection schema if used;
- link and redirect register;
- custom-code inventory;
- domain and SEO checklist;
- accessibility report;
- mobile screenshots;
- launch and rollback instructions;
- handoff recording describing how the Director can update content safely.
