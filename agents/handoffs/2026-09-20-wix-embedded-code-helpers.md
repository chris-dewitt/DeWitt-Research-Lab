---
document_id: DRL-HO-WEB-20260920-EMBEDS
title: "Handoff: Embedded-code helpers for remaining Studio polish"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Handoff: Embedded-code helpers for remaining Studio polish

## 1. Branch and last commit

- Final PR branch: `cursor/website-portfolio-polish-f70f` (legacy non-conforming name; no compliant rename was recorded before merge)
- Base: `origin/main`
- Commit: `5d8a5c8` — `docs(web): embedded-code helpers shrink Studio paste pack`

## 2. Objective completed

Director said “New idea: Embedded code” mid-Studio edit. Interpreted as: move
more remaining polish into BODY_END/HEAD custom embeds so he pastes less.

Shipped **Studio paste helpers** embed live; shrunk paste pack to Studio-musts.

## 3. Files and interfaces changed

**Live Wix**

- New BODY_END embed `Studio paste helpers (GitHub/About/footer/privacy)`
  id `b21ad726-f151-48ec-894e-b87aba691d2d` **rev 4**
  - Fix `http://www.github.com/chris-dewitt` → `https://github.com/chris-dewitt`
  - TreeWalker: `ABOUT CHRIS` → `About`
  - Footer: leaf-safe mailto wrap; inject GitHub + Privacy links
  - Privacy panel via `#cd-privacy` until `/privacy` page exists
  - No container `textContent` flatten (TreeWalker / document-fragment only)

**Already live (unchanged this pass)**

- Softener `8d0df783-…` rev 11, enrichment `0505c503-…` rev 4, gap
  `4ebc7135-…` rev 8, open-weight `73d6abb6-…` rev 2

**Repo**

- `docs/08-web-brand/WIX_LIVE_PASTE_NOW.md` 1.2.0 — embed vs Studio table
- `WIX_REMAINING_EDITOR_FIXES.md` 1.7.0, `SITE_COPY.md` 3.9.0
- `WORKLOG.md` 4.36.0, `DIRECTORS_MEMO.md` 1.24.0, this handoff

## 4. ADRs

None.

## 5. Tests

```text
uv run python scripts/validate_foundation.py
→ (run on commit)
```

Headless Chrome: bad GitHub hrefs cleared; About no longer shows `ABOUT CHRIS`;
footer GitHub/Privacy links present; `#cd-privacy` opens privacy panel.
Screenshots under `/opt/cursor/artifacts/screenshots/helpers-*.png`.

## 6. Deployment

Embeds apply on next render (no Studio Publish required for embeds). Creating
`/privacy` and permanent Text transform need Director **Publish**.

## 7. Known failures / risks

- `/privacy` is still 404 — Privacy link uses panel interim.
- Helpers are temporary; permanent Studio paste should eventually retire them.
- Gap may still need Studio delete of an empty strip.
- Softener capitalize fix is temporary until Studio Text transform → None.
- Hero name already on live DOM; no inject attempted (avoids layout risk).

## 8. Artifacts

Screenshots (not committed): `helpers-home-footer.png`,
`helpers-about-heading.png`, `helpers-home-footer-scroll.png`,
`helpers-privacy-panel.png`.

## 9. Next

Director creates `/privacy`, sets hero subtitle Text transform → None,
optional empty-strip delete, Publishes; agent re-verifies route + permanent
settings.

## 10. Reading order

1. This handoff
2. `docs/08-web-brand/WIX_LIVE_PASTE_NOW.md`
3. `docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md`
4. Live hard-refresh: Home footer links, About heading, `#cd-privacy`
