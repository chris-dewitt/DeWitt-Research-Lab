---
document_id: DRL-WEB-025
title: "Wix Live Paste Now (Director — do these in Studio)"
version: 1.3.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Do this in Wix Studio now

You are editing `www.dewitt-labs.com`. **Embedded code is carrying most of the
remaining polish live** — hard-refresh before you paste. Studio pastes below
are only what embeds cannot permanently own (new page, structural delete,
permanent Text settings).

No Chapel Hill / MADS in public body copy (per RES-016 (which defines the site
as Christopher Noxon DeWitt's personal academic portfolio). Keep UNC Charlotte
on About.

---

## Already live via embeds (no paste required for interim look)

| Fix | Embed |
| --- | --- |
| Chapel Hill / MADS strip + And-fix + subtitle `text-transform: none` | Softener `8d0df783-…` rev 11 |
| Research / Projects softened panels (+ header nav restore on `/research` and `/work`) | Enrichment `0505c503-…` rev 7 |
| Home gap collapse between CTAs and “Why complex systems?” | Cleanup `4ebc7135-…` rev 8 (`DL_HOME_GAP_V4`) |
| Open-weight thesis block | `73d6abb6-…` rev 2 |
| Bad GitHub href → `https://github.com/chris-dewitt` | **Helpers** `b21ad726-…` rev 4 |
| About heading `ABOUT CHRIS` → `About` (TreeWalker) | Helpers rev 4 |
| Footer mailto + GitHub | Helpers rev 5 (Privacy link and panel removed) |

Hero already shows **Chris DeWitt** above the thesis on the live site.

---

## Still paste / do in Studio (short list)

### 1. Remove the footer Privacy link and panel

The Director retired `/privacy` on 2026-09-20: no page, no footer link, no
interim panel. Helpers embed `b21ad726-…` goes to **rev 5**, which drops the
Privacy anchor and the `#cd-privacy` panel and leaves the footer as mailto plus
GitHub.

Nothing needs creating in Studio for this. If a Privacy link was already pasted
permanently into the footer, delete it there too, or the embed will be removing
a link the editor keeps putting back.

### 2. Permanent Text transform (hero subtitle)

Select `Forecast engineer and graduate student…` → **Text transform → None**.
Softener already forces this live; Studio must match or capitalize returns when
embeds are removed.

### 3. Optional: delete empty strip under hero CTAs

If a black void remains after hard-refresh, delete/collapse the empty section
in the editor (gap CSS V4 already tries).

### 4. Optional permanent paste (when you want embeds off)

- Hero body / About body from the longer pack in
  `WIX_REMAINING_EDITOR_FIXES.md` / `SITE_COPY.md`
- Footer copy as native Studio text + links (helpers already cover interim)
- Research / Projects panel facts into Studio text (enrichment already covers)

### 5. Publish

**Publish**, hard-refresh. Ping for re-verify that the footer carries mailto
and GitHub only, and that the hero subtitle transform is permanent.
