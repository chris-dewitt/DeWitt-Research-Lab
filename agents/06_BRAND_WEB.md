---
document_id: DRL-AGT-006
title: "Agent Mission 06: Brand, Workshop Website, and Public Experience"
version: 4.2.0
status: APPROVED EXECUTION MISSION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Agent Mission 06: Brand, Workshop Website, and Public Experience

## Mission objective

Implement Christopher Noxon DeWitt's cream-on-black personal academic portfolio.
The site leads with his current UNC-Chapel Hill Master of Applied Data Science
study, interest in complex systems, selected work, and intended progression
toward graduate work in computer science. Projects and evidence support that
story. It must remain fast, accessible, responsive, and truthful.


## Operating contract

This mission is executed on a dedicated feature branch and ends in a reviewable pull request. Before changing files, the agent must read `LABORATORY_BIBLE.md`, root `AGENTS.md`, `docs/00-program/SPECIFICATION_MAP.md`, `docs/00-program/DECISION_REGISTER.md`, the current `WORKLOG.md`, this mission, and every listed prerequisite.

The agent must not silently reinterpret the laboratory. Missing or contradictory decisions become a documented blocker or an ADR proposal. All external factual or technical assumptions that could have changed must be revalidated against authoritative primary documentation and entered in the technical reference register.

## Branch, commit, and pull-request protocol

- Create a branch named `agent/<mission-number>-<short-scope>` from the latest approved integration branch.
- Reserve the mission in `WORKLOG.md` before modifying controlled files.
- Commit after coherent work packages; avoid one giant undifferentiated commit.
- Rebase or merge the latest integration branch before final verification.
- Open a pull request containing requirement IDs, changed contracts, ADRs, test evidence, security/privacy impact, documentation impact, known limitations, and exact handoff state.
- Never merge the pull request yourself unless the Director has explicitly delegated that authority for the specific PR.

## Universal constraints

- No credentials, personal/private content, employer material, unlicensed corpora, or generated secrets may be committed.
- Do not weaken security, privacy, evaluation, accessibility, open-weight, provenance, or deterministic-computation requirements to make a demo pass.
- Do not claim completion without verifiable evidence.
- Do not alter another component's public contract without coordination and, when material, an approved ADR.
- Public write actions and unrestricted shell execution remain outside the public Atticus trust boundary.
- LLM output never becomes an authoritative numerical financial result; BalanceLab calculations must be deterministic and auditable.

## Required artifacts in every mission PR

1. Implemented or revised artifacts owned by the mission.
2. Automated tests or executable validation for every material behavior.
3. Updated controlled documentation and requirement traceability.
4. A completed handoff ledger entry using `agents/HANDOFF_TEMPLATE.md`.
5. A list of decisions made, assumptions retained, unresolved blockers, and follow-on issues.
6. Evidence that relevant local and CI commands pass.

## Stop conditions

Stop rather than improvise when a change would expose private data, expand write authority, change a public protocol, add a new upstream model/license, materially change cloud cost, undermine reproducibility, or contradict an approved foundation decision. Draft an ADR or blocker with alternatives and impact.



## Open Research Charter obligations

This mission must preserve DRL's open-by-construction identity. Read `OPEN_RESEARCH_CHARTER.md` and the relevant `docs/09-open-source/` standards. For every material feature, record the public artifact, license, modification surface, self-hosted path, upstream dependencies, reproducibility evidence, and any open exception. Prefer upstream contribution over permanent private forks. Use “open source,” “open weight,” and “source available” precisely.

## Entry prerequisites

- Missions 00–03 merged.
- Brand constitution, product requirements, public Atticus boundaries, protocol contracts, and design requirements approved.
- Content authority and claim/evidence policy available.

## Owned paths

- `apps/lab-web/**`
- `apps/atticus-console/**` for visual/client concerns
- `docs/08-web-brand/**`
- shared TypeScript design-system package and public content schema
- public documentation rendering and demo-replay client

## Protected or coordinated paths

