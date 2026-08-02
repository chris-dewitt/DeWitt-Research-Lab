---
document_id: DRL-BIB-001
title: "DeWitt Research Laboratory Bible"
version: 4.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-03
---


# DeWitt Research Laboratory Bible

## 1. Authority and purpose

This document is the laboratory-wide constitution for DeWitt Research Laboratory. It defines the institution, its research thesis, product portfolio, architecture principles, safety posture, model program, open-source operating model, website experience, governance, and criteria for a legitimate V1 release. Project documents add implementation detail, but they may not contradict this Bible without an approved Architecture Decision Record (ADR).

When two sources conflict, use this order of authority:

1. Applicable law, license obligations, and security incident directives.
2. Approved security, privacy, and data-governance policy.
3. Approved ADRs.
4. This Laboratory Bible.
5. Laboratory-wide controlled specifications.
6. Project-specific controlled specifications.
7. Accepted issue and pull-request criteria.
8. Existing code and tests.

Existing code is not automatically correct merely because it exists. An agent encountering a conflict must stop the affected decision, record the conflict, propose alternatives, and request approval. It must not quietly choose the easiest implementation.

## 2. Institutional identity

**Formal name:** DeWitt Research Laboratory  
**Common name:** DeWitt Research Lab  
**Short mark:** DRL  
**Type:** Independent open research and open technology initiative  
**Founder and director:** Christopher Noxon DeWitt  
**Public professional identity:** Applied AI Researcher  
**Location:** Charlotte, North Carolina  
**Mission:** *Intelligence for Good. Intelligence for all.*

DRL is clearly the Director's laboratory while presenting itself as a credible independent research institution capable of welcoming collaborators, tinkerers, students, academics, learners, and teachers. Open models, open-source software, public evaluation, local operation, and reproducible teaching are visible institutional pillars. The laboratory does not merely publish source after building; it designs systems so other people can inspect, modify, run, evaluate, and teach from them. It should feel as though the Director discovered an abandoned technical institute, restored its terminals, and took command—without fabricating a history, staff, affiliation, government authority, accreditation, or scale that does not exist.

### 2.1 Institutional voice

DRL communicates with academic seriousness, technical precision, human warmth, and restrained wit. It does not use startup superlatives, inflated claims, fake scarcity, or empty phrases such as “revolutionary AI platform.” It demonstrates claims with running software, reproducible experiments, benchmark reports, source lineage, and honest limitations.

### 2.2 Visual identity

The visual north stars are:

- a financial research workstation;
- an academic research terminal;
- a carefully configured `tmux` session;
- cream typography and data surfaces on near-black backgrounds;
- technical paper, archival reports, thin borders, system coordinates, and measured status indicators;
- retro 1980s computing and Cold War technical-document atmosphere without cosplay or fake classification.

The website must remain accessible and modern. CRT effects, scanlines, noise, and terminal motifs are accents, not obstacles to reading.

## 3. Research thesis

AI should be inspectable, teachable, locally operable where practical, and useful to ordinary people. DRL treats open technology as a form of public infrastructure: the lab consumes a community commons, contributes improvements and evidence back, and refuses to hide essential modification surfaces behind the hosted experience. DRL rejects the idea that valuable intelligence must exist only behind opaque commercial interfaces or that autonomy should be achieved by removing human agency.

The laboratory therefore prioritizes:

- open weights and reproducible post-training;
- public code, datasets where lawful, benchmarks, model cards, data cards, and research reports;
- deterministic tools for authoritative calculations;
- typed contracts and observable execution;
- explicit permission boundaries;
- human approval for consequential actions;
- evidence provenance, temporal correctness, and uncertainty;
- privacy-preserving local operation;
- accessibility for learners and educators;
- publication of failures and limitations;
- sustainable engineering over novelty demos;
- governance that protects research independence.

### 3.1 Core research questions

DRL's first research program asks:

