---
document_id: DRL-WEB-018
title: "Canonical Domain, Wix Institutional Site, and Application Integration"
version: 1.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-02
---

# Canonical Domain, Wix Institutional Site, and Application Integration

## Recorded assets and binding decision

The Director has registered **`dewitt-labs.com`** and has acquired a Wix site. The canonical public laboratory address is:

```text
https://www.dewitt-labs.com
```

**Status (2026-08-02):** the Wix site is live at the canonical address. Earlier documentation used the misspelling `dwit-labs.com`; that spelling is retired and must not appear in DNS, links, metadata, or copy (see `DIRECTORS_MEMO.md` RES-011).

This is existing DRL infrastructure, not a placeholder. The Wix site is the canonical institutional front door for V1: laboratory identity, public mission, research publishing, project discovery, teaching, collaboration, founder profile, news, and clear launch points into Atticus and the specialist applications.

The apex domain `https://dewitt-labs.com` shall redirect permanently to the canonical `www` origin unless a later approved ADR selects the apex as canonical. All public documents, model cards, package metadata, social profiles, repository descriptions, and release manifests shall use the canonical address and avoid competing primary URLs.

## Architectural principle

Wix is the **institutional publishing and discovery layer**. It is not required to become the execution environment for every DRL service.

Serious interactive systems remain independently deployable, open-source applications and services. They are linked through DRL-controlled subdomains and a shared design, navigation, authentication, consent, telemetry, and provenance contract.

```text
www.dewitt-labs.com          Wix institutional site and editorial front door
atticus.dewitt-labs.com      public Atticus laboratory console
atlas.dewitt-labs.com        Atlas research experience
fedlens.dewitt-labs.com      FedLens policy archive and analysis
balancelab.dewitt-labs.com   BalanceLab AI scenario workstation
evalforge.dewitt-labs.com    EvalForge reports and comparison lab
docs.dewitt-labs.com         versioned technical documentation
status.dewitt-labs.com       public operational and release status
api.dewitt-labs.com          public API gateway where justified
```

Subdomains are planned namespaces, not claims that each service is already deployed. An implementation PR may consolidate frontends while retaining these stable names. Any renaming, removal, or ownership transfer of a canonical public hostname requires an ADR and redirect plan.

## Why DRL uses a split-site architecture

The split preserves four goals simultaneously:

1. **Use the purchased Wix platform immediately.** DRL can publish a polished laboratory identity, research pages, teaching material, calls for collaborators, and updates before every application is finished.
2. **Keep the computational systems real.** Atticus, Atlas, FedLens, BalanceLab, and EvalForge can use the frameworks, deployment targets, streaming interfaces, GPU runtimes, and security controls their work requires.
3. **Preserve open-source forkability.** The monorepo remains the authoritative source for application code, documentation, schemas, training materials, and reproducible demonstrations. A contributor does not need Wix to run the laboratory locally.
4. **Avoid brittle primary-app embedding.** Small widgets may be embedded, but core experiences should open as first-class applications under DRL subdomains rather than operate as deeply nested iframe products.

Wix supports connecting an existing domain, custom elements, embedded URLs, Velo site APIs, and headless projects. Those capabilities are useful integration surfaces, but each adds security, accessibility, performance, and maintenance implications. Primary application flows therefore use direct subdomain navigation by default. Embeds are reserved for bounded previews, status panels, diagrams, replay viewers, or other interactions that remain useful if the embed is unavailable.

## Wix responsibilities

The Wix site owns the following public surfaces for V1:

- canonical homepage and laboratory mission;
- institute-first brand system and navigation;
- high-level system pages and launch links;
- research abstracts, essays, announcements, and teaching index;
- founder/director profile and résumé entry point;
- collaboration, contribution, sponsorship, and contact pages;
- open-source overview and links into evidence-rich artifact pages;
- mailing-list, event, or membership features if deliberately enabled;
- SEO metadata, social cards, canonical URLs, and public redirects;
- prominent truthful status labels for systems that are specified, prototyped, live, replay-only, or unavailable.

Wix content must not become the sole authoritative copy of architecture, security, model, dataset, benchmark, or release documentation. Controlled repository documents remain the technical source of truth.

