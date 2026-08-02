---
document_id: DRL-EVA-005
title: "RAG, Citation, and Temporal Evaluation"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# RAG, Citation, and Temporal Evaluation

## Retrieval gold

Gold may include required documents/passages, relevant sets, timestamp validity, and acceptable contradictory sources. Gold is not always one exact chunk because chunking changes.

## Citation checks

- identifier resolves;
- version and timestamp correct;
- passage supports claim;
- quote integrity;
- claim scope not broader than source;
- calculation claims cite calculation artifact;
- all material factual claims have support or inference label.

## Temporal tests

- future document excluded from as-of query;
- revised series distinguished from vintage if relevant;
- publication versus event time handled;
- latest means latest known by query execution/as-of date;
- stale index detected;
- documents with later corrections/version changes handled.

## Contradiction

Evaluate whether system surfaces material conflicting evidence and reduces confidence rather than cherry-picking.
