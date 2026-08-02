---
document_id: DRL-OSS-018
title: "Open Source Health, Reciprocity, and Impact Metrics"
version: 3.2.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Open Source Health, Reciprocity, and Impact Metrics

## Purpose

Stars, downloads, and social impressions may indicate attention but not health. DRL measures whether artifacts are usable, reproducible, maintained, teachable, safe, and improved by people beyond the founder.

## Metric families

### Artifact health

- supported artifacts with current owner;
- releases with complete manifest, card, license, checksum, and SBOM;
- median time from vulnerability disclosure to triage and fix;
- dependency freshness and unsupported-version count;
- local quickstart success rate;
- percentage of public interfaces with compatibility tests.

### Reproducibility and forkability

- clean-room installation pass rate;
- published claims independently reproduced;
- reproduction bundles passing on declared environments;
- undocumented-step count;
- percentage of flagship features available without paid model APIs;
- model/runtime substitutions passing the compatibility suite.

### Model and research quality

- AtticusBench task and safety slices with uncertainty;
- regressions caught before release;
- community evaluations accepted and reproduced;
- negative or null results published;
- dataset issues corrected with visible lineage;
- claims with linked evidence and artifact versions.

### Community health

- first-contribution completion rate;
- median time to first human response;
- review turnaround by issue class;
- contributor retention without pressure to volunteer;
- maintainer load and unreviewed backlog;
- accessibility, documentation, teaching, data, and research contributions recognized alongside code;
- Code of Conduct and moderation incidents resolved through documented process.

### Reciprocity

- upstream issues and pull requests opened;
- accepted upstream changes;
- downstream patches retired after upstream release;
- projects receiving financial sponsorship when budget permits;
- upstream maintainers credited in release and website materials;
- dependency risks and exit plans kept current.

### Public benefit

- learners completing teaching labs;
- educational institutions or community groups using released material;
- self-hosted installations and local/offline profiles reported voluntarily;
- accessible documentation coverage;
- public-interest research questions completed;
- evidence that low-resource users can operate Atticus Edge.

## Measurement rules

Metrics disclose collection method, window, denominator, limitations, and privacy impact. DRL does not rank individual volunteers, publish private productivity metrics, or optimize for superficial contribution volume. Public dashboards use aggregate data and avoid conversation content.

## Release gate

V1 must publish a baseline report even when values are zero. Zero is evidence; invented momentum is not. Later releases compare against the baseline and explain material deterioration.