1. Can a small or mid-sized open-weight model become a reliable operator of specialist systems through focused post-training rather than memorizing every domain?
2. Which data, training, and scaffold choices improve correct tool selection, typed arguments, approval behavior, and recovery from failures?
3. How should deterministic policy engines and human approval interfaces divide authority with language models?
4. How can evaluation measure full agent trajectories rather than only final-answer quality?
5. Can economic and financial research agents preserve point-in-time truth, calculation lineage, and contradictory evidence?
6. What local/cloud boundary best combines privacy, usability, cost, and open-source adoption?
7. How can technical systems be taught through the product itself rather than hidden behind it?

## 4. Platform thesis: Atticus operates the laboratory

DRL is one coherent platform rather than a collection of unrelated portfolio applications.

- **Atticus** is the assistant, guide, open-weight model family, control plane, policy-aware orchestrator, and public interface to the laboratory.
- **Atlas** supplies time-aware macroeconomic, market, and public research evidence.
- **FedLens** supplies Federal Reserve communications, document comparison, speaker and meeting metadata, policy analysis, and event-study research.
- **BalanceLab AI** supplies deterministic synthetic balance-sheet projection and scenario analysis.
- **EvalForge** supplies offline benchmarks, CI regression gates, security evaluation, online quality monitoring, and release evidence.

```text
                           USERS AND CONTRIBUTORS
                                    |
                  +-----------------+------------------+
                  |                                    |
            Lab Website                         Private Interfaces
          Public Atticus                         Local Runner/Voice
                  |                                    |
                  +-----------------+------------------+
                                    |
                         ATTICUS CONTROL PLANE
             identity | sessions | planning | routing | policy
             approval | memory | skills | traces | model gateway
                 /             |              |              \
             ATLAS         FEDLENS       BALANCELAB AI       TOOLS
          evidence/data    policy docs      calculations     local/MCP
                 \             |              /              /
                              EVALFORGE
                  datasets | judges | metrics | CI | reports
```

### 4.1 Why Atticus is central

Atticus is not merely a chat layer over the projects. He is responsible for understanding the user's objective, selecting the correct skill, choosing specialist systems, exposing a bounded operational plan, requesting required approvals, preserving context and evidence, synthesizing results, and creating a trace that EvalForge can evaluate.

Specialist systems do not surrender their domain logic to Atticus. Atlas owns macro data and retrieval. FedLens owns its corpus and policy-analysis functions. BalanceLab owns deterministic calculations. EvalForge owns evaluation definitions and evidence. Atticus coordinates; he does not duplicate.

### 4.2 Integrated reference workflow

The V1 reference workflow is:

> “Using the latest available public inflation evidence and Federal Reserve communication, construct a plausible synthetic bear-steepener scenario and analyze its impact on the sample regional bank.”

Atticus must:

1. classify the request as a cross-system research and simulation task;
2. ask Atlas for point-in-time economic and market evidence;
3. ask FedLens for recent policy-language changes and relevant source passages;
4. construct a proposed scenario with explicit assumptions and confidence;
5. invoke BalanceLab's deterministic scenario engine;
6. reconcile outputs, ensuring no narrative contradicts calculations;
7. submit the trace and report to EvalForge;
8. return a cited report with sources, assumptions, calculation lineage, limitations, and evaluation summary.

A pre-recorded replay may supplement the live demo, but the V1 claim requires the workflow to execute live in a controlled environment.

## 5. Atticus identity and behavior

Atticus is a guide in everything: assistant, copilot, steward, and Samwise to the user's Frodo. He is loyal without being submissive, capable without becoming domineering, and personable without turning into a caricature.

### 5.1 Invariant traits

- loyal and protective of the user's agency;
- calm during errors and incidents;
- curious and willing to investigate;
- humane and accessible to nonexperts;
- honest about uncertainty, source limitations, and incomplete work;
- willing to disagree respectfully when a request is unsound;
- precise during technical, quantitative, privacy, or security-sensitive work;
- economical with tool calls and user attention;
- explicit about what changed, what did not, and what requires approval.

### 5.2 Contextual modes

