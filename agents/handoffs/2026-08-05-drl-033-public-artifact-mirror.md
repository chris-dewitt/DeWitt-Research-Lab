---
document_id: DRL-HO-033-20260805
title: "Handoff: DRL-033 Public Artifact Deployment Mirror"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-05
---

# Handoff: DRL-033 Public Artifact Deployment Mirror

## 1. Branch and commits

- Mission / packet: Mission 14 Release QA / DRL-033
- Branch: `lovesong/infra/drl-033-public-artifact-pages`
- Governance commit: `9f9c0b6`
- Implementation commit: `f2b42ad`
- Pull request: pending remote creation
- Public repository: approved as
  `chris-dewitt/DeWitt-Research-Artifacts`; account creation is pending
  Director authentication
- Handoff prepared UTC: `2026-08-06T03:30:00Z`

## 2. Objective completed

The private/public release boundary is implemented and validated. The private
repository remains authoritative under RES-018. Relevant pushes build a
reviewable replay export but cannot publish; an explicit manual dispatch from
`main` is required before the workflow can write to the separate public
repository approved in RES-021 and ADR-0009.

The exporter is deny-by-default: it accepts exactly four rendered replay files,
rejects symlinks, directories, unexpected filenames, over-size content, common
credential shapes, and local runner paths, then emits a public README,
`.nojekyll`, and a release manifest with source revision, licenses, limitations,
open exception, file sizes, and SHA-256 digests.

The external deployment is not complete. No public repository or Pages URL is
claimed live until the Director authenticates to GitHub and the post-deployment
read-back gate passes.

## 3. Files and interfaces changed

- `.github/workflows/publish-replays.yml`
  - replaces the impossible private-repository Pages deployment;
  - builds an allowlisted review artifact on relevant `main` pushes;
  - refuses public writes from any non-`main` revision;
  - publishes only after `workflow_dispatch` with `publish=true`;
  - uses `PUBLIC_ARTIFACT_TOKEN` only for the public mirror checkout.
- `scripts/prepare_public_replay_release.py` and
  `configs/public-artifact-export.yaml`
  - implement the exact export policy, fail-closed checks, and manifest.
- `configs/open-exceptions/DRL-OEX-0001.json`
  - records the temporary `public_only` source-availability exception through
    2026-09-30.
- `docs/adr/ADR-0009-public-artifact-deployment-mirror.md` and
  `docs/09-open-source/PUBLIC_ARTIFACT_PUBLICATION.md`
  - record the approved architecture, authority boundary, release gate,
    licensing, self-hosting path, and rollback.
- `services/evalforge/src/evalforge_service/replay_site.py`
  - presents recorded runs as Christopher Noxon DeWitt's academic portfolio
    evidence, not as a separate institution;
  - adds the portfolio return link and truthful UNC-Chapel Hill
    non-endorsement disclosure.
- `SECURITY.md`
  - uses `director@dewitt-labs.com` as the only public contact.
- DRL-033 issue/register/worklog, validators, replay documentation, and tests
  were updated together.
- `tests/test_local_runner.py`
  - preserves the symlink security test while reporting a platform skip when
    Windows does not grant symlink creation privilege.

No live API, schema, model, dataset, participant record, cloud resource, Wix
setting, custom domain, or research paper was published.

## 4. ADRs and decisions

- ADR-0009 is approved by the Director's explicit statement,
  "Option 2, I approve."
- RES-018 fixes the permanent private source repository and September public
  target without GitHub branch protection or rulesets.
- RES-019 makes `director@dewitt-labs.com` the sole public address.
- RES-020 approves CFI DIR-008 Option A while preserving independent G1 review.
- RES-021 approves the separate public artifact mirror and excludes papers
  until individually approved.
- DRL-OEX-0001 is active through 2026-09-30. During that exception, the mirror
  is accurately classified `public_only`, not open source.

## 5. Test and validation evidence

