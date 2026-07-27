---
document_id: DRL-ADR-0008
title: "Use Wix at www.dwit-labs.com as the Canonical Institutional Site"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# ADR-0008: Use Wix at `www.dwit-labs.com` as the canonical institutional site

## Context

DeWitt has registered `dwit-labs.com` and acquired a Wix website. The previous foundation assumed Firebase App Hosting would deliver the entire laboratory website. DRL now has a real public domain and an available institutional publishing platform.

## Decision

`https://www.dwit-labs.com` is the canonical public institutional origin, hosted on Wix for V1. The apex redirects to the canonical `www` origin.

Atticus and specialist computational experiences remain open-source applications deployed under DRL subdomains or linked routes. Wix is not required to host GPU inference, streaming traces, authenticated private tooling, deterministic scenario computation, or the complete application runtime.

Firebase/App Hosting and Google Cloud remain approved for interactive frontends, APIs, documentation, model serving, and specialist systems. `apps/lab-web` becomes the portable open-source interactive web platform and application shell rather than the only canonical institutional homepage.

## Consequences

- Wix and external applications need one design, navigation, consent, SEO, and status contract.
- DNS, TLS, redirect, CORS, CSP, cookie, and cross-origin decisions become explicit release work.
- Primary applications use first-class subdomains rather than iframe-only delivery.
- Controlled technical documentation remains repository-authoritative.
- Wix may author editorial content, events, collaboration pages, and public introductions.
- A future migration to Wix Headless, a fully custom Next.js institutional site, or unified membership requires another ADR and redirect plan.

## Superseded assumption

The statement in ADR-0002 that Firebase delivers the public platform is narrowed: Google remains the computational and application cloud, while Wix owns the canonical institutional website.
