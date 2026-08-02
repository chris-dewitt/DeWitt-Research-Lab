---
document_id: DRL-FED-107
title: "FedLens System Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # FedLens System Specification

    ## 1. Purpose and authority

    FedLens creates an inspectable public research corpus and analytical service for Federal Reserve statements, minutes, speeches, testimony, projections, and related releases. It combines exact document provenance and diffs with carefully bounded NLP and reproducible market event studies.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for FedLens. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - Atticus and Atlas requesting specialized Federal Reserve evidence.
- Researchers studying monetary-policy communication.
- Students and teachers learning document analysis and event-study methods.
- Contributors adding corpora, annotation, models, and visualization.
- Reviewers reproducing DRL findings.

    ## 3. V1 capabilities

    - Acquire and normalize approved Federal Reserve documents.
- Preserve meeting, publication, effective, correction, and retrieval metadata.
- Segment and align comparable documents.
- Produce exact lexical and source-bound semantic change views.
- Extract topics and tone with baselines, confidence, and human review.
- Search by speaker, meeting, role, topic, date, and text.
- Build reproducible event windows from approved market data.
- Return cited evidence bundles, timelines, and research snapshots.

    ## 4. Explicit non-goals

    - Predicting policy with unjustified certainty.
- Presenting sentiment as objective truth.
- Causal market claims from naive correlations.
- Redistributing content beyond permitted terms.
- Real-time trading recommendations.
- Replacing exact document text with model paraphrase.

    ## 5. Logical architecture

    ```text
Official Source Registry -> Acquisition -> Raw/Versioned Documents
       -> Parse/Segment/Metadata -> Alignment/Diff + Search Index
       -> NLP Baselines/Models -> Event Study Engine
       -> Evidence Bundle / Timeline / Research Snapshot
```

    ## 6. Canonical workflows

    ### Statement comparison
Resolve meetings and exact versions; align sections and sentences; compute insert/delete/replace spans; run semantic-change annotations; attach source spans; show confidence and reviewer overrides.

### Speaker research
Retrieve documents by speaker, role, and as-of date; identify themes with exact spans; compare through time; return evidence rather than personality labels.

### Event study
Pin release timestamp, instrument, window, benchmark, timezone, and missing-data rules before calculation. Compute deterministic results and publish limitations; do not imply causal identification unless a separate design supports it.

    ## 7. Interfaces and integration

    - Document, meeting, comparison, search, speaker, timeline, event-study, and snapshot APIs.
- Corpus build CLI and Python SDK.
- FedDocument, Meeting, SpeakerRole, Alignment, ChangeSpan, Annotation, EventWindow, EventStudyResult, and PolicySnapshot schemas.
- Read-only public corpus; corpus administration and publication require privileged identities.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - Displayed source text is exact and versioned.
- Every model annotation links to a source span and model version.
- Release timestamps use documented timezone and correction history.
- Event-study arithmetic is deterministic.
- Tone and topic labels disclose uncertainty and validation.
- As-of queries exclude later corrections and annotations unless requested.
- Document comparison never relies only on LLM paraphrase.

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

    - M1 source, corpus, version, and meeting schemas with pilot statements.
- M2 parsing, segmentation, alignment, and exact diff.
- M3 search, metadata, and policy timelines.
- M4 NLP baselines, annotation process, and evaluation.
- M5 event-study engine and replication notebook.
- M6 Atticus/Atlas integration and public policy microscope.

    ## 11. V1 acceptance

    - Pilot corpus is complete, deduplicated, and rights/provenance reviewed.
- Golden document alignment and diff cases pass.
- Search, citation, topic, and tone slice thresholds pass.
- Reference event study reproduces exactly.
- Atticus invokes a statement comparison and receives cited evidence.
- Public timeline/demo and replication package pass release review.

    ## 12. Principal risks and controls

    - Document corrections and drift: immutable versions and source integrity checks.
- Subjective tone labels: multiple baselines, annotation guidelines, agreement, and uncertainty.
- Market timestamp error: explicit calendars/timezones and validation.
- Overclaiming: claims/evidence policy and methods review.
- Rights risk: source register and metadata/link-only release strategy.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.
