---
document_id: DRL-WEB-107
title: "DeWitt Research Workshop Web System Specification"
version: 4.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # DeWitt Research Workshop Web System Specification

    ## 1. Purpose and authority

    The DRL interactive web platform complements the canonical Wix institutional site at `https://www.dewitt-labs.com` and makes advanced laboratory experiences legible at multiple depths: a visitor understands the institution in under a minute; a collaborator finds an entry point; an engineer inspects architecture and evidence; a researcher reproduces work; and Atticus guides all of them without replacing ordinary navigation.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for DeWitt Research Workshop Web. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - Collaborators and open-source contributors.
- Students, teachers, academics, and independent learners.
- Applied AI hiring managers and technical reviewers.
- The Director publishing and operating the laboratory.
- Anonymous and authenticated public Atticus users.

    ## 3. V1 capabilities

    - Portable laboratory/application shell that shares identity with the Wix institutional site.
- Repository-backed documentation and advanced research workspaces under DRL subdomains.
- Project pages generated from controlled documents and signed evidence.
- Public Atticus console with tours, replays, and bounded live workflows.
- Research archive for papers, notebooks, datasets, models, benchmarks, and reports.
- Open-source portal for repositories, packages, releases, roadmaps, and contribution.
- System status and metrics from signed artifacts.
- Failure museum linked to regression tests.
- Global command palette and optional tmux-inspired workspace.
- Founder/researcher page and tasteful résumé context.
- Consent, privacy, history, account, device, and trace-donation controls.

    ## 4. Explicit non-goals

    - Generic résumé template or startup marketing funnel.
- Chat-only navigation.
- Fake terminal output or fabricated metrics.
- Autoplay sound, excessive scanlines, inaccessible motion, or government impersonation.
- Arbitrary public code or external-write execution.
- Hand-maintained duplicate project facts that drift from repository sources.
- Replacing the canonical Wix institutional site without an approved ADR.
- Making primary authenticated or computational applications iframe-only.

    ## 5. Logical architecture

    ```text
Next.js App Router
  |-- shared application chrome + controlled MDX renderer
  |-- Wix publishing payload/widget adapters
  |-- DRL design system + terminal/workspace components
  |-- Atticus console client and SSE event reducer
  |-- signed replay and artifact renderer
  |-- project/research/open-source indexes
  |-- auth, consent, analytics, and account controls
  |-- server/BFF for safe API mediation
       -> Atticus and specialist APIs
       -> signed reports / status / releases
```

    ## 6. Canonical workflows

    ### Explore normally
Visitors use navigation, search, project cards, or command palette. Core content and contribution paths work without an active model.

### Ask Atticus
The console creates a bounded session; plan, policy, tool, evidence, artifact, and evaluation events render in accessible panes; the final result links to canonical documents.

### Guided tour
A visitor selects a persona or subject; the tour advances through real pages and signed traces, remains shareable, and can be resumed.

### Publish
Merged controlled documents and signed release artifacts trigger validation of frontmatter, links, claims, evidence, accessibility, and routes before deployment.

    ## 7. Interfaces and integration

    - Controlled content manifest and document metadata.
- Public Atticus session, task, run, event, trace, and approval APIs.
- Signed replay, report, status, metric, model, dataset, and release schemas.
- Authentication, consent, analytics, and account services.
- No browser-side credentials to private backends.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - Core content and navigation work without Atticus or client enhancement.
- Metrics identify artifact, source, and date.
- Live, replayed, cached, and illustrative states are distinct.
- Cream-on-black design meets contrast and user preferences.
- No public visitor reaches private/local tools.
- Consent precedes optional analytics or content capture.
- Every public research claim links to methods, evidence, and limitations.
- Production builds exclude secrets and private drafts.

    ## 9. Quality attributes

    - **Correctness:** typed inputs and verifiable artifacts, not ungrounded prose.
    - **Traceability:** operational steps can be reconstructed without storing hidden chain-of-thought.
    - **Security:** least privilege, deny by default, bounded egress, and approval for consequential actions.
    - **Privacy:** collection minimization and separation of public, DRL-private, and local-personal data.
    - **Reliability:** deadlines, cancellation, retry budgets, idempotency, and truthful degraded states.
    - **Accessibility:** public workflows support keyboard, screen readers, reduced motion, contrast, and mobile use.
    - **Portability:** Docker/open fixtures for baseline; Google Cloud is reference production, not a mandatory local dependency.
    - **Evaluability:** every headline claim maps to a versioned suite and release gate.

    ## 10. Milestones

    - M1 design tokens, components, content renderer, and validation.
- M2 homepage, project template, research and open-source indexes.
- M3 signed replay, architecture visualizations, and status console.
- M4 public Atticus console, authentication, consent, and quotas.
- M5 failure museum, guided tours, founder and résumé.
- M6 accessibility, performance, security, SEO, content, and coordinated launch.

    ## 11. V1 acceptance

    - All required pages and controlled content pass build validation.
- WCAG-aligned automated and manual keyboard, screen-reader, contrast, and reduced-motion review passes.
- Performance budgets pass on representative mobile and desktop.
- Atticus replay and bounded live integrated demo succeed.
- All public metrics resolve to valid signed artifacts.
- Consent, analytics, auth, session isolation, and abuse controls pass.
- Preview, production, domain, TLS, and rollback are tested.

    ## 12. Principal risks and controls

    - Style overwhelms usability: strict component/motion budgets and user testing.
- Content drift: generated indexes and source-of-truth links.
- Demo failure or cost: signed replays and truthful cold-state UX.
- Accessibility regression: CI plus manual release audit.
- Institutional overstatement: transparent independent-initiative and founder language.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.

## Open-source identity requirements

- Open models, open-source software, public evaluation, local operation, and reproducible research must be visible without opening a footer or README.
- Every project page identifies upstream models/software, artifact licenses, maturity, local/self-hosted path, evaluation evidence, and contribution entry points.
- The public Atticus interface exposes the active model identity, version, routing mode, and whether output is live, replayed, cached, or illustrative.
- A dedicated Open Source portal presents Atticus model releases, datasets, packages, benchmarks, upstream contributions, self-hosting profiles, open exceptions, and independent replications.
- A `REPRODUCE` action is generated from tested release metadata rather than hand-authored marketing commands.
- The website credits upstream projects through a useful dependency graph, not a logo wall or implied endorsement.


## 14. Wix and domain integration

- `www.dewitt-labs.com` is the canonical institute and editorial origin.
- This project supplies open-source application shells, docs, advanced workspaces, release/status data, and bounded widgets to Wix.
- Deployments use approved DRL subdomains and include visible return navigation.
- Authentication and authorization are application responsibilities; Wix membership does not implicitly grant privileged access.
- Cross-host links, canonical metadata, consent, CORS/CSP, cookie scope, and unavailable-service fallbacks are testable release requirements.
- See `../../../docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md`.
