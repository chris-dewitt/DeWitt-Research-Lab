---
document_id: DRL-HO-WEB-20260827-REPLAYS
title: "Handoff: DRL-035 recorded-runs evidence archive"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-27
---

# Handoff: DRL-035 recorded-runs evidence archive

## 1. Branch and last implementation commit

- Issue: DRL-035 (rebuild the recorded-runs page as an accessible evidence
  archive), GitHub issue #68.
- Branch: `fix/drl-035-replay-evidence-archive`.
- Last implementation commit: `ce226a0`.
- Pull request: to be opened after this handoff commit is pushed.

## 2. Objective completed

The public GitHub Pages replay viewer is rebuilt as a responsive DeWitt
Research Laboratory evidence archive. The success run is presented as the
baseline workflow and the degraded run as the resilience test. Visitors can
inspect the execution trace, evidence lineage, limitations, and provenance
without mistaking the page for live inference or market analysis.

## 3. Files and interfaces changed

- `services/evalforge/src/evalforge_service/replay_site.py`: new self-contained
  visual system; shared masthead/navigation/footer; index and replay hero
  summaries; stronger run comparison; direct research/source routes; semantic
  landmarks; keyboard-reachable data regions; captioned and scoped tables.
- `tests/test_replay_site.py`: public identity, landmark, table accessibility,
  and non-colour-only status assertions.
- `WORKLOG.md`: DRL-035 reservation and active scope.

No signed replay bundle, manifest, evaluation result, workflow, or deployment
configuration changed.

## 4. ADRs created or needed

None. This is a presentation and accessibility correction to the existing
static GitHub Pages viewer. It does not change the publication topology,
signature contract, replay schema, or public-service boundary.

## 5. Tests and exact results

- `uv run pytest tests/test_replay_site.py -q` — 26 passed.
- `uv run ruff check services/evalforge/src/evalforge_service/replay_site.py tests/test_replay_site.py`
  — passed.
- `uv run mypy services/evalforge/src/evalforge_service/replay_site.py tests/test_replay_site.py`
  — passed with no issues.
- `make docs-check program-check open-check public-check` — all four validators
  passed; 381 controlled documents, 132 requirements, 122 work packages,
  26/26 schemas/examples, and 701 tracked files inspected.
- `uv run pytest -q` — full Python suite passed.
- `pnpm -r test` — all declared workspace test commands completed; both UI
  workspaces remain explicit implementation-pending shells.
- `make replay-site` — generated non-empty `index.html`, `success.html`,
  `degraded.html`, and `site.json` after verifying both signed bundles.
- `git diff --check` — passed.

Generated HTML was inspected structurally. Automated screenshot capture was
attempted, but this environment could not obtain a browser binary from the
upstream browser archive; no visual-regression screenshot is claimed.

## 6. Deployment or migration notes

Merging the pull request into `main` retriggers `.github/workflows/publish-pages.yml`
because `replay_site.py` changed. That workflow verifies the bundles, rebuilds
the static viewer, deploys GitHub Pages, and checks that the published URL
returns HTTP 200. No DNS, Wix, database, runtime service, or migration action is
required.

## 7. Known failures and risks

- Visual hierarchy and responsive CSS have structural and generated-output
  evidence but no captured browser screenshot in this handoff.
- The viewer links to the current `www.dewitt-labs.com` research and about
  routes. If the replacement canonical site changes those slugs, update the
  viewer links in the same release as that site change.
- The demo HMAC key proves structural integrity only; every page continues to
  say it is not a production signing identity.

## 8. Uncommitted or generated artifacts

`site/replays/` is generated and gitignored. No generated viewer output should
be committed. The worktree should be clean after this handoff commit.

## 9. Next dependency-unblocking task

Review and merge the pull request. Then verify the `publish-pages` workflow and
the live success and degraded routes. After publication, update the replacement
`dewitt-labs.com` site to point its primary recorded-run action at the archive.

## 10. Exact reading order for the next agent

1. GitHub issue #68.
2. This handoff.
3. `services/evalforge/src/evalforge_service/replay_site.py`.
4. `tests/test_replay_site.py`.
5. `.github/workflows/publish-pages.yml`.
6. The terminal status and logs of the post-merge `publish-pages` run.