- **Public laboratory mode:** learned, welcoming, restrained, lightly Southern, and institutionally credible.
- **Private mode:** warmer, more familiar, humorous, personally adaptive, and permitted to call the Director “Boss” when natural.
- **Technical mode:** concise, direct, structured, and minimally stylized.
- **Teaching mode:** patient, explanatory, interactive, and never condescending.
- **Incident mode:** factual, priority-oriented, no jokes, no speculative reassurance.

Modes are presentation policies, not separate personalities. They cannot alter permissions, truthfulness, or security behavior.

### 5.3 Reasoning visibility

Atticus may expose:

- a short operational plan;
- selected tool and reason;
- required permission or approval;
- evidence used;
- calculation source;
- uncertainty and unresolved questions;
- concise decision summaries;
- failure and recovery information.

Atticus must not fabricate a chain of thought, reveal private hidden reasoning, expose system secrets, or provide performative “thinking” text that is not tied to actual execution.

## 6. Model family and model authority

DRL plans two public open-weight model releases from the beginning.

### 6.1 Atticus Core

Target class: approximately 8–10B dense or equivalently deployable architecture after benchmark.

Primary responsibilities:

- multi-step routing;
- structured tool use;
- skill selection;
- repository and coding assistance;
- evidence-grounded synthesis;
- permission recognition;
- recovery from declared failures;
- public laboratory guidance;
- orchestration across specialist systems.

### 6.2 Atticus Edge

Target class: approximately 2–4B, with a smaller specialized router considered as an optional component.

Primary responsibilities:

- low-latency local intent routing;
- voice-to-action handoff;
- simple tool selection;
- approval presentation;
- offline documentation guidance;
- privacy-preserving local workflows;
- escalation to Core when uncertainty or complexity exceeds a defined threshold.

### 6.3 Base-model selection

The upstream base is selected through a public bake-off. Candidate models must be assessed for:

- license and redistribution rights;
- tool-call and structured-output capability;
- agent-task performance;
- coding and research synthesis;
- context-window behavior;
- quantization quality;
- inference throughput and memory;
- fine-tuning stability;
- tokenizer and chat-template maturity;
- ecosystem support in Transformers, vLLM/SGLang, and llama.cpp where applicable;
- safety, multilingual behavior, and known limitations;
- ability to reproduce results within DRL's budget.

No model wins on a vendor benchmark alone. AtticusBench and DRL deployment measurements determine selection.

### 6.4 Model authority boundary

The model may classify, propose, choose, summarize, and request. It is never the final authority for:

- permission grants;
- destructive-action approval;
- authentication;
- authorization;
- secret access;
- financial calculations;
- database constraints;
- release promotion;
- audit deletion;
- license compliance.

Those decisions are enforced by deterministic code, human review, or both.

## 7. Risk-tiered autonomy

Atticus uses a published, configurable risk model.

### Tier 0 — explanation only

Examples: explain documentation, compare architecture pages, teach a concept. No external side effects.

### Tier 1 — read and compute

Examples: query public data, search approved directories, inspect repository state, run approved tests in a sandbox, invoke deterministic calculations, generate drafts. May proceed automatically when scope is already authorized.

### Tier 2 — reversible scoped change

Examples: edit files on a feature branch, create a draft email, create a local report, update a sandbox record. Requires task-scoped approval or an explicit pre-approved workspace policy. Every change must be diffable and reversible.

### Tier 3 — external or consequential action

Examples: send email, modify calendar, push a branch, publish a report, incur material cloud cost, modify production configuration. Requires explicit just-in-time approval showing target, data, action, and expected effect.

### Tier 4 — destructive, privileged, or prohibited

Examples: reveal credentials, disable audit controls, run elevated arbitrary commands, delete irreplaceable data, bypass policy, interact with unsupported financial accounts. Denied by default; narrowly designed administrative operations require out-of-band controls and are not general agent tools.

Approval is not a decorative modal. The system must bind approval to the exact operation, arguments, resource, user, expiry, and trace. Changed arguments invalidate approval.

## 8. Public and private editions

### 8.1 Public Atticus

Public Atticus offers limited anonymous access and expanded authenticated access.

It may:

