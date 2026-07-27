---
document_id: DRL-OSS-005
title: "Plugin, Skill, Model Adapter, and Registry Program"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Plugin, Skill, Model Adapter, and Registry Program

## V1 position

V1 publishes stable extension contracts, reference plugins, model-provider adapters, and validation tools. A public searchable registry launches only after security review, compatibility tests, moderation, ownership, signing/attestation, and incident processes exist. Git repositories remain a valid distribution method; the registry adds governed discovery rather than becoming a mandatory gatekeeper.

## Extension classes

- Atticus skills and workflow definitions;
- typed tools and MCP-compatible adapters;
- Atlas/FedLens data connectors;
- BalanceLab scenarios, products, and calculation modules;
- EvalForge scorers, datasets, reporters, and judge adapters;
- model providers, runtimes, templates, and tool parsers;
- user-interface panels and research visualizations;
- teaching modules and guided tours.

## Registry metadata

- name, namespace, version, and type;
- author and canonical repository;
- license and notices;
- DRL protocol and application compatibility;
- maturity and support status;
- permissions, risk class, data classes, and external destinations;
- package/artifact hash, SBOM, signature or provenance where supported;
- tests and evaluation bundle;
- model/runtime requirements;
- security contact;
- maintainer and abandonment policy;
- verification status and review date.

## Status vocabulary

- **Community:** submitted and structurally valid; no DRL endorsement.
- **Reviewed:** manual/automated review completed for stated version.
- **Verified:** passes compatibility, security, provenance, and evaluation criteria.
- **Official:** maintained or explicitly adopted by DRL.

Status is version-specific. A verified version does not grant permanent trust to future uploads.

## Safety and permissions

Plugins declare capabilities before execution. Undeclared network destinations, file paths, subprocess use, or data access are prohibited. The registry provides policy previews and an install-time permission diff. Model-generated plugin descriptions are never accepted as the authority over manifest and code analysis.

## Model adapter registry

The model adapter section records base model, license, runtime, parser, template, context, quantization, benchmark evidence, and known tool-use limitations. Community adapters can be listed without becoming official Atticus releases.

## Removal and quarantine

An extension can be quarantined or removed from discovery for compromise, malicious behavior, abandoned critical risk, license violation, misrepresentation, namespace dispute, or inability to reproduce the published artifact. The record and reason remain visible where safe.

## Trademark and forks

Community extensions may state compatibility factually but cannot imply official DRL status. Official badges follow the trademark and verification policy.
