---
document_id: DRL-AGT-009
title: "Agent Mission 09: Private Local Runner, Voice, and Edge Runtime"
version: 3.0.0
status: APPROVED EXECUTION MISSION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Agent Mission 09: Private Local Runner, Voice, and Edge Runtime

## Mission objective

Implement the optional private Atticus node for Windows-first local operation: device pairing, outbound-only secure task transport, local open-weight inference, voice, approved-directory file and repository tools, sandboxed commands, private memory, and user-controlled approvals.


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


## Entry prerequisites

- Missions 00–08 relevant foundations merged.
- Control-plane device protocol, policy model, Edge/Core artifacts or mocks, and cloud endpoint available.
- Windows test environment identified; no private user data is required for tests.

## Owned paths

- `apps/atticus-local-runner/**`
- local transport/runtime portions of `packages/atticus-sdk/**`
- local tool adapters and sandbox fixtures
- installer/packaging documentation and local security tests

## Protected or coordinated paths

- Cloud services cannot initiate inbound access to the device.
- Credentials use OS-protected storage; no repository `.env` for production device credentials.
- Default tool set is deny-by-default and constrained to approved directories/commands.
- Raw voice, files, private memory, or local adapters do not leave the device unless a specific approved workflow requires it and disclosure is explicit.

## Required work packages

### WP-09-01 — Device identity, pairing, and revocation
Implement short-lived pairing, device keys, OS credential storage, capability manifest, outbound authenticated channel, signed tasks/results, replay protection, revocation, and lost-device procedure.

### WP-09-02 — Local runtime and model routing
Package Edge/Core local backends, hardware detection, quantized model selection, offline mode, cloud-escalation consent, health checks, resource limits, and safe upgrade/rollback.

### WP-09-03 — Voice and interaction loop
Implement push-to-talk first, optional wake-word research path, local audio handling, transcription/synthesis adapters, interruption/cancellation, accessibility, and explicit recording state.

### WP-09-04 — File, repository, and shell tools
Implement approved-root file search/read, reviewable file edits, Git inspect/test/patch flows, command allowlists/sandboxing, path/symlink defenses, output limits, and strong approval for mutation.

### WP-09-05 — Private memory and data lifecycle
Implement encrypted/local stores, user inspection/deletion/export, namespace boundaries, retention, provenance, poisoning defenses, and opt-in trace donation that strips or excludes private payloads by default.

### WP-09-06 — Packaging and adversarial validation
Create reproducible Windows installation/update/uninstall, mock demo environment, threat tests, failure recovery, offline smoke test, and private data exfiltration test suite.

Every work package must name the requirements it satisfies, the evidence it produces, and its failure/rollback behavior. Create focused commits at work-package boundaries.

## ADR and director-approval triggers

- Any inbound network listener, administrator/elevated execution, broad filesystem default, automatic email send, hidden recording, persistent raw audio, or cloud upload of local content.
- Any use of a closed model without explicit per-use routing disclosure/consent.
- Any new OS integration with consequential authority.

## Verification matrix

- Pairing/revocation/replay tests pass.
- Local runner functions offline for documented capabilities.
- Security tests cover path traversal, symlink escape, command injection, malicious repo content, secret redaction, prompt injection, and result-size abuse.
- Voice capture state is always visible/audible and interruptible.
- Private content remains local in network-capture tests except deliberately approved minimum payload.
- Installer, update, rollback, and uninstall are exercised on clean Windows test environments.

## Handoff requirements

Provide signed protocol fixtures, supported hardware/runtime matrix, installer artifacts, tool permission matrix, local data map, network-flow evidence, threat-test report, known OS limitations, and exact pairing/run/revoke commands.

## Definition of mission complete

A user can install, pair, operate, inspect, revoke, and remove the local runner; approved local workflows work with open weights; no inbound exposure or unauthorized data movement occurs; security and usability evidence meets V1 gates.
