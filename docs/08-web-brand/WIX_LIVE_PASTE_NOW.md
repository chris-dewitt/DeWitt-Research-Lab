---
document_id: DRL-WEB-025
title: "Wix Live Paste Now (Director — do these in Studio)"
version: 1.2.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Do this in Wix Studio now

You are editing `www.dewitt-labs.com`. **Embedded code is carrying most of the
remaining polish live** — hard-refresh before you paste. Studio pastes below
are only what embeds cannot permanently own (new page, structural delete,
permanent Text settings).

No Chapel Hill / MADS in public body copy. Keep UNC Charlotte on About.

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
| Footer mailto + GitHub + Privacy (panel until `/privacy` exists) | Helpers rev 4 |

Hero already shows **Chris DeWitt** above the thesis on the live site.

---

## Still paste / do in Studio (short list)

### 1. Privacy page (must be Studio — embeds cannot create a route)

Create page slug `/privacy` with:

```text
Privacy

This is an independent personal academic portfolio operated by Christopher Noxon
DeWitt. It is not a laboratory, institute, or employer site.

Contact and inquiry mail goes to director@dewitt-labs.com. Do not send secrets,
credentials, or employer-confidential material.

Wix may process ordinary hosting and traffic metadata for the site. Prefer
minimal analytics. Application subdomains and research-trace donation, if any,
are separate purposes and need their own consent.

No employer name, customer data, or private traces belong on this site.
```

Until that page exists, the helpers embed’s **Privacy** footer link opens a
panel (`#cd-privacy`) with the same copy. After the page ships, retarget the
footer Privacy link to `/privacy` and we can disable the panel.

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

**Publish**, hard-refresh. Ping for re-verify of `/privacy` and permanent
subtitle transform.
