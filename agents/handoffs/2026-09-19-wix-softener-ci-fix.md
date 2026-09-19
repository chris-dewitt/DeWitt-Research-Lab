---
document_id: DRL-HO-WEB-20260919-SOFTENER
title: "Handoff: Softener v6 + PR #74 CI document_id fix"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-19
---


# Handoff: Softener v6 + PR #74 CI document_id fix

## 1. Branch and last commit

- Branch: `cursor/website-portfolio-fixes-f70f`
- Base: `origin/main`
- PR: https://github.com/chris-dewitt/DeWitt-Research-Lab/pull/74
- Prepared UTC: `2026-09-19`

## 2. Objective completed

- Fixed PR #74 CI failure (`Duplicate document_id DRL-WEB-023`) by assigning
  `WIX_REMAINING_EDITOR_FIXES.md` → **DRL-WEB-024** (Research page copy keeps
  DRL-WEB-023).
- Fixed live Home/About wreckage from softener rev 5 (container `textContent`
  flattened the DOM into a raw text dump). Emergency-disabled, then published
  rev 7: TreeWalker text-node rewrite only.
- Softened Chapel Hill / MADS visible copy; preserved UNC Charlotte; cleaned
  punctuation debris; raised length gate so About paragraphs are rewritten.
- Strengthened homepage gap CSS (`DL_HOME_GAP_V2` on cleanup embed rev 6).

## 3. Files and interfaces changed

**Live Wix (metaSiteId `e9a5dda4-53c7-46c2-8600-cc2a6fecf4e8`):**

- Softener BODY_END `8d0df783-b31a-4c18-8cdc-3cf006e3e3a6` → revision `9`,
  enabled, `createTreeWalker` / `nodeValue` only (comma + period hero variants;
  clean pairs array — rev 8 inject had a missing comma).
- Homepage cleanup HEAD `4ebc7135-9a6f-44e8-b9f9-a2056ed92e88` → revision `7`,
  `DL_HOME_GAP_V3` + empty-section collapse JS.

**Repo:**

- `docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md` (DRL-WEB-024, 1.4.0;
  softened hero paste pack)
- `docs/08-web-brand/SITE_COPY.md` (3.6.0)
- `WORKLOG.md`, `DIRECTORS_MEMO.md`, this handoff

## 4. ADRs created or needed

None.

## 5. Tests and results

```text
uv run python scripts/validate_foundation.py
→ VALIDATION PASSED
  Controlled documents: 392
```

Browser (computer-use):

- Home/About layouts restored (not text dumps).
- About: Chapel Hill removed; UNC Charlotte kept.
- Home: Chapel Hill / `Student, .` debris gone.
- Research/Work enrichment still OK.
- Screenshots: `/opt/cursor/artifacts/screenshots/home-after-softener6.webp`,
  `about-after-softener6.webp`, `research-after-softener6.webp`,
  `work-after-softener6.webp`.

Incident evidence (do not regress): `home-after-softener5.webp` shows the
flattened dump from rev 5.

## 6. Deployment or migration notes

Custom embeds apply on next render; no Studio Publish required for softener or
gap CSS. Permanent Studio paste of softened hero copy still preferred so the
softener is not the only defense.

## 7. Known failures and risks

- Homepage may still show some vertical air below the hero; gap CSS is
  aggressive but Wix mesh min-heights can fight it. Permanent Studio layout
  edit is the durable fix.
- Hero subtitle may appear title-cased via Wix `text-transform` (“And”).
- Softener must never assign `textContent` on non-leaf containers again.
- Editor-only remaining: hero density (#3/#8), GitHub URL (#4), footer/privacy
  (#5) — see paste pack.

## 8. Uncommitted or generated artifacts

Screenshots under `/opt/cursor/artifacts/screenshots/` (not in git).

## 9. Next dependency-unblocking task

Director pastes softened hero + GitHub + footer from
`docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md`, Publishes, then may disable
softener/enrichment embeds once Studio copy matches.

## 10. Exact reading order for the next agent

1. This handoff
2. `docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md`
3. `docs/08-web-brand/SITE_COPY.md` (live status)
4. PR #74 CI status
5. Live spot-check Home/About for Chapel Hill and layout integrity