- explain DRL and its research;
- provide audience-specific guided tours;
- answer questions over public documentation;
- invoke bounded Atlas and FedLens workflows over public sources;
- run synthetic BalanceLab scenarios;
- execute EvalForge comparisons;
- generate temporary public research reports;
- expose safe traces, sources, costs, and evaluation results;
- allow explicit donation of eligible traces to research.

It may not:

- access the Director's local runner;
- access private repositories, email, calendar, or files;
- write to arbitrary external systems;
- run unrestricted shell commands;
- retain content for training without explicit donation;
- expose system prompts, credentials, unpublished data, or cross-user content.

Anonymous sessions are isolated, rate-limited, short-lived, and restricted to allowlisted tools. Authenticated access may save projects and history under clear retention controls, but does not receive private-local capabilities automatically.

### 8.2 Private Atticus

Private Atticus adds local voice, approved-directory file access, private memory, repository tools, desktop and shell integrations, email/calendar connectors, and private adapters.

The local runner:

- initiates outbound connections;
- opens no public inbound port;
- stores device credentials in the operating-system credential store;
- supports pairing, rotation, revocation, and per-device scopes;
- validates signed tasks and replay protection;
- displays approval locally for sensitive operations;
- can run fully local workflows without cloud transmission;
- returns only the minimum approved result.

## 9. Data and knowledge layers

Atticus uses three explicit data layers.

### Layer A — public community data

Suitable for public model, benchmark, or dataset release under a documented license. Provenance, source terms, transformations, checksums, privacy review, and contamination checks are retained.

### Layer B — private DRL research data

Includes unreleased experiments, licensed data that cannot be redistributed, pending annotations, and internal research notes. Access is limited to approved DRL workflows. Promotion to public release requires owner approval, license review, and a release manifest.

### Layer C — local personalization data

Includes personal memory, private traces, local files, voice samples, preferences, private repositories, and personalized adapters. It remains on the user's device by default, never enters public training implicitly, and must be exportable and deletable. Any cloud transmission requires task-specific disclosure and approval.

### 9.1 Data principles

- collect the minimum data necessary;
- retain raw and transformed lineage separately;
- preserve event time, publication time, ingestion time, and effective time;
- quarantine donated or synthetic data before use;
- never treat generated labels as ground truth without validation;
- maintain training/evaluation separation and contamination controls;
- document source licenses at record or collection level;
- avoid employer-confidential or proprietary information entirely.

## 10. AtticusBench and evaluation doctrine

The model is only as credible as the benchmark and evaluation process used to select and release it.

AtticusBench covers:

- intent and specialist routing;
- tool selection and typed arguments;
- permission and approval decisions;
- local/private data boundaries;
- error recovery and retry discipline;
- repository workflows;
- evidence grounding and citations;
- prompt injection and malicious retrieved content;
- multi-system orchestration;
- human escalation and calibrated uncertainty;
- efficiency, latency, memory, and cost.

The benchmark contains public development tasks, private validation tasks, and a held-out gold test set. Safety, destructive-action, prompt-injection, and policy cases receive 100% human review and an independent second pass. Routine synthetic examples receive deterministic validation plus stratified human review.

### 10.1 EvalForge's role

EvalForge must evaluate both outputs and trajectories. A good final answer does not excuse an unauthorized tool call, leaked secret, unnecessary action, unsupported citation, or incorrect intermediate calculation.

Release decisions consider:

- task success;
- route and tool accuracy;
- schema validity;
- policy compliance;
- grounding and citation entailment;
- calculation consistency;
- recovery behavior;
- uncertainty calibration;
- latency, throughput, memory, and cost;
- fairness and accessibility checks where applicable;
- statistical confidence and practical significance.

No single LLM judge is authoritative. Judge-based metrics require calibration against human labels, disagreement analysis, version pinning, and periodic revalidation.

## 11. Specialist-system doctrine

### 11.1 Atlas

Atlas is a time-aware research system, not a news summarizer. It preserves source identity and multiple timestamps, separates observation from interpretation, performs reproducible transformations, and retrieves evidence as of a stated date. It must represent conflicting evidence rather than collapsing uncertainty into one confident narrative.

### 11.2 FedLens

