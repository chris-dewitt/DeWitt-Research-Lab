---
document_id: DRL-PRG-095
title: "Release Dashboard and Weekly Program Review"
version: 1.2.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-17
---

# Release Dashboard and Weekly Program Review

## Purpose

Give the Director a concise, evidence-backed view of program health. Update the
dashboard weekly and before any public claim.

## Weekly review agenda

1. Director decisions, blockers, and the assumed-silence check.
2. Active issue and the dependency it unblocks.
3. Exact local and CI evidence for the current revision.
4. Material risks and privacy or public-claim drift.
5. Cloud and model spend, including `$0` when undeployed.
6. Claims that lack evidence or an honest maturity label.
7. The next single dependency-unblocking issue.

## Dashboard — 2026-08-17

| Field | Current value |
|---|---|
| Active milestone | M4 Public Research Foundation |
| Active issue | DRL-034 public-repository readiness |
| Working branch | `lovesong/chore/drl-034-public-repository-readiness` |
| Last green remote foundation CI | Draft PR #46, run `32092338028` |
| Open P1 Director decisions | DIR-002 cloud scope |
| Evidence-ready prototypes | Atticus integrated path, specialist fixtures, replay viewer/export, reports, teaching lab |
| Specified-only surfaces | lab-web, atticus-console, Atticus Core/Edge weights, live cloud deployment |
| Website | `www.dewitt-labs.com` is live; portfolio content remains Director-edited in Wix |
| Repository visibility | Private through 2026-09-30 under RES-018 |
| Cloud/model spend | `$0` recorded; no live project or model training authorized |
| Public-claim boundary | Do not call the system V1, production, or an open-weight model release |
| Top release blocker | RES-018 date gate; visibility not before 2026-09-30 |
| Next unblocking issue | Complete review and merge of DRL-034 |

## Release-readiness scorecard

| Gate family | Public-source milestone | V1 target | Current state |
|---|---|---|---|
| Source content and metadata | Required | Required | DRL-034 draft PR #46 remotely green |
| Automated public-source audit | Required | Required | Implemented and green in run `32092338028` |
| Git-history privacy | Required | Required | Accepted risk under RES-022 |
| CI and reproducibility | Required | Required | All three DRL-034 jobs green |
| Protocol and policy behavior | Useful evidence | Hard gate | Prototype tests present |
| Open-weight production path | Not required | Required | Selection gate open |
| Wix portfolio | Linked identity surface | Linked identity surface | Live; independently edited |
| Cloud deployment | Not required | Preview target | No deployment authorized |

Public-source readiness is a bounded milestone. It does not imply V1 readiness
or authorize changing repository visibility before the date in RES-018.
