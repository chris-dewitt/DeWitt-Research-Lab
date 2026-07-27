---
document_id: DRL-MOD-010
title: "Model Serving, Capacity, and Admission Control"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Model Serving, Capacity, and Admission Control

## Public serving path

Cloud Run GPU is the initial target because it can scale to zero. The design must account for model download/load, container size, startup probes, request concurrency, and queue behavior.

## Cold-start strategy

- build image layers and model artifact strategy for fast startup;
- benchmark baked image versus mounted/downloaded model subject to platform limits;
- display immediate wake status;
- route simple questions to Edge/CPU or documentation retrieval if available;
- offer signed replay;
- optionally schedule minimum instance during launches or demos;
- never hide a replay as live.

## Admission control

Before inference:

- validate session quota;
- estimate input/output tokens;
- enforce max context and output;
- check global daily budget;
- reserve request capacity;
- queue with timeout or return replay;
- shed low-priority work before operational failure.

## Capacity experiments

Measure warm/cold p50/p95, concurrent users, throughput, GPU utilization, model load, error rate, structured output, and cost per successful workflow. Use representative multi-tool prompts, not only short chat completions.
