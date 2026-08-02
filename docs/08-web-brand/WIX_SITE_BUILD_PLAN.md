---
document_id: DRL-WEB-019
title: "Wix Institutional Site Build Plan and Page Blueprint"
version: 1.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Wix Institutional Site Build Plan and Page Blueprint

## Objective

Build `www.dewitt-labs.com` into the credible public home of DeWitt Research Laboratory: an independent open research initiative that feels like a financial research workstation, academic institute, and restored 1980s computing laboratory without sacrificing clarity, accessibility, or truthfulness.

The Wix site introduces DRL. Atticus guides visitors after the laboratory is understood. The site sells no fictional institutional history and never implies government, university, accreditation, staff, or production maturity that does not exist.

## Wix page tree

```text
Home
Laboratory
  Mission and research thesis
  Systems map
  Methods and principles
Systems
  Atticus
  Atlas
  FedLens
  BalanceLab AI
  EvalForge
Research
  Working papers
  Experiments and notebooks
  Model and dataset releases
  Replications and negative results
Open Source
  Software
  Models
  Datasets
  Benchmarks
  Open Stack
  Contribute
Teaching
  Guides and courses
  Workshops and lectures
  Student/tinkerer pathways
Failure Museum
About
  Christopher Noxon DeWitt / Founder and Director
  Governance
  Contact and collaborate
Status / Launch
  Launch Atticus
  System status
  Documentation
```

The initial Wix release may combine shallow sections, but it must retain stable paths or redirects so pages can expand without link breakage.

## Global shell

### Header

- compact DRL wordmark;
- primary links: Laboratory, Systems, Research, Open Source, Teaching, About;
- utility actions: `Launch Atticus`, search, system status;
- keyboard-visible focus and mobile menu;
- no oversized sticky header that consumes the workstation viewport.

### Footer

- canonical address and independent-initiative disclosure;
- GitHub, model hub, documentation, contact, governance, security, privacy, license, status;
- active public release and updated date from controlled metadata;
- small terminal-style line such as `NODE: CHARLOTTE / STATUS: <evidence>` without fake classified markings.

### Visual system

- near-black background and warm cream foreground;
- high-contrast functional accent only for state, selection, links, and system family;
- thin borders, data labels, tabs, evidence stamps, and research-paper metadata;
- mono font for commands, identifiers, data, and code—not long body copy;
- restrained scanline, grid, signal, or blinking effects; reduced-motion mode removes nonessential motion;
- meaningful use of asymmetry and panes rather than a generic centered startup template.

## Homepage composition

### 1. Hero: the institute exists

Required text hierarchy:

```text
DEWITT RESEARCH LABORATORY
Independent research in open and applied intelligence.

AI for Good. AI for all.
Intelligence of the people and for the people.
```

Primary actions:

- Enter the Laboratory
- Explore Open Source
- Launch Atticus

The hero may show a low-motion systems map, terminal cursor, or research telemetry. It must load without an external application and retain useful content when JavaScript or model services fail.

### 2. Laboratory thesis

Explain in plain language:

- Atticus is the open-weight guide and operator;
- specialist systems own research, policy analysis, deterministic modeling, and evaluation;
- open models and open software are institutional commitments;
- safety, traceability, evaluation, and human agency matter as much as capability.

### 3. Systems map

Show Atticus at the orchestration center with Atlas, FedLens, BalanceLab, and EvalForge as specialist systems. Each node displays current maturity from controlled metadata and routes to a system page.

### 4. Current transmission

Feature exactly one substantive current item: model release, benchmark report, working paper, integrated replay, or call for collaborators. Include methods/evidence links and do not inflate ordinary updates into research breakthroughs.

### 5. Open by construction

Show five evidence-backed pillars:

- open-weight models;
- open-source software;
- public evaluation;
- local/self-hosted operation;
- reproducible research and teaching.

Every card links to an actual artifact or a truthful planned-state page.

### 6. Atticus invitation

Introduce Atticus as guide and copilot, not as the laboratory itself. Suggested actions:

- Take the laboratory tour
- Explain the architecture
- Replay the integrated workflow
- Find a contribution task

The full experience opens at `atticus.dewitt-labs.com` or an approved route. A Wix teaser must be bounded and contain a direct fallback link.

### 7. Research, teaching, and collaboration

Provide distinct entry points for:

- collaborators and maintainers;
- tinkerers and open-source developers;
- students and independent learners;
- teachers and academic researchers.

### 8. Failure museum preview

Show one real failure record with failure, detection, correction, and regression-test links. Do not invent an incident for visual drama.

### 9. Founder/director

A restrained introduction to Christopher Noxon DeWitt as founder, director, and Applied AI Researcher. Link to research interests, biography, résumé, GitHub, and contact. Finance/quantitative background supports the work but does not dominate the institutional homepage.

## System page template

Every system page contains:

1. Problem and public value.
2. Current maturity and last verified date.
3. Signature workflow.
4. Architecture and trust boundary.
5. Live/replay/documentation launch controls.
6. Open-source artifacts and upstream lineage.
7. Evaluation and limitations.
8. Contribution tasks.
9. Research and teaching references.
10. Return path to the laboratory and related systems.

## Research page template

- controlled title, authors, status, version, and date;
- abstract and plain-language summary;
- methods and limitations;
- code/data/model/benchmark links;
- citation and license;
- reproduce action;
- correction history;
- related failures or negative results.

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
- external app chrome includes `Return to Laboratory`;
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
