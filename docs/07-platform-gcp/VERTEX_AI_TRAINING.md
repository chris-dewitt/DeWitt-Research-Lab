---
document_id: DRL-GCP-007
title: "Vertex AI Custom Training and Experiment Pipeline"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Vertex AI Custom Training and Experiment Pipeline

## Promotion from Colab

A Colab experiment is promoted when its code, config, dataset manifest, and evaluation run are stable. Production research jobs use a versioned training container and command, not notebook cell state.

## Custom job inputs

- container digest;
- machine/GPU profile;
- base model and revision;
- data manifest URIs and hashes;
- training config;
- output/checkpoint bucket;
- experiment/run ID;
- service identity;
- network and egress policy;
- labels and budget estimate.

## Job behavior

- validate rights/manifests before GPU allocation;
- checkpoint to Cloud Storage;
- emit metrics and structured status;
- handle preemption only if selected machine type supports/justifies;
- stop on NaN/divergence or budget threshold;
- evaluate promoted checkpoints;
- write immutable run summary.

## Isolation

Research project cannot access production user data or secrets. Public datasets are copied/promoted through manifests, not by granting training jobs blanket production bucket access.
