---
document_id: DRL-WEB-016
title: "Open Source Portal, Model Commons, and Open Stack Website Experience"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Open Source Portal, Model Commons, and Open Stack Website Experience

## Product intent

The website must make openness visible within the first two minutes. Visitors should understand that DRL builds public models and software, depends proudly on upstream communities, and provides a path to run, reproduce, modify, teach, or contribute—not merely watch polished demos.

## Homepage signals

The homepage introduces the laboratory first, then displays an institutional strip:

```text
OPEN MODELS / OPEN SOFTWARE / PUBLIC EVALUATION / LOCAL OPERATION / REPRODUCIBLE RESEARCH
```

A featured panel presents **Atticus Open Model Commons** with direct links to model cards, weights, benchmark reports, local quickstarts, and the current candidate/release status. The panel must distinguish planned, experimental, release-candidate, and public-release artifacts.

The homepage also contains a restrained Open Stack acknowledgment: “DRL is built with and contributes to open technologies.” It links to the full ledger rather than using a meaningless logo wall.

## Required routes

```text
/open-source
/open-source/models
/open-source/datasets
/open-source/software
/open-source/benchmarks
/open-source/stack
/open-source/contribute
/open-source/replications
/open-source/upstream
/open-source/exceptions
```

## Open-source landing page

The landing page answers:

1. What can I run today?
2. What can I inspect or reproduce?
3. Which artifacts are truly open source, open weight, source available, or public only?
4. What hardware and cost are required?
5. How do I contribute at my current skill level?
6. Which research questions are open?
7. What is managed by DRL and what can be self-hosted?

Artifact cards show license, maturity, latest release, local/cloud requirements, reproducibility badge, security status, maintainers, and next good issue.

## Atticus model page

The model page is a research instrument, not a marketing landing page. It includes:

- Core/Edge relationship;
- exact base and license once selected;
- architecture and training stages;
- data mixture and review summary;
- benchmark tables with uncertainty and failure slices;
- tool-use and policy examples;
- quantization/runtime matrix;
- model card and safety report;
- Hugging Face/GitHub/container links;
- Colab and local quickstarts;
- community evaluations;
- release lineage;
- current limitations and withdrawal notices.

Visitors can compare base versus Atticus and Core versus Edge, while seeing exact artifact versions.

## Open Stack page

The Open Stack page visualizes the lineage from upstream communities to DRL systems:

```text
OPEN MODELS -> ATTICUS POST-TRAINING -> ATTICUS RUNTIME
HF/TRL/PEFT -> DATA + TRAINING -> MODEL RELEASES
vLLM/llama.cpp -> SERVING -> PUBLIC + LOCAL ATTICUS
PostgreSQL/pgvector -> EVIDENCE + STATE -> SPECIALISTS
OpenTelemetry -> TRACES -> EVALFORGE + STATUS
```

Each node explains why it was selected, license, version, official source, DRL modifications, open issues, upstream contributions, and alternatives. No node implies endorsement.

## Reproduce button

Every project page provides a `REPRODUCE` action opening a terminal-style panel with:

- exact release and digest;
- hardware profile;
- clone/install commands;
- fixture/live data mode;
- expected outputs;
- evaluation command;
- cost notes;
- troubleshooting and issue link.

Commands are generated from release metadata and tested in CI. They may not be hand-written marketing snippets that have never run.

## Contributor routing

The portal asks what the visitor wants to contribute: code, model/data, evaluation, documentation, teaching, accessibility, design, security, or research. It then shows appropriate issues, required background, mentors, setup, and governance. Atticus may guide the visitor but traditional navigation must remain complete.

## Community evidence

Display:

- accepted upstream contributions;
- community adapters/plugins;
- verified independent evaluations;
- replications;
- contributor releases;
- teaching use cases;
- correction history.

Community work is opt-in and attributed. DRL does not display private names or inflate participation.

## Visual identity

The open-source section keeps the cream-on-black terminal language but incorporates “commons” motifs: branching repository graphs, model lineage, artifact hashes, public-release stamps, and contribution routes. It must feel like an active academic systems lab—not a cryptocurrency dashboard or corporate developer portal.
