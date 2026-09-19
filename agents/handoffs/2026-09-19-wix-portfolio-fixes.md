---
document_id: DRL-HO-WEB-20260919-PORTFOLIO
title: "Handoff: Wix portfolio redirect, SEO, and remaining editor fixes"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-19
---


# Handoff: Wix portfolio redirect, SEO, and remaining editor fixes

## 1. Branch and last commit

- Branch: `cursor/website-portfolio-fixes-f70f`
- Base: `origin/main`
- Prepared UTC: `2026-09-19`

## 2. Objective completed

- Replaced live redirect `/projects` → `/research` with `/projects` → `/work`
  (also `/projects-1` → `/work`).
- Applied Home/About SEO meta (superseding earlier option B): light academic
  signal without naming MADS/UNC. Research SEO title set to
  `Research | Chris DeWitt`.
- Synced controlled docs and the Wix auditor with live slug/SEO reality.
- Wrote paste pack for remaining Studio editor body-copy (hero, GitHub URL,
  footer, privacy, research cards, projects clarification).

## 3. Files and interfaces changed

- Live Wix (API): SEO Redirects + Item SEO Tags for static pages `c1dmp`,
  `xgi96`, `p0nvs`.
- Repo: `docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md` (new),
  `SITE_COPY.md`, `WIX_SITE_BUILD_PLAN.md`, `WIX_EDITOR_HANDOFF_CHECKLIST.md`,
  `scripts/audit_wix_site.py`, `tests/test_wix_auditor.py`, `WORKLOG.md`,
  `DIRECTORS_MEMO.md`, this handoff.

## 4. ADRs created or needed

None. SEO meta wording is a Director choice under RES-016, not a new ADR.

## 5. Tests and results

```bash
python -m pytest tests/test_wix_auditor.py -q
```

(Run on this branch before merge.)

Live checks:

- `GET /projects` → `301 Location: /work`
- Home/About meta: light graduate-student line without MADS/UNC

## 6. Deployment or migration notes

Redirects take effect without a Wix site publish. SEO tag writes used
`publish: true`. Body-copy items still require Editor → Publish.

## 7. Known failures and risks

- Studio page body cannot be edited via the Wix MCP; editor login blocked this
  agent. Items #3–#9 remain in `WIX_REMAINING_EDITOR_FIXES.md`.
- `/work` remains the Projects slug; renaming the page slug to `/projects` in
  the editor would be a separate Director choice (would recreate PAGE_SLUG_RENAME
  redirects).

## 8. Uncommitted or generated artifacts

Screenshots under `/opt/cursor/artifacts/screenshots/` (not in git).

## 9. Next dependency-unblocking task

Director opens the Wix editor and applies
`docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md`, then Publishes.

## 10. Exact reading order for the next agent

1. This handoff
2. `docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md`
3. Live: `https://www.dewitt-labs.com/projects` → `/work`
4. Live Home/About `<meta name="description">` for the light graduate-student line
5. `scripts/audit_wix_site.py` if re-auditing
