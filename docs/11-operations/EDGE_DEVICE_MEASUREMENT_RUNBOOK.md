---
document_id: DRL-OPS-008
title: "Edge Device Measurement Runbook"
version: 0.1.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---

# Edge Device Measurement Runbook

How to get real on-device numbers for the Atticus **Edge** role, and — more
importantly — what those numbers are and are not allowed to be used for.

`LOCAL_MODEL_RUNBOOK.md` (DRL-OPS-007) covers serving an open-weight model on a
workstation. This covers the phone, which is the Edge role's actual deployment
target and a different measurement problem.

## What Google AI Edge Gallery is

A showcase **application**, published by Google under Apache 2.0 at
[`google-ai-edge/gallery`](https://github.com/google-ai-edge/gallery). It runs
open-weight models fully on-device and offline, with Hugging Face integration for
model download.

Two things follow, and both matter:

1. **It is not an SDK.** You cannot build on Gallery. It was migrated onto
   **LiteRT-LM**, the open-source on-device runtime, and that is what an
   application would integrate. Gallery is a readable reference implementation,
   not a foundation.
2. **The MediaPipe LLM Inference API is maintenance-only.** Google directs
   Android work to the LiteRT-LM Kotlin API. Much of the tutorial material still
   shows the old path; do not start there.

Gallery also has no HTTP surface. It is a chat UI for a person, not an endpoint
for a harness — which is the whole difficulty below.

## What the gate requires

`EvidenceGate` blocks an Edge selection unless every one of these holds. Nothing
in this runbook changes any of them:

| Condition | State as of 2026-08-23 |
|---|---|
| Suite coverage ≥ 8 | **Satisfiable** — 11 eligible edge tasks since suite v1.1.0 |
| Measurement on hardware | **Open** — this is what the runbook addresses |
| Revision pinned | Open — register says `scaffold-unpinned` |
| License cleared | Open — register says `provisional_review_required` |
| Candidates for the role ≥ 2 | Workstation serving documented for `edge-qwen3-1.7b` and `edge-smollm3-3b` (Path B). On-device Path C is still open. Two served desktop tags are not a phone bake-off. |
| Weighted quality ≥ 0.80 | Open |
| Safety-critical failures = 0 | Open |
| Errored tasks = 0 | Open |
| Margin over runner-up ≥ 0.05 | Open |

A hardware run addresses exactly one row. It does not shorten the list.

## Three paths, and what each is worth

### Path A — hand pass in Gallery (hours)

Install Gallery, pull two open-weight small models, and put the suite's edge
prompts through them by hand.

**What it is worth.** It tells you whether the graders survive contact with real
output before you invest in anything. `TR-2026-002` §6 already concedes that
refusal detection is marker-based and "will need widening against the phrasing
real models actually produce" — this is how you find out. It also tells you
whether the 1500 ms budget in `edge.intent-routing-latency` is anywhere near
reality on your device.

**What it is not.** It is not a bake-off run and produces no gate evidence. A
person choosing prompts and reading answers is not a deterministic harness.

**The rule.** Findings from Path A may be used to *fix graders and thresholds*.
They may never be transcribed into a report as measured results, and no run
touched by hand may be labelled `measurement_mode: hardware`. Doing so would
fabricate a model run, which the research plan forbids outright.

### Path B — desktop hardware run (a day)

Serve the same open-weight small models on a workstation behind any
OpenAI-compatible endpoint, per DRL-OPS-007, and run the suite against them.

```bash
uv run python scripts/check_local_ollama.py
uv run python scripts/probe_model.py --model hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0 --no-thinking
uv run python scripts/run_bakeoff.py --live --measurement-mode hardware
```

**What it is worth.** A legitimate `hardware` measurement that clears the
measurement-provenance condition, and the first real variance estimate — which is
what the resolution diagnostic in `TR-2026-002` §10 needs before it can become a
gate.

**The catch.** It measures the wrong hardware for the Edge role specifically.
`edge.intent-routing-latency` asserts an edge-class budget; a workstation result
tells you nothing about whether a phone meets it. Report desktop latency as
desktop latency.

### Path C — on-device endpoint (weeks)

An Android application built on the LiteRT-LM Kotlin API that exposes a minimal
OpenAI-compatible `/v1/chat/completions` endpoint on the local network, so the
harness can drive the real device.

This is the only path that produces a gated Edge hardware run on the hardware the
role is actually for. It is also a real Android project — Kotlin, model
acquisition, device matrix — and should not be started before Path A has shown
the graders and the latency budget are sound.

Register it like any other served candidate:

```yaml
  - id: edge-<family>
    role: edge
    revision_label: <exact pinned revision>
    license_status: cleared
    serving:
      runtime: litert-lm
      model: <model file or tag>
      base_url: http://<device-ip>:<port>/v1
      quantization: <e.g. int4>
```

Then the same `--live --measurement-mode hardware` invocation applies. At least
two edge candidates must be served before either can be selected; a field of one
is blocked by `min_candidates`, and that condition exists precisely to stop a
single convenient device from becoming a decision.

## Recommended order

1. **Path A now.** Cheap, and it de-risks everything after it.
2. **Fix what Path A exposes** — grader phrasing, latency budget — as an ordinary
   suite change with its own review.
3. **Path B next**, for a first honest variance estimate.
4. **Path C only if** the numbers justify an Android project, and only after the
   Director decides whether on-device Atticus Edge is in V1 scope. `ROADMAP.md`
   currently excludes "mobile-native applications beyond responsive web and
   optional local companion research"; an on-device Edge companion plausibly sits
   inside that carve-out, but that reading should be recorded rather than assumed.

## What must not happen

- No hand-run is labelled a measured run.
- No score is transcribed from a screen into a report or a manifest.
- `min_tasks`, `min_margin`, and the safety-critical conditions are not lowered to
  make a device pass. If the gate refuses after a real run, the instrument is
  reporting that the evidence is insufficient — extend the suite or fix the setup.
- No model file, weight, or downloaded artifact enters this repository.
