---
document_id: DRL-ACC-003
title: "Public Repository Readiness Checklist"
version: 1.1.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-17
---

# Public Repository Readiness Checklist

## Scope

This checklist governs making the authoritative source repository publicly
readable. It does not declare the platform V1, authorize a model release, or
override RES-018: the repository remains private through 2026-09-30.

## Automated source gates

`uv run python scripts/validate_public_repository.py` fails closed when the
tracked tree contains:

- missing public repository policy or citation files;
- credentials or high-confidence secret shapes;
- employer identifiers, unapproved public emails, or local user-home paths;
- private/generated paths, symlinks, large files, or gated binary artifacts;
- incomplete package license, author, README, or repository metadata;
- unsupported README maturity claims; or
- placeholder web packages presented as release candidates.

`uv run python scripts/validate_public_repository.py --release` adds the
reachable Git-author-metadata gate.

## Readiness ledger

| Gate | State on DRL-034 | Evidence or owner |
|---|---|---|
| Public README and evidence map | Ready for review | `README.md` |
| License, notice, citation, security, conduct, governance | Ready for review | Root policy files and `CITATION.cff` |
| Tracked-source privacy and credential audit | Automated | `scripts/validate_public_repository.py` |
| Package metadata consistency | Automated | Public-source audit and package TOML |
| Honest prototype/scaffold maturity | Ready for review | Current-state baseline and component READMEs |
| Generated manifest excluded from source | Automated | `scripts/generate_manifest.py`, CI artifact |
| Current dependency/action baseline | Complete | GitHub Actions run `32092338028` passed all three jobs |
| Reachable Git-author metadata | Accepted risk | RES-022 resolves DIR-009; audit reports the count without blocking |
| Remote branch cleanup | Awaiting explicit deletion approval | 22 branches are merged and no open PR references them |
| Repository About description, homepage, and topics | Complete | GitHub repository metadata updated 2026-08-17 |
| Anonymous clone and link verification | Release-day gate | Director or release operator |
| Repository visibility | Date-gated | RES-018; not before 2026-09-30 |

## Resolved Decision — DIR-009

Some reachable commits expose an institutional author address (16 when DIR-009
was raised; 15 reachable today — the figure moves with the ref set). The
Director chose documented risk acceptance over a coordinated history rewrite in
**RES-022**: the address stays, commit SHAs are preserved, and new commits
continue to use the GitHub no-reply address so the exposure does not grow.

`scripts/validate_public_repository.py --release` still counts and reports these
commits, printing them as `ACCEPTED (RES-022)` rather than failing. The check is
retained deliberately — a *new* unapproved institutional address would still
surface. This no longer gates public visibility.

## Release-day procedure

1. DIR-009 is resolved by RES-022; confirm the memo still records that acceptance.
2. Confirm the DRL-034 PR and its required CI checks are merged and green.
3. Run `make public-release-check` from a clean checkout of `main`.
4. Remove only remote branches proven merged and not referenced by an open PR.
5. Confirm repository About metadata, license detection, topics, and contact.
6. Change visibility only on or after 2026-09-30 with Director authorization.
7. Verify an anonymous clone, root links, reproduction commands, and absence of
   private data from the public view.
8. Record the public URL, exact revision, checks, and rollback plan in a handoff.

If any gate fails, restore private visibility if necessary and treat the failed
check as release-blocking evidence rather than weakening the rule.
