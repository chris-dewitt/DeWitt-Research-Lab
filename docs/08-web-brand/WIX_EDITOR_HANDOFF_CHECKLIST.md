---
document_id: DRL-WEB-020
title: "Wix Editor Build, Review, and Handoff Checklist"
version: 1.0.0
status: APPROVED OPERATING PROCEDURE
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Wix Editor Build, Review, and Handoff Checklist

## Access and safety

- [ ] Wix site and domain ownership are confirmed under Director-controlled accounts.
- [ ] MFA and recovery methods are enabled.
- [ ] Collaborator roles are least privilege.
- [ ] No password, transfer code, API key, or verification secret appears in Git, screenshots, or tickets.
- [ ] A pre-change site duplicate, revision, or rollback path exists.

## Domain

- [ ] `www.dewitt-labs.com` is assigned to the correct Wix site.
- [ ] `dewitt-labs.com` redirects permanently to the canonical `www` URL.
- [ ] HTTPS certificate is valid.
- [ ] Existing mail and verification records are preserved.
- [ ] Domain renewal ownership and alerts are documented privately.

## Site structure

- [ ] Home, Laboratory, Systems, Research, Open Source, Teaching, About, Contact, and Launch/Status paths exist.
- [ ] Atticus and every specialist has a page or truthful planned-state entry.
- [ ] Header and footer navigation are consistent.
- [ ] The site is understandable without opening Atticus.
- [ ] No empty or misleading page is published merely to fill navigation.

## Brand and UX

- [ ] Cream-on-black design tokens match the controlled brand guidance.
- [ ] Body text remains readable and is not all monospace.
- [ ] Terminal/tmux motifs explain structure rather than obstruct content.
- [ ] Mobile and reduced-motion modes are intentionally designed.
- [ ] Institutional language does not imply government, university, accreditation, or staff scale that is not real.

## Open-source identity

- [ ] Open Source appears in primary navigation or first-scroll content.
- [ ] Model, software, data, benchmark, and documentation classifications are precise.
- [ ] Upstream projects are credited without false endorsement.
- [ ] Run, read, reproduce, fork, and contribute routes point to real artifacts or truthful planned states.
- [ ] The Atticus Open Model Commons has a discoverable entry point.

## Applications and embeds

- [ ] Primary application buttons point to approved HTTPS DRL subdomains.
- [ ] Every external app has a return-to-workshop path.
- [ ] Embeds are bounded, public, and non-privileged.
- [ ] Every embed has fallback content and a direct link.
- [ ] Mobile height, scrolling, keyboard, and failure states are tested.
- [ ] No authenticated Atticus, private runner, file upload, or admin flow is iframe-only.

## Content and evidence

- [ ] Project maturity labels come from controlled metadata.
- [ ] Metrics have evidence, date, and source.
- [ ] Research pages link methods, limitations, code/data/model assets, license, and citation.
- [ ] Wix summaries point to canonical technical documents.
- [ ] Drafts and private artifacts are not accidentally published.
- [ ] Corrections and superseded content have redirect/history treatment.

## Privacy and analytics

- [ ] Privacy notice describes Wix and application-subdomain data flows.
- [ ] Analytics categories and consent agree across surfaces.
- [ ] Atticus research-trace donation is separate explicit opt-in.
- [ ] Custom code and forms have a data owner and retention rule.
- [ ] Staging, previews, private traces, and admin routes are not indexed.

## SEO and sharing

- [ ] Canonical URLs use `www.dewitt-labs.com` for institutional pages.
- [ ] Application pages use their own canonical subdomain URLs.
- [ ] Sitemap and robots behavior are reviewed.
- [ ] Page titles and descriptions are unique and accurate.
- [ ] Social cards, favicon, and organization metadata are tested.
- [ ] No duplicate technical content competes without canonical ownership.

## Accessibility

- [ ] Keyboard-only navigation reaches every primary action.
- [ ] Focus is visible.
- [ ] Heading structure is logical.
- [ ] Images and diagrams have alternatives.
- [ ] Color is not the only status indicator.
- [ ] Forms announce validation and completion.
- [ ] Zoom, contrast, reduced-motion, and representative screen-reader review pass.

## Launch verification

- [ ] Apex, `www`, and every live application hostname pass HTTPS/redirect tests.
- [ ] Links and return links pass automated and manual checks.
- [ ] Live, cached, replayed, simulated, planned, and unavailable states are labeled.
- [ ] Model outage leaves useful Wix content and replay paths.
- [ ] Contact, security report, governance, license, privacy, and status links work.
- [ ] Release/commit/version shown on the site matches the launch dossier.

## Handoff

- [ ] The Director receives page map, component inventory, custom-code list, content owners, and update instructions.
- [ ] DNS and domain operations are documented separately from editorial updates.
- [ ] Wix collaborators and permissions are reviewed.
- [ ] Known limitations and future ADR gates are recorded.
- [ ] A rollback exercise is completed before calling the site production-ready.
