---
document_id: DRL-WEB-107
title: "DeWitt Research Workshop Web System Specification"
version: 4.2.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# DeWitt Research Workshop Web System Specification

## 1. Purpose and authority

The open `lab-web` application complements Christopher Noxon DeWitt's canonical personal portfolio at
`https://www.dewitt-labs.com`. Its first V1 responsibility is to make
repository-authoritative evidence usable on the web: signed replay viewing,
technical-report reading, trace inspection, and reproducibility links.

Wix explains the research program and links to evidence. `lab-web` renders
advanced evidence and future workspaces that do not fit Wix well. It does not
replace the canonical site or imply that Atticus is a hosted service.

## 2. Users and jobs

- Faculty, prospective advisers, admissions readers, and research peers inspect selected reports, methods, and limitations.
- Research-oriented employers inspect architecture, failure handling, and code.
- Developers and learners inspect traces, reproduce fixtures, and follow source.
- The Director publishes controlled artifacts and maintains the public record.
- Future contributors reach governance and setup after understanding the work.

## 3. V1 capabilities

- Signed success/degraded replay viewer with transcript fallback.
- Full `TR-2026-001` reading experience.
- Trace, policy, evidence, calculation, and evaluation panes.
- Repository-backed project, writing, method, and open-artifact indexes.
- Truthful maturity and live/replayed/cached/illustrative/planned state labels.
- Architecture and source views with direct return navigation to Wix.
- Local/self-hosted operation with no private service dependency.
- Future Atticus console components behind explicit deployment and safety gates.

## 4. Explicit non-goals

- Replacing Wix as the canonical editorial origin without an approved ADR.
- Claiming `atticus.dewitt-labs.com` is live before deployment evidence exists.
- Making chat, authentication, or a warm model required for public research.
- Generic résumé template, startup funnel, or collaborator recruitment portal.
- Fake terminal output, fabricated metrics, or invented institutional scale.
- Arbitrary public code execution or access to private/local tools.
- Hand-maintained duplicate facts that drift from repository sources.
- Making primary computational applications iframe-only.

## 5. Logical architecture

```text
Next.js application shell
  |-- controlled document and report renderer
  |-- signed replay verifier and timeline
  |-- evidence, trace, policy, calculation, and evaluation panes
  |-- project/writing/open-artifact indexes
  |-- Wix link and canonical-metadata adapters
  |-- optional future session/consent/account boundary
       -> public Atticus API only after separate release approval
```

## 6. Canonical workflows

### Inspect a recorded run

Open success replay -> verify manifest -> inspect trace/evidence/evaluation ->
switch to degraded replay -> compare outcome -> open source or report.

### Read the report

Open `TR-2026-001` -> read abstract/methods/limitations -> inspect linked replay
and code -> copy citation or reproduction path.

### Explore a project

Open project -> read research question and maturity -> inspect strongest artifact
-> review failure/limitation -> return to Wix or follow source.

### Publish

Merged controlled documents and signed artifacts pass frontmatter, links, claim,
evidence, accessibility, and route validation before publication.

### Future Atticus session

A bounded live session is enabled only after identity, quota, consent, policy,
abuse, cost, unavailable-state, and deployment gates pass. Until then the UI
shows replay or planned state.

## 7. Interfaces

- controlled content manifests and document metadata;
- signed replay, report, evaluation, model, dataset, and release schemas;
- public artifact URLs and Wix return/canonical links;
- future Atticus task, run, event, trace, approval, auth, and consent APIs;
- no browser-side credentials to private backends.

Cross-project requests and results use versioned protocol envelopes. Internal
types may be richer but cannot silently change public semantics.

## 8. Invariants

- Core content and navigation work without Atticus or client enhancement.
- Replay verification never upgrades a demo HMAC to production trust.
- Metrics identify artifact, source, date, and method.
- Live, replayed, cached, illustrative, and planned states are distinct.
- No public visitor reaches private or local tools.
- Consent precedes optional analytics or content capture.
- Every public research claim links to methods, evidence, and limitations.
- Production builds exclude secrets, private drafts, and employer material.

## 9. Quality attributes

- **Correctness:** typed inputs and verifiable artifacts.
- **Traceability:** reconstructable operational events without hidden reasoning.
- **Security:** least privilege, deny by default, bounded egress.
- **Privacy:** collection minimization and public/private/local separation.
- **Reliability:** truthful degraded states and static fallbacks.
- **Accessibility:** keyboard, screen reader, reduced motion, contrast, zoom, and
  mobile support.
- **Portability:** local/open fixtures; no mandatory managed-cloud dependency.
- **Evaluability:** every headline claim maps to a versioned artifact or gate.

## 10. Milestones

- M1 tokens, components, document renderer, and validation.
- M2 signed replay viewer and `TR-2026-001` reading experience.
- M3 project, writing, and open-artifact indexes plus Wix return contract.
- M4 future bounded Atticus session behind release gates.
- M5 accessibility, performance, security, SEO, and coordinated launch evidence.

## 11. V1 acceptance

- Success and degraded replays verify and render with transcript fallbacks.
- `TR-2026-001` renders with methods, limitations, citation, and source links.
- Academic evaluator reaches both artifacts from Wix without search or sign-in.
- WCAG-oriented and representative mobile/desktop review passes.
- Every public state and metric is evidence-backed and dated.
- Preview, production, canonical metadata, TLS, Wix return, and rollback are tested.

## 12. Open identity

Every artifact identifies source, upstream foundations, license, maturity,
local/self-hosted path, evaluation evidence, and open exceptions. Reproduce
actions are generated from tested metadata. Contributor entry points remain
available but secondary to evidence inspection. A visible **Open Source portal**
route returns visitors to the canonical Wix catalog.
