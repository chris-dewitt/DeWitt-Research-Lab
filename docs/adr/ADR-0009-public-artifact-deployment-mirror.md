---
document_id: DRL-ADR-0009
title: "Use a Separate Public Repository for Sanitized Deployment Artifacts"
version: 2.0.0
status: SUPERSEDED
owner: Christopher Noxon DeWitt
last_updated: 2026-08-22
---

# ADR-0009: Use a separate public repository for sanitized deployment artifacts

> **SUPERSEDED on 2026-08-22 by RES-024.** The Director elected to publish the
> authoritative repository itself rather than a sanitized derivative of it.
>
> This decision rested on one constraint: GitHub Pages will not deploy from a
> private personal repository on the Director's plan, and RES-018 kept the
> source private through 2026-09-30. RES-024 supersedes that date clause, which
> removes the constraint and with it the mirror's only reason to exist —
> alternative 1 below, rejected here, is what was ultimately chosen.
>
> Retired with this decision: `configs/public-artifact-export.yaml`,
> `configs/open-exceptions/DRL-OEX-0001.json`,
> `scripts/prepare_public_replay_release.py`,
> `.github/workflows/publish-replays.yml`, and
> `tests/test_public_artifact_export.py`. `scripts/build_replay_site.py`
> survives — it builds the viewer, which a public repository can serve from its
> own Pages.
>
> The document is retained unedited below as the record of why the boundary was
> built and what it enforced. Nothing below is current practice.

## Context

The authoritative repository, `chris-dewitt/DeWitt-Research-Lab`, remains
private through 2026-09-30 under RES-018. Its replay workflow built a valid
GitHub Pages artifact at source revision `1feda7f`, but GitHub rejected the
deployment because the Director's current plan does not provide Pages for a
private personal repository. Making the authoritative repository public early
would violate the approved disclosure schedule.

The academic portfolio still needs visible, linkable evidence. A generated
replay viewer is specifically designed to remain useful without a backend,
model, cloud account, or private data.

## Decision

Use the public repository `chris-dewitt/dewitt-research-artifacts` as a
deployment-only mirror for sanitized portfolio evidence.

The private repository remains the only preferred modification source and the
only place where builds originate. Publication is a one-way export with these
controls:

1. a policy file names the exact target repository, source directory, admitted
   filenames, size limits, maturity, licenses, contact, and active open
   exception;
2. signed replay bundles are verified before rendering;
3. an export step rejects symlinks, unexpected files, path escapes, known
   credential shapes, local filesystem paths, and over-size output;
4. the exported envelope records the immutable source revision and SHA-256 for
   every deployed content file;
5. ordinary pushes build a review artifact but never publish it;
6. publication requires a manual workflow dispatch and a fine-grained token
   scoped only to contents write on the public mirror;
7. the public repository contains generated artifacts, release metadata, and a
   deployment README, but no private source checkout or working documents.

The first admitted artifact is the experimental success/degraded replay
viewer. Research papers are excluded until each controlled document reaches an
approved public-release state and the allowlist is deliberately amended.

## Alternatives considered

1. Make the authoritative repository public immediately. Rejected because it
   conflicts with RES-018.
2. Purchase GitHub Pro and deploy Pages from the private repository. Valid but
   unnecessary once the Director approved a free public mirror.
3. Deploy on Cloudflare, Vercel, Firebase, or GCP. Deferred because the static
   viewer does not justify a new provider, billing identity, or secret surface.
4. Upload files manually without a recorded export policy. Rejected because it
   makes the private/public boundary unauditable and easy to widen accidentally.

## Consequences

### Positive

- The portfolio gains public evidence while research source remains private.
- Publication is free, static, cacheable, and independent of live inference.
- The exported revision, hashes, maturity, and limitations remain inspectable.
- The same generated bundle can be served locally or by another static host.

### Negative

- The deployment mirror is a second repository to operate.
- Until the source repository becomes public, the mirror is accurately labeled
  `public_only`, not open-source software.
- Cross-repository publication requires a narrowly scoped credential and a
  one-time Pages configuration in the Director's GitHub account.
- GitHub Pages is an interim delivery surface, not a replacement for the
  Google-first application architecture in ADR-0002.

## Security, privacy, data, licensing, and cost

- No credential, private trace, employer data, user content, model secret, or
  unrestricted repository file may enter the export.
- The fine-grained token receives contents write only for
  `dewitt-research-artifacts` and is stored only as a private-repository Actions
  secret named `PUBLIC_ARTIFACT_TOKEN`.
- The replay renderer is DRL-authored Apache-2.0 software; rendered narrative
  and replay content are distributed under CC-BY-4.0. The public mirror states
  both categories rather than presenting a false single-license claim.
- The demo HMAC signature is disclosed as a fixture integrity mechanism, not a
  production signing identity.
- Hosting cost is $0 under GitHub Pages limits. A future paid or custom-domain
  migration requires evidence and an ADR when it changes the accepted boundary.
- DRL-OEX-0001 records the temporary source-availability exception through
  2026-09-30.

## Compatibility, migration, and rollback

The generated bundle is ordinary static HTML and JSON. It can be served from a
local directory or migrated to any static host without changing the renderer.

Rollback is to disable the publishing workflow, remove the Wix link, and
unpublish GitHub Pages. Historical release manifests remain evidence. Revoking
`PUBLIC_ARTIFACT_TOKEN` stops future cross-repository writes without affecting
the private source repository.

## Approval

- Proposed by: Codex
- Date: 2026-08-05
- Approved by the Director: 2026-08-05 ("Option 2, I approve")
- Status: APPROVED
