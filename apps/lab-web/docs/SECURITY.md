---
document_id: DRL-WEB-106
title: "DRL Web Security and Privacy Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # DRL Web Security and Privacy Specification

    ## Objective

    DRL Web must stay useful under hostile, malformed, ambiguous, and failure-prone inputs without giving a model authority it does not possess. Models propose. Deterministic systems authenticate, authorize, validate, constrain, execute, audit, and obtain human approval.

    ## Protected assets

    - Brand and research integrity.
- User account, session, and consent.
- Atticus prompts, results, and traces.
- Signed demos and metrics.
- Deployment credentials.
- Private preview content.

    ## Principal threats

    - XSS, MDX, or content injection.
- Dependency and supply-chain compromise.
- Stolen auth session or CSRF.
- API abuse and denial of wallet.
- Prompt content leaked to analytics.
- Private preview leak.
- Forged report, metric, or replay.
- Cache poisoning and clickjacking.

    ## Required controls

    - Strict CSP and typed/safe rendering.
- No arbitrary MDX component execution from untrusted content.
- Server-side API mediation and audience-bound auth.
- Secure cookies, origin/CSRF protections, and session rotation.
- Signed artifact verification.
- Secret-free client bundle and environment checks.
- Dependency locks, scans, SBOM, and security headers.
- Preview access controls and safe external links.

    ## Privacy behavior

    - Granular revocable consent separate from core functionality.
- Generic analytics never receive prompt, response, tool, file, email, or document payloads.
- Trace-donation controls are explicit and inspectable.
- Anonymous mode avoids durable advertising identity.
- Policies name vendors, purposes, retention, and user controls plainly.

    ## Public abuse controls

    - API quotas and concurrency.
- File restrictions and safe parsing.
- Accessible anti-bot friction only when needed.
- Cached demos.
- Authentication for expensive workflows.
- No public external writes.
- Kill switches and abuse reporting.

    ## Verification

    - Static and dynamic scans.
- CSP and rendering tests.
- Auth, session, origin, and CSRF E2E.
- Content fuzzing.
- Artifact-signature tamper tests.
- Analytics payload inspection.
- Preview leak and dependency/SBOM review.
- External pre-release security review.

    “Sanitize input,” “encrypt it,” and “use least privilege” are not evidence. Each control identifies the boundary, exact mechanism, negative test, telemetry signal, owner, and incident response.
