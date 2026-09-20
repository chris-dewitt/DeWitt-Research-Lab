---
document_id: DRL-HO-WEB-20260920-POLISH
title: "Handoff: Portfolio polish — paste pack + softened embeds"
version: 1.1.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Handoff: Portfolio polish — paste pack + softened embeds

## 1. Branch and last commit

- Final PR branch: `cursor/website-portfolio-polish-f70f` (legacy non-conforming name; no compliant rename was recorded before merge)
- Base: `origin/main`
- Commit: `6a2077a` — `docs(web): softener uncapHero note and paste-pack Text-transform fix`

## 2. Objective completed

Director answered: PROJECTS label; soften/remove Chapel Hill; home B+C (gap +
name); softer monorepo; footer paste now; Research softened; big chunk.

API embeds updated. Softener rev 11 also clears capitalize CSS so And-fix
shows. Studio paste pack written for the Director who is live in Wix.

## 3. Files and interfaces changed

**Live Wix**

- Enrichment `0505c503-…` → rev **4** (Research/Projects tone)
- Softener `8d0df783-…` → rev **11** (And-fix + Chapel Hill strip + `uncapHero`
  `text-transform: none`)
- Gap cleanup `4ebc7135-…` → rev **8** (`DL_HOME_GAP_V4`)

**Repo**

- `docs/08-web-brand/WIX_LIVE_PASTE_NOW.md` (DRL-WEB-025) 1.1.0 — do-this-now pack
  (includes Text transform → None note)
- `WIX_REMAINING_EDITOR_FIXES.md` 1.6.0, `SITE_COPY.md` 3.8.0
- `WORKLOG.md`, `DIRECTORS_MEMO.md` 1.23.0, this handoff

## 4. ADRs

None.

## 5. Tests

```text
uv run python scripts/validate_foundation.py
→ VALIDATION PASSED
```

Browser (CDP, hard-refresh): Home `Forecast engineer and graduate student`
with computed `text-transform: none`; Research softened intro (no peer-reviewed
apology); Work `a project in this portfolio`; `DL_HOME_GAP_V4` present.
Screenshots: `/opt/cursor/artifacts/screenshots/verify-*-v11.png`.

## 6. Deployment

Embeds apply on next render (no Studio Publish required for embeds). Studio
pastes need Director **Publish**.

## 7. Known failures / risks

- Gap may still need Studio delete of an empty strip even with V4 CSS/JS.
- Softener is temporary; permanent paste must set subtitle Text transform to
  None or capitalize returns when embeds are disabled.
- Generic softener pair ` And ` → ` and ` is broad; watch for odd mid-sentence
  casing elsewhere (unlikely on this site).
- `gh` / integration token cannot create PRs (403); open PR from GitHub UI if
  ManagePullRequest is unavailable.

## 8. Artifacts

Screenshots under `/opt/cursor/artifacts/screenshots/` (not committed).

## 9. Next

Director finishes `WIX_LIVE_PASTE_NOW.md` (hero + Text transform None, footer,
GitHub, privacy, About), Publishes, pings agent to re-verify.

## 10. Reading order

1. This handoff
2. `WIX_LIVE_PASTE_NOW.md`
3. `WIX_REMAINING_EDITOR_FIXES.md`
4. Live site hard-refresh
