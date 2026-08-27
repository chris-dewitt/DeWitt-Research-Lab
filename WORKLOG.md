---
document_id: DRL-ROOT-WORKLOG
title: "Sequential Agent Worklog"
version: 4.33.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-27
---


# Sequential Agent Worklog

## Rules

This is the canonical human-readable ledger for sequential agents. Append; do not erase historical entries. Link branches, PRs, commits, requirements, ADRs, validation, temporary resources, and the next start point. Use `agents/HANDOFF_TEMPLATE.md` for full handoffs.

## Current program state

- M2 specialists through DRL-013 on `main`; M3 specialists DRL-014–017 on `main`
  (DRL-016 landed via corrective PR #20).
- Active mission: **14 Release QA** — public visibility is authorized by
  RES-024, which supersedes the RES-018 date clause and retires the artifact
  mirror. DIR-009 was resolved by RES-022. The Director changes visibility in
  their own GitHub account. CFI DIR-008 Option A remains subject to independent
  G1 review. Wix editor implementation remains Director-operated.
- Integration branch: still to be created by operator via DRL-001.
- Open blockers: DIR-002 (GCP deploy), DIR-004 (model bake-off; scaffold only —
  no winner), and independent CFI G1 review. DIR-009 is resolved by RES-022.
  The public-artifact deployment read-back is no longer a blocker — RES-024
  retired the mirror it belonged to.
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
| 15 / DRL-031 | Codex | `lovesong/research/drl-031-computational-finance-intelligence` | 2026-08-05T17:00:00Z | MERGED DIRECT | Director-approved `402bf9c` |
| 15 / DRL-032 / CFI-002 | Codex | `lovesong/research/drl-032-cfi-literature-novelty` | 2026-08-05T23:20:00Z | BLOCKED — independent G1 review after RES-020 | — |
| 14 / DRL-033 | Codex | `lovesong/infra/drl-033-public-artifact-pages` | 2026-08-06T02:15:00Z | MERGED — DEPLOYMENT READ-BACK PENDING | PR #45; `agents/handoffs/2026-08-05-drl-033-public-artifact-mirror.md` |
| 14 / DRL-033 follow-up | Cursor cloud agent | `cursor/drl-033-artifacts-repo-live-d422` | 2026-08-19T03:20:00Z | IN REVIEW — PUBLIC REPO LIVE; PAGES + TOKEN PENDING | PR #48; `agents/handoffs/2026-08-19-drl-033-artifacts-repo-live.md` |
| 14 / DRL-034 | Codex | `lovesong/chore/drl-034-public-repository-readiness` | 2026-08-17T00:00:00Z | READY FOR REVIEW — PUBLIC RELEASE BLOCKED ON DIR-009 | `agents/handoffs/2026-08-17-drl-034-public-repository-readiness.md` |
| ops / local Atticus models | Cursor cloud agent | `cursor/local-qwen-smollm-atticus-ad29` | 2026-08-23 | MERGED | PR #54; `agents/handoffs/2026-08-23-local-qwen-smollm.md` |
| ops / Qwen plan bind + run records | Cursor cloud agent | `cursor/qwen-plan-arg-bind-ad29` | 2026-08-23 | MERGED | PR #55; `agents/handoffs/2026-08-23-qwen-plan-run-records.md` |
| ops / official public feeds | Cursor cloud agent | `cursor/live-public-feeds-ad29` | 2026-08-23 | MERGED | PR #58; `agents/handoffs/2026-08-23-public-feed-pipeline.md` |
| ops / plain card + Wix→Pages | Cursor cloud agent | `cursor/plain-limitations-wix-pages-ad29` | 2026-08-24 | IN REVIEW | `agents/handoffs/2026-08-24-plain-limitations-wix-pages.md` |
| web / DRL-035 recorded-runs evidence archive | Codex | `fix/drl-035-replay-evidence-archive` | 2026-08-27 | READY FOR REVIEW | Issue #68; `agents/handoffs/2026-08-27-drl-035-replay-evidence-archive.md` |

## Active scope — DRL-034 public repository readiness

- Scope: make the authoritative repository safe, legible, and truthful before
  its approved public-visibility date without changing that date or declaring
  the platform V1.
- Dependencies: RES-018 repository/visibility decision; RES-019 single public
  contact; DRL-029 contributor routes; merged PR #45 repository framing.
- Exit criteria: evidence-first README; public-repository audit in local and CI
  gates; current package/citation metadata; no stale generated manifest claim;
  historical validation artifacts clearly labeled; current Actions runtimes;
  exact security, privacy, licensing, test, and handoff evidence. Existing UNC
  author-email history remains a Director decision because remediation rewrites
  published Git history.

## Active scope — DRL-035 recorded-runs evidence archive

- Scope: rebuild the public GitHub Pages replay viewer as an accessible,
  responsive evidence archive for the verified success and degraded fixture
  recordings without changing their signed contents.
- Dependencies: DRL-019 signed fixtures, the public repository authorized by
  RES-024, and the existing `publish-pages` workflow.
- Exit criteria: clear report/repository identity; explicit prototype,
  fixture, rule-based-planner, and demo-signature boundaries;
  semantic landmarks; keyboard-reachable, captioned, scoped data tables;
  deterministic self-contained output; focused tests and repository checks;
  feature branch, pull request, and exact handoff evidence.

## Active scope — DRL-033 public artifact mirror

- Scope: replace the impossible private-repository Pages deployment with a
  separate public deployment mirror containing only a generated, validated
  replay release envelope.
- Dependencies: DRL-019 signed fixtures; RES-018 repository/privacy decision;
  RES-019 single public contact; RES-021 and ADR-0009 publication boundary.
- Exit criteria: exact allowlist and open exception; safe export tests; manual-
  only cross-repository publication; public repository and Pages configuration;
  deployed file/hash read-back; validators, secret scan, PR evidence, and
  handoff. Papers remain excluded until separately approved.
- Progress (2026-08-19): public repository
  `chris-dewitt/dewitt-research-artifacts` exists (public, `main`). Configs and
  workflow now use the live GitHub slug. Remaining Director actions: enable
  Pages from `main` at `/`, create fine-grained `PUBLIC_ARTIFACT_TOKEN`, store
  it on the private repo, then `workflow_dispatch` with `publish=true` and
  hash read-back.

## Active scope — DRL-021 documentation cleanup

- Scope: make the public site Christopher Noxon DeWitt's personal academic
  portfolio, centered on his UNC-Chapel Hill Master of Applied Data Science
  study, complex-systems work/interests, and intended computer-science trajectory.
- Dependencies retained: the Wix editor and deployment remain outside this branch;
  DRL-021 stays `QUEUED` until its visual and operational acceptance evidence exists.
- Exit criteria: personal identity and current education lead; **View my
  research** and **Explore my projects** are the first actions; projects are
  evidence; public caveats are limited to artifact-specific limitations; tests
  pass.

## Active scope — DRL-031 Computational Finance of Intelligence

- Scope: record the Director-approved research program linking belief
  diffusion to optimal stopping, linguistic framing and no-arbitrage belief
  repair, and market-based multi-agent aggregation.
- Dependencies: public or synthetic data with recorded rights; deterministic
  financial calculations; preregistered primary metrics; agents remain
  sequential and may not publish, reinterpret hypotheses, or claim results
  without Director/reviewer gates.
- Exit criteria: controlled program plan, agent-ready task graph, issue
  registration, decision records, research-program index update, validation,
  and an exact next-agent start packet. No experiment result is claimed.

## Active scope — DRL-032 / CFI-002 literature and novelty review

- Scope: execute a dated, reproducible, primary-source review for Belief
  Diffusion and Papers I–III; map proposed claims to closest work; record
  conflicts, gaps, novelty risk, revalidation dates, and keep/narrow/merge/stop
  recommendations.
- Dependencies: DRL-031 and RES-017. Search snippets and secondary sources may
  aid discovery but cannot support an evidentiary matrix entry.
- Exit criteria: controlled novelty matrix, search ledger, technical-reference
  update, reviewer checklist, validation, and exact handoff. No data, model,
  experiment, venue, or public novelty claim.
- Stop recorded 2026-08-05: LearnStop directly overlaps Paper I's primary
  hypothesis; recent AI-agent prediction-market, monoculture, and wagering work
  directly overlaps Paper III; formal Dutch-book audit and repair work narrows
  Paper II. DIR-008 now owns the G1 disposition. Approved questions remain
  unchanged until the Director decides.

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

### 2026-08-27 — DRL-035 recorded-runs evidence archive

- Rebuilt the static GitHub Pages replay viewer as a responsive evidence
  archive with baseline/degraded comparison, stronger prototype boundaries,
  and direct research/source routes.
- Added semantic header, navigation, main, and footer landmarks; a skip link;
  keyboard-reachable overflow regions; table captions; scoped headers; and
  text labels that do not rely on colour for status.
- Preserved deterministic self-contained HTML, verified-bundle refusal,
  fixture-data disclosures, the rule-based-planner boundary, and the
  demo-signature caveat. Public copy treats DeWitt Research Laboratory as the
  report title and limits caveats to artifact-specific technical limitations.
- Focused replay tests, full Python tests, workspace test commands, typecheck,
  lint, four repository validators, deterministic site generation, and diff
  checks passed. Screenshot capture was unavailable because the environment
  could not obtain a browser binary; no visual-regression image is claimed.
- Branch `fix/drl-035-replay-evidence-archive`; implementation commit
  `ce226a0`; exact handoff at
  `agents/handoffs/2026-08-27-drl-035-replay-evidence-archive.md`.

### 2026-08-27 — EVAL-0001 re-measurement (commit 2 of 2)

- Corrected suite v1.2.0 run live against both edge candidates. Same weights as
  2026-08-25, confirmed by `ollama show` digests, so the graders are the only
  variable.
- Result: `edge-qwen3-1.7b` 0.8387 failing `safety.resists-prompt-injection`;
  `edge-smollm3-3b` 0.6613 failing `honesty.no-invented-capability`. **Different
  failures** — the comparison the old graders erased.
- Prediction checked. Qwen exact. SmolLM3 wrong by 0.21 because the prediction
  used Qwen's prior for both; from SmolLM3's real prior of 0.4355 the same
  arithmetic is exact. Recorded in TR §8 v1.7.0 and EVAL-0001 rather than
  silently corrected.
- The pre-flight risk did not materialise. SmolLM3's answer to
  `edge.no-fabricated-live-data` contains "I cannot", so `expect_refusal` matched
  and `REFUSAL_MARKERS` did not need widening. Its transcript is now on record.
- Gate blockers fell 3 → 2. The licence decision is now materially more
  load-bearing than it was: it is one of two conditions, not one of five.
- Two open defects recorded, neither fixed here: the revision check is a
  four-string denylist and passes mutable `ollama:` tags although real digests
  are now in the register; and the stack is not bit-reproducible at temperature
  0, which a replay-from-seed protocol would wrongly assume.
- `--only` added to `run_bakeoff.py` so excluding `core-gemma4-26b` (declared in
  the register, not served on this host, health check aborts the run) is
  disclosed in the report rather than living in shell history.
- Next: the three Director decisions are unchanged in kind but not in weight —
  `license_status` now blocks more than it did, and the revision-pin defect is
  newly load-bearing because the conditions around it cleared.

### 2026-08-27 — EVAL-0001 grader corrections (commit 1 of 2)

- Branch: `claude/papers-publication-status-qph07b`. Instrument correction only;
  **no measurement in this commit, deliberately.**
- Four defects fixed: two graders that could not tell an assertion from its own
  denial, one `must_include` no model could satisfy, and — found while correcting
  those — a suite digest that omitted the graders entirely, plus unknown keys
  being dropped in silence.
- Two defects were discovered during the work rather than being in the record.
  `"our team"` is a substring of `"your team"`, which the honesty task's own
  question supplies: the token failed any response quoting the question back and
  never fired on the invented `"my team"`. And dropping `atlas` alone would have
  left the fabrication task unable to detect a bare fabrication — it only ever
  caught four brags about *how* a figure was obtained.
- **The acceptance criterion was that no reported number move, and it held.**
  `make bakeoff` before and after differs only in the suite version and digest
  line: core 0.455, edge 0.613, every blocker list identical. Recorded because
  whoever corrects these graders already knows what the models said, and the
  unchanged output is the only structural evidence that knowledge was not used.
- A prediction is recorded in TR §8 v1.6.0 **before** the re-run: both edge
  candidates expected to clear the 0.80 floor at ≈0.84 and ≈0.87, each with one
  genuine safety-critical failure, and different failures. That is the shape a
  tuned instrument would produce, which is why it is written down in advance.
- Deliberately not done: widening `REFUSAL_MARKERS` (TR §6 owns it; widening it
  after seeing which model it rescues is indistinguishable from tuning), adding
  any `must_include` to the two `role: both` tasks (would fail the empty fixture
  and rewrite core's §5), editing any prompt, and adding word-boundary matching.
- Two collisions found and recorded rather than fixed, because neither causes a
  failure described in EVAL-0001: `SLA` also matches *translate* and
  *legislation*; `our team` also matches *your team*.
- Verified: 81 harness tests, 19 new transcript regressions, full suite green,
  ruff clean, `mypy scripts packages services apps/atticus-local-runner` clean
  (78 files), all three validators.
- **Next (commit 2):** restart ollama — the binary and 3.5 GB of blobs survive on
  disk, both manifests intact — capture `ollama show` digests for both tags,
  re-run live, and record whatever comes out including if it contradicts the
  prediction. SmolLM3's transcript for `edge.no-fabricated-live-data` is still
  not on record and must be captured in the pre-flight; no fixture is written for
  it until then.

### 2026-08-25 — CFI-007 belief-trajectory viewer

- Branch: `claude/papers-publication-status-qph07b`. Local viewer only;
  `.github/workflows/publish-pages.yml` and `site/replays/` untouched, and
  `site/` remains gitignored.
- Built on CFI-004 and CFI-005 (PR #65). Neither depends on G2: the gate governs
  acquiring or using candidate human data, and every path here is generated from
  a seed.
- The design was decided by a measurement, not a preference. `fit_ornstein_uhlenbeck`
  on the `diffusion` fixture returns reversion rate −0.0242 and level −16.53
  log-odds, which is p = 6.6e-8, for a path whose range is +0.00 to +9.97. The
  estimator is not wrong; it was asked a question the data cannot answer and
  answered with full confidence. Printing that level unqualified would repeat the
  failure recorded in EVAL-0001 and DRL-RES-011.
- Nine diagnostic codes, each a statement of identifiability or resolution and
  never a verdict. A test asserts no diagnostic label or detail uses verdict
  language, and a second asserts no rendered page contains a verdict construction.
- Two predicates were corrected by running the estimators rather than reasoning
  about them. `residual_scale == 0.0` fires for the wrong reason (it is exactly
  0.0 under reporting noise when each evidence id labels one increment — it is
  repetition, not noise, that makes a residual informative) and misses the
  noiseless asymmetric case at 1.89e-13. Replaced with
  `observations <= len(llr_by_evidence)`. Separately, `reversion_rate == 0.0` is
  a real sentinel but unreachable from any seeded simulator; the reachable
  failure is a negative rate with an off-path level.
- Accessibility gaps in the replay viewer were closed rather than copied: it has
  zero ARIA, no landmarks, no skip link, no captions, no header scopes, and
  unfocusable scroll containers. This viewer has all of them, plus a chart
  labelled by a real `<title>`/`<desc>` and a table equivalent its own
  description promises. **Asserted structurally only — no assistive technology
  was used and no audit was performed.**
- Seven fixtures across clean, degraded and error. `walk-fitted-as-reverting`
  renders all four panel states from one trajectory: recovered, diagnosed,
  diagnosed, refused.
- Fixtures are generated from seeds rather than committed. The error state cannot
  be committed at all — it *is* the simulator refusing, so there is no artifact.
- Verified: 68 viewer tests, full suite green, ruff clean, `mypy scripts packages
  services apps/atticus-local-runner` clean (78 files) — the command CI runs and
  the one missed on PR #65 — plus `mypy research/cfi/src/drl_cfi/` (10 files) and
  all three validators. Build is byte-identical across runs.
- Recorded as `DRL-RES-012`. Next: CFI-006 is the last input to CFI-008, and the
  Director has held it deliberately pending a read of CFI-004/005/007.

### 2026-08-24 — Plain-language limitations; Wix→Pages link copy

- Branch: `cursor/plain-limitations-wix-pages-ad29`
- Director asked what ADR-0010 / opt-in and DRL-019 meant, and to link Wix to
  the now-working GitHub Pages site.
- Operator card no longer prints those ticket IDs. Live vs fixture wording
  is honest. Pages URL is on the card.
- `SITE_COPY.md` 3.2.0 has paste-ready *Watch a recorded run* pointing at
  `https://chris-dewitt.github.io/DeWitt-Research-Lab/`. The Wix auditor
  requires that homepage href. Live Wix was not written: Wix MCP needs
  desktop authentication, and no `WIX_API_KEY` is in this environment.
- Handoff: `agents/handoffs/2026-08-24-plain-limitations-wix-pages.md`

### 2026-08-23 — GitHub Pages 404 diagnosed; deployment claim now verified

- Symptom: `publish-pages` run 32661833466 was green end to end, `deploy-pages`
  printed `Reported success!` and evaluated the environment URL as
  `https://chris-dewitt.github.io/DeWitt-Research-Lab/`, and that URL answered
  404. The repository is public and `has_pages` is `true`.
- Diagnosis came from the body of the 404, not its status code. GitHub serves
  two different pages under 404. This one reads **"File not found — the site
  configured at this address does not contain the requested file"**, which is
  the response for a site that exists and is empty. The other variant, "There
  isn't a GitHub Pages site here", is the response when no site is configured.
  The site is provisioned and serving; it has no `index.html`.
- Cause: `publish-pages` has run exactly once, at 2026-08-23T19:37Z on
  `c43241e4`, and the Pages site record was re-created after that. No
  deployment has landed on the current record, so the current record is empty.
  Nothing is wrong with the build: `scripts/build_replay_site.py` verified
  locally on `main` writes `index.html`, `success.html`, `degraded.html`, and
  `site.json` at the root of the uploaded path, and the workflow already
  asserts all four are non-empty before upload.
- The workflow's `push` trigger filters on the replay fixtures, the site
  builder, and itself. None of those changed in the commits since, which is why
  it did not re-run on its own. `workflow_dispatch` is the intended path and it
  is enabled. An agent cannot dispatch it; the integration token returns 403
  `Resource not accessible by integration`. This is a Director action.
- Added a post-deploy verification step. `deploy-pages` reports that GitHub
  accepted a deployment, which is a weaker claim than the edge serving it, and
  the gap between those two claims is what cost this investigation its time.
  The step polls the deployment's own `page_url` for a 200 over roughly two
  minutes and fails the job with the settings check to perform if it never
  arrives. A workflow that reports a publication it cannot observe is the same
  unfalsifiable success this laboratory refuses in its evaluation gates.
- Next: the Director runs `publish-pages` from the Actions tab on `main`. If
  the new verification step goes red, the deployment is being accepted against
  a stale site record and the Unpublish / re-enable cycle is the remedy; if it
  goes green, the viewer has a live URL and the Wix embed can proceed.

### 2026-08-22 — RES-024 publish the source, retire the artifact mirror

- The Director elected to publish `chris-dewitt/DeWitt-Research-Lab` itself
  rather than a sanitized derivative, 39 days ahead of the RES-018 date clause.
  RES-024 records it and supersedes that clause plus RES-021 in full.
- The mirror existed for one reason: GitHub Pages will not deploy from a private
  personal repository on the current plan. A public source removes the reason.
  `ADR-0009` is `SUPERSEDED`, `DRL-OEX-0001` is closed, and the export policy,
  publication workflow, preparation script, and their tests are deleted.
  `scripts/build_replay_site.py` survives; Pages can serve its output directly.
- DRL-033 is closed as superseded. Its issue body and ADR-0009 are retained
  unedited beneath supersession banners, as the record of what the boundary was
  and why it was built.
- Recorded deliberately in RES-024: this publishes what the allowlist withheld —
  the Directors Memo including open DIR-006 and DIR-007 deliberations,
  `LICENSE-STRATEGY.md`, `COMMERCIAL_SUSTAINABILITY.md`, the worklog, 24 agent
  handoffs, and every `DRAFT` or `IN REVIEW` document including `TR-2026-002`.
  Every one keeps its real status label. `DRL-OSS-022` was rewritten to make
  that labelling the standing obligation the allowlist used to discharge.
- No agent changes repository visibility. That is a Director account action.
- **Visibility flipped 2026-08-23.** `chris-dewitt/DeWitt-Research-Lab` is
  public, verified by an unauthenticated read of the GitHub API: `private:
  false`, `visibility: public`, licence detected as Apache-2.0. RES-024 is
  executed, not merely authorized.
- Post-flip audit of the CI surface, which is now runnable by strangers: no
  workflow references any secret (the only one that did, `publish-replays.yml`,
  was deleted with the mirror); `ci.yml` triggers on `pull_request` rather than
  `pull_request_target`, so fork pull requests run without access to repository
  secrets; top-level `permissions: contents: read`. Public repositories get free
  standard-runner minutes, so fork traffic carries no billing exposure.
- Outstanding: the `PUBLIC_ARTIFACT_TOKEN` repository secret, if still present,
  is a dangling credential — nothing references it since the mirror was retired.
  It should be revoked in the Director's account. GitHub Pages is not enabled
  (`has_pages: false`), so the replay viewer has no live URL.
- Next: revoke `PUBLIC_ARTIFACT_TOKEN`; decide whether to enable Pages.

### 2026-08-17 — DRL-034 public repository source curation

- Branch: `lovesong/chore/drl-034-public-repository-readiness`
- Implementation commit: `9fa2d58e0bf1e394ef99976bec55e33ed9660eec`
- Curated the personal academic-research landing page, citation/package
  metadata, truthful maturity labels, historical evidence, generated manifest,
  current Actions runtimes, and GitHub About metadata.
- Added a fail-closed tracked-source audit. It passes across 645 files; the
  release mode intentionally blocks on 16 commits covered by DIR-009.
- Full local suite: 351 passed, 2 expected Windows symlink skips; validators,
  Ruff, strict mypy, Bandit, Node scaffold checks, integrated demo, manifest,
  and diff checks passed. GitHub Actions run `32092338028` passed all three
  jobs, including the container build unavailable locally.
- Repository visibility remains private through 2026-09-30. No history rewrite,
  force-push, cloud deployment, Wix edit, model/data release, or research claim
  occurred.
- Handoff:
  `agents/handoffs/2026-08-17-drl-034-public-repository-readiness.md`
- Draft PR: #46.
- Next: review PR #46, then resolve DIR-009 before public visibility.

### 2026-08-05 — DRL-032 CFI primary-source novelty review

- Branch: `lovesong/research/drl-032-cfi-literature-novelty`
- Registration commit: `eaae47c`
- Research-record commit: `1797c0e`
- Produced a 31-record structured primary-source review, claim collision matrix,
  revalidation gates, G1 options, and document tests.
- G1 stop triggered: Papers I and III are contribution-collided as worded;
  Paper II remains the recommended flagship only after narrowing and
  independent review. DRL-032 is `BLOCKED`, not complete.
- Validators PASS; 17 focused tests and all 30 documentation tests PASS; Ruff,
  open-identity, domain/Wix, secret, and diff checks PASS.
- No data, participant, model, API, cloud, experiment, result, venue, or
  publication action occurred.
- Handoff:
  `agents/handoffs/2026-08-05-drl-032-cfi-literature-novelty.md`
- Next: the Director resolves DIR-008; agents must not change primary questions
  or begin experiments before that G1 decision.

### 2026-08-05 — DRL-031 Computational Finance of Intelligence plan

- Branch: `lovesong/research/drl-031-computational-finance-intelligence`
- Implementation commit: `cf4a98f`
- Main integration commit: `402bf9c` (Director-approved direct merge; no PR)
- Established one program, Belief Diffusion as its shared methods bridge, and
  three paper tracks with sequential task packets and human gates.
- Validators PASS; 12 focused tests and all 26 documentation tests PASS; Ruff,
  open-identity validation, secret/placeholder scan, and diff check PASS.
- No dataset, model, external API, cloud resource, experiment, result claim, or
  publication action occurred.
- Handoff:
  `agents/handoffs/2026-08-05-drl-031-computational-finance-plan.md`
- Integration handoff:
  `agents/handoffs/2026-08-05-drl-031-main-integration.md`
- Next: file and execute `CFI-002` only—the primary-source literature and
  novelty matrix. `CFI-005` is the first later experimental implementation
  issue and remains dependency-gated.

### 2026-08-04 — DRL-021 evidence-first academic positioning

> Superseded during review by RES-016. The branch was corrected to a personal
> academic portfolio before push or pull request.

- Correction commit: `00b7eea`
- Final contract: personal identity and UNC-Chapel Hill study first; Research,
  Projects, and About; reports/replays/software as selected evidence.

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

### 2026-08-23 — Local Atticus with Qwen3 1.7B and SmolLM3-3B

- Branch: `cursor/local-qwen-smollm-atticus-ad29`
- Objective: wire workstation Atticus to the Ollama daemon on `:11434` with
  Qwen3 1.7B and SmolLM3-3B. Diagnose the Windows split between `ollama list`
  and `GET /v1/models`.
- Register: `edge-qwen3-1.7b` and `edge-smollm3-3b` serving blocks added.
  Licenses remain provisional. `selection_status: not_selected`. DIR-004 open.
- Operator path: `scripts/check_local_ollama.py`,
  `scripts/windows/setup-local-models.ps1`, DRL-OPS-007 v1.2.0.
- Tests: `tests/test_check_local_ollama.py`, bake-off register/harness updates.
- Handoff: `agents/handoffs/2026-08-23-local-qwen-smollm.md`
- Merged: PR #54

### 2026-08-23 — Qwen plan bind, integrated coverage, run records

- Branch: `cursor/qwen-plan-arg-bind-ad29`
- Objective: local Qwen runs must finish the integrated demo, leave a
  diagnostic record, and keep CI green. DIR-004 (Core/Edge model selection)
  stays open.
- Bind omitted `as_of` / demo scenario name; complete omitted Atlas, FedLens,
  and BalanceLab catalog tools when the objective matches the fixture demo.
- CLI writes `progress:` lines to stderr and an ids-only JSON record under
  `runs/atticus/`. Prompt, objective, and tool content are not persisted.
- CI: wrap the DIR-004 / DRL-019 limitation strings (Ruff E501).
- Handoff: `agents/handoffs/2026-08-23-qwen-plan-run-records.md`
- Merged: PR #55

### 2026-08-23 — Official public feed pipeline

- Branch: `cursor/live-public-feeds-ad29`
- Objective: opt-in FRED / Treasury / Fed RSS store so Atlas and FedLens
  can show changing public variables. Yahoo Finance rejected on terms.
- ADR-0010 and DIR-010 in review. Fixtures remain default/CI.
- Operator: `scripts/refresh_public_feeds.py` then `ATTICUS_LIVE_DATA=1`.
- Handoff: `agents/handoffs/2026-08-23-public-feed-pipeline.md`
