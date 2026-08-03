---
document_id: DRL-HO-WIX-20260803
title: "Handoff: Wix Site Audit Remediation and Auditor Defect Fixes"
version: 1.0.0
status: PROTOTYPE
owner: Christopher Noxon DeWitt
last_updated: 2026-08-03
---

# Handoff: Wix site audit — two open tasks

Two independent tasks. **Task A** is repo-only and unblocked. **Task B** touches the live
site and is **NOT AUTHORIZED** — see the gate.

## Context

`www.dewitt-labs.com` was built by Aria and is live. An audit on 2026-08-02 compared it to
the approved specs. A second pass on 2026-08-03 re-verified after Director changes.

- Wix site ID: `e9a5dda4-53c7-46c2-8600-cc2a6fecf4e8`
- Auth: `WIX_API_KEY` env var (Authorization header, no Bearer prefix). Never print it.
- Network: the session must allowlist `www.wixapis.com`, `www.dewitt-labs.com`,
  `dewitt-labs.com`, or every call returns proxy 403.
- Governing specs: `docs/08-web-brand/{BRAND_SYSTEM,WIX_SITE_BUILD_PLAN,WIX_EDITOR_HANDOFF_CHECKLIST}.md`,
  `docs/01-product/PRODUCT_MATURITY_AND_SCOPE.md`.

---

## TASK A — Fix `scripts/audit_wix_site.py` (repo only, unblocked)

The script merged in PR #27 (on `main`) **produces mostly false positives**. It reported 40+
GAPs of which ~35 were wrong. Anyone running it today gets misleading output. Four defects,
all confirmed against the live site:

| # | Line | Defect | Evidence it is wrong |
|---|------|--------|----------------------|
| A1 | 88, 300 | `UNTRUTHFUL_TERMS` substring-matches "government", "university", "accredited" | Matches the **required disclosure** "Not a government, university, or accredited institution." Flagged a compliance item as a violation on all 14 pages. |
| A2 | 313–314 | Colour check reads only inline CSS hex literals | Wix paints via CSS variables. Real theme is `--wst-base-1-color:#0B0B0C` on `--wst-base-2-color:#EDE6D6` — correct cream-on-black — but the script reported "predominantly light". |
| A3 | 65, 360 | `EXPECTED_SYSTEM_PAGES` uses unhyphenated slugs | Reported fedlens/balancelab/evalforge missing; actual slugs are `/fed-lens`, `/balance-lab-ai`, `/eval-forge`. |
| A4 | ~247 | Reads `headers.get("Location")` case-sensitively | HTTP/2 sends lowercase `location`; apex 301 **does** work but was reported as a gap. |

Also fix: line 171 posts to `/wix-data/v2/collections/query` (404). The working call is
`GET https://www.wixapis.com/wix-data/v2/collections` with the `wix-site-id` header.
Handle `WDE0110` (CMS app not installed) as UNVERIFIED, not as a gap.

### Required fixes

1. **A1** — negative-lookaround, or skip any match inside a sentence containing "not a"/"independent
   initiative". Better: match phrases that *assert* affiliation ("accredited by", "in partnership with
   the University of"), not bare nouns.
2. **A2** — resolve `--color_NN` / `--wst-base-N-color` declarations before judging luminance; weight
   the page-section background variable (`--color_11`) over incidental widget `#fff`.
3. **A3** — normalise both sides (strip hyphens/underscores, casefold) before matching.
4. **A4** — case-insensitive header lookup.
5. Add a regression test under `tests/` asserting the disclosure sentence does **not** trigger a
   truthfulness gap.

### Verification (all must pass — CI runs these)

```bash
uv sync --all-packages --locked
uv run ruff check scripts tests packages services apps/atticus-local-runner
uv run mypy scripts packages services apps/atticus-local-runner
uv run bandit -q -r scripts packages services apps/atticus-local-runner
uv run pytest
```

Notes: repo is `mypy --strict` — annotate everything. Bandit flags dict literals containing a
`"PASS"` key as B105; build such maps with `enumerate`. Keep lines ≤100 chars.

