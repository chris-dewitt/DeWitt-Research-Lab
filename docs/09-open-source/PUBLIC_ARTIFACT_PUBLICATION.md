---
document_id: DRL-OSS-022
title: "Public Artifact Publication Boundary"
version: 1.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-05
---

# Public Artifact Publication Boundary

## Purpose

This document operationalizes ADR-0009. It prevents a private-repository Pages
limitation from becoming an excuse either to expose the authoritative research
repository early or to publish an unreviewed directory wholesale.

## Repositories and authority

| Surface | Visibility | Authority | Purpose |
|---|---|---|---|
| `chris-dewitt/DeWitt-Research-Lab` | Private through 2026-09-30 | Authoritative preferred source | Code, controlled documents, signed replay fixtures, tests, build policy |
| `chris-dewitt/DeWitt-Research-Artifacts` | Public | Generated deployment mirror only | Sanitized static pages, release manifest, hashes, public limitations |
| `www.dewitt-labs.com` | Public | Canonical academic portfolio | Personal introduction and links to approved evidence |

The deployment mirror is not a second development repository. Direct edits to
generated pages are overwritten by the next approved publication and must not
be treated as authoritative corrections.

## First admitted artifact

- **Public artifact:** experimental success and degraded replay viewer.
- **Classification:** `public_only` until the preferred source becomes public.
- **Licenses:** Apache-2.0 renderer software; CC-BY-4.0 rendered narrative and
  replay content.
- **Modification surface:** private preferred source revision plus public file
  hashes during DRL-OEX-0001; full source is scheduled for 2026-09-30.
- **Self-hosted path:** serve the generated directory with any static HTTP
  server; no GPU, account, database, or paid API is required.
- **Upstream dependencies:** GitHub Actions for the official build and GitHub
  Pages for the official mirror; neither is required to serve the files locally.
- **Reproducibility evidence:** verified replay manifests and digests, immutable
  source SHA, deterministic file allowlist, per-file SHA-256 manifest, build
  commands, success and degraded fixtures.
- **Open exception:** DRL-OEX-0001, review due 2026-09-30.

## Publication gate

An ordinary push may build and retain a review artifact but may not change the
public repository. A public write requires all of the following:

1. the source branch is `main` at the exact reviewed revision;
2. replay signature and digest verification passes;
3. `prepare_public_replay_release.py` accepts every generated file and rejects
   every unexpected file;
4. the release manifest identifies the source revision, maturity, licenses,
   limitations, contact, and active open exception;
5. the workflow is manually dispatched with `publish=true`;
6. `PUBLIC_ARTIFACT_TOKEN` is a fine-grained credential restricted to contents
   write on `DeWitt-Research-Artifacts`;
7. post-deployment read-back confirms the public URL and file hashes.

Research papers are not implicitly covered by the replay allowlist. Adding a
paper requires public-release status, rights review, a publication manifest,
and a reviewed policy change naming the exact file.

## Rollback

Disable the workflow, revoke `PUBLIC_ARTIFACT_TOKEN`, unpublish GitHub Pages,
and remove the portfolio link. Do not delete historical source evidence or
rewrite a release manifest to hide an error; publish a correction and new
revision instead.
