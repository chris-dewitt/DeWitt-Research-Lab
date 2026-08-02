---
document_id: DRL-SEC-007
title: "Software, Model, Data, and Artifact Supply-Chain Security"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Software, Model, Data, and Artifact Supply-Chain Security

## Controls

- lock dependencies and review updates;
- pin GitHub Actions to immutable commits where practical;
- build containers in controlled CI;
- generate SBOMs and vulnerability scans;
- sign release tags and artifacts where feasible;
- pin images by digest in production;
- record model/data source revision and checksum;
- scan model files and avoid unsafe serialization formats;
- sandbox untrusted conversion tools;
- verify Terraform plans and provider locks;
- restrict publishing credentials;
- use protected environments for release.

## Model artifact specifics

Prefer safetensors over unsafe pickle-based formats. Quantization/conversion runs in isolated environments and outputs hashes, tool versions, and comparison evaluation.

## Dependency policy

A dependency must have a clear purpose, maintained release, acceptable license, and security posture. Avoid adding frameworks for one convenience function. High-risk runtime dependencies receive an ADR or explicit review.
