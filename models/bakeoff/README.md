---
document_id: DRL-MOD-100
title: "Atticus Bake-Off Scaffold"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-29
---

# Atticus Bake-Off Scaffold

Prototype scaffolding for **DRL-012**. Loads `candidates.yaml`, scores
synthetic Stage-A fixture metrics, and emits a report covering candidates,
licenses, hardware, cost, latency, quality, and limitations.

## Non-claims

- This is **not** a live hardware bake-off.
- This does **not** select Atticus Core or Edge.
- **DIR-004** remains open until measured evidence is reviewed.

## Commands

```bash
uv run python -c "from drl_ai_core import run_bakeoff_scaffold; import json; print(json.dumps(run_bakeoff_scaffold(), indent=2))"
uv run pytest -q tests/test_bakeoff_scaffold.py
```