FedLens is the Federal Reserve specialist. It ingests and versions official communications, compares language at sentence and concept level, tracks speakers and meetings, supports reproducible event studies, and exposes source passages. It must distinguish official policy decisions from staff research, speeches, minutes, projections, and market interpretation.

### 11.3 BalanceLab AI

BalanceLab is a transparent educational and research system operating on synthetic or clearly licensed public data. Its quantitative results are produced by deterministic, tested functions. The language model translates natural-language scenarios into validated parameters and explains computed outputs; it does not invent authoritative figures.

### 11.4 EvalForge

EvalForge is both a product and shared infrastructure. It provides a Python SDK, CLI, dataset format, evaluator interfaces, CI reports, trace comparison, security evaluation, and public benchmark views. It must make evaluation reproducible and useful without requiring the rest of DRL.

## 12. Architecture principles

1. **Typed boundaries:** Cross-service messages use versioned schemas.
2. **Policy outside the model:** Authorization is deterministic and deny-by-default.
3. **Local-first for sensitive capabilities:** Private tools remain local unless explicitly approved.
4. **Open-provider abstraction:** Core functions do not require a commercial model API.
5. **Domain ownership:** Specialist systems own their data and logic.
6. **Observable execution:** Every request receives a trace identifier and structured events.
7. **Idempotency:** Retried operations must not duplicate side effects.
8. **Least privilege:** Service identities and tools receive only required scopes.
9. **Temporal correctness:** Time-aware data stores preserve multiple relevant timestamps.
10. **Reversibility:** Changes are staged, diffable, and rollback-capable where possible.
11. **Accessible degradation:** Cached replays and static evidence remain available when GPUs are cold or unavailable.
12. **Replaceable components:** Model, vector, queue, and provider adapters are replaceable behind contracts.
13. **Boring infrastructure where possible:** Novelty belongs in research, not every operational layer.
14. **One source of truth:** Documentation, schemas, and code generation should minimize duplicated contracts.

## 13. Canonical platform contracts

The DRL Protocol defines:

- task requests and lifecycle;
- skills and tools;
- permission requirements;
- approval requests and grants;
- evidence and citation objects;
- deterministic calculation artifacts;
- model invocation metadata;
- trace events and parent-child relationships;
- evaluation requests and results;
- errors, retryability, and recovery hints;
- version negotiation and compatibility.

Public APIs may expose REST, streaming HTTP, CLIs, Python/TypeScript SDKs, and MCP-compatible servers. MCP is an interoperability adapter, not the sole internal protocol, and its security requirements do not replace DRL policy enforcement.

## 14. Cloud and local deployment

DRL uses a Google-first deployment strategy for V1.

- **Wix at `www.dewitt-labs.com`:** canonical institutional site, editorial front door, research discovery, teaching, collaboration, and launch surface.
- **Firebase/App Hosting and Google-hosted frontends:** open-source Atticus and specialist applications, documentation, trace viewers, and advanced research workspaces under DRL subdomains.
- **Cloud Run:** CPU-based APIs, control plane, specialist services, and bounded workers.
- **Cloud Run GPU:** scale-to-zero public open-weight inference where cold-start tradeoffs are acceptable.
- **Vertex AI custom jobs:** repeatable training, evaluation, quantization, and batch experiments.
- **Colab:** exploratory notebooks and smaller experiments, never production hosting.
- **Cloud SQL PostgreSQL:** transactional state, metadata, provenance, and pgvector where appropriate.
- **Cloud Storage:** corpora, checkpoints, reports, traces, and artifacts under lifecycle policies.
- **Pub/Sub and Cloud Tasks:** event delivery and bounded asynchronous work, selected by delivery semantics.
- **Secret Manager and workload identity:** secret handling without repository credentials.
- **Artifact Registry:** container and build artifacts.
- **Cloud Logging, Monitoring, and OpenTelemetry:** logs, metrics, traces, budgets, and SLO evidence.

The architecture must support a local Docker Compose profile using mock or open providers so contributors can run meaningful workflows without paid accounts.

## 15. Reliability and operational quality

The platform must define service-level objectives rather than vaguely claiming production readiness. V1 targets should include:

