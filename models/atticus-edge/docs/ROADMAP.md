---
document_id: DRL-MODE-105
title: "Atticus Edge Build Roadmap"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Edge Build Roadmap

    ## Delivery philosophy

    Atticus Edge is built as thin verified vertical slices. Each slice includes contracts, implementation, tests, telemetry, documentation, demo evidence, and rollback—not an isolated subsystem no user can exercise.

    ## Workstreams

    - Task boundary and device profiles.
- Small-model bake-off.
- Reviewed SFT and distillation data.
- Escalation calibration.
- Quantization and device optimization.
- Voice and local-runner integration.
- Public release and comparative paper.

    ## Dependency order

    Boundary and gates → candidates → reviewed data → training → escalation/failure repair → quantization/device → integration/security → signed release.

    ## Cross-project dependencies

    - Core traces and model program.
- AtticusBench.
- EvalForge.
- Local runner.
- Runtime packaging.
- Rights and license review.

    ## Release evidence

    - Candidate report.
- Reviewed data manifest.
- Training logs.
- Escalation calibration.
- Device and quantization report.
- Offline workflow.
- Public weights, cards, and signatures.

    ## Explicitly deferred

    - Complex autonomous agent operation.
- Broad long-context research.
- Every hardware platform.
- Mobile-specific model optimization.
- Silent online fallback.
- Public private-personalization adapter.

    Deferred work may appear on the public roadmap but cannot be implied by V1 marketing. Agents must not widen authority or scope “helpfully.”
