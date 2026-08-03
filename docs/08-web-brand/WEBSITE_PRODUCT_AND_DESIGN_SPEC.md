---
document_id: DRL-WEB-001
title: "Laboratory Website Product and Design Specification"
version: 4.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Laboratory Website Product and Design Specification

## Canonical site and delivery model

The public institutional website is the registered domain **`https://www.dewitt-labs.com`**, hosted on Wix for V1. Wix introduces the laboratory and publishes editorial/research discovery content. The open-source DRL web applications, Atticus console, documentation, and specialist workstations deploy under DRL subdomains and share one design and navigation contract. See [`DOMAIN_AND_WIX_INTEGRATION.md`](DOMAIN_AND_WIX_INTEGRATION.md).

## Creative direction

One person's research workshop rendered as a modern financial research workstation. The atmosphere references `tmux`, Bloomberg-like density, academic working papers, UNIX terminals, and declassified technical archives without becoming a costume.

**Palette:** cream on near-black. Accent color is restrained and functional—amber, muted signal red, or phosphor green may identify status, focus, or system family but never overwhelm the cream/black foundation.

## Experience principles

- introduce the laboratory before Atticus;
- make the platform understandable without chat;
- let advanced users navigate by keyboard;
- use panels to compare evidence, traces, code, and calculations;
- motion explains state and flow;
- every live feature has an honest loading/error/replay state;
- institutional mystery comes from restraint, not fake secrecy;
- mobile is a designed mode, not a collapsed desktop terminal.

## Top-level Wix routes

```text
/
/laboratory
/systems
/systems/atticus
/systems/atlas
/systems/fedlens
/systems/balancelab
/systems/evalforge
/research
/research/<document>
/open-source
/models
/data
/benchmarks
/teaching
/failures
/launch/atticus
/about
/resume
/docs
/status
```

## Homepage narrative

1. **Institutional hero:** name, mission, one-sentence research thesis, system status.
2. **Systems map:** Atticus at center, specialists and EvalForge visible.
3. **Current transmission/research:** featured release, paper, benchmark, or experiment.
4. **Explore the systems:** signature interactive cards with real maturity and evidence.
5. **Atticus invitation:** ask for tour, run integrated replay, compare architecture.
6. **Open-source catalog:** installable packages, model/data releases, contribution calls.
7. **Failure museum preview:** one honest failure and fix.
8. **Teaching and collaboration:** current modules and calls for collaborators.
9. **Founder/director:** restrained profile and résumé.
10. **Footer terminal:** release, commit, model, docs status, license.

## Layout system

Desktop supports a configurable three-pane research workspace:

```text
[left index/nav] [primary document/demo] [Atticus/evidence/trace inspector]
```

Panes can resize, collapse, and persist locally. Default page reading remains conventional and accessible; `tmux` metaphor enhances rather than controls navigation.

## Signature interaction

`Ctrl/Cmd+K` opens the laboratory command palette:

- navigate pages;
- search docs/research;
- ask Atticus;
- start a guided tour;
- open current trace/evidence;
- switch workspace layout;
- view keyboard help.

Commands are searchable and have visible keyboard alternatives.

## Performance

- static content ships quickly without waiting for model APIs;
- hydrate only interactive panels;
- lazy-load charts/trace graphs;
- replay assets use content-addressed caching;
- animation respects reduced-motion;
- model wake state never blocks reading.

## Open-source identity requirements

- Open models, open-source software, public evaluation, local operation, and reproducible research must be visible without opening a footer or README.
- Every project page identifies upstream models/software, artifact licenses, maturity, local/self-hosted path, evaluation evidence, and contribution entry points.
- The public Atticus interface exposes the active model identity, version, routing mode, and whether output is live, replayed, cached, or illustrative.
- A dedicated Open Source portal presents Atticus model releases, datasets, packages, benchmarks, upstream contributions, self-hosting profiles, open exceptions, and independent replications.
- A `REPRODUCE` action is generated from tested release metadata rather than hand-authored marketing commands.
- The website credits upstream projects through a useful dependency graph, not a logo wall or implied endorsement.

## Cross-host product architecture

- Wix routes present the institution, editorial research, teaching, system summaries, collaboration, and launch pages.
- `atticus.dewitt-labs.com` and specialist subdomains present high-interaction tools, traces, calculations, and authenticated sessions.
- `apps/lab-web` remains a self-hostable open reference platform and can render docs, research workspaces, replay viewers, and shared application chrome.
- Primary apps must have direct URLs and may not depend solely on Wix iframes.
- Every external app exposes a clear return path to `www.dewitt-labs.com` and a visible release/model/status identity.
- Navigation, consent, analytics, accessibility, and canonical-link behavior are validated across host boundaries.
