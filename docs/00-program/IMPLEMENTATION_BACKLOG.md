---
document_id: DRL-PRG-013
title: "Implementation Backlog"
version: 4.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Implementation Backlog

This controlled backlog contains **122** planned work packages. The machine-readable source is `requirements/work-packages.yaml`.

| Work package | Mission | Title | Status |
|---|---:|---|---|
| WP-00-01 | 00 | Audit all requirements and create a machine-readable requirement/work-package register. | PLANNED |
| WP-00-02 | 00 | Build a directed dependency graph and critical path with entry/exit gates. | PLANNED |
| WP-00-03 | 00 | Create GitHub milestone, label, issue, and PR templates with requirement/evidence fields. | PLANNED |
| WP-00-04 | 00 | Create initial issue backlog and assign each issue to exactly one mission and one evidence owner. | PLANNED |
| WP-00-05 | 00 | Identify unresolved director decisions and prepare ADR proposals without deciding them. | PLANNED |
| WP-00-06 | 00 | Define release dashboard and weekly program review format. | PLANNED |
| WP-01-01 | 01 | Create one-command setup, lint, typecheck, unit, contract, docs, and validation targets. | PLANNED |
| WP-01-02 | 01 | Implement controlled-document frontmatter, ID, status, link, and reference validators. | PLANNED |
| WP-01-03 | 01 | Validate all JSON Schemas, YAML configuration, OpenAPI, and example fixtures. | PLANNED |
| WP-01-04 | 01 | Create generated specification, ADR, requirement, schema, package, and agent indexes. | PLANNED |
| WP-01-05 | 01 | Establish Python and TypeScript workspace packages with minimal compilable skeletons. | PLANNED |
| WP-01-06 | 01 | Build fast CI with cache and artifact publication; create slower scheduled/full workflow placeholders with explicit gates. | PLANNED |
| WP-01-07 | 01 | Generate SBOM and license inventory foundations. | PLANNED |
| WP-02-01 | 02 | Implement generated or hand-maintained canonical types with cross-language conformance. | PLANNED |
| WP-02-02 | 02 | Implement task/run/event/error/claim/evidence/artifact/approval envelopes. | PLANNED |
| WP-02-03 | 02 | Implement run state machine and property-based transition tests. | PLANNED |
| WP-02-04 | 02 | Implement idempotency-key and request-digest helpers. | PLANNED |
| WP-02-05 | 02 | Implement provenance and content-digest utilities. | PLANNED |
| WP-02-06 | 02 | Implement safe trace event builder and redaction hooks. | PLANNED |
| WP-02-07 | 02 | Create protocol simulator and example end-to-end fixture trace. | PLANNED |
| WP-02-08 | 02 | Generate OpenAPI foundation and SDK compatibility report. | PLANNED |
| WP-03-01 | 03 | Implement rule-driven deny-by-default policy engine. | PLANNED |
| WP-03-02 | 03 | Implement resource/action scope normalization and risk classification. | PLANNED |
| WP-03-03 | 03 | Implement approval request/grant digest binding, expiry, versioning, and revocation. | PLANNED |
| WP-03-04 | 03 | Implement consent snapshot, telemetry filtering, and content-capture separation. | PLANNED |
| WP-03-05 | 03 | Implement quota/budget/circuit-breaker primitives. | PLANNED |
| WP-03-06 | 03 | Implement identity/session/service principal adapters and authorization helpers. | PLANNED |
| WP-03-07 | 03 | Build security fixtures for injection, replay, cross-session access, egress, and secret redaction. | PLANNED |
| WP-03-08 | 03 | Produce threat-model-to-control-to-test matrix and incident hooks. | PLANNED |
| WP-04-01 | 04 | Implement suite/case/target/scorer/gate manifests and validation. | PLANNED |
| WP-04-02 | 04 | Implement deterministic local execution and artifact recording. | PLANNED |
| WP-04-03 | 04 | Implement paired baseline/candidate analysis and bootstrap intervals. | PLANNED |
| WP-04-04 | 04 | Implement JSON, Markdown, HTML, JUnit, and PR-summary reports. | PLANNED |
| WP-04-05 | 04 | Implement accepted-baseline registry and manual promotion. | PLANNED |
| WP-04-06 | 04 | Implement target adapters for local function, HTTP, OpenAI-compatible endpoint, and trace import. | PLANNED |
| WP-04-07 | 04 | Implement CI gate with seeded pass/fail regressions. | PLANNED |
| WP-04-08 | 04 | Design judge/human-review interfaces and calibration records without making them release-critical yet. | PLANNED |
| WP-05-01 | 05 | Terraform foundation and project topology | PLANNED |
| WP-05-02 | 05 | Identity and trust boundaries | PLANNED |
| WP-05-03 | 05 | Deployment pipelines | PLANNED |
| WP-05-04 | 05 | Observability and SLO plumbing | PLANNED |
| WP-05-05 | 05 | Model training and serving substrate | PLANNED |
| WP-05-06 | 05 | Resilience and cost operations | PLANNED |
| WP-06-01 | 06 | Design system and tokens | PLANNED |
| WP-06-02 | 06 | Information architecture and content engine | PLANNED |
| WP-06-03 | 06 | Atticus public console | PLANNED |
| WP-06-04 | 06 | Demonstration and replay system | PLANNED |
| WP-06-05 | 06 | Accessibility, performance, privacy, and analytics | PLANNED |
| WP-06-06 | 06 | Recruiter, researcher, learner, and contributor journeys | PLANNED |
| WP-07-01 | 07 | Request/session lifecycle | PLANNED |
| WP-07-02 | 07 | Skill registry and planner | PLANNED |
| WP-07-03 | 07 | Model gateway and open-weight routing | PLANNED |
| WP-07-04 | 07 | Policy, approval, and tool execution | PLANNED |
| WP-07-05 | 07 | Specialist orchestration and synthesis | PLANNED |
| WP-07-06 | 07 | Recovery, observability, and public sandbox | PLANNED |
| WP-08-01 | 08 | Current base-model bakeoff | PLANNED |
| WP-08-02 | 08 | AtticusBench v1 | PLANNED |
| WP-08-03 | 08 | Training data production | PLANNED |
| WP-08-04 | 08 | Core post-training | PLANNED |
| WP-08-05 | 08 | Edge distillation and specialization | PLANNED |
| WP-08-06 | 08 | Quantization, packaging, and public release | PLANNED |
| WP-09-01 | 09 | Device identity, pairing, and revocation | PLANNED |
| WP-09-02 | 09 | Local runtime and model routing | PLANNED |
| WP-09-03 | 09 | Voice and interaction loop | PLANNED |
| WP-09-04 | 09 | File, repository, and shell tools | PLANNED |
| WP-09-05 | 09 | Private memory and data lifecycle | PLANNED |
| WP-09-06 | 09 | Packaging and adversarial validation | PLANNED |
| WP-10-01 | 10 | Source registry and connector SDK | PLANNED |
| WP-10-02 | 10 | Temporal canonical data model | PLANNED |
| WP-10-03 | 10 | Retrieval and deterministic analytics | PLANNED |
| WP-10-04 | 10 | Research workflow and evidence bundles | PLANNED |
| WP-10-05 | 10 | Public demo and contributor interface | PLANNED |
| WP-10-06 | 10 | Evaluation and operations | PLANNED |
| WP-11-01 | 11 | Official corpus and metadata | PLANNED |
| WP-11-02 | 11 | Document processing and semantic diff | PLANNED |
| WP-11-03 | 11 | Policy timeline and retrieval | PLANNED |
| WP-11-04 | 11 | Event-study framework | PLANNED |
| WP-11-05 | 11 | Atticus tools and public demo | PLANNED |
| WP-11-06 | 11 | Evaluation and publication | PLANNED |
| WP-12-01 | 12 | Domain model and synthetic institutions | PLANNED |
| WP-12-02 | 12 | Deterministic scenario engine | PLANNED |
| WP-12-03 | 12 | Explainability and audit | PLANNED |
| WP-12-04 | 12 | Atticus tool interface and public workstation | PLANNED |
| WP-12-05 | 12 | Verification and model risk discipline | PLANNED |
| WP-12-06 | 12 | Educational publication and safety | PLANNED |
| WP-13-01 | 13 | Contract compatibility and environment matrix | PLANNED |
| WP-13-02 | 13 | Integrated workflow implementation | PLANNED |
| WP-13-03 | 13 | Trace, evidence, and replay | PLANNED |
| WP-13-04 | 13 | Failure and degradation drills | PLANNED |
| WP-13-05 | 13 | User experience and narrative | PLANNED |
| WP-13-06 | 13 | Staging endurance and release evidence | PLANNED |
| WP-14-01 | 14 | Clean-room reproducibility | PLANNED |
| WP-14-02 | 14 | Requirement and evidence audit | PLANNED |
| WP-14-03 | 14 | Independent quality suites | PLANNED |
| WP-14-04 | 14 | Operational readiness | PLANNED |
| WP-14-05 | 14 | Public release dossier | PLANNED |
| WP-14-06 | 14 | Go/no-go review | PLANNED |
| WP-15-01 | 15 | V1 publication portfolio | PLANNED |
| WP-15-02 | 15 | Teaching and onboarding | PLANNED |
| WP-15-03 | 15 | Open-source contributor system | PLANNED |
| WP-15-04 | 15 | Public research archive | PLANNED |
| WP-15-05 | 15 | Launch communications | PLANNED |
| WP-15-06 | 15 | Post-launch research agenda | PLANNED |
| WP-06-07 | 06 | Build Open Source portal, Open Stack lineage, model commons, reproduce panel, and artifact/maturity badge surfaces. | PLANNED |
| WP-06-08 | 06 | Integrate evidence-derived model identity, licenses, upstream attribution, community replications, and self-hosting routes into project pages. | PLANNED |
| WP-08-07 | 08 | Publish Atticus Open Model Commons release structure across Hugging Face, GitHub, OCI, GGUF/Ollama, cards, and replication bundles. | PLANNED |
| WP-08-08 | 08 | Run open-model ecosystem bakeoff with precise license classification, runtime compatibility, local performance, and upstream-community factors. | PLANNED |
| WP-14-07 | 14 | Execute clean-room forkability, open-artifact, badge-evidence, SBOM/provenance, and terminology audit. | PLANNED |
| WP-14-08 | 14 | Verify every managed capability has a documented portable boundary and that V1 runs without paid commercial model APIs. | PLANNED |
| WP-15-07 | 15 | Launch public Open Stack and upstream contribution ledger with attribution, dependency ownership, and temporary-fork status. | PLANNED |
| WP-15-08 | 15 | Launch Atticus model/data/evaluation commons and community submission, replication, mentorship, and research sprint processes. | PLANNED |
| WP-15-09 | 15 | Publish annual open research accountability template covering artifacts, exceptions, upstream work, replications, community health, and sustainability. | PLANNED |
| WP-05-07 | 05 | Run director-gated OpenTofu and Valkey compatibility spikes; record evidence without silently changing approved architecture. | PLANNED |
| WP-06-09 | 06 | Implement open-source visual identity, artifact cards, lineage graph, contributor credit, and evidence-derived status rendering. | PLANNED |
| WP-08-09 | 08 | Execute the Atticus Open Model Commons release train for Core and Edge with full modification surfaces and community submission lanes. | PLANNED |
| WP-13-07 | 13 | Build the signature V1 open-source showcase workflow and reproduction bundle across all specialist systems. | PLANNED |
| WP-14-09 | 14 | Run dedicated open-identity validator, open artifact schemas, public-link checks, and clean-room showcase acceptance. | PLANNED |
| WP-15-10 | 15 | Publish contributor credit, open-source health baseline, sustainability statement, and open research accountability report. | PLANNED |
| WP-05-08 | 05 | Implement domain, DNS, TLS, Wix/cloud subdomain routing, monitoring, rollback, and cross-origin security evidence for dwit-labs.com. | PLANNED |
| WP-06-10 | 06 | Build the canonical Wix institutional site at www.dwit-labs.com and integrate truthful application launch, repository content, brand, consent, SEO, accessibility, and fallback behavior. | PLANNED |
| WP-13-08 | 13 | Verify the integrated reference journey from the Wix laboratory homepage through Atticus and specialist subdomains and back, including degraded/replay behavior. | PLANNED |
| WP-14-10 | 14 | Perform independent clean-room domain, Wix, TLS, redirect, cross-host navigation, consent, indexing, and iframe-boundary release acceptance. | PLANNED |