## Monorepo and application responsibilities

The monorepo owns:

- Atticus and specialist application source code;
- shared cream-on-black tokens and reusable UI specifications;
- versioned public documentation and research artifacts;
- release manifests, model cards, dataset cards, benchmark reports, and checksums;
- public API and protocol contracts;
- demonstration replays and evidence manifests;
- machine-readable system status and maturity metadata;
- generated Wix publishing payloads or content exports where implemented;
- tests that verify Wix links, canonical URLs, subdomain routing, consent, and cross-origin policy.

`apps/lab-web` becomes the open-source **DRL interactive web platform**, not a duplicate marketing homepage. It provides shared application shells, documentation rendering, advanced research workspaces, trace viewers, and a portable reference frontend that can be deployed under DRL subdomains or self-hosted by contributors.

## Content synchronization model

DRL uses a dual-surface, single-authority approach:

### Repository-authoritative material

The following begins in Git and is published or summarized into Wix:

- controlled specifications;
- research papers and technical reports;
- release notes;
- model, dataset, and benchmark cards;
- open-source artifact metadata;
- project maturity and status;
- reproducibility instructions;
- failure records and corrections.

### Wix-authored editorial material

The following may begin in Wix and be archived or indexed in the repository when material:

- concise homepage copy;
- announcements and event pages;
- visually composed feature stories;
- collaborator spotlights;
- newsletter landing pages;
- lightweight educational introductions.

No automated synchronization may publish a controlled document as `PUBLIC RELEASE` merely because a Wix page exists. Publication authority remains governed by document status and release gates.

## Navigation and visual continuity

Wix and external DRL applications must appear to belong to one laboratory without pretending to be one runtime.

Required continuity:

- `DeWitt Research Laboratory` wordmark and canonical mission language;
- cream-on-black base palette;
- shared typography and spacing guidance;
- consistent system names and maturity labels;
- persistent `Return to Laboratory` link from every external application;
- consistent links for Research, Open Source, Systems, Teaching, About, and Status;
- visible hostname changes for security-sensitive actions;
- no deceptive recreation of Wix browser chrome or authentication UI.

External apps may be denser and more workstation-like than the Wix editorial site. Consistency comes from tokens and language, not forced pixel identity.

## Embeds and custom elements

### Allowed uses

- system-status badge or compact status panel;
- non-sensitive architecture animation;
- artifact or model-release card;
- replay viewer with no privileged credentials;
- newsletter or contribution widget;
- bounded Atticus teaser that routes to the full console;
- charts backed by public, cacheable data.

### Prohibited uses for V1

- the complete authenticated Atticus console;
- private file, voice, shell, email, or calendar interactions;
- unrestricted model input;
- payment or secret-bearing flows implemented in arbitrary embed code;
- primary BalanceLab analysis with user uploads;
- administration or deployment controls;
- any experience whose accessibility or mobile behavior depends on an untested iframe.

Every embed must define fallback content, CSP and origin policy, height/responsive behavior, keyboard behavior, loading/error state, analytics behavior, and data classification.

## Domain and DNS operating model

The implementation agent must inventory the registrar, current DNS host, Wix connection mode, and existing records before making changes. Wix supports connection through nameservers or pointing; the correct method depends on who should own DNS operations and how many non-Wix subdomains DRL needs.

DRL requirements:

- preserve registrar ownership and renewal access under Director-controlled credentials;
- enable registrar lock and multi-factor authentication where available;
- avoid deleting unrelated mail, verification, or service records;
- document all A, AAAA, CNAME, TXT, MX, CAA, and redirect records;
- use least-privilege access for anyone changing DNS;
- issue TLS certificates for every public hostname;
- prohibit wildcard DNS unless its necessity and routing controls are approved;
- stage changes with rollback records and propagation checks;
- monitor certificate expiration and DNS resolution;
- publish no secret values in screenshots, tickets, or repository files.

If Wix hosts authoritative DNS, the infrastructure documentation must still represent required application records and ownership. If an external DNS host remains authoritative, Wix records and cloud subdomain records must be managed through one reviewed change plan.

## Authentication and session strategy

