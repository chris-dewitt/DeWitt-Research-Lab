---
document_id: DRL-OSS-006
title: "Open Research and Open Technology Charter"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Open Research and Open Technology Charter

## Constitutional position

DeWitt Research Laboratory is not simply a portfolio whose source code happens to be visible. Open models, open-source software, reproducible experiments, and public teaching artifacts are part of the laboratory's institutional identity and research method. The laboratory exists to help ordinary people inspect, run, question, modify, and learn from useful AI systems. Openness is therefore a design constraint applied before architecture and release decisions—not a packaging task performed after the interesting work is complete.

The governing phrase is:

> **Built in public. Powered by open models. Reproducible by design. Improved with the community.**

This charter is subordinate only to law, binding license terms, privacy and security obligations, and approved incident directives. Any exception to the charter must be narrow, documented, time-bounded where possible, and entered in the Open Exception Register.

## Precise terminology

DRL uses vocabulary carefully because imprecise language becomes openwashing.

- **Open-source software** means software distributed under an OSI-approved license that permits use, study, modification, and redistribution.
- **Open Source AI** is reserved for systems that meet the applicable Open Source AI Definition or a later recognized standard, including access to the preferred form for modification.
- **Open-weight model** means weights are available under stated terms, but the complete system may not satisfy the Open Source AI definition because training data, source, or other modification materials are unavailable or restricted.
- **Source-available** means source can be inspected but the license is not an OSI-approved open-source license.
- **Public artifact** means an artifact can be downloaded; it does not imply open-source rights.
- **Open research** means methods, evidence, limitations, and sufficient reproduction materials are published where lawful and safe.

Every public page, README, model card, dataset card, and release note must identify the correct category. DRL will not call a custom-license open-weight model “open source” merely because it can be downloaded.

## The open-commons flywheel

DRL's preferred research cycle is:

```text
USE -> STUDY -> ADAPT -> EVALUATE -> PUBLISH -> UPSTREAM -> TEACH -> REPEAT
```

1. **Use:** build on strong community software, models, datasets, standards, and research.
2. **Study:** inspect behavior, licenses, failure modes, architecture, and constraints.
3. **Adapt:** create DRL-specific integrations, post-training, connectors, tests, and teaching examples.
4. **Evaluate:** produce reproducible evidence, including failures and unfavorable results.
5. **Publish:** release useful code, artifacts, methods, reports, and documentation.
6. **Upstream:** contribute generally useful fixes and improvements to the projects DRL depends upon.
7. **Teach:** convert the work into accessible labs, notes, workshops, and contributor pathways.
8. **Repeat:** use feedback and external replication to improve the next release.

A DRL release that consumes community work without attribution, usable release artifacts, or a plan to contribute knowledge back is institutionally incomplete.

## Open-by-construction promises

DRL commits to the following defaults for V1 and later public releases:

1. Core DRL-authored software is released under Apache License 2.0 unless a documented compatibility issue requires another OSI-approved license.
2. The central self-hosted path remains functional without a paid commercial model API.
3. Atticus Core and Atticus Edge are released publicly with weights or derivative artifacts where upstream terms lawfully permit, plus recipes, exact base revisions, evaluation evidence, and local serving profiles.
4. Public model and dataset claims include cards, provenance, intended use, limitations, and release review.
5. Every major hosted feature has a documented self-hosted or local research equivalent, although the managed service may provide convenience, scale, support, and operations.
6. Stable protocols, schemas, SDKs, CLIs, and extension interfaces are public.
7. Public benchmark methodology and scoring code are open. Hidden cases may remain private only to preserve benchmark validity and must be governed separately.
8. Reproducibility is measured by evidence levels rather than asserted in prose.
9. DRL publishes a dependency and upstream-attribution ledger.
10. DRL tracks and celebrates upstream contributions, community extensions, replications, and independent evaluations.
11. Security artifacts include SBOMs, checksums, signatures or attestations where available, provenance, and vulnerability reporting paths.
12. Closed artifacts require an exception record explaining why they cannot be open, who approved the exception, and what open substitute or interface remains available.

## What openness does not require

The charter does not require publication of:

- credentials, private user content, personal memory, private repositories, or employer information;
- raw donated traces before consent, de-identification, rights review, and quarantine;
- exploit details during an active security incident;
- hidden benchmark answers whose disclosure would destroy validity;
- third-party material DRL lacks rights to redistribute;
- private client data or commissioned work governed by a valid agreement;
- trademark rights to impersonate the official laboratory or misrepresent endorsement.

The absence of publication for one artifact does not permit vague claims. Public documentation must state the boundary and the reason.

## Forkability and sovereignty

A technically capable user should be able to fork the laboratory, inspect its interfaces, run a local profile, substitute compatible models, reproduce published examples, and add a specialist system without seeking DRL's permission. Official DRL identity and marks remain protected, but technical freedom is a feature rather than a threat.

The V1 sovereignty test is a clean-room installation that runs the public reference workflow using only openly licensed software, publicly distributable artifacts, and open-weight models. Cloud convenience may be demonstrated separately, but it cannot be the only functional path.

## Sustainable openness

DRL may charge for managed hosting, private deployment, integration, consulting, paid training, support, commissioned research, custom adapters, and operational services. Monetization must not depend on secretly withholding the modification surface of artifacts represented as open. The official distribution should remain useful to individuals, classrooms, researchers, and independent developers.

Enterprise capabilities may add administration, support, identity integration, compliance workflows, deployment automation, private connectors, and service guarantees. They must not retroactively remove rights from prior open releases or falsify the openness of the core.

## Institutional measures

The laboratory will report at least annually:

- public releases and their licenses;
- models, datasets, benchmarks, papers, and teaching artifacts released;
- upstream pull requests and issues contributed;
- external contributors and maintainers recognized;
- independent replications and community evaluations;
- open exceptions and their disposition;
- self-hosted installation success rate;
- unresolved licensing or provenance risks;
- security and supply-chain maturity;
- managed-service revenue used to sustain open work, when public reporting is appropriate.

The purpose of these measures is accountability, not vanity. Stars and downloads may be reported, but they are not substitutes for usefulness, reproducibility, safety, or community health.
