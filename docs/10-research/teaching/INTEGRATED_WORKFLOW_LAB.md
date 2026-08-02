---
document_id: DRL-TEACH-001
title: "Integrated Workflow Teaching Lab"
version: 1.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-01
---


# Integrated Workflow Teaching Lab

Maturity: **prototype** teaching material for the local fixture path.  
No private datasets, personal content, live market feeds, or production credentials are used.

## Learning objectives

1. Run the Atticus evidence-to-scenario workflow offline.
2. Read cited Atlas / FedLens / BalanceLab evidence without treating fixture text as live Fed or bank data.
3. Inspect the five-way `linked_workflow` digests on one task.
4. Distinguish completed vs degraded outcomes and honest limitation labels.
5. (Optional, after DRL-019 merges) Verify a signed fixture replay package.

## Prerequisites

- Supported Python 3.12/3.13 environment
- Repository bootstrap: `make doctor` (or the documented `uv`/`pnpm` setup)
- No cloud project, API keys, or paid model accounts

## Lab 0 — Bootstrap honesty check (5 minutes)

```bash
make doctor
make demo
```

**Exercise 0.1.** In the demo output, list three limitation lines.  
**Exercise 0.2.** Confirm the run is labeled as fixture/synthetic in those limitations.

## Lab 1 — Integrated prompt (10 minutes)

Canonical teaching prompt (also the product demo contract):

> Using the latest available public inflation evidence and Federal Reserve communication, construct a plausible synthetic bear-steepener scenario and analyze its impact on the sample regional bank. Show sources, assumptions, calculations, limitations, and an evaluation of the workflow.

Run:

```bash
uv run --package atticus-control-plane atticus-demo --public
```

**Exercise 1.1.** Record the reported EvalForge score.  
**Exercise 1.2.** Name the three specialist tools that ran (Atlas, FedLens, BalanceLab).  
**Exercise 1.3.** Why must BalanceLab numbers never come from model prose?

## Lab 2 — Evidence and citations (15 minutes)

Write a short Python probe (or use pytest) to inspect a completed `TaskResult`:

```python
from atticus_control_plane import build_local_runtime
from drl_protocol import TaskRequest

result = build_local_runtime().run(
    TaskRequest(
        "teach-lab-2",
        "Using inflation and Federal Reserve evidence, run a bear-steepener bank scenario",
        public_session=True,
        as_of="2026-07-24",
    )
)
assert result.evaluation["passed"]
for item in result.evidence:
    print(item.evidence_id, item.citation)
print(sorted(result.artifacts["linked_workflow"]["links"]))
```

**Exercise 2.1.** Copy one Atlas citation URI and one FedLens citation URI.  
**Exercise 2.2.** Confirm every evidence item has a non-empty citation.  
**Exercise 2.3.** List the five keys under `linked_workflow["links"]`.

## Lab 3 — Deterministic calculation (10 minutes)

```bash
uv run pytest tests/test_balancelab_scenarios.py tests/test_atticus_foundation.py -q
```

**Exercise 3.1.** What is the hand-verifiable annual NII change for the synthetic bear-steepener?  
**Exercise 3.2.** Which artifact carries the BalanceLab digest (`calculation_artifact`)?

## Lab 4 — Degraded and replay literacy (10 minutes)

Truthful degradation matters more than a pretty success screen.

**Exercise 4.1.** Read `docs/01-product/INTEGRATED_REFERENCE_DEMO.md` and name one required failure behavior.  
**Exercise 4.2.** After DRL-019 is on `main`, run:

```bash
uv run pytest tests/evalforge/test_signed_replays.py -q
```

Explain in one sentence why fixture HMAC signing is not a production release signature.

## Lab 5 — Open research posture (5 minutes)

**Exercise 5.1.** Quote the laboratory mission from `LABORATORY_BIBLE.md` or the demo guide output.  
**Exercise 5.2.** Identify one Director decision (`DIR-*`) that still blocks calling this a production V1.

## Instructor notes

- Keep maturity language precise: this is a **prototype** local vertical slice.
- Do not imply live FRED/Treasury/Fed APIs or trained Atticus Core/Edge weights.
- Sponsors must not set answers, grades, or research conclusions (see open-source governance docs).
- Preferred verification for contributors: `make verify`.

## Answer key (instructor)

| Exercise | Expected signal |
|---|---|
| 0.x | Fixture/synthetic limitations present |
| 1.3 | Deterministic BalanceLab engine is authoritative for numbers |
| 2.3 | `atlas`, `fedlens`, `balancelab`, `report`, `evaluation` |
| 3.1 | `15.81` |
| 4.2 | Demo HMAC key / `live_at_capture=false` / not production identity |
| 5.2 | e.g. DIR-002, DIR-004, or DIR-001 |

## Related documents

- `docs/01-product/INTEGRATED_REFERENCE_DEMO.md`
- `docs/09-open-source/CONTRIBUTOR_EXPERIENCE.md`
- `agents/15_RESEARCH_COMMUNITY.md`
- `services/evalforge/fixtures/signed_replays/README.md` (after DRL-019)
