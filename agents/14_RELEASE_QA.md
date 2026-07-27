---
document_id: DRL-AGT-014
title: "Agent Mission 14: Independent Quality Assurance and V1 Release"
version: 3.1.0
status: APPROVED EXECUTION MISSION
owner: DeWitt
last_updated: 2026-07-26
---

# Agent Mission 14: Independent Quality Assurance and V1 Release

## Mission objective

Act as an independent release authority: verify rather than build. Audit requirement traceability, tests, security, privacy, accessibility, licensing, model/data reproducibility, cloud operations, documentation, and public claims; prepare the all-at-once V1 release candidate for DeWitt’s final decision.


## Operating contract

This mission is executed on a dedicated feature branch and ends in a reviewable pull request. Before changing files, the agent must read `LABORATORY_BIBLE.md`, root `AGENTS.md`, `docs/00-program/SPECIFICATION_MAP.md`, `docs/00-program/DECISION_REGISTER.md`, the current `WORKLOG.md`, this mission, and every listed prerequisite.

The agent must not silently reinterpret the laboratory. Missing or contradictory decisions become a documented blocker or an ADR proposal. All external factual or technical assumptions that could have changed must be revalidated against authoritative primary documentation and entered in the technical reference register.

## Branch, commit, and pull-request protocol

- Create a branch named `agent/<mission-number>-<short-scope>` from the latest approved integration branch.
- Reserve the mission in `WORKLOG.md` before modifying controlled files.
- Commit after coherent work packages; avoid one giant undifferentiated commit.
- Rebase or merge the latest integration branch before final verification.
- Open a pull request containing requirement IDs, changed contracts, ADRs, test evidence, security/privacy impact, documentation impact, known limitations, and exact handoff state.
- Never merge the pull request yourself unless DeWitt has explicitly delegated that authority for the specific PR.

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

- All implementation missions complete with merged evidence.
- Release candidate versions pinned.
- Staging environment and clean-room local setup available.
- No mission owner may self-certify unresolved critical findings.

## Owned paths

- `docs/12-acceptance/**`
- release dossier and verification reports
- changelog, release notes, SBOM/provenance manifests
- final validation scripts/tests
- release branch coordination and packaging

## Protected or coordinated paths

- Do not rewrite component behavior to make tests pass; file defects to owners.
- Do not waive a release blocker without DeWitt’s explicit recorded approval and public disclosure where material.
- Do not certify licenses, privacy, security, or research claims without evidence.
- Production promotion remains DeWitt-approved.

## Required work packages

### WP-14-01 — Clean-room reproducibility
Build and run the documented local/mock stack from a clean checkout; verify deterministic assets, model/dataset manifests, documentation commands, and contributor setup.

### WP-14-02 — Requirement and evidence audit
Walk every V1 requirement through the traceability matrix to tests, reports, artifacts, and owner signoff; reject orphaned claims or evidence-free completion.

### WP-14-03 — Independent quality suites
Run full unit/integration/contract/e2e/performance/accessibility/security/privacy/red-team/model/data/reproducibility/license scans and compare results to gates.

### WP-14-04 — Operational readiness
Witness deployment, canary, rollback, backup/restore, incident drill, quota/budget enforcement, telemetry redaction, and status communication.

### WP-14-05 — Public release dossier
Prepare version map, checksums, SBOMs, model/data cards, evaluation/safety reports, architecture/security notes, known limitations, release notes, website claim register, and reproducibility instructions.

### WP-14-06 — Go/no-go review
Classify blockers, require remediation or recorded waiver, create final launch checklist, and present a recommendation to DeWitt without merging/promoting unapproved production changes.


### WP-14-07 — Open artifact and forkability audit
Verify Open Artifact Standard compliance, terminology, maturity and badge evidence, cards, notices, SBOM/provenance, clean-room setup, model substitution, export, and upstream attribution.

### WP-14-08 — Portable-boundary and no-paid-API verification
Demonstrate the V1 local research profile and integrated fixture workflow without proprietary DRL credentials or a paid commercial model API; audit every managed capability for a documented portable boundary.

Every work package must name the requirements it satisfies, the evidence it produces, and its failure/rollback behavior. Create focused commits at work-package boundaries.

## ADR and director-approval triggers

- Any release-gate waiver.
- Any unresolved critical/high security, privacy, licensing, data leakage, calculation correctness, or public-claim issue.
- Any divergence between public artifacts and tested commit.
- Any production promotion or public model-weight publication.

## Verification matrix

- Clean-room and staged validations pass from pinned commits/artifacts.
- Manifest hashes and signatures verify.
- No unresolved release-blocking findings.
- All known limitations are accurate and public where relevant.
- Website metrics/claims match release evidence.
- Rollback/restore/incident and budget controls are demonstrated.
- DeWitt receives a concise evidence-based go/no-go packet.

## Handoff requirements

Provide final validation report, evidence index, blocker register, signed artifact manifest, release candidate identifiers, go/no-go recommendation, exact deployment/release commands, rollback plan, and post-launch watch list.

## Definition of mission complete

DeWitt can make an informed public V1 decision from complete evidence; the tested artifacts are exactly the artifacts proposed for release; all release criteria pass or deviations are explicit, approved, and disclosed.

### WP-14-09 — Independent open-identity release audit

Run `make open-check`, verify the open artifact schemas and website metadata, execute the clean-room showcase, test public download/install links, audit precise terminology, and reject unsupported openness or maturity claims.
