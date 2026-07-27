---
document_id: DRL-WEB-103
title: "DRL Web Evaluation and Acceptance Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # DRL Web Evaluation and Acceptance Specification

    ## Evaluation contract

    Evaluations test actual product/research claims. Each claim has population, threat model, metric, uncertainty treatment, slices, failure examples, owner, and release threshold. A single aggregate score is never sufficient.

    ## Claims

    - Visitors understand DRL and find relevant work.
- The site is accessible and performant.
- Project claims and metrics are truthful and traceable.
- Public Atticus and demo states are understandable.
- Consent and privacy controls are usable.
- The aesthetic is distinctive without impairing work.

    ## Required suites

    - Automated semantic HTML, contrast, keyboard, focus, and reduced-motion checks.
- Manual screen-reader and mobile touch review.
- Performance, bundle, image, and Core Web Vitals budgets.
- Visual regression across breakpoints and states.
- Content schema, links, and claim-provenance validation.
- Atticus replay/live/error/cold/degraded E2E.
- Auth, session, consent, and analytics tests.
- Moderated usability sessions across target personas.

    ## Metrics and analysis

    - Task completion, time, and errors for core journeys.
- Accessibility findings by severity.
- LCP, INP, CLS, bundle and image budgets.
- Broken/stale link and unsupported metric counts.
- Demo-state and approval comprehension.
- Search relevance and zero-result rate.
- Consent selection and revocation correctness.

    Paired tests or bootstrap intervals are used where appropriate. Repeated tuning against a benchmark is tracked. Human and model judges include calibration, disagreement, and limitations; model-judge output is not objective truth.

    ## Release gates

    - Zero critical accessibility, security, privacy, or provenance defects.
- Approved performance budgets on representative devices.
- All headline metrics resolve to valid artifacts.
- Core journeys pass desktop, mobile, keyboard, and screen-reader review.
- Public console cannot reach private tools and handles all operational states.
- Reviewers can distinguish live, replay, cached, and illustrative content.

    A noncritical regression needs a time-bounded exception with user value, affected slices, mitigation, owner, expiry, and director approval. Security/privacy boundary and deterministic-correctness failures cannot be averaged away.

    ## Adversarial program

    - XSS or MDX injection.
- Malicious document links and forged artifacts.
- Auth/session confusion and CSRF.
- Consent dark patterns.
- Motion/flash and screen-reader flooding.
- Deceptive terminal status.
- Cold-start loops.
- Analytics leakage of prompt content.

    ## Required evidence

    - Accessibility conformance report.
- Performance report.
- Provenance validation log.
- Usability findings and resolutions.
- Visual regression snapshots.
- E2E results.
- Privacy/analytics verification.
- Signed integrated demo.

    Reports pin code, data, model/provider, prompt/template, tool, configuration, environment, sample counts, exclusions, costs, failures, and reproduction commands. Public metrics link to signed reports.