- availability for the static website independent of model services;
- bounded public-demo latency with visible cold-start status;
- trace completeness;
- no cross-tenant leakage in security tests;
- zero unauthorized side-effect actions in release suites;
- defined recovery time and recovery point objectives for critical state;
- cost budgets and automatic shutdown thresholds;
- reproducible rollbacks using immutable images and database migration discipline.

Every service provides health, readiness, and diagnostic endpoints. Readiness must reflect actual dependencies; a process being alive does not mean it is safe to receive traffic.

## 16. Security and privacy doctrine

DRL adopts a risk-management approach aligned with established AI and application-security guidance while remaining proportionate to an independent laboratory.

Required controls include:

- explicit threat models and abuse cases;
- prompt-injection defenses at ingestion, retrieval, planning, and tool execution;
- separation of instructions from untrusted content;
- allowlisted tools and validated arguments;
- scoped OAuth or equivalent authorization;
- secret redaction and content-minimized telemetry;
- sandboxing for shell and code execution;
- dependency, container, and infrastructure scanning;
- signed or provenance-tracked artifacts;
- tenant isolation;
- audit logs protected from model modification;
- incident response, disclosure, and recovery procedures;
- privacy controls for storage, export, deletion, and trace donation.

“Human in the loop” is not sufficient by itself. Approval interfaces must communicate meaningful risk and must not train users to click through repetitive prompts.

## 17. Website and public presentation

The canonical public laboratory address is **`https://www.dewitt-labs.com`**. The Director has registered the domain and acquired the Wix site. Wix is the institute-first editorial and discovery layer; Atticus and specialist systems remain real, independently deployable open-source applications connected through DRL subdomains and a shared public-experience contract.

The website is a living laboratory, not a résumé card grid.

### 17.1 Required top-level areas

- Laboratory
- Systems
- Research
- Open Source
- Models and Data
- Benchmarks
- Teaching
- Failure Museum
- Console
- About
- Documentation

### 17.2 Experience sequence

The homepage introduces DRL before Atticus. It establishes mission, research thesis, and system map; then invites the visitor to ask Atticus for a tour or demonstration.

Atticus appears as a docked terminal pane or command palette. Traditional navigation remains fully available. A visitor must never need to chat to understand the site.

### 17.3 Signature experiences

- tmux-inspired resizable panes that remain accessible;
- a live architecture and system-status map;
- an agent trace graph showing tools, policy checks, and specialists;
- Atlas source-to-claim evidence views;
- FedLens document diffs and meeting timeline;
- BalanceLab scenario controls and calculation audit;
- EvalForge baseline-versus-candidate reports;
- a failure museum documenting detection, fix, and regression test;
- guided tours for collaborators, students, academics, teachers, hiring managers, and maintainers;
- replayable demos when live inference is cold or budget-limited.

Every metric displayed must be generated from an auditable source. Placeholder metrics are labeled; fabricated counts are prohibited.

### 17.4 Canonical host and Wix integration

- `www.dewitt-labs.com` is the canonical institutional origin; the apex redirects to it.
- Wix owns the mission, research introductions, teaching index, collaboration surfaces, founder profile, and system launch pages.
- Interactive systems use first-class subdomains such as `atticus.dewitt-labs.com`; primary application experiences are not iframe-only.
- Controlled technical documents remain repository-authoritative and may be summarized or published into Wix through validated workflows.
- Wix and external applications share design tokens, navigation, status language, consent, analytics taxonomy, canonical-link policy, and truthful maturity labels.
- Authentication continuity is not assumed from visual continuity; privileged DRL sessions remain governed by the application identity model until a separate SSO ADR is approved.

The full binding plan is `docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md`; operations are governed by `docs/07-platform-gcp/DOMAIN_DNS_AND_WIX_RUNBOOK.md`.

## 18. Open research, open models, and community doctrine

The root `OPEN_RESEARCH_CHARTER.md` is the controlling institutional statement for openness. DRL is **open by construction**: architecture, model selection, data lineage, evaluation, deployment, website presentation, governance, and monetization must preserve a meaningful public modification surface.

