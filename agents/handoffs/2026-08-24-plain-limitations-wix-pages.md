---
document_id: DRL-HO-OPS-20260824-PAGES
title: "Handoff: Plain-language demo card and Wix→Pages link"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-24
---


# Handoff: Plain-language demo card and Wix→Pages link

## 1. Branch and last commit

- Mission: Director request — explain ADR-0010 / opt-in and DRL-019; link
  Wix to the live GitHub Pages replay viewer
- Branch: `cursor/plain-limitations-wix-pages-ad29`
- Base: `origin/main` (`ac2baa8`)
- Ending commit: `95b02d0`
- Pull request: https://github.com/chris-dewitt/DeWitt-Research-Lab/pull/59
- Prepared UTC: `2026-08-24`

## 2. Objective completed

- Operator card speaks English instead of ticket IDs.
- Paste-ready Wix copy and auditor gate point at the live Pages URL.
- Live Wix was **not** edited. This environment cannot authenticate the Wix
  MCP, and no Wix API key is present.

## 3. Files and interfaces changed

- `services/atticus-control-plane/.../orchestrator.py` — limitations, summary
  honesty, quantity formatting, Pages URL
- `services/atticus-control-plane/.../cli.py` — `PUBLIC RECORDINGS` line
- `services/evalforge/.../replay_site.py` — index copy
- `scripts/audit_wix_site.py` — homepage must link Pages
- `docs/08-web-brand/SITE_COPY.md` — *Watch a recorded run* target
- README, DIRECTORS_MEMO, ADR-0010 plain-language section, publication doc

## 4. ADRs created or needed

None new. ADR-0010 remains IN REVIEW. DIR-010 remains IN REVIEW.

## 5. Tests and results

See the PR for exact commands. Focused suites: Atticus foundation, public
feeds, replay site, Wix auditor, website positioning.

## 6. Deployment or migration notes

Merging this branch retriggers `publish-pages` because `replay_site.py`
changed. That updates the GitHub Pages copy. It does **not** change Wix.

Director action to finish the Wix link (one paste):

1. Wix editor → Home (and `/projects` until `/research` exists; that route
   404s today).
2. Add a button labeled **Watch a recorded run**.
3. Set the URL to
   `https://chris-dewitt.github.io/DeWitt-Research-Lab/`.
4. Use the surrounding copy in `docs/08-web-brand/SITE_COPY.md` § Recorded
   runs. Label it fixture recordings, not a live Atticus service.

## 7. Known failures and risks

- Live homepage currently has no Pages link. The auditor will GAP it until
  the paste lands.
- Wix `/research` 404s; research copy currently lives on `/projects`.
- A local live Atticus run is still not published to Pages. That is
  intentional.

## 8. Uncommitted or generated artifacts

None intended.

## 9. Next dependency-unblocking task

Director pastes the Pages URL on Wix, or authenticates the Wix MCP in Cursor
desktop so an agent can apply it.

## 10. Exact reading order for the next agent

1. This handoff
2. `docs/08-web-brand/SITE_COPY.md` recorded-runs section
3. `DIRECTORS_MEMO.md` current implementation truth
4. Live check: `https://www.dewitt-labs.com` homepage hrefs include
   `chris-dewitt.github.io/DeWitt-Research-Lab`
5. Live check: `https://chris-dewitt.github.io/DeWitt-Research-Lab/`
