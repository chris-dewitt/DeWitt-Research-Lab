---
document_id: DRL-ARC-011
title: "Provenance, Citations, Claims, and Calculation Lineage"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Provenance, Citations, Claims, and Calculation Lineage

## Evidence model

Each evidence item records publisher, source identifier/URI, title, content or excerpt hash, relevant timestamps, license/terms note, collection method, transformation chain, chunk location, retrieval score, and access scope.

## Claim graph

A final report is decomposed into claims. Claims can be:

- directly supported;
- inferred from evidence;
- calculated;
- contradicted;
- assumption;
- unresolved.

Each claim links supporting and contradicting evidence or calculation artifact IDs. Confidence is not a magic probability unless calibrated; the UI labels its meaning.

## Citation validation

EvalForge evaluates:

- source exists and was accessible at run time;
- cited passage supports the claim;
- source date is valid for the as-of question;
- citation refers to the correct version;
- quote/excerpt has not been altered;
- claim does not overgeneralize the evidence.

## Calculation lineage

Narrative values link to `CalculationArtifact` fields. Renderers use structured values rather than copying numbers from model prose. Unit, rounding, tolerance, engine version, input hash, and scenario assumptions are exposed.
