---
document_id: DRL-ROOT-WORKLOG
title: "Sequential Agent Worklog"
version: 4.12.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---


# Sequential Agent Worklog

## Rules

This is the canonical human-readable ledger for sequential agents. Append; do not erase historical entries. Link branches, PRs, commits, requirements, ADRs, validation, temporary resources, and the next start point. Use `agents/HANDOFF_TEMPLATE.md` for full handoffs.

## Current program state

- M2 specialists through DRL-013 on `main`; M3 specialists DRL-014–017 on `main`
  (DRL-016 landed via corrective PR #20).
- Active mission: **06 Brand/Web** — DRL-021 evidence-first academic website
  documentation cleanup. Wix editor implementation remains Director-operated.
- Integration branch: still to be created by operator via DRL-001.
- Open blockers: DIR-001, DIR-003, DIR-002 (deploy), DIR-004 (model bake-off;
  scaffold only — no winner).
- First sprint plan: `docs/00-program/FIRST_SPRINT_PLAN.md`.

## Reservation table

| Mission | Agent/tool | Branch | Started UTC | Status | PR |
|---|---|---|---|---|---|
| 00/01 follow-up | Cursor cloud agent | `cursor/mission-00-program-bootstrap-ad29` | 2026-07-27 | MERGED | PR #6, #7 |
| 02 / DRL-005 | Cursor cloud agent | `cursor/drl-005-protocol-state-machine-ad29` | 2026-07-27 | MERGED | PR #8 |
| 07 / DRL-007 | Cursor cloud agent | `cursor/drl-007-model-provider-interface-ad29` | 2026-07-27 | MERGED | PR #9 |
| 07 / DRL-008 | Cursor cloud agent | `cursor/drl-008-structured-output-repair-ad29` | 2026-07-27 | MERGED | PR #10 |
| 04 / DRL-011 | Cursor cloud agent | `cursor/drl-011-evalforge-permission-suite-ad29` | 2026-07-28 | MERGED | PR #11 |
| 09 / DRL-009 | Cursor cloud agent | `cursor/drl-009-approved-root-inspection-ad29` | 2026-07-28 | MERGED | PR #12 |
| 00 docs | Claude Code cloud agent | `claude/reas-repo-review-ch2zh6` | 2026-07-29 | MERGED | PR #13 |
| 09 / DRL-010 | Claude Code cloud agent | `claude/reas-repo-review-ch2zh6` | 2026-07-29 | MERGED | PR #14 |
| 08+09 / DRL-012+013 | Cursor cloud agent | `cursor/drl-012-013-bakeoff-voice-ad29` | 2026-07-29 | MERGED | PR #15 |
| 10 / DRL-014 | Cursor cloud agent | `cursor/drl-014-atlas-adapter-ad29` | 2026-07-29 | MERGED | PR #16 |
| 11 / DRL-015 | Cursor cloud agent | `cursor/drl-015-fedlens-corpus-ad29` | 2026-07-29 | MERGED | PR #17 |
| 12 / DRL-017 | Cursor cloud agent | `cursor/drl-017-balancelab-scenarios-ad29` | 2026-07-29 | MERGED | PR #18 |
| 11 / DRL-016 | Cursor cloud agent | `cursor/drl-016-fedlens-citations-ad29` | 2026-07-29 | MERGED OFF-TARGET | PR #19 → 015 branch |
| 11 / DRL-016 land | Cursor cloud agent | `cursor/drl-016-land-main-ad29` | 2026-07-30 | MERGED | PR #20 |
| 13 / DRL-018 | Cursor cloud agent | `cursor/drl-018-integrated-workflow-ad29` | 2026-07-30 | MERGED | PR #21 |
| 13 / DRL-019 | Cursor cloud agent | `cursor/drl-019-signed-replays-ad29` | 2026-08-01 | MERGED | PR #22 |
| 15 / DRL-020 | Cursor cloud agent | `cursor/drl-020-teaching-guide-ad29` | 2026-08-01 | MERGED | PR #23 |
| 15 / DRL-028 | Cursor cloud agent | `cursor/drl-028-technical-report-ad29` | 2026-08-01 | MERGED | PR #24 |
| 15 / DRL-029 | Cursor cloud agent | `cursor/drl-029-contributor-routes-ad29` | 2026-08-01 | IN REVIEW | PR #25 |
| 06 / DRL-021 docs | Codex | `lovesong/docs/drl-021-positioning-cleanup` | 2026-08-05T03:11:02Z | READY FOR REVIEW | — |

## Active scope — DRL-021 documentation cleanup

- Scope: reconcile the controlled identity, audience, website, and application-shell
  documents around an evidence-first academic workshop; update traceability and
  regression checks in the same change.
- Dependencies retained: the Wix editor and deployment remain outside this branch;
  DRL-021 stays `QUEUED` until its visual and operational acceptance evidence exists.
- Exit criteria: recorded replay and TR-2026-001 are the canonical first actions;
  academic evaluation is the primary journey; degraded evidence and the Stage-B
  no-winner result are visible; Atticus is labeled as a documented research artifact;
  targeted documentation tests pass; exact evidence and remaining work are handed off.

## Weekly dashboard snapshot — 2026-07-27

| Field | Value |
|---|---|
| Active milestone | M1 |
| Active mission | 00 |
| Next issue to file/execute | DRL-001 |
| Integration branch | not created yet |
| P0 Director decisions | DIR-001, DIR-003 |
| Cloud spend | $0 |
| Maturity caution | Fixture Atticus demo is prototype/simulated, not V1 |

## Handoff entries

Append completed handoffs below this line. Never place credentials, private data, or ephemeral chat-only context here.

### 2026-08-04 — DRL-021 evidence-first academic positioning

- Branch: `lovesong/docs/drl-021-positioning-cleanup`
- Implementation commit: `71d5b55`
- Reconciled controlled site/product/app-shell docs around replay +
  `TR-2026-001`, academic evaluation, visible degraded/no-winner evidence, and
  planned Atticus state.
- Validators PASS; 31 focused tests PASS; 198 executable full-suite tests PASS.
  One unchanged Windows symlink test requires a host with symlink privilege.
- Handoff: `agents/handoffs/2026-08-04-drl-021-positioning.md`
- Next: Director/Wix operator implements and captures DRL-021 visual, link,
  accessibility, and rollback evidence; issue remains `QUEUED` until then.

### 2026-08-01 — DRL-029 contributor routes and good-first issues

- Branch: `cursor/drl-029-contributor-routes-ad29`
- Route map, GFI seeds, issue template, CONTRIBUTING updates
- Next: M4 blocked items needing Director (Wix/GCP) or DRL-001/002 operator gates

### 2026-08-01 — DRL-028 technical report TR-2026-001

- Branch: `cursor/drl-028-technical-report-ad29`
- Prototype integrated-workflow technical report + doc guard
- Next: DRL-029 contributor routes


### 2026-08-01 — DRL-020 integrated workflow teaching lab

- Branch: `cursor/drl-020-teaching-guide-ad29`
- Teaching lab + contributor path link + doc guard test
- Next after merge: M4 / DRL-021+ or remaining M1 housekeeping

### 2026-08-01 — DRL-019 signed success and degraded replays

- Branch: `cursor/drl-019-signed-replays-ad29`
- Fixture HMAC-signed replay bundles + digest verification
- Next: DRL-020 teaching guide


### 2026-07-30 — DRL-018 evidence-to-scenario linked workflow

- Branch: `cursor/drl-018-integrated-workflow-ad29`
- Composed M3 Atlas/FedLens/BalanceLab specialists into Atticus runtime
- Added `linked_workflow` digests + `workflow_linked` trace event
- Docs/traceability/memo/changelog/issue-register updated
- Next: DRL-019 signed replays after merge


### 2026-07-27 — Foundation implementation upgrade

- Upgraded the recovered Wix/domain build-bible foundation.
- Added the living Director's decision ledger and recorded the Director's approved
  institutional, implementation, cloud, and execution decisions.
- Added a runnable deterministic Atticus vertical slice and working Atlas,
  FedLens, BalanceLab AI, and EvalForge starters.
- Added GCP-primary/Azure-portable deployment guidance and a 90-day GitHub
  execution program.
- Next start point: initialize the remote repository and execute Mission 00
  without introducing production credentials.

### 2026-07-27 — Mission 00 program bootstrap (planning)

- Mission / agent: 00 Program Director / Cursor
- Branch: `cursor/mission-00-program-bootstrap-ad29`
- Status: PARTIAL → awaiting PR review and operator filing of GitHub issues
- Objective: convert foundation into executable M1 sprint + issue program
- Follow-up sprint: repaired failed Node CI setup, added program validation,
  made bootstrap portable, and produced Linux clean-clone evidence.

#### Work packages

| Work package | Status | Evidence |
|---|---|---|
| WP-00-01 | COMPLETE | `CURRENT_STATE_BASELINE.md`, registers retained/audited |
| WP-00-02 | COMPLETE | `CRITICAL_PATH_AND_GATES.md` |
| WP-00-03 | COMPLETE | issue/PR templates, `.github/labels.yml` |
| WP-00-04 | COMPLETE | `requirements/issue-register.yaml`, `.github/ISSUE_BODIES/DRL-001..030.md` |
| WP-00-05 | COMPLETE | `ADR_APPROVAL_QUEUE.md` + Memo updates |
| WP-00-06 | COMPLETE | `RELEASE_DASHBOARD.md` + weekly WORKLOG snapshot |

#### M1 issue evidence prepared

| Issue | Repository evidence | Remaining closure condition |
|---|---|---|
| DRL-003 | Release dashboard + dated WORKLOG review | File/close remote issue |
| DRL-004 | `docs/00-program/evidence/M1-CLEAN-CLONE-2026-07-27.md` | Windows clean-room run |
| DRL-006 | CI-0001 + SETUP-0001 Failure Museum records | File/close remote issue |

#### Verification after CI repair

```text
make verify       # PASS; 25 Python tests
make lint         # PASS
make typecheck    # PASS; 33 source files
make security     # PASS
make build        # PASS
clean clone       # bootstrap 1.312s; demo 0.087s; verify 2.694s
GitHub Actions     # PASS; run 30239648838; all three jobs green
```

The original PR failure was duplicate pnpm version configuration. The first
clean-clone proof also exposed nonportable `python` and `/usr/bin/time`
assumptions. Both have regression evidence in the Failure Museum.

#### Paths outside Mission 00 ownership (noted)

- `DIRECTORS_MEMO.md` — DIR-001 remote observation / blockers
- `requirements/work-packages.yaml`, `requirements/issue-register.yaml`
- `.github/labels.yml`, `.github/ISSUE_BODIES/**`, `.github/ISSUE_BACKLOG.md`
- `scripts/file_github_program.sh` — operator helper (needs write-capable gh)

#### Public contracts changed

NONE

#### Next-agent start instructions

1. Merge this Mission 00 PR (or mark integration-ready).
2. Operator: create `integration/v1`; run `scripts/file_github_program.sh` **or**
   manually file DRL-001–006 from `.github/ISSUE_BODIES/`.
3. Confirm DIR-001 / DIR-003 in Director's Memo.
4. Execute DRL-001 → DRL-002 → DRL-003 → DRL-004 on `integration/v1`.
5. First implementation-ready mission after M1 trust issues: **Mission 02 / DRL-005**
   (protocol tests), then Mission 01 cleanup from clean-clone gaps, then **DRL-007**.
6. Do not start specialist public adapters or model selection in M1.

Full handoff copy: `agents/handoffs/2026-07-27-mission-00.md`.

### 2026-07-27 — DRL-005 protocol state-machine hardening

- Branch: `cursor/drl-005-protocol-state-machine-ad29`
- Added `drl_protocol.state_machine` with legal/terminal transition helpers
- Orchestrator now validates transitions via protocol helpers and supports
  `cancel_check` before planning, after planning, while awaiting approval, and
  between tool invocations
- Invalid blank task/objective/session IDs rejected
- Tests: success, denial (unknown tool + public private tool), invalid input,
  cancellation, failed terminal, illegal transition table
- Outside Mission 02 owned paths: `services/atticus-control-plane/**` (required
  for executable orchestration contracts)
- Verification: `make verify` → 58 passed; `make typecheck` clean
- Next: DRL-007 provider interface, or continue Mission 02 packages
- Handoff: `agents/handoffs/2026-07-27-drl-005.md`

### 2026-07-27 — DRL-007 typed open-weight provider interface

- Branch: `cursor/drl-007-model-provider-interface-ad29`
- Added `ModelProvider`, `ModelIdentity`, `CompletionConstraints`,
  `StructuredModelResponse`, and typed provider errors in `drl_ai_core`
- Added deterministic `MockOpenWeightProvider` and disclosed `ModelGateway`
  with open-weight enforcement and fallback disclosure
- Atticus local factory: `build_local_model_gateway` /
  `build_local_open_weight_gateway`
- Tests: identity disclosure, timeout, unavailable, fallback, closed-weight
  rejection, unpaid demo preserved
- DIR-004 unchanged: no upstream model brand selected
- Handoff: `agents/handoffs/2026-07-27-drl-007.md`

### 2026-07-27 — DRL-008 structured-output validation and bounded repair

- Branch: `cursor/drl-008-structured-output-repair-ad29`
- Added `StructuredOutputValidator` with JSON Schema draft 2020-12 validation,
  nested JSON extraction, bounded repair via `ModelProvider`, and
  content-minimized trace events
- Injection markers in model text are observed as data only; `$schema`/`$id`
  cannot redefine the fixed control-plane schema; repair budgets fail closed
- Atticus helper: `TOOL_CALL_PLAN_SCHEMA` / `build_tool_plan_validator`
- Tests: malformed output, schema failure, repair success, budget exhaustion,
  injection/schema-strip, additionalProperties deny
- Requirements evidence: DRL-SEC-007, DRL-SYS-004 (partial in matrix)
- Handoff: `agents/handoffs/2026-07-27-drl-008.md`
- Merged: PR #10

### 2026-07-28 — DRL-011 held-out permission/trajectory evaluation suite

- Branch: `cursor/drl-011-evalforge-permission-suite-ad29`
- Added deterministic graders with separate `terminal_outcome` and `trajectory`
  scores; critical unauthorized actions cannot be averaged away
- Held-out suite covers allow/deny/approval/injection against Atticus fixtures
- Emits `evaluation-result`-shaped report with `gate_decision` and slices
- Fixture report: `services/evalforge/fixtures/held_out_permission_trajectory/report.json`
- Tests: suite pass, terminal≠trajectory disagreement, seeded gate failure,
  schema validation
- Requirements evidence: DRL-EVL-001, DRL-EVL-005, DRL-SEC-010 (partial)
- Verification: `make verify` → 83 passed; lint/typecheck/security clean;
  fixture demo EvalForge 1.0
- PR: #11
- Handoff: `agents/handoffs/2026-07-28-drl-011.md`
- Merged: PR #11

### 2026-07-28 — DRL-009 approved-root repository inspection

- Branch: `cursor/drl-009-approved-root-inspection-ad29`
- Hardened `SandboxedWorkspace` with redacted `inspect_text`/`read_text`,
  raw-preserving write digests, size/binary limits, traversal/symlink denial
- Tests: traversal, symlink escape + list skip, oversized read, binary reject,
  secret redaction without corrupting writes
- Requirements evidence: DRL-SEC-005, DRL-SEC-008 (partial)
- Verification: `make verify` → 87 passed; lint/typecheck clean
- PR: #12
- Handoff: `agents/handoffs/2026-07-28-drl-009.md`
- Merged: PR #12

### 2026-07-29 — DRL-010 patch proposal and local approval flow

- Branch: `claude/reas-repo-review-ch2zh6`
- Added `ApprovedWriteFlow` propose/approve/apply over `SandboxedWorkspace`
  with expiring, actor-identified, workspace-scoped `LocalApprovalGrant`
  bound to the exact proposal digest (TTL 1–3600 s, default 300 s)
- Added redacted append-only `LocalAuditLog` with JSONL export; proposal,
  grant, apply, and every denial (expired, rebound digest/workspace, changed
  workspace) leave audit records
- Changed-workspace and exact-digest invalidation preserved from DRL-009;
  atomic apply unchanged
- Tests: TTL apply, expiry denial, digest/workspace rebinding denial,
  changed-workspace denial, TTL/actor validation, audit append-only/redaction
- Requirements evidence: DRL-SEC-003, DRL-SEC-004 (partial in matrix)
- Verification: `make verify` → 93 passed; lint/typecheck (45 files)/security
  clean
- Handoff: `agents/handoffs/2026-07-29-drl-010.md`
- Merged: PR #14 (docs fix was PR #13)

### 2026-07-29 — DRL-012 + DRL-013 combined (bake-off scaffold + local voice)

- Branch: `cursor/drl-012-013-bakeoff-voice-ad29`
- DRL-012: versioned Core/Edge candidate register + `run_bakeoff_scaffold`
  report (licenses/hardware/cost/latency/quality/limitations); no winner;
  DIR-004 remains open
- DRL-013: `LocalVoiceSession` push-to-talk arming, visible capture, local/
  offline processing, optional raw retention, turn deletion
- Tests: `tests/test_bakeoff_scaffold.py`, `tests/test_local_voice.py`
- Verification: `make verify` → 101 passed; lint/typecheck clean
- PR: #15
- Handoff: `agents/handoffs/2026-07-29-drl-012-013.md`

### 2026-07-29 — DRL-014 Atlas public point-in-time adapter

- Branch: `cursor/drl-014-atlas-adapter-ad29`
- Source terms, temporal validation, disk cache, failure fixture
- Handoff: `agents/handoffs/2026-07-29-drl-014.md`

