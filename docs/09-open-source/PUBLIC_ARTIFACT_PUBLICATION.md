---
document_id: DRL-OSS-022
title: "Public Artifact Publication Boundary"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-22
---

# Public Artifact Publication Boundary

## Purpose

This document described how sanitized artifacts crossed from a private
repository to a public deployment mirror. **RES-024 removed that boundary** by
making the authoritative repository itself public, so there is no longer a
private side to cross from.

It is retained, rewritten, because the question it answered is still worth
answering: what may be published, and under what claim.

## Repositories and authority

| Surface | Visibility | Authority | Purpose |
|---|---|---|---|
| `chris-dewitt/DeWitt-Research-Lab` | Public (RES-024) | Authoritative preferred source | Code, controlled documents, signed replay fixtures, tests, build policy |
| `www.dewitt-labs.com` | Public | Canonical academic portfolio | Personal introduction and links to approved evidence |

The separate mirror `chris-dewitt/dewitt-research-artifacts` is **retired**. No
configuration, workflow, or script in this repository targets it. It may be
deleted or left dormant at the Director's discretion.

## What changed, and what did not

**Changed.** There is no export allowlist, no cross-repository credential, and
no manual publication dispatch. Anything merged to `main` is public the moment
it lands. The `public_only` classification is gone: with the preferred source
public, this is open-source software rather than a published derivative of
something withheld.

**Not changed.** Publication is not endorsement, and public is not finished.
Every controlled document still carries its real status, and the status is the
claim:

- `DRAFT` — incomplete and non-authoritative. Public, and not to be cited as
  settled.
- `IN REVIEW` — proposed; implementation must not depend on it.
- `APPROVED FOUNDATION` — approved for implementation.
- `SUPERSEDED` — retained for history, linked to its successor.

A reader encountering `TR-2026-002` or the CFI novelty review will find them
marked `DRAFT` and `IN REVIEW` respectively, with their limitations stated in
the documents themselves. That labelling now carries the weight the allowlist
used to.

## The standing obligation

Removing the gate raises rather than lowers the bar on honesty, because nothing
mechanical now stands between a draft and a reader.

1. **Maturity labels are load-bearing.** Never mark a document `APPROVED
   FOUNDATION` to make it look finished. `docs/01-product/PRODUCT_MATURITY_AND_SCOPE.md`
   governs the vocabulary.
2. **Research claims stay gated by evidence, not by visibility.** G1 through G6
   in `docs/10-research/COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md` are unchanged.
   A public draft is still not a result.
3. **The tracked-source audit still runs.** `make public-check` fails closed on
   credentials, employer identifiers, private filesystem paths, binary
   artifacts, unsupported maturity claims, and unapproved contact addresses.
   It is now the only automated check between a commit and the public, so it
   must not be weakened to make a commit pass.
4. **Corrections are published, not erased.** Do not rewrite history to hide an
   error. Publish a dated correction and a new revision, as the failure records
   under `docs/10-research/failures/` already do.

## Serving the replay viewer

`make replay-site` builds the viewer into `site/replays` — `index.html`,
`success.html`, `degraded.html`, and `site.json`. Any static HTTP server serves
them, with no GPU, account, database, or paid API required.

`.github/workflows/publish-pages.yml` publishes them to GitHub Pages on every
push to `main` that touches the replay bundles, the renderer, the build script,
or the workflow itself, and on manual dispatch. It is a restoration rather than
a new design: the same workflow existed before and was correct, and failed only
because Pages will not serve a private personal repository. Making the source
public removed that constraint.

The build verifies each bundle's manifest signature and artifact digests before
rendering, so a tampered recording fails the workflow rather than being
published under a claim of provenance it does not have. The signature remains a
published demo HMAC — fixture integrity, not a production signing identity — and
must not be described as one on the site or anywhere else.

## Licensing

Apache-2.0 for renderer and harness software; CC-BY-4.0 for rendered narrative
and replay content. The distinction is stated rather than collapsed into a
single false claim.

The demo HMAC on replay bundles remains a fixture-integrity mechanism, not a
production signing identity, and must not be described as one.

## History

`ADR-0009` records why the mirror was built and what it enforced, and is marked
`SUPERSEDED`. `DRL-OEX-0001`, the open exception covering the period when the
preferred source was unavailable, is closed: the source is available.
