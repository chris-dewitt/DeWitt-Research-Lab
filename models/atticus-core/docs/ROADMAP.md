---
document_id: DRL-MODC-104
title: "Atticus Core Build Roadmap"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atticus Core Build Roadmap

    ## Delivery philosophy

    Atticus Core is built as thin verified vertical slices. Each slice includes contracts, implementation, tests, telemetry, documentation, demo evidence, and rollback—not an isolated subsystem no user can exercise.

    ## Workstreams

    - Candidate and rights intake.
- Baseline bake-off.
- Data and review pipeline.
- SFT experimentation.
- Preference/safety stage if warranted.
- Quantization and serving.
- Integrated evaluation and public release.

    ## Dependency order

    Candidate register → baseline freeze → data freeze → pilot sweeps → selected training → failure repair → quantized runtime → signed release.

    ## Cross-project dependencies

    - AtticusBench and data governance.
- EvalForge.
- Colab and Vertex training.
- Model gateway, control plane, and local runner.
- Security and license review.

    ## Release evidence

    - Upstream and data rights register.
- Baseline/candidate reports.
- Training logs and checkpoints.
- Quantization/runtime matrix.
- Model/data/safety/reproducibility cards.
- Signed weights/manifests.
- Integrated demonstration.

    ## Explicitly deferred

    - From-scratch foundation pretraining.
- Frontier-scale general model.
- Continuous hidden production self-training.
- Private personalization in public weights.
- Unsupported model sizes and runtimes.

    Deferred work may appear on the public roadmap but cannot be implied by V1 marketing. Agents must not widen authority or scope “helpfully.”
