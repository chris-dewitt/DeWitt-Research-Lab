---
document_id: DRL-HO-WEB-20260919-ENRICH
title: "Handoff: Research and Projects status enrichment on Wix"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-19
---


# Handoff: Research and Projects status enrichment on Wix

## 1. Branch and last commit

- Branch: `cursor/website-portfolio-fixes-f70f`
- Base: `origin/main`
- PR: https://github.com/chris-dewitt/DeWitt-Research-Lab/pull/74
- Prepared UTC: `2026-09-19`

## 2. Objective completed

Deepened live `/research` and `/work` with honest maturity and project status
drawn from `CURRENT_STATE_BASELINE.md`, `OPEN_SOURCE_MATURITY_MODEL.md`, and
`SITE_COPY.md`, without waiting on Studio editor access.

## 3. Files and interfaces changed

- Live Wix: BODY_END custom embed `Research/Projects status enrichment`
  (id `0505c503-cd89-425e-8b35-da977b7cc2b3`, revision `2`). Revision 2 hides
  original thin Studio cards so `/research` and `/work` are not doubled.
- Repo: `docs/08-web-brand/SITE_COPY.md` (3.4.0),
  `WIX_REMAINING_EDITOR_FIXES.md` (1.1.0), `WORKLOG.md`, `DIRECTORS_MEMO.md`,
  this handoff.

## 4. ADRs created or needed

None. Maturity vocabulary already approved in DRL-OSS-012; copy restates
baseline facts.

## 5. Tests and results

Browser verification (computer-use agent):

- `/research`: Status from the lab baseline; TR-2026-001 Prototype/Working paper
  with Limitations + Read the report / Source / Watch a recorded run;
  TR-2026-002 Null result / Result: no winner; What is not settled.
- `/work`: Project status; DeWitt Research Lab monorepo note + Atticus, Atlas,
  FedLens, BalanceLab, EvalForge as Prototype; SIGKILL In progress; Dead Drift
  Experiment.

Screenshots:

- `/opt/cursor/artifacts/screenshots/research-status-enrichment.webp`
- `/opt/cursor/artifacts/screenshots/projects-status-enrichment.webp`

Body-end script syntax checked with `new Function(...)` — OK. Unrelated Wix
viewer console noise may still appear (`Unexpected token 'if'` elsewhere).

## 6. Deployment or migration notes

Custom embeds apply on next render; no Studio Publish required for the panel.
Permanent Studio paste remains preferred so the page survives embed disable.

## 7. Known failures and risks

- Original thin Wix cards remain above the injected panel until the Director
  pastes permanent copy and removes duplication.
- Embed is the source of truth for the new detail until Studio paste lands.
- Hero (#3/#8), GitHub URL (#4), footer/privacy (#5) still editor-only.

## 8. Uncommitted or generated artifacts

Screenshots under `/opt/cursor/artifacts/screenshots/` (not in git).

## 9. Next dependency-unblocking task

Director applies remaining paste pack items in
`docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md` (hero, GitHub, footer,
privacy; optional permanent research/projects paste), then Publishes and may
disable the enrichment embed.

## 10. Exact reading order for the next agent

1. This handoff
2. Live: `https://www.dewitt-labs.com/research` and `/work` (scroll to status panels)
3. `docs/08-web-brand/WIX_REMAINING_EDITOR_FIXES.md`
4. `docs/08-web-brand/SITE_COPY.md` §§ Research / Projects
5. Prior handoff `agents/handoffs/2026-09-19-wix-portfolio-fixes.md`