V1 deliberately separates the Wix public/member experience from privileged DRL application sessions unless a tested identity integration is approved.

- Anonymous visitors may browse Wix and use limited public demos.
- Authenticated Atticus and specialist sessions use the approved DRL application identity provider and security model.
- Wix Members may support editorial/community features, but Wix membership does not automatically grant access to privileged DRL tools.
- Cross-platform single sign-on is a later ADR gate requiring threat modeling, account-linking rules, logout behavior, token audience separation, and recovery testing.

This avoids treating visual continuity as authorization continuity.

## Analytics, consent, and privacy

Wix and external applications share one public privacy narrative and event taxonomy while retaining separate technical collectors where required.

- Consent categories and plain-language disclosures must agree across hosts.
- Tracking must not silently expand when a visitor moves from Wix to an application subdomain.
- A consent state must be propagated only through an approved privacy-preserving mechanism; query-string consent tokens are prohibited.
- Public Atticus content donation remains explicit opt-in and separate from ordinary product analytics.
- Operational telemetry must redact prompts, private document content, credentials, and user secrets by default.
- Analytics dashboards must distinguish Wix page traffic, application usage, model/tool operations, and research donation.

## SEO, discovery, and canonical content

- `www.dewitt-labs.com` is the canonical institutional origin.
- Wix pages use canonical tags and stable human-readable paths.
- External application pages use their own canonical subdomain URLs.
- Duplicate technical content is either summarized on Wix with a canonical link to docs or generated from the repository with explicit canonical ownership.
- Sitemap and robots policies must exclude private, staging, preview, trace-secret, and administrative routes.
- Structured metadata may identify DRL as an independent research initiative; it must not imply accreditation, university affiliation, government status, or staff scale that does not exist.

## Availability and graceful degradation

The Wix site must remain useful when model services are cold, rate-limited, or unavailable. It shall always provide:

- the laboratory mission;
- research and system documentation;
- current maturity/status labels;
- replay demonstrations;
- contact and contribution routes;
- incident or maintenance notices.

A model outage must not make the laboratory website disappear.

## Implementation phases

### Phase A — Domain and institutional launch

1. Connect `www.dewitt-labs.com` to the Wix site.
2. Establish apex redirect and HTTPS.
3. Implement brand shell, laboratory mission, systems overview, open-source overview, research index, About, Contact, and Status link.
4. Publish only truthful project maturity labels.
5. Add temporary launch links to repository documentation and replay assets.

### Phase B — Application subdomains

1. Reserve and document subdomain records.
2. Deploy the Atticus public console and shared application shell.
3. Deploy or route specialist experiences.
4. Add consistent return navigation, consent language, status identity, and release metadata.
5. Exercise cross-origin, redirect, cookie, CORS, and CSP tests.

### Phase C — Controlled integration

1. Add bounded custom elements or status/replay widgets where they improve the Wix experience.
2. Add repository-to-Wix publishing automation only after preview, rollback, and public-status checks exist.
3. Evaluate Wix Headless or member integration through an ADR if it materially improves the platform.
4. Publish a domain and web-architecture operations report.

## Acceptance evidence

V1 domain and Wix integration is complete only when:

- `www.dewitt-labs.com` resolves over HTTPS to the approved Wix site;
- the apex redirects to the canonical origin;
- every published DRL application has an approved hostname and TLS;
- no core application relies on an iframe as its sole public surface;
- navigation and design continuity pass desktop/mobile review;
- application links and return links pass automated checks;
- canonical tags, sitemap, robots, and social metadata are reviewed;
- consent and privacy disclosures remain coherent across hosts;
- DNS inventory, change procedure, rollback, and ownership are documented;
- staging and preview origins are not indexed;
- the website truthfully distinguishes live, replayed, cached, simulated, and planned systems;
- a clean-room visitor can enter at Wix, understand DRL, launch Atticus, inspect evidence, and return without confusion.

## Authoritative Wix references

Implementation agents must revalidate Wix behavior before changes. Foundation references are recorded in `docs/references/TECHNICAL_REFERENCE_REGISTER.md`, including Wix domain connection, Wix custom elements and embeds, Velo custom site APIs, and Wix Headless capabilities.
