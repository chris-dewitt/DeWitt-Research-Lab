---
document_id: DRL-WEB-105
title: "Workshop Web Build Roadmap"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Workshop Web Build Roadmap

## Delivery philosophy

The web experience is built as thin verified vertical slices. Each slice
includes contracts, implementation, tests, accessibility, documentation,
artifact evidence, and rollback.

## Workstreams

- Design system and controlled-content engine.
- Signed success/degraded replay viewer with transcript fallback.
- `TR-2026-001` report reader.
- Project, method, and open-artifact views.
- Wix return navigation and canonical metadata.
- Future Atticus console behind deployment, consent, policy, and abuse gates.
- Accessibility, performance, SEO, privacy, and release evidence.

## Dependency order

Tokens/content validation -> report reader -> signed replay viewer -> Wix evidence
links -> project/method/open views -> future live Atticus/auth -> optional public
status -> exhaustive release audit.

## Cross-project dependencies

- controlled documents and signed artifacts;
- replay manifests and evaluation reports;
- project maturity and source metadata;
- Wix/domain integration;
- brand, security, privacy, and open-artifact policies.

## Release evidence

- content/provenance validation;
- success/degraded replay verification;
- report, source, citation, and fallback links;
- accessibility, performance, visual, and end-to-end reports;
- consent/privacy verification where applicable;
- deployment and rollback evidence.

## Explicitly deferred

- public live Atticus before its separate gates pass;
- standalone status or failure-museum sites;
- community social network and unrestricted user-generated pages;
- native mobile app, elaborate 3D scenes, autoplay media;
- commercial billing/marketplace;
- full multilingual localization beyond architecture readiness.

Deferred work may appear only as clearly labeled planned work.
