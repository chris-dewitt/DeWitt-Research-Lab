---
document_id: DRL-GCP-006
title: "Cloud Run GPU Inference Design and Bake-Off"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Cloud Run GPU Inference Design and Bake-Off

## Goal

Serve Atticus Core publicly using managed GPU capacity that can scale to zero, while preserving honest cold-start UX and cost controls.

## Candidate runtimes

- vLLM;
- SGLang;
- llama.cpp/Ollama for specific smaller or quantized profiles;
- native Transformers only for testing, not assumed production choice.

## Bake-off

Measure on supported GPU types:

- image/model load time;
- startup probe time;
- warm time to first token;
- tokens/s and concurrency;
- tool-call/parser validity;
- memory/KV behavior at 8K/16K/32K contexts;
- scale-from-zero total latency;
- cost per successful Atticus workflow;
- revision rollout and failure recovery;
- artifact size and registry pull.

## Design options

1. model included in image layer;
2. model downloaded from controlled object storage at startup;
3. runtime-specific artifact caching/mount approach supported by platform.

Selection considers platform limits, image size, startup, integrity, and update operations.

## Public UX

API immediately returns accepted/waking status or streams a wake event. Website offers replay. Request expires rather than sitting indefinitely. During launch events, a scheduled minimum instance may be used within budget.

## Security

Inference service has no general-purpose tools or private data access. It receives model requests from control plane only, uses restricted identity, and emits content-minimized telemetry.
