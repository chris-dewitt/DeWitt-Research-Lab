---
document_id: DRL-ATL-107
title: "Atlas System Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atlas System Specification

    ## 1. Purpose and authority

    Atlas converts approved public economic, policy, market, and research sources into point-in-time, provenance-rich evidence and reproducible quantitative analysis. It preserves what was knowable as of a stated time, including releases and revisions, and surfaces supporting, contradicting, and missing evidence rather than producing timeless generic summaries.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for Atlas. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - Atticus requesting evidence for cross-system workflows.
- Researchers investigating macroeconomic and market questions.
- Students and teachers exploring public data and methods.
- Developers adding connectors, transformations, retrieval methods, or reports.
- Reviewers reproducing published DRL findings.

    ## 3. V1 capabilities

    - Ingest approved public series and documents with rights and provenance records.
- Separate observation, release, revision, ingestion, and as-of time.
- Normalize data into versioned canonical forms.
- Perform hybrid lexical, semantic, metadata, and temporal retrieval.
- Run deterministic analytical tools and chart/report generation.
- Return evidence bundles with support, contradiction, uncertainty, and missing evidence.
- Produce reproducible research snapshots and cached public demos.
- Expose a connector SDK and validation harness.

    ## 4. Explicit non-goals

    - Trading recommendations or individualized financial advice.
- Unlicensed redistribution of restricted content.
- Invented real-time market coverage.
- Treating revised data as historically known.
- Allowing LLMs to fabricate quantitative values.
- Becoming a broad generic news aggregator.

    ## 5. Logical architecture

    ```text
Source Registry -> Collectors -> Raw Immutable Zone -> Normalize/Validate
                                      |
                         Release/Revision Ledger
                                      |
        Time-series Store + Document/Object Store + Search Index
                                      |
                      Retrieval and Analytics Engine
                                      |
                Evidence Bundle / Research Snapshot API
```

    ## 6. Canonical workflows

    ### Point-in-time research
Resolve as-of timestamp; select eligible source versions; retrieve documents and series; run deterministic calculations; assemble evidence and contradiction; synthesize only from valid artifacts.

### Ingestion
Review source rights and interface; fetch with checksum; parse in isolation; validate; record release and effective times; normalize; deduplicate; index; run quality tests; publish a new snapshot.

### Reproduction
Load snapshot manifest, source digests, code/config/model versions, and environment lock; rerun transformations and compare artifact digests and declared numeric tolerances.

    ## 7. Interfaces and integration

    - Research query, evidence bundle, series/document, snapshot, and connector-job APIs.
- Python connector SDK and CLI.
- Canonical SourceRecord, ObservationVersion, DocumentVersion, EvidenceBundle, Claim, ChartArtifact, and ResearchSnapshot schemas.
- Read-only public surface; ingestion and source administration require privileged identities.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - Every value has source, unit, frequency, time semantics, and version.
- As-of queries never use data unavailable at cutoff.
- LLM prose cannot overwrite deterministic artifacts.
- Rights restrictions propagate to derivatives and exports.
- Contradictory evidence is retained.
- Cached demos identify the snapshot date.
- Connector failure cannot silently produce a successful empty update.

    ## 9. Quality attributes

    - **Correctness:** typed inputs and verifiable artifacts, not ungrounded prose.
    - **Traceability:** operational steps can be reconstructed without storing hidden chain-of-thought.
    - **Security:** least privilege, deny by default, bounded egress, and approval for consequential actions.
    - **Privacy:** collection minimization and separation of public, DRL-private, and local-personal data.
    - **Reliability:** deadlines, cancellation, retry budgets, idempotency, and truthful degraded states.
    - **Accessibility:** public workflows support keyboard, screen readers, reduced motion, contrast, and mobile use.
    - **Portability:** Docker/open fixtures for baseline; Google Cloud is reference production, not a mandatory local dependency.
    - **Evaluability:** every headline claim maps to a versioned suite and release gate.

    ## 10. Milestones

    - M1 source registry, canonical schemas, and fixtures.
- M2 pilot FRED, BLS, BEA, Treasury connectors and revision ledger.
- M3 document ingestion and hybrid temporal retrieval.
- M4 deterministic analytics and evidence bundles.
- M5 Atticus adapter and public research workflow.
- M6 scale, reproducibility, evaluation, and release hardening.

    ## 11. V1 acceptance

    - Approved source set ingests idempotently and passes rights/data-quality review.
- Historical as-of tests prove no future leakage.
- Retrieval, citation, and temporal benchmark gates pass.
- One macro research question reproduces from a signed manifest.
- Atticus integrated demo consumes an Atlas evidence bundle.
- Public API, replay, SLO, cost, and rollback evidence is approved.

    ## 12. Principal risks and controls

    - Revision leakage: bitemporal/release ledger and adversarial tests.
- Licensing: source register and metadata/link-only release when needed.
- Hallucination: claim-evidence binding and deterministic calculations.
- Source outage/change: contract checks, quarantine, snapshots, and alerts.
- False precision: uncertainty and limitations in artifact schemas.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.
