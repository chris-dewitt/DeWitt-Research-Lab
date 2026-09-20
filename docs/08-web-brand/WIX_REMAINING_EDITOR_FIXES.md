---
document_id: DRL-WEB-024
title: "Wix Remaining Editor Fixes (Director Paste Pack)"
version: 1.5.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Wix remaining editor fixes

**Right now:** follow `docs/08-web-brand/WIX_LIVE_PASTE_NOW.md` while you are in
Studio, then Publish. This file keeps the longer pack and the API ledger.

Director decisions (2026-09-20): keep nav label **PROJECTS** (`/work` slug
stays); Chapel Hill / MADS stay softened/removed from public body; home hero
gets **name above thesis** + hard gap kill; monorepo line softens (not deletes);
Research intro drops “not peer-reviewed / not coursework”; footer + GitHub +
privacy paste now.

## Already applied via API

- `/projects` → `/work`; `/projects-1` → `/work`.
- Home/About SEO (no MADS/UNC in meta). Research title `Research | Chris DeWitt`.
- Enrichment embed `0505c503-…` **rev 4**: Research intro softened (no
  peer-reviewed/coursework apology); Projects monorepo line → *Monorepo · a
  project in this portfolio*; work intro leads with personal projects.
- Softener `8d0df783-…` **rev 10**: TreeWalker text nodes; Chapel Hill/MADS
  strip; `Forecast Engineer And …` → lowercase and; UNC Charlotte preserved.
- Homepage cleanup `4ebc7135-…` **rev 8**: `DL_HOME_GAP_V4` + stronger empty
  section collapse between hero CTAs and “Why complex systems?”.
- Home open-weight thesis embed `73d6abb6-…` rev 2 still live.

Nav label remains **PROJECTS** → `/work`. `/projects` redirects there.

## 1. Home hero (#3, #8)

See `WIX_LIVE_PASTE_NOW.md` §1. Paste name + softened subtitle + shorter body.
Delete the empty strip under the CTAs in the editor if the gap CSS does not
fully clear it.

## 2. GitHub URL (#4)

`https://github.com/chris-dewitt` everywhere (not `http://www.github.com/...`).

## 3. Footer (#5)

See `WIX_LIVE_PASTE_NOW.md` §3 — mailto + GitHub + Privacy.

## 4. Privacy page

See `WIX_LIVE_PASTE_NOW.md` §4 — slug `/privacy`.

## 5. About

See `WIX_LIVE_PASTE_NOW.md` §5 — heading `About`; no Chapel Hill; keep UNC
Charlotte pride.

## 6. Research / Projects permanent paste (optional)

Embeds already show softened panels. Prefer pasting the same facts into Studio
text later so embeds can be disabled.

## Verify after publish

1. Home first viewport shows **Chris DeWitt** above the thesis.
2. Subtitle is `Forecast engineer and graduate student. Charlotte…` (no Chapel
   Hill, no title-case **And**).
3. No huge black void between hero CTAs and “Why complex systems?”.
4. Research intro has no “not peer-reviewed / not coursework”.
5. Projects card says *Monorepo · a project in this portfolio*.
6. Footer: clickable mailto, GitHub, Privacy.
7. `/projects` still lands on Projects (`/work`).
