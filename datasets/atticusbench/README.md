# AtticusBench

AtticusBench is DRL's versioned benchmark for tool use, routing, permissions, approvals, recovery, grounded synthesis, and cross-system agent workflows. It is a research dataset and evaluation program—not a collection of prompt examples.

Authoritative documents: [`docs/SPEC.md`](docs/SPEC.md), [`docs/TASK_AUTHORING.md`](docs/TASK_AUTHORING.md), and laboratory data/evaluation policies.

## Public Seed 0.1.0

The first executable slice of the program is in this tree: **32 cases across all
ten V1 families, 9 environment fixtures, and 4 deterministic baselines** whose
results are committed under [`runs/atticusbench/`](../../runs/atticusbench/).

This is a seed, not the V1 release. The V1 exit gate asks for at least 1,000
held-out tasks; this is 32 public ones, and no model has been run against it.
The dataset card records what it does and does not support:
[`docs/DATASET_CARD.md`](docs/DATASET_CARD.md).

```
schemas/    case and fixture JSON Schemas (2020-12)
fixtures/   9 content-addressed environment fixtures; declarations, no code
cases/public/<family>/<case_id>.yaml
src/atticusbench/   loader, environment builder, harness, baselines, scoring
release/    case index, contamination report, dataset release manifest
```

## Quickstart

```bash
uv run python scripts/validate_atticusbench.py        # schema, digests, coverage, duplication
uv run python scripts/run_atticusbench.py             # run the split, rewrite runs/atticusbench
uv run python scripts/run_atticusbench.py --check     # fail if the committed output drifted
uv run pytest tests/atticusbench -q

make atticusbench atticusbench-check atticusbench-validate
```

## How a case executes

A case declares its environment fixture, the request, the session mode, the tool
catalog offered, a reference plan, any approval grants, the acceptable terminal
states, and hard invariants. The harness builds a tool registry from the
fixture's declarations and runs the case through the **shipped** Atticus
orchestrator, policy engine, and approval service — not a copy of them — so a
case measures the authorization path the runtime actually has.

Scoring is a vector, never one number: terminal-state correctness, required-tool
coverage, unauthorized actions, forbidden effects actually executed,
required-approval recall, citation grounding, calculation delegation, step budget,
abstention correctness, and critical-suite failures reported as case ids. A
system that completes more tasks by acting without authority must not be able to
average past one that safely refused, and a system that refuses everything is
scored for excessive refusal rather than credited with safety.

Fixtures carry no executable code. Each tool declares its risk tier, whether a
public session may reach it, its deterministic response, an argument contract,
any side effect it performs, and any failure it raises. Every invocation and every
executed side effect lands in an effect ledger, which is how a scorer can say an
external write happened rather than infer it from prose.

## Adding a case

1. Read [`docs/TASK_AUTHORING.md`](docs/TASK_AUTHORING.md); name the capability,
   the risk, and the failure before writing anything.
2. Reuse an existing fixture where the world state already fits; add a fixture
   only when the environment genuinely differs.
3. Write the case YAML, then run
   `uv run python scripts/validate_atticusbench.py --write-digests`.
4. Confirm `reference-plan-v1` satisfies the case: if the recorded safe plan
   cannot pass, the case is wrong, and `tests/atticusbench/test_harness.py`
   enforces that.
5. Rerun `scripts/run_atticusbench.py`, then
   `scripts/validate_atticusbench.py --write-manifest`, in that order. The
   manifest digests the results file and the dataset card, so it goes last;
   a test fails if it is stale.

Hidden-test material never enters this tree. The case schema admits only the
`public-test` split.
