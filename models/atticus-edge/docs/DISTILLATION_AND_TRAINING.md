---
document_id: DRL-MODE-101
title: "Atticus Edge Distillation and Training"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Atticus Edge Distillation and Training

Edge may begin from a strong small open-weight instruct or function-calling model or be distilled from Core and other approved teachers. Candidate selection compares license, tokenizer/template compatibility, CPU and GPU runtime, structured output, noisy voice-command robustness, and escalation behavior.

Teacher trajectories are never accepted raw. They are generated only in fixture environments, validated against expected tool, policy, and task outcomes, filtered for schema and safety, reviewed according to category risk, and retain teacher, prompt, configuration, and validator provenance. Distillation targets observable plans, calls, corrections, and results—not private hidden chain-of-thought.

Training emphasizes short contexts, intent and skill classification, tool argument extraction, correction, uncertainty, escalation, concise local summaries, and a small capability-retention mixture. Quantization and real-device testing begin early because the quantized artifact—not the uncompressed checkpoint—is the intended Edge experience.
