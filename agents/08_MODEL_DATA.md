---
document_id: DRL-AGT-008
title: "Agent Mission 08: Atticus Model Family, AtticusBench, and Data Program"
version: 3.1.0
status: APPROVED EXECUTION MISSION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Agent Mission 08: Atticus Model Family, AtticusBench, and Data Program

## Mission objective

Create the reproducible research and release program for Atticus Core and Atticus Edge: base-model bakeoff, public/DRL-private/local-personal data boundaries, AtticusBench, supervised and preference training, safety post-training, distillation, quantization, evaluation, model cards, and public weight releases.


## Operating contract

This mission is executed on a dedicated feature branch and ends in a reviewable pull request. Before changing files, the agent must read `LABORATORY_BIBLE.md`, root `AGENTS.md`, `docs/00-program/SPECIFICATION_MAP.md`, `docs/00-program/DECISION_REGISTER.md`, the current `WORKLOG.md`, this mission, and every listed prerequisite.

The agent must not silently reinterpret the laboratory. Missing or contradictory decisions become a documented blocker or an ADR proposal. All external factual or technical assumptions that could have changed must be revalidated against authoritative primary documentation and entered in the technical reference register.

## Branch, commit, and pull-request protocol

- Create a branch named `agent/<mission-number>-<short-scope>` from the latest approved integration branch.
- Reserve the mission in `WORKLOG.md` before modifying controlled files.
- Commit after coherent work packages; avoid one giant undifferentiated commit.
- Rebase or merge the latest integration branch before final verification.
- Open a pull request containing requirement IDs, changed contracts, ADRs, test evidence, security/privacy impact, documentation impact, known limitations, and exact handoff state.
- Never merge the pull request yourself unless the Director has explicitly delegated that authority for the specific PR.

## Universal constraints

- No credentials, personal/private content, employer material, unlicensed corpora, or generated secrets may be committed.
- Do not weaken security, privacy, evaluation, accessibility, open-weight, provenance, or deterministic-computation requirements to make a demo pass.
- Do not claim completion without verifiable evidence.
- Do not alter another component's public contract without coordination and, when material, an approved ADR.
- Public write actions and unrestricted shell execution remain outside the public Atticus trust boundary.
- LLM output never becomes an authoritative numerical financial result; BalanceLab calculations must be deterministic and auditable.

## Required artifacts in every mission PR

1. Implemented or revised artifacts owned by the mission.
2. Automated tests or executable validation for every material behavior.
3. Updated controlled documentation and requirement traceability.
4. A completed handoff ledger entry using `agents/HANDOFF_TEMPLATE.md`.
5. A list of decisions made, assumptions retained, unresolved blockers, and follow-on issues.
6. Evidence that relevant local and CI commands pass.

## Stop conditions

Stop rather than improvise when a change would expose private data, expand write authority, change a public protocol, add a new upstream model/license, materially change cloud cost, undermine reproducibility, or contradict an approved foundation decision. Draft an ADR or blocker with alternatives and impact.



## Open Research Charter obligations

This mission must preserve DRL's open-by-construction identity. Read `OPEN_RESEARCH_CHARTER.md` and the relevant `docs/09-open-source/` standards. For every material feature, record the public artifact, license, modification surface, self-hosted path, upstream dependencies, reproducibility evidence, and any open exception. Prefer upstream contribution over permanent private forks. Use “open source,” “open weight,” and “source available” precisely.

## Entry prerequisites

- Missions 00–04 merged.
- Tool/protocol schemas and evaluation interfaces stable enough to generate tasks.
- Source and licensing review process approved.
- Secure Cloud Storage/Vertex/Colab experiment paths documented.

## Owned paths

- `models/**`
- `datasets/atticusbench/**` and approved public training-data manifests
- `docs/03-model/**`, `docs/04-data/**`
- training/evaluation notebooks and scripts under approved model tooling paths
- model and dataset release manifests

