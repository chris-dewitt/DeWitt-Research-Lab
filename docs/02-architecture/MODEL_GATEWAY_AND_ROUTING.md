---
document_id: DRL-ARC-005
title: "Model Gateway, Routing, and Fallback Architecture"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Model Gateway, Routing, and Fallback Architecture

## Responsibilities

- stable provider-neutral API;
- model registry and exact revision identity;
- chat-template/tool-parser adaptation;
- request validation and token budgeting;
- routing by task, privacy, latency, cost, and capability;
- streaming normalization;
- structured-output enforcement;
- timeout, retry, and fallback policy;
- usage and quality telemetry;
- content-minimized caching where allowed.

## Routing policy

Inputs include:

- required capability: route, tool, code, synthesis, embedding, speech;
- task complexity and uncertainty;
- privacy class and local-only requirement;
- context length;
- allowed providers;
- deadline and cost budget;
- model health and recent EvalForge performance;
- user preference.

Example:

```text
simple local intent -> Atticus Edge
public multi-system task -> Atticus Core cloud
private file summary -> local Core/Edge based on hardware
structured fallback after invalid output -> same model constrained retry, then approved alternate
unsupported task -> transparent refusal/escalation, not silent commercial routing
```

## Fallback rules

- Fallback is declared in trace and UI.
- Private-local content does not move to cloud merely because the local model failed.
- A fallback cannot have broader data rights than the primary.
- Commercial fallback is disabled for the core open-weight demonstration and opt-in elsewhere.
- Model changes invalidate hidden state assumptions; prompts use canonical task context.

## Caching

Cache only deterministic or public-safe requests under tenant-aware keys. Do not cache private prompts, donated traces, approval decisions, or tool results across tenants. Model-response cache metadata includes model revision, prompt-template version, tool set hash, and policy version.