- Server-side agent orchestration, model serving, and specialist algorithms are coordinated through typed APIs.
- Do not use fake live metrics, fake institute scale, fake historical classification markings, inaccessible effects, autoplay sound, or private analytics capture.
- Root identity and mission language require director review.

## Required work packages

### WP-06-01 — Design system and tokens
Implement cream-on-black tokens, typography, spacing, terminal panes, data tables, diagrams, status/trace primitives, focus/keyboard states, motion-reduction behavior, and story/demo fixtures.

### WP-06-02 — Information architecture and content engine
Build the four-page personal portfolio (Home, Research, Projects, About),
selected evidence viewers, project pages, profile/CV paths, and a controlled
content model sourced from repository documents.

### WP-06-03 — Atticus public console
Implement anonymous/authenticated entry states, guided tours, command palette, session/consent controls, tool trace, evidence panel, approval rendering, evaluation summary, graceful cold-start and replay fallback, and mobile behavior.

### WP-06-04 — Demonstration and replay system
Create signed/versioned replay manifests, deterministic curated demonstrations, project demo launch surfaces, a full cross-system reference demo, and clear distinction among live, cached, simulated, and recorded output.

### WP-06-05 — Accessibility, performance, privacy, and analytics
Meet WCAG-oriented keyboard, screen-reader, contrast, reduced-motion, form, chart, and status semantics; enforce performance budgets; implement consent-aware product analytics and operational telemetry disclosures.

### WP-06-06 — Faculty, admissions, research-peer, and employer journeys
Test the personal journey first: current education and interests to selected
research/projects, methods/limitations, future direction, CV, and contact.


### WP-06-07 — Open Source portal and model commons
Implement the complete Open Source portal, Open Stack lineage, Atticus model commons, artifact cards, maturity/reproducibility badges, self-hosting routes, upstream ledger, and generated reproduce panels.

### WP-06-08 — Open identity across project pages
Ensure each system page shows upstream foundations, artifact rights, local path, evaluation evidence, contribution routes, community replications, and accurate live/replay/model identity.

Every work package must name the requirements it satisfies, the evidence it produces, and its failure/rollback behavior. Create focused commits at work-package boundaries.

## ADR and director-approval triggers

- Any change to public identity, tagline, institution claims, or Atticus personality invariants.
- Any analytics/content capture beyond approved policy.
- Any public interaction that adds write authority.
- Any major frontend framework or hosting change.
- Any design choice that knowingly excludes keyboard, screen-reader, low-motion, or mobile use.

## Verification matrix

- Visual regression, unit, integration, end-to-end, accessibility, performance, and content-schema checks pass.
- No fabricated metrics or unlabeled simulation.
- Every live claim has an evidence link or controlled source.
- Anonymous and authenticated consent states are tested.
- Keyboard-only user can reach all primary functions.
- Slow/cold/unavailable backends degrade to truthful replay or documentation rather than blank failure.
- Persona usability tests and acceptance notes are recorded.

## Handoff requirements

Provide stable component contracts, content schemas, screen/flow map, analytics event catalog, accessibility audit, performance report, demo manifests, known browser/device limitations, and explicit backend API requirements.

## Definition of mission complete

The public site is deployment-ready, accurately represents the laboratory, exposes real and clearly labeled demonstrations, works across priority devices and assistive modes, and gives Atticus a compelling but bounded public interface.

### WP-06-09 — Open-source visual identity

Implement evidence-derived artifact cards, Open Stack lineage, contributor credit, reproduce/fork/contribute actions, model/runtime identity, exception notices, and accessible cream-on-black open-research visual language.


### WP-06-10 — Wix canonical site and `dewitt-labs.com` integration

Implement the canonical personal academic portfolio at `www.dewitt-labs.com`:
education-first information architecture, cream-on-black visual translation,
selected research/project evidence, repository-backed content workflow,
SEO/canonical metadata, mobile/accessibility validation, and fallback behavior.
Build or document
bounded custom elements only where they improve the Wix experience; do not
place primary applications exclusively in iframes. Produce Wix editor
instructions, content inventory, page map, redirect map, and a deployment/handoff
checklist that another operator can execute without source-code access.
