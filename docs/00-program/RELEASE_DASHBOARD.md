---
document_id: DRL-PRG-095
title: "Release Dashboard and Weekly Program Review"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-27
---

# Release Dashboard and Weekly Program Review

## Purpose

Give DeWitt a one-page, evidence-backed view of program health. Update this
dashboard in `WORKLOG.md` weekly and before any public claim.

## Weekly review agenda (30–45 minutes)

1. **Director's Memo** — new/closed decisions, blockers, assumed silence check.
2. **Critical path** — which mission/issue is active; what it unblocks.
3. **Evidence** — commands run, CI status, demo transcript age.
4. **Risks** — exposure ≥15 items from `RISK_REGISTER.md`.
5. **Cost** — cloud/model spend vs budget (or `$0` if undeployed).
6. **Claims** — any public text lacking evidence or maturity labels.
7. **Next single issue** — only one dependency-unblocking issue named.

## Dashboard fields

| Field | Current value (update weekly) |
|---|---|
| Date (UTC) | 2026-07-27 |
| Active milestone | M1 Repository Online and Trusted |
| Active mission | 00 Program Director |
| Active issue | DRL-001 (after filing) |
| Integration branch | *to create* `integration/v1` |
| Last green `make verify` | 2026-07-27 at `0eaabd7` (clean clone; 25 tests) |
| Open P0 Director decisions | DIR-001, DIR-003 |
| Open P1 ADRs | ADR-0006, ADR-0007; DIR-002 |
| Prototype surfaces | Atticus + specialists + local-runner primitives |
| Specified-only surfaces | lab-web, atticus-console, model weights, Wix live, GCP live |
| Cloud spend (period) | $0 (no project configured) |
| Public claims requiring caution | Do not call platform V1.0; label fixture demos as simulated/replay |
| Top risk this week | R-01 scope; R-12 unverified agent completeness; R-07 docs drift |
| Next unblocking issue | DRL-001 → DRL-002 → DRL-003 |

## Release readiness scorecard (preview ≠ V1)

| Gate family | M1 target | V1 target | Status |
|---|---|---|---|
| Repo trust / CI | Required | Required | In progress |
| Clean-clone demo | Required | Required | Linux evidence ready; Windows pending |
| Protocol/policy tests | Started | Hard gate | Pending DRL-005 |
| Open-weight production path | Not required | Required | Blocked on bake-off |
| Wix + domain | Not required | Required | Blocked on accounts |
| GCP budget-capped deploy | Not required | Preview in M4 | Blocked on DIR-002 |
| Clean-room no-paid-API | Local fixture OK | Full matrix | Fixture only |

## Cadence artifacts

- Weekly: append a dated dashboard snapshot under `WORKLOG.md`.
- Biweekly: one small demonstration (fixture demo acceptable if labeled).
- Per PR: commands + results in the PR template; update Memo if material.
