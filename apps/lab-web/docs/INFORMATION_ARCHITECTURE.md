---
document_id: DRL-WEB-104
title: "Workshop Web Information Architecture"
version: 3.2.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Workshop Web Information Architecture

## Host responsibilities

### Canonical Wix origin

```text
www.dewitt-labs.com/
  Home
  Projects
  Writing
  Open Source
  About
```

Wix owns orientation, editorial summaries, founder context, and links to public
evidence. It does not own privileged application sessions.

### `lab-web` evidence application

```text
/replays/{id}            signed run viewer and transcript
/reports/tr-2026-001     full report reader
/projects/{slug}         advanced artifact/evidence view
/methods/{slug}          reproducibility and teaching view
/open/{type}/{slug}      source, license, lineage, and local path
```

Future routes such as `/atticus` or `atticus.dewitt-labs.com` remain planned
until their deployment and trust-boundary gates pass.

## Primary navigation

The evidence application keeps a small contextual nav:

- Recorded Runs
- Report
- Projects
- Methods
- Source
- Return to Workshop

It does not reproduce the entire Wix navigation tree or pretend to be an
operations console.

## Evidence-page layers

1. Identity, research question, maturity, and recorded/live/planned state.
2. Plain-language result and limitation.
3. Trace, source, calculation, and evaluation evidence.
4. Success/degraded comparison or negative result.
5. Methods, reproducibility, environment, and artifact digest.
6. Architecture, security, and trust boundaries.
7. Source, license, upstream lineage, related writing, and return path.

## Content states

Every public asset carries maturity (`experimental`, `prototype`, `alpha`,
`beta`, `stable`, `archived`, or `historical`), publication status, version,
owner, last-verified date, and runtime state (`live`, `replayed`, `cached`,
`illustrative`, or `planned`). “Stable” describes a declared interface, not
scientific finality.

## Search and keyboard navigation

Search covers public titles, abstracts, tags, projects, methods, document IDs,
releases, and technologies. It excludes private drafts and user traces. All
search, replay, tab, disclosure, comparison, and return actions are keyboard and
screen-reader usable.

## Open identity

Evidence pages expose source, artifact rights, upstream lineage, modification
surface, local/self-hosted path, evaluation, hardware/cost assumptions, and open
exceptions. `REPRODUCE` is generated from tested metadata, not hand-authored
marketing copy.
