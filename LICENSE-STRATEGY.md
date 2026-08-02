---
document_id: DRL-ROOT-LICENSE
title: "Licensing, Trademark, and Commercial Sustainability Strategy"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Licensing, Trademark, and Commercial Sustainability Strategy

## Objectives

The strategy must maximize learning, reuse, contribution, and institutional adoption while preserving attribution, patent clarity, user freedom, scientific provenance, the DRL identity, and viable future services. “Open source” is not used as a vague marketing label: each artifact states its actual license and upstream obligations.

## Default artifact matrix

| Artifact | Default | Notes |
|---|---|---|
| DRL-authored software | Apache License 2.0 | permissive commercial use, patent grant, notices, modification disclosure where required by license text |
| APIs/schemas/examples | Apache-2.0 | compatibility and reuse encouraged |
| Documentation and original reports | CC BY 4.0 unless marked otherwise | attribution and adaptation allowed; embedded third-party material retains its own terms |
| Original datasets | selected per source/composition, often CC BY 4.0 or ODC-style license | only when DRL has rights to grant; otherwise scripts/manifests may be released instead of data |
| Benchmarks | dataset-specific license plus Apache-2.0 scoring code | hidden test portions may be access-controlled to protect validity |
| Model adapters/weights | upstream-compatible license stated per release | no model is called Apache-2.0 merely because DRL training code is Apache-2.0 |
| Brand marks and logos | all rights reserved under trademark policy | software license does not authorize confusing use of DRL identity |
| Personal/private adapters | not public by default | owned/controlled by the user subject to upstream model terms |

## Why Apache 2.0

Apache 2.0 supports adoption and commercial use and includes an express patent grant. It does **not** prevent another party from hosting, selling, or forking the software. DRL should compete through trusted official releases, research quality, community, brand, security, managed operation, data/model stewardship, and service expertise—not through pretending a permissive license creates exclusivity.

## Monetization preserved

Potential revenue that remains compatible with an open core includes:

- managed DRL/Atticus hosting with reliability, upgrades, monitoring, and support;
- private deployments, security hardening, enterprise integrations, and governance/evaluation services;
- consulting and applied research;
- paid training, workshops, curricula, and institutional teaching;
- custom adapters, evaluation suites, and domain workflows built from client-owned data;
- support subscriptions and maintenance agreements;
- premium data products only where rights, provenance, privacy, and scientific integrity permit;
- sponsored research that cannot control methods or conclusions.

No business plan should depend on restricting users from exercising rights already granted by a published license.

## Release review

Before release, produce a software bill of materials and source/license register. Confirm:

1. DRL has authority to license each file/artifact.
2. Upstream notices, attribution, acceptable-use, naming, weight-redistribution, and patent obligations are met.
3. Dataset source terms allow the proposed transformation and redistribution.
4. Model output/synthetic data provenance is disclosed where material.
5. The release does not include confidential, personal, employer, or credential material.
6. The repository and artifact metadata state exact license identifiers.

Unclear artifacts are quarantined until reviewed; lack of objection is not permission.

## Contributions

Contributions are accepted under the repository’s applicable license unless a contributor agreement is later adopted through governance. Contributors certify that they have the right to submit the work. DRL may use a Developer Certificate of Origin sign-off for provenance. A future CLA, dual-license, or commercial exception requires an ADR and cannot retroactively revoke already granted rights.

## Trademark boundary

“DeWitt Research Laboratory,” “Atticus,” official logos, and release badges identify source and trust. Forks may accurately state origin and license but may not imply endorsement, official status, or institutional affiliation. See `TRADEMARK_POLICY.md`.

## Not legal advice

This document is an engineering and governance policy, not a legal opinion. Material releases, sponsorships, trademark filings, enterprise contracts, or ambiguous model/data terms should receive qualified legal review when stakes justify it.

## Repository-level implementation

Each repository/package root includes an SPDX identifier or license file, `NOTICE` where required, and a machine-readable source/license inventory. Files copied or adapted from upstream retain headers and are documented. Generated files identify their generator and source license. Examples and schemas inherit the repository software license unless explicitly marked.

Documentation may be published under CC BY 4.0 while the repository also contains Apache-2.0 software; file headers, site footer, and release metadata must make the boundary clear. Dataset cards state whether DRL licenses the data itself, only annotations/metadata, or only acquisition/transformation code. A source URL is not a license.

## Model-specific release questions

Before publishing merged weights or adapters, answer:

- Does the upstream license permit modification, redistribution, commercial use, hosting, naming, and derivative weights?
- Are use restrictions or acceptable-use terms compatible with the way DRL describes the release?
- Must downstream users accept additional terms?
- Can DRL legally provide a merged artifact, or should it release an adapter/recipe requiring users to obtain upstream weights?
- Do training datasets allow model training and the intended weight release?
- Are tokenizer, config, code, and quantized derivatives covered consistently?
- Does the proposed Atticus name conflict with upstream naming or attribution conditions?

The release manifest records answers and links the exact upstream revision and terms reviewed. Later upstream changes do not automatically change the terms of an already acquired/released revision, but legal interpretation may require advice.

## Dataset-specific release questions

Publicly accessible does not mean redistributable. For each dataset or corpus, distinguish source documents, extracted text, metadata, annotations, embeddings, transformations, and benchmark cases. Where full redistribution is uncertain, DRL should release source registries, checksums, acquisition/normalization scripts, and original annotations so users can reproduce from lawful access.

Personal data requires a lawful and ethical basis beyond copyright. Consent to use a public Atticus session operationally is not consent to release it as training data. De-identification reduces risk but does not create rights or guarantee anonymity.

## Compatibility and exceptions

Dependencies with copyleft, source-available, research-only, noncommercial, field-of-use, or custom model terms receive explicit compatibility review. They are not automatically rejected, but their obligations may make them unsuitable for the default Apache-2.0 distribution or future managed services. Exceptions are isolated, documented, and approved rather than obscured in a transitive dependency.

## Future dual licensing or proprietary modules

DRL may create separate proprietary services or modules, accept private client work, or offer dual licensing only for code/artifacts it has authority to license. Existing Apache-2.0 releases remain Apache-2.0. Community contributions complicate relicensing unless rights were assigned or all contributors agree; therefore no business plan should assume effortless conversion of the open core.

## Release checklist output

The release dossier includes SPDX/SBOM inventory, upstream notices, model/data/license cards, trademark naming review, contribution provenance, unresolved legal questions, and a signed decision identifying exactly which artifacts are public and under what terms.

## Open research alignment

This document is interpreted with the root `OPEN_RESEARCH_CHARTER.md` and the controlled standards in `docs/09-open-source/`.

## Open identity labeling

Each artifact uses its exact category: open-source software, Open Source AI, open-weight model, source-available, public-only, or restricted. Apache-2.0 remains the default for DRL-authored software, while upstream model terms, datasets, papers, documentation, and trademarks remain separately governed. Public metadata must never collapse these categories into vague "open AI" language.
