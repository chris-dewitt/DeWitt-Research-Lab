---
document_id: DRL-AGT-011
title: "Agent Mission 11: FedLens Monetary-Policy Intelligence"
version: 3.0.0
status: APPROVED EXECUTION MISSION
owner: DeWitt
last_updated: 2026-07-26
---

# Agent Mission 11: FedLens Monetary-Policy Intelligence

## Mission objective

Implement FedLens as a reproducible Federal Reserve communication research service: official-source corpus, document lineage/diffs, policy themes, retrieval, event-study artifacts, and evidence-backed Atticus tools.


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


## Entry prerequisites

- Missions 00–07 merged.
- Project specification, DRL protocol, security policy, platform contracts, and EvalForge interfaces stable.
- Approved data/source or synthetic-data rules available.

## Owned paths

- `services/fedlens/**`
- corresponding project documentation and fixtures
- project-specific public tools, SDK adapters, demos, and evaluations

## Protected or coordinated paths

- Cross-service protocol changes require Architecture/Protocol coordination.
- Public data and content must pass rights/provenance review.
- Model-generated claims cannot bypass evidence, deterministic artifacts, or uncertainty requirements.
- No project may create direct public external-write authority.

## Required work packages

### WP-11-01 — Official corpus and metadata
Build official-source acquisition, document identity, meeting/speaker metadata, corrections, checksums, rights notes, and reproducible corpus manifest.

### WP-11-02 — Document processing and semantic diff
Implement parsing, section/sentence alignment, exact and semantic changes, quotation spans, model-assisted labels with provenance, and gold evaluation fixtures.

### WP-11-03 — Policy timeline and retrieval
Implement meeting/speaker/topic/tone timeline, point-in-time filters, hybrid retrieval, source excerpts, and contradiction/uncertainty representation.

### WP-11-04 — Event-study framework
Implement reproducible event windows, market-data abstraction, deterministic calculations, sensitivity checks, caveats, and artifact lineage without causal overclaiming.

### WP-11-05 — Atticus tools and public demo
Expose statement comparison, latest-policy-summary, timeline, and research tools; build a side-by-side diff demo and replay.

### WP-11-06 — Evaluation and publication
Measure alignment/diff accuracy, topic/tone calibration, retrieval/citation, event-study reproduction, latency, and release a corpus/data card.

Every work package must name the requirements it satisfies, the evidence it produces, and its failure/rollback behavior. Create focused commits at work-package boundaries.

## ADR and director-approval triggers

- New data/source license or redistribution assumptions.
- Changes to public schemas or specialist authority.
- Any claim of real-time coverage, causality, financial advice, or production-bank equivalence.
- Material cloud cost or retention changes.

## Verification matrix

- Corpus artifacts derive from documented official sources and preserve version lineage.
- Diff output points to exact spans and separates literal from model-inferred change.
- Tone/topic output includes calibrated uncertainty and abstention.
- Event-study outputs reproduce from manifests and do not imply unsupported causality.
- Atticus can use FedLens in integrated workflows with valid citations.
- Dataset/corpus release passes source and license review.

## Handoff requirements

Provide stable API/schema version, fixture/local-mode commands, data/source manifests, evaluation and security report, performance/cost baseline, demo/replay, known limitations, publication artifacts, and exact Atticus integration examples.

## Definition of mission complete

The specialist service is independently useful, locally reproducible, publicly demonstrable, fully integrated through DRL protocol, provenance/evaluation/security complete, and meets its project-specific V1 acceptance gates.
