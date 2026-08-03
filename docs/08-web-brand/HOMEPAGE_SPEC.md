---
document_id: DRL-WEB-004
title: "Homepage Detailed Specification"
version: 4.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-03
---


# Homepage Detailed Specification

## Canonical implementation

This homepage is implemented at **`https://www.dewitt-labs.com`** in Wix. Interactive previews may use bounded custom elements or public embeds, but primary Atticus and specialist experiences launch on DRL application subdomains. The homepage must remain complete and useful when those services are cold or unavailable.

## Hero

```text
DEWITT RESEARCH WORKSHOP
Independent research in open and applied intelligence.

Intelligence for Good. Intelligence for All.

[Enter the laboratory] [Read the research thesis]
```

Background: slow, subtle system diagram showing Atticus and specialist nodes. No animation required for comprehension.

Metadata strip:

```text
NODE: CHARLOTTE / STATUS: ACTIVE / RELEASE: <actual> / OPEN SYSTEMS: <actual>
```

## Systems map

Hover/focus reveals problem, maturity, live/replay state, latest release. Modes:

- mission;
- architecture;
- data flow;
- evaluation;
- local/cloud trust boundary.

## Featured research

One current substantial artifact: AtticusBench report, model release, evaluation paper, or integrated demonstration. Show abstract, methods/evidence links, and replication button.

## Atticus invitation

Atticus is introduced after DRL:

> Atticus operates the laboratory. Ask him to explain a system, begin a guided tour, or replay the integrated research workflow.

Suggested commands are real and versioned.

## Open source

Show up to five high-value artifacts with install/run command, license, maturity, and use case. Avoid showing empty repositories.

## Failure museum

Feature one failure with a short timeline: failure → detection → fix → regression test. Link full record.

## Founder

Short biography, research interests, location, résumé/GitHub/contact. No long personal story on homepage.

## Open-source identity requirements

- Open models, open-source software, public evaluation, local operation, and reproducible research must be visible without opening a footer or README.
- Every project page identifies upstream models/software, artifact licenses, maturity, local/self-hosted path, evaluation evidence, and contribution entry points.
- The public Atticus interface exposes the active model identity, version, routing mode, and whether output is live, replayed, cached, or illustrative.
- A dedicated Open Source portal presents Atticus model releases, datasets, packages, benchmarks, upstream contributions, self-hosting profiles, open exceptions, and independent replications.
- A `REPRODUCE` action is generated from tested release metadata rather than hand-authored marketing commands.
- The website credits upstream projects through a useful dependency graph, not a logo wall or implied endorsement.

## Wix launch requirements

- Domain, HTTPS, canonical URL, apex redirect, social cards, favicon, robots, and sitemap are verified before public launch.
- System cards link to approved subdomains or clearly labeled replay/documentation pages.
- Wix status labels are sourced from controlled release metadata rather than manually optimistic copy.
- The homepage contains a visible Open Source path and a direct `Launch Atticus` action without making chat mandatory.
- Any embedded teaser has a plain link fallback and passes mobile, keyboard, reduced-motion, and unavailable-backend testing.
