---
document_id: DRL-HO-WEB-20260920-NAV
title: "Handoff: Restore Research/Work header nav (enrichment hide lists)"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Handoff: Restore Research/Work header nav

## 1. Branch and last commit

- Final PR branch: `cursor/website-portfolio-polish-f70f` (legacy non-conforming name; no compliant rename was recorded before merge)
- Base: `origin/main`
- Commit: `bda0a23` — `fix(web): restore Research/Work header nav after enrichment hide bug`
- PR: https://github.com/chris-dewitt/DeWitt-Research-Lab/pull/76
- Live embed: Research/Projects status enrichment `0505c503-…` → **rev 7**

## 2. Objective completed

Urgent live bug: `/research` (and `/work`) had no header/navigation.
Root cause and embed fix verified in browser.

## 3. Root cause

Enrichment BODY_END `0505c503-cd89-425e-8b35-da977b7cc2b3` hide lists
accidentally included the **page HEADER components themselves**:

- Research: `comp-msfldjxx` = `<header>` (nav: Home / Research / Projects / …)
- Work: `comp-mswd0roa` = `<header>` (same nav)

`hideOriginals()` + generated CSS set those to `display:none`, so the chrome
disappeared. Home was unaffected (different header id `comp-mb7ogqrp`).

## 4. Fix (live embed)

- Removed `comp-msfldjxx` from `RESEARCH_HIDE` and `comp-mswd0roa` from
  `WORK_HIDE`.
- Added `isChrome()` guard so `kill()` never hides `HEADER`/`NAV`/`FOOTER` /
  known site-chrome ids.
- CSS hide builder filters the same ids.
- Bumped panel MARK to `dewitt-status-enrich-v3` and clears v1/v2 roots/CSS.
- Fixed a transient syntax error from a mangled `querySelector` escape in an
  intermediate patch (rev 6); rev **7** uses a quote-safe `isChrome`.

## 5. Tests and results

CDP / headless Chrome @ 1440×900, cache disabled:

- `/research`: header visible (`HOME RESEARCH PROJECTS ABOUT BLOG`); enrichment
  v3 root mounted; `cd-enrich-research`; hide CSS does not mention header ids.
- `/work`: same; `cd-enrich-work`; enrichment mounted.
- Script `new Function(...)` syntax OK.

Screenshots:

- Before: `/opt/cursor/artifacts/screenshots/before-research-nav.png`,
  `before-research-nav-bug.png`, `before-work-nav-bug.png`
- After: `/opt/cursor/artifacts/screenshots/after-research-nav.png`,
  `after-work-nav.png`

## 6. Files / ADRs

- Repo: `WORKLOG.md`, `docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md`,
  `docs/08-web-brand/SITE_COPY.md`, this handoff.
- ADRs: none.

## 7. Known risks

- Enrichment still hides original Studio cards by id list; if Studio rebuilds
  comps, ids may drift (re-audit hide lists; never include `HEADER`).
- Softener / helpers unchanged this pass.

## 8. Next

Continue Director paste pack (`WIX_LIVE_PASTE_NOW.md`); create `/privacy` page.
No further nav action needed unless Studio reassigns header component ids.

## 9. Reading order for next agent

1. This handoff
2. Live hard-refresh: `/research`, `/work`
3. `docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md`
4. Prior polish handoff `agents/handoffs/2026-09-20-wix-portfolio-polish.md`
