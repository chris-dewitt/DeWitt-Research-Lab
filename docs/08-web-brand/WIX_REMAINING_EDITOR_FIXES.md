---
document_id: DRL-WEB-024
title: "Wix Remaining Editor Fixes (Director Paste Pack)"
version: 1.8.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Wix remaining editor fixes

**Right now:** follow `docs/08-web-brand/WIX_LIVE_PASTE_NOW.md` while
you are in Studio. Most interim polish is **already live via embeds**. This
file is the longer ledger + what still must be Studio.

**2026-09-20 nav fix:** enrichment `0505c503-…` **rev 7** no longer hides
Research/Work `<header>` comps (`comp-msfldjxx` / `comp-mswd0roa`). Hard-refresh
`/research` and `/work` to confirm nav.

Director decisions (2026-09-20): keep nav label **PROJECTS** (`/work` slug
stays); Chapel Hill / MADS stay softened/removed from public body; home hero
gets **name above thesis** + hard gap kill; monorepo line softens (not deletes);
Research intro drops “not peer-reviewed / not coursework”; footer + GitHub +
privacy via embeds first, permanent Studio when ready.

## Embed vs Studio (blunt)

| Item | Via embeds now? | Must stay Studio? |
| --- | --- | --- |
| Hero name above thesis | Already on live DOM | Optional permanent paste |
| Subtitle And / capitalize CSS | Softener `uncapHero` | Permanent Text transform → None |
| Chapel Hill / MADS strip | Softener TreeWalker | Permanent About/Home paste |
| Home gap under CTAs | Gap V4 CSS/JS | Delete empty strip if void remains |
| GitHub `http://www.github…` | Helpers href rewrite | Permanent link edit |
| About `ABOUT CHRIS` | Helpers TreeWalker | Permanent heading paste |
| Footer mailto / GitHub / Privacy | Helpers (Privacy = panel) | Create `/privacy` page; permanent footer |
| Research / Projects tone | Enrichment panels | Optional permanent paste |
| New `/privacy` route | No (404 today) | **Yes — create page** |

## Already applied via API

- `/projects` → `/work`; `/projects-1` → `/work`.
- Home/About SEO (no MADS/UNC in meta). Research title `Research | Chris DeWitt`.
- Enrichment embed `0505c503-…` **rev 7**: Research/Projects panels + tone;
  hide lists exclude page HEADER comps (nav restore); `isChrome()` guard;
  MARK `dewitt-status-enrich-v3`.
- Softener `8d0df783-…` **rev 11**: TreeWalker text nodes; Chapel Hill/MADS
  strip; And-fix pairs; **`uncapHero` forces `text-transform: none`** on the
  hero subtitle. UNC Charlotte preserved.
- Homepage cleanup `4ebc7135-…` **rev 8**: `DL_HOME_GAP_V4` + empty section
  collapse between hero CTAs and “Why complex systems?”.
- Home open-weight thesis embed `73d6abb6-…` rev 2 still live.
- **Studio paste helpers** `b21ad726-…` **rev 4** (BODY_END): leaf-safe
  TreeWalker / document-fragment patterns only (no container `textContent`
  flatten). Fixes bad GitHub hrefs; About heading; footer mailto + GitHub +
  Privacy panel (`#cd-privacy`) until `/privacy` exists.

Nav label remains **PROJECTS** → `/work`. `/projects` redirects there.

## Studio remaining (see `WIX_LIVE_PASTE_NOW.md`)

1. Create `/privacy` page (required for a real route).
2. Hero subtitle Text transform → None (permanent).
3. Optional: delete empty hero strip; permanent hero/About/footer paste when
   ready to retire embeds.

## Verify after publish / hard-refresh

1. Home first viewport shows **Chris DeWitt** above the thesis.
2. Subtitle is `Forecast engineer and graduate student. Charlotte…` (no Chapel
   Hill, no title-case **And**).
3. No huge black void between hero CTAs and “Why complex systems?”.
4. Research intro has no “not peer-reviewed / not coursework”.
5. Projects card says *Monorepo · a project in this portfolio*.
6. Footer: mailto, GitHub, Privacy (panel or `/privacy`).
7. No live `http://www.github.com/chris-dewitt` hrefs.
8. About heading is not `ABOUT CHRIS`.
9. `/projects` still lands on Projects (`/work`).
