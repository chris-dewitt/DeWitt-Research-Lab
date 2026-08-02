---
document_id: DRL-WEB-013
title: "Content Model, Repository Publishing, and Search"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Content Model, Repository Publishing, and Search

## Source of truth

Controlled Markdown/MDX and release manifests in the repository feed the website. The build validates frontmatter, links, status, and public eligibility.

## Content schema

- ID, type, title, summary/abstract;
- authors;
- status/version/date;
- system/tags;
- license;
- public path;
- related code/data/model;
- citation;
- search text/keywords;
- feature image/video/replay;
- evidence/metrics manifest.

## Search

Hybrid local/static index for docs and public research; optional server search for larger corpora. Search respects status and public eligibility. Atticus citations link to exact document heading/version.

## Preview

Draft content can preview in PR but does not publish to production without public-release status.

## Wix publishing bridge

Wix is the public editorial surface at `www.dewitt-labs.com`; Git remains the source of truth for controlled technical and research artifacts. A publishing bridge may export approved summaries, artifact cards, release metadata, status, and links into Wix. It must support preview, field validation, idempotency, rollback, and public-status filtering.

Wix-authored editorial pages may be indexed or archived into the repository when they become part of a research, teaching, or release record. Editorial convenience never changes controlled-document status.

The bridge must not publish secrets, private traces, unpublished benchmarks, local personalization data, or draft documents. It records source commit, Wix page identifier, publication timestamp, checksum, and canonical owner for every synchronized item.