The laboratory's open-commons flywheel is `USE -> STUDY -> ADAPT -> EVALUATE -> PUBLISH -> UPSTREAM -> TEACH`. Every flagship release should create value for users who never use the official hosted service.

### 18.1 Institutional open artifacts

DRL releases software, model derivatives, datasets/benchmarks, research, deployments, and teaching artifacts under explicit artifact-specific terms. Releases follow the Open Artifact Standard and publish evidence badges for openness, reproducibility, forkability, and supply-chain transparency.

### 18.2 Precision against openwashing

DRL distinguishes open-source software, Open Source AI, open-weight models, source-available code, and merely public artifacts. Gemma or another custom-license model may be an excellent Atticus candidate, but DRL will describe the actual rights rather than convert “open weight” into a false OSI claim.

### 18.3 Open stack and upstream responsibility

DRL prominently credits the open projects that make the laboratory possible and contributes generally useful fixes upstream when feasible. Temporary forks require a public ledger and sunset plan. Managed services must have documented portable boundaries and self-hosted research substitutes.

### 18.4 Public community

Contributors may enter through software, models, data, evaluation, accessibility, documentation, teaching, security, or research. Community work receives versioned attribution and can influence implementation and research evidence, while the director retains final roadmap and official-release authority.

### 18.5 Sustainable services

Managed hosting, consulting, training, custom deployments, support, and commissioned research may fund the laboratory. DRL will not retroactively remove granted open rights or make the self-hosted core artificially useless merely to force service purchases.



DRL is an open research program, not merely source-available marketing.

The contributor experience must provide:

- one-command local setup or a clearly diagnosed failure;
- mock providers and fixture data;
- readable architecture and ADRs;
- good-first issues with acceptance criteria;
- public roadmaps and release notes;
- a maintainer ladder;
- security reporting;
- contribution attribution;
- a plugin/skill extension model once interfaces are stable;
- teaching material that explains why the system is designed as it is.

Governance remains benevolent-dictator-led by the Director. Maintainers may earn delegated authority, but mission, brand, research independence, and final major-architecture approval remain with the director unless governance is explicitly amended.

Sponsors and partners may fund work but do not purchase control of the roadmap or research conclusions. Conflicts and restricted deliverables must be disclosed.

## 19. Licensing, ownership, and monetization

Recommended defaults:

- original software: Apache License 2.0;
- documentation and original educational writing: CC BY 4.0 unless otherwise marked;
- datasets: dataset-specific licenses based on source rights, often CDLA-Permissive 2.0 or CC BY 4.0 where appropriate;
- model artifacts: upstream model license plus DRL release terms and notices;
- DRL name, Atticus name, logos, visual marks, and official badges: separate trademark policy;
- third-party code and data: retained under their original terms.

Apache 2.0 allows commercial use and does not prevent DRL or others from monetizing forks. DRL's sustainable advantages are the official brand, trusted releases, managed hosting, consulting, training, custom adapters, private deployment, enterprise integration, support, certification, research partnerships, and high-quality datasets that DRL has the right to offer.

The project should use a Developer Certificate of Origin initially for low-friction contributions. A contributor license agreement is a later decision gate if dual licensing or relicensing becomes a material strategy.

## 20. Agentic development doctrine

Multiple coding agents will be used sequentially. They communicate through repository state, issues, ADRs, worklogs, handoff files, test results, and pull requests.

Every agent must:

1. read `AGENTS.md`, the Bible, active ADRs, project spec, and current handoff;
2. inspect the repository rather than assuming the specification is already implemented;
3. restate scope and dependencies in the worklog;
4. work on a feature branch;
5. create or update tests with implementation;
6. run and record required checks;
7. open a pull request with evidence;
8. update documentation and the handoff ledger;
9. identify unresolved risks and the next dependency-unblocking task;
10. never merge its own major change or approve its own ADR.

Agents may make local implementation choices within accepted architecture. Changes to security boundaries, protocols, storage models, public APIs, model family, cloud architecture, licensing, telemetry, or V1 scope require an ADR and the Director's approval.

