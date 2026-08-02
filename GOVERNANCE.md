---
document_id: DRL-ROOT-GOV
title: "Governance of DeWitt Research Laboratory"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Governance of DeWitt Research Laboratory

## Constitutional model

DRL is an independent research initiative founded and directed by Christopher Noxon DeWitt. Governance follows a **benevolent dictator for life (BDFL)** model for mission, public identity, final architecture, security posture, licenses, model/data releases, budgets, partnerships, and release decisions. This preserves coherence while the laboratory is small and does not authorize arbitrary or undocumented decisions.

## Decision classes

| Class | Examples | Authority |
|---|---|---|
| Constitutional | mission, brand, governance, core open-weight commitment | The Director; recorded decision/ADR |
| Architectural | public protocols, trust boundaries, data model, cloud topology | proposal + reviewers + the Director's approval when major |
| Maintainer | compatible implementation, defects, docs, tests | responsible maintainer within approved specs |
| Research release | model, dataset, benchmark, paper | research/security/license review + the Director |
| Operational | incident action, rollback, temporary rate reduction | on-call authority, documented after action |

## ADR and RFC process

Major decisions begin as an ADR/RFC describing context, options, consequences, security/privacy/license/cost effects, migration, reversibility, and evidence. Reviewers challenge assumptions; the Director accepts, rejects, requests revision, or defers. Accepted ADRs are immutable historical records; superseding decisions link rather than rewrite history.

## Maintainers and researchers

Maintainers may be appointed based on sustained high-quality contributions, review judgment, security/privacy discipline, respectful collaboration, and ability to maintain—not merely code—a subsystem. Researchers may be recognized for datasets, experiments, replications, papers, or teaching. Roles, scopes, and revocation are public. No title implies employment or the right to bind DRL commercially.

## Sponsors and partners

Sponsors may fund infrastructure, events, research, or accessibility and may be acknowledged. They do not buy roadmap, benchmark, review, publication, or result control. Conflicts and material support are disclosed. Any sponsored research agreement must protect publication integrity, user privacy, open-source obligations, and the Director’s final mission authority.

## Conflicts of interest

Reviewers disclose employment, financial, data-source, model-vendor, or sponsorship relationships relevant to a decision. A conflicted reviewer may contribute evidence but should not be the sole approver. Research publications list material support and limitations.

## Appeals and disagreements

Technical disagreement is documented in issues/ADRs with evidence and alternatives. Maintainer decisions may be appealed to the relevant lead and ultimately the Director. Conduct matters follow the Code of Conduct. Security disclosure disputes prioritize user protection and coordinated disclosure.

## Succession and continuity

The Director may designate maintainers, archive projects, transfer repositories, or establish a steering structure as the community grows. Until a recorded succession plan exists, no contributor may claim control of the DRL name, domains, official releases, or trademark identity. If development stops, repositories should be clearly archived rather than presented as maintained.

## Repository and release authority

Official repositories, package/model/dataset registry namespaces, domains, signing keys, and production environments are controlled assets. Access is granted by minimum role, reviewed periodically, and revoked when no longer needed. A maintainer’s merge permission does not imply production, registry, billing, secrets, or release-signing permission.

A public release requires the evidence and approval in the release process. Nightly builds, research checkpoints, previews, and release candidates are clearly labeled and cannot use the official stable badge. Published artifacts are immutable; corrections create a new version and an advisory rather than silently replacing history.

## Delegation and review quorum

The Director may delegate routine compatible merges to maintainers. Changes touching security authority, personal/private data, model/dataset release, licenses, public claims, money, sponsorship, or constitutional identity always retain director approval unless a future recorded governance change explicitly delegates them. When practical, the author should not be the only substantive reviewer of high-risk code or research.

## Transparency records

The laboratory maintains public ADRs, release notes, known limitations, material sponsorship/conflict disclosures, and corrections. Private security, personal data, unreleased benchmark answers, and contract-confidential material are excluded from public records but still receive controlled internal evidence. Governance does not require exposing secrets or vulnerable users.

## Community growth stages

- **Founder stage:** The Director is primary owner/reviewer; contribution scopes are narrow and documented.
- **Maintainer stage:** subsystem maintainers receive compatible merge/review authority and documented service expectations.
- **Council stage, if needed:** a technical/research council may advise or receive delegated decisions through a governance ADR; the Director remains constitutional authority unless succession changes it.
- **Foundation or company stage, if ever:** legal/entity changes require explicit treatment of assets, licenses, trademarks, conflicts, community rights, and previously granted promises.

Growth is triggered by demonstrated maintenance burden and community stewardship, not appearance. DRL will not invent committees or titles to look larger than it is.

## Open research alignment

This document is interpreted with the root `OPEN_RESEARCH_CHARTER.md` and the controlled standards in `docs/09-open-source/`.

## Open technology stewardship

The Director approves open-research exceptions, model/license classifications, official Atticus releases, and material substitutions between open-source and source-available infrastructure. Maintainers steward dependencies and contribution lanes but cannot weaken the Open Research Charter through implementation convenience. Sponsorship does not purchase roadmap control or favorable research outcomes.
