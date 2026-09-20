---
document_id: DRL-HO-WEB-20260920-POLISH
title: "Handoff: Portfolio polish — paste pack + softened embeds"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Handoff: Portfolio polish — paste pack + softened embeds

## 1. Branch and last commit

- Branch: `cursor/website-portfolio-polish-f70f`
- Base: `origin/main`
- Prepared UTC: `2026-09-20`

## 2. Objective completed

Director answered: PROJECTS label; soften/remove Chapel Hill; home B+C (gap +
name); softer monorepo; footer paste now; Research softened; big chunk.

API embeds updated immediately. Studio paste pack written for the Director who
is live in Wix.

## 3. Files and interfaces changed

**Live Wix**

- Enrichment `0505c503-…` → rev **4** (Research/Projects tone)
- Softener `8d0df783-…` → rev **10** (And-fix + Chapel Hill strip)
- Gap cleanup `4ebc7135-…` → rev **8** (`DL_HOME_GAP_V4`)

**Repo**

- `docs/08-web-brand/WIX_LIVE_PASTE_NOW.md` (DRL-WEB-025) — do-this-now pack
- `WIX_REMAINING_EDITOR_FIXES.md` 1.5.0, `SITE_COPY.md` 3.7.0
- `WORKLOG.md`, `DIRECTORS_MEMO.md` 1.23.0, this handoff

## 4. ADRs

None.

## 5. Tests

```text
uv run python scripts/validate_foundation.py
```

(Run before merge.) Softener unit checks for And-fix + UNC Charlotte preserve.

## 6. Deployment

Embeds apply on next render. Studio pastes need Director **Publish**.

## 7. Known failures / risks

- Gap may still need Studio delete of an empty strip even with V4 CSS/JS.
- Softener is temporary; permanent paste should match softened copy.
- Generic softener pair ` And ` → ` and ` is broad; watch for odd mid-sentence
  casing elsewhere (unlikely on this site).

## 8. Artifacts

None committed.

## 9. Next

Director finishes `WIX_LIVE_PASTE_NOW.md`, Publishes, pings agent to re-verify
Home/About/Research/Work + footer links.

## 10. Reading order

1. This handoff
2. `WIX_LIVE_PASTE_NOW.md`
3. `WIX_REMAINING_EDITOR_FIXES.md`
4. Live site hard-refresh
