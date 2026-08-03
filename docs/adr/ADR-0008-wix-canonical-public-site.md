---
document_id: DRL-ADR-0008
title: "Use Wix at www.dewitt-labs.com as the Canonical Institutional Site"
version: 1.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-03
---

# ADR-0008: Use Wix at `www.dewitt-labs.com` as the canonical institutional site

## Context

The Director has registered `dewitt-labs.com` and acquired a Wix website. The previous foundation assumed Firebase App Hosting would deliver the entire laboratory website. DRL now has a real public domain and an available institutional publishing platform.

## Decision

`https://www.dewitt-labs.com` is the canonical public institutional origin, hosted on Wix for V1. The apex redirects to the canonical `www` origin.

Atticus and specialist computational experiences remain open-source applications deployed under DRL subdomains or linked routes. Wix is not required to host GPU inference, streaming traces, authenticated private tooling, deterministic scenario computation, or the complete application runtime.

Firebase/App Hosting and Google Cloud remain approved for interactive frontends, APIs, documentation, model serving, and specialist systems. `apps/lab-web` becomes the portable open-source interactive web platform and application shell rather than the only canonical institutional homepage.

## Consequences

- Wix and external applications need one design, navigation, consent, SEO, and status contract.
- DNS, TLS, redirect, CORS, CSP, cookie, and cross-origin decisions become explicit release work.
- Primary applications use first-class subdomains rather than iframe-only delivery.
- Controlled technical documentation remains repository-authoritative.
- Wix may author editorial content, events, collaboration pages, and public introductions.
- A future migration to Wix Headless, a fully custom Next.js institutional site, or unified membership requires another ADR and redirect plan.

## Implementation status (2026-08-03)

The decision is implemented. `https://www.dewitt-labs.com` is live on Wix with the apex
redirecting to the canonical `www` origin, and the institutional page tree is published.

Two consequences recorded above are not yet satisfied and remain open release work:

- *"Primary applications use first-class subdomains rather than iframe-only delivery."*
  No application subdomain resolves yet; `atticus.dewitt-labs.com` is unallocated and
  launch actions route to Wix pages. Nothing is delivered by iframe, so the decision is
  not violated, but the subdomain contract is unfulfilled.
- *"Wix and external applications need one design, navigation, consent, SEO, and status
  contract."* The consent and status contracts are not published; privacy, governance,
  security, and license routes exist as footer text without targets.

No part of this ADR is superseded by the as-built site. See
`docs/08-web-brand/WIX_SITE_BUILD_PLAN.md` §As-built state for the page-level record.

## Superseded assumption

The statement in ADR-0002 that Firebase delivers the public platform is narrowed: Google remains the computational and application cloud, while Wix owns the canonical institutional website.