## Protected or coordinated paths

- Private personalization data and adapters never enter public datasets or releases.
- Commercial models may assist synthetic generation but must be disclosed and cannot be the required production model.
- No dataset enters training without source, rights, transformations, review class, and contamination status.
- Upstream model license changes or weight-merging implications require legal/license review.

## Required work packages

### WP-08-01 — Current base-model bakeoff
Revalidate candidate licenses and model cards; benchmark Core and Edge candidates on structured tool use, routing, code/research tasks, safety, latency, memory, and quantized runtime. Publish a scorecard and selection ADR.

### WP-08-02 — AtticusBench v1
Implement task taxonomy, environment fixtures, train/dev/test separation, hidden held-out suite, scoring adapters, provenance, deduplication, contamination checks, and at least the V1-required held-out task count.

### WP-08-03 — Training data production
Build public and DRL-private data pipelines with category-specific review. Include correct, refusal, permission, recovery, multi-tool, citation, routing, and adversarial examples. Store local-personal data only under local private controls.

### WP-08-04 — Core post-training
Create reproducible SFT and preference/safety recipes, checkpointing, experiment registry, ablations, dataset mixture report, and release-candidate comparisons against base and commercial reference systems.

### WP-08-05 — Edge distillation and specialization
Distill or fine-tune a smaller model for routing, low-latency tool selection, voice command resolution, and approval interaction. Define escalation thresholds to Core.

### WP-08-06 — Quantization, packaging, and public release
Produce approved precision/quantization artifacts, checksums, runtime templates, model cards, safety/evaluation/license reports, reproducibility bundle, and Hugging Face/Ollama/llama.cpp-compatible releases where upstream terms allow.


### WP-08-07 — Atticus Open Model Commons release structure
Produce public release repositories and manifests for weights/adapters, quantizations, runtimes, model/data cards, recipes, evaluations, license notices, and replication bundles across approved distribution channels.

### WP-08-08 — Open model ecosystem bakeoff
Refresh and evaluate Qwen, Mistral, Gemma, and other eligible candidates for rights, preferred modification materials, tool reliability, runtime support, local/cloud performance, community health, and upstream contribution feasibility.

Every work package must name the requirements it satisfies, the evidence it produces, and its failure/rollback behavior. Create focused commits at work-package boundaries.

## ADR and director-approval triggers

- Selection or replacement of upstream base model.
- Any source with uncertain training or redistribution rights.
- Any plan to release merged weights contrary to upstream license.
- Any inclusion of donated/private traces in public training without valid consent and review.
- Any release gate waiver, hidden benchmark contamination, or unexplained metric regression.

## Verification matrix

- Dataset schemas and examples validate; lineage is complete.
- Held-out benchmark cannot be reconstructed from released training partitions.
- Training runs are reproducible from pinned config/container/checkpoints and tracked seeds.
- Statistical comparison and confidence intervals accompany score changes.
- Safety/permission suites record no release-blocking unauthorized action.
- Core and Edge meet declared capability, latency, memory, and escalation thresholds on documented hardware profiles.
- Every released artifact has checksum, license, model/dataset card, and reproducibility report.

## Handoff requirements

Provide selected model ADR, experiment ledger, dataset manifests, benchmark version, model artifacts/checksums, training and evaluation commands, failure analysis, license findings, serving requirements, and exact integration contract for the runtime and local runner.

## Definition of mission complete

Atticus Core and Edge release candidates are publicly releasable, reproducible, evaluated, legally reviewed under documented assumptions, packaged for supported runtimes, and demonstrably improve target capabilities over their upstream baselines.

### WP-08-09 — Atticus Open Model Commons release train

Execute the Core and Edge release train from candidate freeze through public V1, including adapters, merged artifacts where lawful, GGUF/runtime profiles, recipes, cards, data manifests, evaluation reports, and community submission lanes.
