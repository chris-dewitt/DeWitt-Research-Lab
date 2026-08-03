---
document_id: DRL-PRG-012
title: "V1 Requirement Catalog"
version: 4.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# V1 Requirement Catalog

This controlled catalog contains **132** approved V1 requirements. The machine-readable source is `requirements/requirements.yaml`.

| ID | Requirement | Owner | Canonical specification |
|---|---|---|---|
| DRL-SYS-001 | Atticus shall coordinate specialist services only through versioned typed contracts. | Architecture | `docs/02-architecture/` |
| DRL-SYS-002 | The V1 production intelligence path shall use identifiable open-weight models and disclose routing. | Architecture | `docs/02-architecture/` |
| DRL-SYS-003 | The local/mock developer profile shall run without paid commercial model APIs. | Architecture | `docs/02-architecture/` |
| DRL-SYS-004 | Every externally visible action and public claim shall be attributable to a trace and artifact/evidence chain. | Architecture | `docs/02-architecture/` |
| DRL-SYS-005 | Every long-running request shall support deadline, cancellation, bounded retries, and terminal status. | Architecture | `docs/02-architecture/` |
| DRL-SYS-006 | Public, private-cloud, private-local, and offline modes shall have distinct capabilities and data policies. | Architecture | `docs/02-architecture/` |
| DRL-SYS-007 | Protocol-breaking changes shall require versioning, migration, consumer compatibility evidence, and ADR. | Architecture | `docs/02-architecture/` |
| DRL-SYS-008 | One integrated reference workflow shall exercise Atticus, Atlas, FedLens, BalanceLab, and EvalForge. | Architecture | `docs/02-architecture/` |
| DRL-SYS-009 | The platform shall degrade truthfully to replay/documentation when live compute is unavailable. | Architecture | `docs/02-architecture/` |
| DRL-SYS-010 | No component shall infer completion solely from prose; evidence artifacts shall determine release status. | Architecture | `docs/02-architecture/` |
| DRL-SEC-001 | The model shall never grant its own permission or override deterministic policy. | Security | `docs/06-security/` |
| DRL-SEC-002 | Public Atticus shall expose no external write tool or unrestricted code/shell execution. | Security | `docs/06-security/` |
| DRL-SEC-003 | Consequential private actions shall require a scoped, digest-bound, expiring approval. | Security | `docs/06-security/` |
| DRL-SEC-004 | Changed arguments or effect shall invalidate a prior approval. | Security | `docs/06-security/` |
| DRL-SEC-005 | Private devices shall initiate outbound connections; cloud services shall not require inbound device exposure. | Security | `docs/06-security/` |
| DRL-SEC-006 | Secrets shall remain outside source, prompts, traces, and public artifacts and use approved secret stores. | Security | `docs/06-security/` |
| DRL-SEC-007 | Untrusted retrieved content and tool output shall be treated as data, not instruction. | Security | `docs/06-security/` |
| DRL-SEC-008 | Tool execution shall enforce path, command, network, data, timeout, and output-size constraints. | Security | `docs/06-security/` |
| DRL-SEC-009 | Anonymous sessions shall be isolated, rate limited, short lived, and unable to access private resources. | Security | `docs/06-security/` |
| DRL-SEC-010 | Release security suites shall record zero unauthorized actions in critical cases. | Security | `docs/06-security/` |
| DRL-SEC-011 | Consent and retention shall be versioned and enforceable independently of interface text. | Security | `docs/06-security/` |
| DRL-SEC-012 | Incident response shall support disablement, revocation, rollback, notification, and evidence preservation. | Security | `docs/06-security/` |
| DRL-MOD-001 | Atticus Core and Edge shall be planned and evaluated as a coordinated model family. | Model/Data | `docs/03-model/` |
| DRL-MOD-002 | Base-model selection shall result from a current, license-reviewed bakeoff rather than an assumed winner. | Model/Data | `docs/03-model/` |
| DRL-MOD-003 | Core shall target orchestration, tool use, research/coding assistance, and synthesis; Edge shall target low-latency routing and local interactions. | Model/Data | `docs/03-model/` |
| DRL-MOD-004 | Training runs shall be reproducible from pinned data manifests, code, configuration, environment, and seeds. | Model/Data | `docs/03-model/` |
| DRL-MOD-005 | Commercial models used for synthetic data shall be disclosed and their outputs reviewed according to category. | Model/Data | `docs/03-model/` |
| DRL-MOD-006 | Public model releases shall include weights/adapters as lawful, checksums, model card, safety/evaluation report, and upstream obligations. | Model/Data | `docs/03-model/` |
| DRL-MOD-007 | Quantized artifacts shall be evaluated separately from full-precision candidates. | Model/Data | `docs/03-model/` |
| DRL-MOD-008 | Edge shall have explicit escalation thresholds rather than pretending to solve unsupported tasks. | Model/Data | `docs/03-model/` |
| DRL-MOD-009 | Model release gates shall include permission, prompt-injection, grounding, latency, memory, and cost slices. | Model/Data | `docs/03-model/` |
| DRL-MOD-010 | Private personalization adapters shall remain local/private unless the owner deliberately publishes them. | Model/Data | `docs/03-model/` |
| DRL-DAT-001 | Every dataset record shall belong to public, DRL-private, or local-personal data tier. | Data | `docs/04-data/` |
| DRL-DAT-002 | Every source shall have identity, rights, provenance, acquisition, transformation, review, and release metadata. | Data | `docs/04-data/` |
| DRL-DAT-003 | Training and held-out evaluation shall use contamination-resistant splits and similarity audits. | Data | `docs/04-data/` |
| DRL-DAT-004 | Donated traces shall require explicit opt-in consent and quarantine before any research use. | Data | `docs/04-data/` |
| DRL-DAT-005 | Raw private files, email, voice, repositories, credentials, and local memory shall never enter public datasets by default. | Data | `docs/04-data/` |
| DRL-DAT-006 | Dataset releases shall include manifests, checksums, license, cards, review report, and contamination report. | Data | `docs/04-data/` |
| DRL-DAT-007 | Data deletion/retention shall be implemented as lifecycle behavior rather than policy prose only. | Data | `docs/04-data/` |
| DRL-DAT-008 | Synthetic data shall record generator/configuration and human/automated review class. | Data | `docs/04-data/` |
| DRL-DAT-009 | Hidden benchmark details shall be protected and rotated when contamination is credible. | Data | `docs/04-data/` |
| DRL-DAT-010 | Data quality failures shall be observable, quarantinable, and reversible. | Data | `docs/04-data/` |
| DRL-EVL-001 | EvalForge shall score terminal outcome and trajectory separately. | Evaluation | `docs/05-evaluation/` |
| DRL-EVL-002 | Deterministic graders shall decide schema, authorization, citation-link, and numerical consistency where possible. | Evaluation | `docs/05-evaluation/` |
| DRL-EVL-003 | Model judges shall be versioned, calibrated, and not solely decide critical safety. | Evaluation | `docs/05-evaluation/` |
| DRL-EVL-004 | Comparisons shall report uncertainty, slices, and critical failures rather than one aggregate score. | Evaluation | `docs/05-evaluation/` |
| DRL-EVL-005 | CI shall block regressions beyond approved thresholds and always block critical policy violations. | Evaluation | `docs/05-evaluation/` |
| DRL-EVL-006 | Evaluation runs shall capture target, configuration, dataset, scorer, environment, and artifact digests. | Evaluation | `docs/05-evaluation/` |
| DRL-EVL-007 | AtticusBench shall contain at least 1,000 held-out V1 cases across required taxonomies. | Evaluation | `docs/05-evaluation/` |
| DRL-EVL-008 | Release reports shall include failures and limitations, not only successful examples. | Evaluation | `docs/05-evaluation/` |
| DRL-EVL-009 | Replay evaluation shall verify that displayed artifacts correspond to the captured run. | Evaluation | `docs/05-evaluation/` |
| DRL-EVL-010 | Baseline thresholds shall be set before observing final release candidates or changed only by approved rationale. | Evaluation | `docs/05-evaluation/` |
| DRL-WEB-001 | The public site shall introduce DeWitt Research Workshop before Atticus. | Web/Brand | `docs/08-web-brand/` |
| DRL-WEB-002 | The visual system shall be cream on black with research-workstation/tmux influence and remain accessible. | Web/Brand | `docs/08-web-brand/` |
| DRL-WEB-003 | Traditional navigation and documentation shall work without chat. | Web/Brand | `docs/08-web-brand/` |
| DRL-WEB-004 | Public demos shall identify live, cached, simulated, and replayed output truthfully. | Web/Brand | `docs/08-web-brand/` |
| DRL-WEB-005 | The Atticus console shall render plan artifacts, tool events, policy/approval, evidence, evaluation, and cancellation states. | Web/Brand | `docs/08-web-brand/` |
| DRL-WEB-006 | The site shall provide project, research, open-source, founder, failure-museum, and system-console routes. | Web/Brand | `docs/08-web-brand/` |
| DRL-WEB-007 | Critical flows shall support keyboard, screen reader, reduced motion, mobile, and high-latency conditions. | Web/Brand | `docs/08-web-brand/` |
| DRL-WEB-008 | Analytics/content capture shall follow visible consent and telemetry policy. | Web/Brand | `docs/08-web-brand/` |
| DRL-WEB-009 | Public metrics and system status shall be derived from release/operational evidence, never invented. | Web/Brand | `docs/08-web-brand/` |
| DRL-WEB-010 | Priority visitor personas shall understand the laboratory and reach relevant evidence in under two minutes in usability testing. | Web/Brand | `docs/08-web-brand/` |
| DRL-PLT-001 | Infrastructure shall be reproducible through Terraform for dev, staging, and production. | Platform | `docs/07-platform-gcp/` |
| DRL-PLT-002 | Application identities shall use least privilege and deployment shall avoid long-lived static cloud credentials. | Platform | `docs/07-platform-gcp/` |
| DRL-PLT-003 | Cloud Run GPU inference shall be cost bounded and support scale-to-zero where compatible with declared SLOs. | Platform | `docs/07-platform-gcp/` |
| DRL-PLT-004 | Wix at www.dewitt-labs.com shall deliver the canonical institutional site; approved Google-hosted frontends shall deliver interactive DRL applications and documentation. | Platform | `docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md` |
| DRL-PLT-005 | Cloud SQL PostgreSQL with pgvector shall be the canonical relational/vector service unless superseded by ADR. | Platform | `docs/07-platform-gcp/` |
| DRL-PLT-006 | Production changes shall use tested artifact promotion, smoke tests, and rollback. | Platform | `docs/07-platform-gcp/` |
| DRL-PLT-007 | Backups and restore procedures shall be tested before V1 release. | Platform | `docs/07-platform-gcp/` |
| DRL-PLT-008 | Budgets shall warn at $150 monthly and enforce a $250 monthly hard planning cap absent director approval. | Platform | `docs/07-platform-gcp/` |
| DRL-PLT-009 | Observability shall separate user, model, tool, queue, database, and cold-start latency/cost while redacting content. | Platform | `docs/07-platform-gcp/` |
| DRL-PLT-010 | Colab shall be used for interactive research, not production service hosting; durable training shall use reproducible cloud jobs. | Platform | `docs/07-platform-gcp/` |
| DRL-ATL-001 | Atlas shall preserve observation, release, revision, effective, ingestion, and as-of time. | Atlas | `services/atlas/docs/SPEC.md` |
| DRL-ATL-002 | Atlas shall not expose revised data as historically knowable before its release. | Atlas | `services/atlas/docs/SPEC.md` |
| DRL-ATL-003 | Atlas evidence bundles shall represent support, contradiction, missing evidence, uncertainty, and source rights. | Atlas | `services/atlas/docs/SPEC.md` |
| DRL-ATL-004 | Atlas numerical analysis and charts shall use deterministic versioned tools. | Atlas | `services/atlas/docs/SPEC.md` |
| DRL-ATL-005 | Atlas connectors shall be independently testable and rights-aware. | Atlas | `services/atlas/docs/SPEC.md` |
| DRL-ATL-006 | Atlas research snapshots shall be reproducible from manifests and source/artifact digests. | Atlas | `services/atlas/docs/SPEC.md` |
| DRL-FED-001 | FedLens shall acquire and identify official Federal Reserve documents with version lineage. | FedLens | `services/fedlens/docs/SPEC.md` |
| DRL-FED-002 | FedLens shall separate literal document changes from semantic/model-inferred interpretation. | FedLens | `services/fedlens/docs/SPEC.md` |
| DRL-FED-003 | FedLens topic/tone results shall report calibration, uncertainty, and abstention. | FedLens | `services/fedlens/docs/SPEC.md` |
| DRL-FED-004 | FedLens event-study artifacts shall be deterministic, reproducible, and avoid unsupported causal claims. | FedLens | `services/fedlens/docs/SPEC.md` |
| DRL-FED-005 | FedLens citations shall point to exact source spans and document versions. | FedLens | `services/fedlens/docs/SPEC.md` |
| DRL-FED-006 | FedLens public corpus releases shall pass source/license review. | FedLens | `services/fedlens/docs/SPEC.md` |
| DRL-BAL-001 | BalanceLab V1 shall use synthetic institutions and public/DRL-authored methodology only. | BalanceLab | `services/balancelab-ai/docs/SPEC.md` |
| DRL-BAL-002 | Authoritative financial outputs shall come exclusively from deterministic versioned calculations. | BalanceLab | `services/balancelab-ai/docs/SPEC.md` |
| DRL-BAL-003 | Every calculation artifact shall expose inputs, assumptions, units, formula/method version, reconciliation, and limitations. | BalanceLab | `services/balancelab-ai/docs/SPEC.md` |
| DRL-BAL-004 | AI explanation shall consume and remain consistent with calculation artifacts. | BalanceLab | `services/balancelab-ai/docs/SPEC.md` |
| DRL-BAL-005 | Golden, property, invariant, metamorphic, and independent-reference checks shall cover critical calculations. | BalanceLab | `services/balancelab-ai/docs/SPEC.md` |
| DRL-BAL-006 | Public output shall be labeled educational/research and not individualized financial advice. | BalanceLab | `services/balancelab-ai/docs/SPEC.md` |
| DRL-OSS-001 | DRL-authored software shall default to Apache-2.0 while models, data, docs, and trademarks use artifact-specific terms. | Governance/License | `docs/09-open-source/` |
| DRL-OSS-002 | Every release shall have source/license register and required notices. | Governance/License | `docs/09-open-source/` |
| DRL-OSS-003 | Sponsors shall not control roadmap, review, benchmarks, or research conclusions. | Governance/License | `docs/09-open-source/` |
| DRL-OSS-004 | Contributors shall have reproducible no-paid-API development paths and clear issue/evidence requirements. | Governance/License | `docs/09-open-source/` |
| DRL-OSS-005 | Forks may exercise licenses but may not imply official DRL status or endorsement. | Governance/License | `docs/09-open-source/` |
| DRL-OSS-006 | Commercial services shall preserve already granted open-source rights and research integrity. | Governance/License | `docs/09-open-source/` |
| DRL-OPS-001 | Major decisions shall be recorded and approved through ADRs. | Operations | `docs/11-operations/` |
| DRL-OPS-002 | Agents shall work sequentially on feature branches and create pull requests with evidence. | Operations | `docs/11-operations/` |
| DRL-OPS-003 | Every mission shall begin from validated inherited state and end with a reproducible handoff. | Operations | `docs/11-operations/` |
| DRL-OPS-004 | V1 shall launch publicly as a coordinated release after independent QA. | Operations | `docs/11-operations/` |
| DRL-OPS-005 | Release artifacts shall match tested commits/configurations and verify by checksum/signature. | Operations | `docs/11-operations/` |
| DRL-OPS-006 | Critical security, privacy, license, calculation, or public-claim findings shall block release absent explicit recorded waiver. | Operations | `docs/11-operations/` |
| DRL-OPS-007 | Public documentation shall identify its release/commit and preserve corrections/history. | Operations | `docs/11-operations/` |
| DRL-OPS-008 | Every public claim shall map to evidence in the release dossier. | Operations | `docs/11-operations/` |
| DRL-OSS-007 | Every flagship release shall satisfy the Open Artifact Standard or publish an approved open exception. | Governance/License | `docs/09-open-source/OPEN_ARTIFACT_STANDARD.md` |
| DRL-OSS-008 | DRL public language shall distinguish open-source software, Open Source AI, open-weight, source-available, and public artifacts precisely. | Governance/License | `OPEN_RESEARCH_CHARTER.md` |
| DRL-OSS-009 | Atticus Core and Edge releases shall include a public model commons with lawful weights or derivatives, recipes, cards, evaluation, and local runtime profiles. | Model/Data | `docs/09-open-source/OPEN_MODEL_COMMONS.md` |
| DRL-OSS-010 | Every managed flagship capability shall document a portable boundary and functional self-hosted or local research path. | Architecture | `docs/09-open-source/FORKABILITY_AND_SELF_HOSTING_STANDARD.md` |
| DRL-OSS-011 | Public release badges shall be generated from verifiable openness, reproducibility, forkability, and supply-chain evidence. | Release QA | `docs/09-open-source/REPRODUCIBILITY_BADGES.md` |
| DRL-OSS-012 | Critical open-source dependencies shall have owners, license/security review, exit plans, and an upstream contribution ledger. | Operations | `docs/09-open-source/OPEN_STACK_AND_UPSTREAM_POLICY.md` |
| DRL-OSS-013 | Generally useful dependency fixes shall be proposed upstream before DRL adopts a permanent private fork, unless documented constraints prevent it. | Operations | `docs/09-open-source/UPSTREAM_CONTRIBUTION_POLICY.md` |
| DRL-OSS-014 | The website shall prominently present the Atticus model commons, open stack, artifacts, self-hosting, contributions, and independent replications. | Web/Brand | `docs/08-web-brand/OPEN_SOURCE_PORTAL_AND_COMMONS.md` |
| DRL-OSS-015 | DRL shall provide meaningful contribution paths for software, models, data, evaluation, accessibility, documentation, teaching, security, and research. | Research/Community | `docs/09-open-source/COMMUNITY_RESEARCH_NETWORK.md` |
| DRL-OSS-016 | Every public artifact shall carry an evidence-derived maturity state and lifecycle policy. | Release QA | `docs/09-open-source/OPEN_SOURCE_MATURITY_MODEL.md` |
| DRL-OSS-017 | The V1 clean-room forkability test shall run the public research profile without proprietary DRL credentials or a paid commercial model API. | Release QA | `docs/09-open-source/FORKABILITY_AND_SELF_HOSTING_STANDARD.md` |
| DRL-OSS-018 | DRL releases shall publish human-readable upstream attribution plus machine-readable license and SBOM evidence. | Governance/License | `docs/09-open-source/UPSTREAM_CONTRIBUTION_POLICY.md` |
| DRL-OSS-019 | DRL shall present open models, open-source software, reproducible research, local operation, and upstream reciprocity as explicit institutional identity pillars. | Governance | `docs/09-open-source/OPEN_SOURCE_IDENTITY_SYSTEM.md` |
| DRL-OSS-020 | Critical technology selections shall be represented in a public open-stack catalog with exact license classification, ownership, review date, and exit strategy. | Architecture/Protocol | `docs/09-open-source/OPEN_TECHNOLOGY_CATALOG.md` |
| DRL-OSS-021 | DRL shall publish sustainability and monetization boundaries that preserve the core public modification surface and sponsor independence. | Governance | `docs/09-open-source/OPEN_SOURCE_SUSTAINABILITY.md` |
| DRL-OSS-022 | DRL shall report open-source health through maintainability, reproducibility, reciprocity, community, and public-benefit metrics rather than vanity metrics alone. | Research/Community | `docs/09-open-source/OPEN_SOURCE_HEALTH_METRICS.md` |
| DRL-OSS-023 | Release and research credit shall recognize code, data, evaluation, security, documentation, accessibility, teaching, replication, and upstream work. | Research/Community | `docs/09-open-source/CONTRIBUTOR_CREDIT_AND_AUTHORSHIP.md` |
| DRL-OSS-024 | The V1 public demonstration shall expose a complete open-weight Atticus workflow with source, model identity, traces, evaluation, reproduction bundle, local run, and contribution paths. | Integration | `docs/09-open-source/V1_OPEN_SOURCE_SHOWCASE.md` |
| DRL-OSS-025 | Open artifact, exception, and upstream dependency metadata shall conform to versioned machine-readable schemas. | Architecture/Protocol | `schemas/open-artifact-release.schema.json` |
| DRL-OSS-026 | The Atticus V1 release shall be delivered as an Open Model Commons release train containing Core, Edge, adapters, runtime profiles, data manifests, benchmark evidence, and community submission lanes. | Model/Data | `docs/03-model/ATTICUS_OPEN_MODEL_COMMONS_RELEASE_TRAIN.md` |
| DRL-WEB-011 | The canonical public laboratory origin shall be https://www.dewitt-labs.com and the apex domain shall redirect to it. | Web/Brand | `docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md` |
| DRL-WEB-012 | Wix shall provide the V1 institutional, editorial, research-discovery, teaching, collaboration, and application-launch surface. | Web/Brand | `docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md` |
| DRL-WEB-013 | Atticus and specialist computational applications shall remain independently deployable open-source experiences and shall not rely solely on Wix iframes. | Web/Brand | `docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md` |
| DRL-WEB-014 | Wix and application subdomains shall share approved navigation, visual identity, status language, consent, analytics taxonomy, canonical-link policy, and truthful maturity labels. | Web/Brand | `docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md` |
| DRL-WEB-015 | Controlled technical and research documents shall remain repository-authoritative even when summarized or published into Wix. | Web/Brand | `docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md` |
| DRL-PLT-011 | Domain, DNS, TLS, application subdomain, monitoring, renewal, change, and rollback operations shall follow a documented and tested runbook. | Platform | `docs/07-platform-gcp/DOMAIN_DNS_AND_WIX_RUNBOOK.md` |
| DRL-PLT-012 | Production promotion shall verify Wix publication, application host mappings, HTTPS, redirects, CORS/CSP, cookie scope, and cross-host links as one coordinated release. | Platform | `docs/02-architecture/DEPLOYMENT_AND_ENVIRONMENTS.md` |
| DRL-SEC-013 | Visual continuity across Wix and DRL applications shall not imply shared authorization; privileged access requires the approved application identity and session model. | Security | `docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md` |