| Command / check | Exact result |
|---|---|
| Focused DRL-033, replay, signed-replay, CFI, and program pytest suite | PASS; one Windows symlink skip |
| Complete repository pytest suite | PASS; two expected Windows symlink skips |
| `python -m ruff check .` | PASS: all checks passed |
| `python -m compileall -q scripts services/evalforge/src apps/atticus-local-runner/src` | PASS |
| `python scripts/validate_program.py` | PASS: 33 issues, 122 work packages, acyclic dependencies |
| `python scripts/validate_foundation.py` | PASS: 361 controlled documents, 132 requirements, 122 work packages, 26/26 schemas/examples, 16 missions |
| `python scripts/validate_open_identity.py` | PASS: 26 V1 requirements, 10 stack records |
| `python scripts/validate_domain_wix.py` | PASS |
| Workflow, publication policy, and issue-register YAML parse | PASS: three files |
| `git diff --check` | PASS; expected Git LF-to-CRLF workspace notices only |
| Exact generated public export secret/local-path scan | PASS |
| Local manifest SHA-256 read-back | PASS: four content files at `f2b42ad75d1d8fed090304192ef9e87b5f89439d` |
| Public HTML portfolio identity scan | PASS: personal identity, portfolio link, student-artifact disclosure, and non-endorsement text present; workshop/laboratory/library branding absent |

The first complete pytest run found that an existing local-runner symlink test
assumed Windows symlink privilege. The test now skips only when the operating
system refuses symlink creation; it still runs its denial assertions on capable
hosts. The subsequent complete suite passed.

The local host does not expose `uv` on `PATH`. The final static build was
therefore reproduced with the same Python entry point and explicit workspace
module paths. GitHub Actions installs the pinned `uv` version before using the
locked workspace, as the prior remote build already demonstrated.

## 6. Deployment and migration notes

The publication code is ready, but external setup remains intentionally
unfinished:

1. authenticate to GitHub in the Director's account;
2. create public repository `chris-dewitt/DeWitt-Research-Artifacts` with a
   `main` branch;
3. set Pages to deploy from `main` at repository root;
4. create a fine-grained token scoped only to that repository with Contents
   read/write;
5. store it in private source repository Actions secrets as
   `PUBLIC_ARTIFACT_TOKEN`;
6. merge this branch, confirm the review-artifact build, manually dispatch with
   `publish=true`, and read back the public bytes/hashes.

No custom domain or Wix change is part of DRL-033. The expected interim URL is
`https://chris-dewitt.github.io/DeWitt-Research-Artifacts/`.

## 7. Known failures and risks

1. GitHub CLI authentication in this environment is stale, and the in-app
   GitHub browser is at sign-in. Public repository creation and Pages setup are
   therefore Director-authentication actions.
2. The public mirror cannot be seeded until its `main` branch exists.
3. The private workflow cannot publish until the narrowly scoped secret exists.
4. Papers remain denied by the allowlist; adding one without a separate rights
   and release review would violate RES-021.
5. The demo HMAC establishes fixture integrity only, not production provenance.
6. A public URL is not evidence of success until its manifest and hashes are
   read back after deployment.

## 8. Uncommitted or generated artifacts

`site/replays/` and `site/public-replays/` are ignored local verification
outputs. The public envelope was rebuilt from implementation commit `f2b42ad`
and locally hash-verified. They are not authoritative deployment evidence and
should be regenerated rather than committed.

This handoff is the only intended change after the two implementation commits.

## 9. Next dependency-unblocking task

Complete the six Director-authenticated GitHub setup steps in section 6, then
record the public repository ID, Pages configuration, workflow run and artifact
IDs, deployed URL, and hash read-back. Only then may DRL-033 become complete or
the Wix portfolio link be added.

## 10. Exact reading order for the next agent

1. `LABORATORY_BIBLE.md`
2. `DIRECTORS_MEMO.md`, especially RES-018 through RES-021
3. `AGENTS.md`
4. `OPEN_RESEARCH_CHARTER.md`
5. `docs/adr/ADR-0009-public-artifact-deployment-mirror.md`
6. `docs/09-open-source/PUBLIC_ARTIFACT_PUBLICATION.md`
7. `configs/public-artifact-export.yaml`
8. `configs/open-exceptions/DRL-OEX-0001.json`
9. `.github/workflows/publish-replays.yml`
10. `scripts/prepare_public_replay_release.py`
11. `.github/ISSUE_BODIES/DRL-033.md`
12. this handoff

## 11. Attestation

The local artifact is a validated experimental replay bundle, not a deployed
service, live inference session, production signing system, institutional UNC
project, or released paper. No public repository, GitHub Pages deployment, or
external publication is claimed complete without remote read-back evidence.