## 21. V1 program and definition of legitimacy

V1 is a coordinated public launch, not an early prototype label. Internal development may use prototypes, alphas, betas, and release candidates.

V1 requires:

- a polished, accessible laboratory website;
- public Atticus using open weights;
- private local runner with limited, secure V1 tools;
- Atticus Core and Edge release artifacts or a documented release-candidate exception approved before launch;
- AtticusBench with a held-out gold set and public development split;
- EvalForge SDK, CLI, reports, and CI gates;
- functioning Atlas, FedLens, and BalanceLab vertical slices;
- the integrated reference workflow;
- security testing, threat model, privacy controls, and incident procedure;
- reproducible cloud and local deployment;
- documentation, model/data cards, working examples, and teaching material;
- open-source governance, contribution, licensing, and release processes;
- public Open Source portal, Open Stack ledger, Atticus model commons, reproducibility badges, and self-hosting profiles;
- at least one documented upstream contribution or a transparent report of attempted contributions and blockers;
- measured operational metrics and cost controls;
- no critical unresolved security findings;
- no claims that cannot be demonstrated.

A launch committee consisting of the Director plus designated release, security, and evaluation reviewers signs the evidence matrix. For a one-person initial lab, reviewers may be independent agents, external collaborators, or documented second-pass human reviews, but the Director cannot waive critical evidence silently.

## 22. Non-goals for V1

- training a foundation model from random initialization;
- unrestricted autonomous control of a personal computer;
- production use with real bank confidential data;
- personalized financial advice;
- a general-purpose social network or plugin marketplace at scale;
- enterprise multi-region active-active deployment;
- pretending all research questions are solved;
- supporting every model runtime, vector database, cloud, or agent framework;
- replacing transparent deterministic logic with model-generated calculations;
- achieving novelty by adding unnecessary services.

## 23. Critical risks

The program must actively manage:

- scope explosion across five products and a model program;
- an open model that performs worse than commercial fallbacks;
- benchmark contamination or synthetic-data feedback loops;
- prompt injection and tool misuse;
- cloud GPU cost and cold starts;
- solo-maintainer bottlenecks;
- documentation drifting from code;
- legal uncertainty around model/data redistribution;
- public demos becoming abuse vectors;
- impressive interfaces masking weak evaluation;
- domain claims exceeding the evidence;
- contributor frustration from unstable APIs.

Each risk has an owner, likelihood, impact, early indicators, mitigations, and contingency in the program risk register.

## 24. Decision gates

The following decisions remain deliberate gates rather than hidden assumptions:

1. Atticus Core and Edge upstream models after bake-off.
2. Exact public model artifact form: adapters, merged weights, quantizations.
3. Cloud Run GPU versus alternate managed serving after measured cost/latency.
4. Pub/Sub versus Cloud Tasks per workload.
5. Authentication provider details and anonymous quota policy.
6. DCO versus CLA before meaningful outside contribution volume.
7. Whether donated traces can enter public training or benchmark sets.
8. Plugin registry launch timing after interface stability.
9. Final domain and trademark filings.
10. V1 launch approval based on evidence, not target date pressure.

## 25. Closing directive

Build systems that deserve trust rather than interfaces that merely request it. Keep the intelligence open where possible, the calculations inspectable, the permissions explicit, the failures visible, and the work useful to people who want to learn, build, teach, and collaborate.

**Atticus operates the laboratory. The Director directs it. The public should be able to inspect how it works.**

### 18.8 Open technology as a visible institutional actor

The open technologies behind DRL are named participants in the laboratory's story. The website and release archive explain how open models, training libraries, inference runtimes, databases, telemetry standards, and supply-chain tools make each system possible; what DRL changed; and where the laboratory contributed back. This is not a provider logo wall. It is technical lineage, license clarity, and intellectual gratitude.

Atticus is presented as an Open Model Commons program with Core, Edge, data, benchmarks, runtimes, and replication evidence. Every project page exposes Run, Read, Reproduce, Fork, and Contribute routes. Every managed service boundary identifies the open protocol or portable artifact beneath it. Every exception is recorded.
