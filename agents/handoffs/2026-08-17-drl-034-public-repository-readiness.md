---
document_id: DRL-HO-034-20260817
title: "Handoff: DRL-034 Public Repository Readiness"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-17
---

# Handoff: DRL-034 Public Repository Readiness

## 1. Branch and last commit

- Mission / issue: Mission 14 Release QA / DRL-034
- Branch: `lovesong/chore/drl-034-public-repository-readiness`
- Implementation commit: `9fa2d58e0bf1e394ef99976bec55e33ed9660eec`
- Handoff commit: the commit containing this file
- Pull request: pending draft creation
- Prepared: 2026-08-17 America/New_York

## 2. Objective completed

The tracked source tree is curated for public review: its landing page is a
personal academic research portfolio, current evidence and limitations are easy
to find, package/citation metadata is consistent, stale validation artifacts
cannot be mistaken for current evidence, and a fail-closed audit enforces the
public-source boundary locally and in CI.

This is source-tree readiness, not public release. The repository remains
private under RES-018. DRL-034 is blocked at the release boundary until DIR-009
is resolved and the draft PR's remote CI passes.

## 3. Files and interfaces changed

- `README.md`, `CITATION.cff`, component READMEs, and all Python package metadata
  now present the work, ownership, licenses, repository, and maturity honestly.
- `scripts/validate_public_repository.py` and
  `tests/test_public_repository.py` enforce required files, credentials,
  employer identifiers, public contact, local paths, private/generated files,
  large or gated artifacts, package metadata, and scaffold maturity without
  printing matched secret values.
- `make public-check` runs the tracked-source gate;
  `make public-release-check` also audits reachable Git-author metadata.
- `.github/workflows/ci.yml` runs the new audit, creates an ignored tracked-
  source manifest as an artifact, identifies Node packages as scaffolds, and
  uses current Node 24 action generations.
- `scripts/generate_manifest.py` now hashes only `git ls-files` input and writes
  to ignored `site/source-manifest.json`; the stale tracked root manifest was
  removed.
- Historical foundation reports are `ARCHIVED`; the current-state baseline,
  release dashboard, approval queue, specification map, changelog, issue
  register, and public-readiness checklist now reflect 2026-08-17 state.
- `tests/test_http_streaming.py` keeps live-socket transport coverage while
  making the refused-connection classification deterministic on Windows hosts
  that silently filter unused loopback ports.
- GitHub About metadata now has a portfolio homepage, accurate description,
  eight research topics, and automatic deletion of future merged PR branches.

No schema, runtime API, model, dataset, cloud resource, Wix page, repository
visibility, branch-protection rule, or research finding changed.

## 4. ADRs and decisions

- No new architecture decision was required for source curation.
- RES-018 still keeps the authoritative repository private through 2026-09-30
  and forbids treating this work as permission to enable branch protection.
- RES-019 keeps `director@dewitt-labs.com` as the only public contact.
- DIR-009 records that 16 reachable commits expose an institutional author
  address. A history rewrite or explicit risk acceptance requires the
  Director's decision; no rewrite or force-push occurred.

## 5. Tests and exact results

| Command / check | Result |
|---|---|
| `uv lock --check` | PASS; 43 packages resolved from the existing lock |
| `scripts/validate_foundation.py` | PASS; 365 controlled documents, 132 requirements, 122 work packages, 26/26 schemas/examples, 16 missions |
| `scripts/validate_program.py` | PASS; 34 issues, 122 work packages, acyclic dependencies |
| `scripts/validate_open_identity.py` | PASS; 26 V1 requirements, 10 stack records |
| `scripts/validate_domain_wix.py` | PASS |
| `scripts/validate_public_repository.py` | PASS; 645 tracked files inspected |
| `scripts/validate_public_repository.py --release` | Expected BLOCK; 144 reachable commits inspected, 16 commits fail DIR-009 author-email gate |
| `ruff check` over declared Python paths | PASS |
| strict `mypy` over declared Python paths | PASS; 63 source files |
| Bandit over declared Python paths | PASS; no findings |
| complete `pytest -ra` | PASS; 351 passed, 2 Windows symlink-privilege skips |
| focused public/program/transport regression tests | PASS |
| `pnpm install --frozen-lockfile` | PASS; workspace already current |
| `pnpm -r lint/typecheck/test/build` | PASS as scaffold declarations; each explicitly reports `Implementation pending` |
| integrated public Atticus demo | PASS; state completed, 5 evidence items, EvalForge score 1.0 |
| tracked-source manifest generation | PASS; 645 entries written to ignored `site/source-manifest.json` |
| staged `git diff --check` | PASS |
| local Docker build | NOT RUN; Docker executable is not installed on this workstation |

Two pre-existing Windows symlink security tests skipped only because this host
does not grant symlink creation privilege. The CI Linux run remains responsible
for executing those deny-path assertions and the container build.

## 6. Deployment and migration notes

There is no runtime deployment or migration. The repository remains private.
The draft PR must run the updated GitHub Actions jobs before merge. At the
approved release date, follow
`docs/12-acceptance/PUBLIC_REPOSITORY_READINESS.md`, including anonymous clone
and link read-back.

GitHub repository metadata was updated out of band and verified:

- description: independent academic research prototypes;
- homepage: `https://www.dewitt-labs.com`;
- topics: agentic AI, applied data science, artificial intelligence,
  computational finance, evaluation, machine learning, open research, and
  reproducible research;
- visibility: still `PRIVATE`;
- delete merged PR branches: enabled.

## 7. Known failures and risks

1. DIR-009 blocks public visibility: 16 reachable commits carry an institutional
   author address. Do not rewrite or force-push without explicit approval and a
   coordinated backup/rollback plan.
2. Remote CI is pending the draft PR. Local Docker evidence is unavailable.
3. The two TypeScript packages remain explicit scaffolds, not implemented apps
   or meaningful lint/type/test/build suites.
4. GitHub secret scanning and push protection remain disabled while the
   repository is private; reconsider them at the visibility change without
   weakening RES-018.
5. Twenty-two remote branches were verified fully merged into `origin/main`,
   and no open PR references them. They were not deleted because broad remote
   branch deletion requires explicit authorization.

## 8. Uncommitted or generated artifacts

`site/source-manifest.json` is an ignored, regenerable verification artifact.
Three temporary pytest/Ruff cache directories created by a failed sandboxed
run were removed after their absolute paths were verified inside the workspace;
they contained no authoritative data and can be regenerated.

This handoff is the intended source change after implementation commit
`9fa2d58`. No other uncommitted source artifacts should remain.

## 9. Next dependency-unblocking task

Review the draft PR and its remote CI. Then obtain an explicit Director choice
for DIR-009. If the Director also authorizes deleting the 22 verified merged
branches, repeat the merged/open-PR checks immediately before deletion. Do not
change repository visibility before 2026-09-30 or treat source readiness as V1.

## 10. Exact reading order for the next agent

1. `LABORATORY_BIBLE.md`
2. `DIRECTORS_MEMO.md`, especially RES-018, RES-019, and DIR-009
3. `AGENTS.md`
4. `OPEN_RESEARCH_CHARTER.md`
5. `docs/12-acceptance/PUBLIC_REPOSITORY_READINESS.md`
6. `.github/ISSUE_BODIES/DRL-034.md`
7. `scripts/validate_public_repository.py`
8. `tests/test_public_repository.py`
9. `.github/workflows/ci.yml`
10. this handoff
