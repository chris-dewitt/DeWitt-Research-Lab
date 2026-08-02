---
document_id: DRL-ACC-001
title: "DeWitt Research Laboratory V1 Release Criteria"
version: 4.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# DeWitt Research Laboratory V1 Release Criteria

V1 is approved only when every critical criterion has evidence and no release blocker remains.

## Website and brand

- `https://www.dewitt-labs.com` resolves over HTTPS as the canonical Wix institutional site and the apex redirects correctly;
- institutional homepage and required routes complete;
- cream-on-black design system consistent and accessible;
- traditional navigation independent of Atticus;
- command palette/tmux workspace functional;
- live/replay labels accurate;
- public metrics generated from evidence;
- mobile, keyboard, screen-reader, contrast, and reduced-motion review passed;
- founder/about/résumé and independent-initiative disclosure complete;
- Atticus and specialist applications use approved DRL subdomains or documented route alternatives;
- core applications remain independently deployable and are not iframe-only;
- Wix and applications pass cross-host navigation, canonical URL, consent, analytics, CORS/CSP, cookie-scope, mobile, and fallback review;
- DNS inventory, TLS, monitoring, rollback, and domain renewal ownership are documented.

## Public Atticus

- open-weight model identity verified in production;
- anonymous and authenticated isolation/quotas;
- documentation citations;
- guided tours;
- bounded specialist tools;
- visible trace, policy, evidence, evaluation;
- cold-start/replay fallback;
- no public route to private runner;
- abuse/kill switches tested.

## Private Atticus

- Windows runner install/update path;
- outbound-only pairing/revocation;
- local voice, approved file search, repository inspect/test/patch;
- local approval and audit;
- private data remains local by default;
- replay/signature/scope tests passed;
- emergency stop.

## Model and data

- Core and Edge selected through bake-off;
- public weights/adapters/quantizations where lawful;
- reproducibility and license review;
- AtticusBench meets size/review/split criteria;
- model/data/safety cards;
- no gold contamination finding;
- quantized runtime qualification.

## EvalForge

- installable SDK/CLI;
- case format and evaluator plugins;
- deterministic policy/tool/trace evaluation;
- RAG/citation and judge calibration;
- baseline/candidate report;
- CI gate and public benchmark report.

## Specialist systems

- FedLens corpus/diff/timeline and evidence tool;
- BalanceLab synthetic institution, deterministic scenarios, calculation audit;
- Atlas source ingestion, temporal retrieval, cited research;
- project-specific tests/evaluation/security/docs;
- public live/replay demos.

## Integrated demonstration

- live open-weight Atticus routes Atlas + FedLens + BalanceLab;
- scenario and calculations valid;
- final claims trace to evidence/artifacts;
- EvalForge report generated from same trace;
- failure/degraded paths demonstrated;
- signed replay published.

## Platform and operations

- local mock stack from clean checkout;
- dev/stage/prod/research infrastructure as code;
- CI/CD, migrations, rollback;
- secret/workload identity controls;
- backup restore and replay-only incident drill;
- SLO dashboards/alerts/runbooks;
- cost budgets and max-instance controls;
- no critical vulnerabilities or unresolved high risk without explicit permitted acceptance.

## Open source and research

- license/notice/trademark strategy;
- governance/contribution/code of conduct/security policy;
- roadmap and good-first issues;
- technical/system report with replication assets;
- failure museum entries;
- teaching quickstarts;
- signed release manifest.

## Signoff matrix

| Area | Evidence owner | Required reviewer | Director approval |
|---|---|---|---|
| Product/web | Web lead | accessibility/release reviewer | yes |
| Security/privacy | Security lead | independent second pass | yes |
| Model/data | Model/data lead | license + eval reviewer | yes |
| EvalForge | Eval lead | integration reviewer | yes |
| Specialists | project leads | eval/integration reviewer | yes |
| Platform/operations | infra lead | release reviewer | yes |

A criterion may be waived only through a public release exception document stating reason, risk, mitigation, and deadline. Critical security, rights, and integrated-claim criteria are not waivable.

## Open research and open technology gate

V1 cannot launch until:

- Atticus Core and Edge have official public model-commons release plans and at least release-candidate artifacts with accurate rights labels;
- the Open Source portal, Open Stack ledger, artifact catalog, maturity labels, reproduce panels, and self-hosting routes are live;
- every flagship artifact passes the Open Artifact Standard or publishes an approved exception;
- clean-room QA runs the local research profile and fixture reference workflow without a paid commercial model API or proprietary DRL credentials;
- model/data cards, license notices, SBOMs, checksums, provenance, evaluation, and failure reports are linked from release manifests;
- the website displays current model identity and distinguishes live, replayed, cached, simulated, and illustrative output;
- generally useful downstream patches have an upstream issue/PR or a documented reason they cannot be contributed;
- no public page mislabels open-weight or source-available artifacts as open-source software or Open Source AI.

## Gate 16 — Open-source institutional identity

- `make open-check` passes.
- At least 26 DRL-OSS V1 requirements are traceable to release evidence.
- Atticus Core and Edge publish the approved Open Model Commons artifact envelope.
- The website renders Open Source portal, Open Stack lineage, artifact classifications, local/reproduction routes, contributor credit, and exceptions from controlled metadata.
- The signature public workflow can be reproduced through the local research profile without a paid commercial model API.
- The clean-room tester records no undocumented critical dependency or credential.
- Open-source health, sustainability, upstream contribution, and community-credit baselines are public.
- ADR-0006 and ADR-0007 are either approved with evidence or explicitly rejected with retained alternatives; no silent tool substitution ships.