Branch: start fresh from `origin/main` (PR #27 is merged; do not reuse it).

---

## TASK B — Site remediation (**GATED — DO NOT EXECUTE**)

> **Authorisation gate.** The Director instructed: *"Don't write or change anything on the site
> without asking me first."* No site write has been approved. Every item below is
> **proposed only**. Do not call any Wix write/PATCH/INSERT endpoint, and do not edit in the Wix
> editor, until the Director approves that specific item. Read-only verification is fine.

### Re-verified state as of 2026-08-03

Fixed since the first audit:

- **Wix CMS is now installed.** All eight proposed collections exist: `Systems`,
  `ResearchArtifacts`, `OpenArtifacts`, `TeachingResources`, `FailureRecords`,
  `PeopleAndContributors`, `Announcements`, `ExternalLaunchTargets`.
- **`Systems` is populated correctly** — 5 items (Atticus, Atlas, FedLens, BalanceLab AI,
  EvalForge), each `maturity=prototype`, `status=prototype`, updated `2026-08-03`. This matches
  controlled metadata and is truthful.

Still open:

| # | Item | Severity | State |
|---|------|----------|-------|
| B1 | `/atticus` shows **`STATUS: ALPHA`** alongside 5× `STATUS: PROTOTYPE` | HIGH | **Unfixed.** Contradicts itself and the CMS. `PRODUCT_MATURITY_AND_SCOPE.md`: Prototype = "no operational claim"; repo evidence says prototype. Delete the ALPHA label. |
| B2 | Pages are static text, **not bound to the CMS** | HIGH | **New root cause.** The CMS now holds correct labels but no page reads them, so B1 persists. Bind system pages to the `Systems` collection. |
| B3 | Six footer items — Governance, Security, Privacy, License, Documentation, Model Hub — are **plain text with zero anchors** | HIGH | **Unfixed.** Fails launch verification; privacy notice is required pre-publication content. |
| B4 | Approved mission line rewritten | HIGH | **Unfixed.** Site: "Intelligence for Good. Intelligence for all." Approved: "AI for Good. AI for all. / Intelligence of the people and for the people." Second line still absent site-wide. |
| B5 | "LAUNCH ATTICUS" → `/atticus` static page; `atticus.dewitt-labs.com` does not resolve | MEDIUM | Unfixed. Spec requires live/replay/planned state shown before launch, plus fallback. |
| B6 | Absolute capability claims: "FULLY DEPLOYABLE", "FULL TRACEABILITY", "FULL ACCESS TO ALL CORE COMPONENTS", "Full audit trail for all…" | MEDIUM | Unfixed. Present-tense absolutes for a prototype. |
| B7 | Filler copy — "We provide the open-weight guide and operator for independent deployment." repeated verbatim on 5 `/atticus` cards | MEDIUM | Unfixed. |
| B8 | 7 of 8 collections empty | MEDIUM | Needed before Research/Open Source/Failure Museum pages can be evidence-backed. |
| B9 | `/research`: "seeking researchers to join our team" | LOW | Judgment call — implies existing staff. |
| B10 | No dedicated `/contact` path (resolves to `/about`) | LOW | Acceptable now; add a redirect so the link doesn't break later. |

### Confirmed compliant — do not "fix"

Page tree complete (14 pages, all 8 sections + 5 system pages); cream-on-black correct
(`#0B0B0C`/`#EDE6D6`, amber `#E0A94E`); IBM Plex Sans/Mono per token intent; apex 301 → www;
independent-initiative disclosure on every page; hero headline and thesis line verbatim; footer
`NODE: CHARLOTTE / STATUS: PROTOTYPE`; no prohibited motifs.

---

## Reading order

1. This handoff
2. `docs/08-web-brand/WIX_SITE_BUILD_PLAN.md` (page tree, homepage composition, CMS schema)
3. `docs/08-web-brand/WIX_EDITOR_HANDOFF_CHECKLIST.md` (launch gates)
4. `docs/01-product/PRODUCT_MATURITY_AND_SCOPE.md` (Prototype vs Alpha)
5. `scripts/audit_wix_site.py` (Task A target)

## Risks

- Re-running the auditor as-is will generate false GAPs; fix Task A before trusting any report.
- Editing static page text (B1) without doing B2 means the next content change reintroduces drift.
- Task B has no approval. Treat the gate as blocking.
