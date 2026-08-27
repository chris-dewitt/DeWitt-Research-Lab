# Computational Finance of Intelligence — research instrumentation

Machine-side apparatus for the CFI program, covering the Paper II track and the
shared Belief Diffusion bridge. This package contains **no experiment, no
dataset, and no result**. It is the instrument a preregistered protocol would
later drive.

Authority: `docs/10-research/COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md`
(DRL-RES-005) and the dispositions in
`docs/10-research/CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md` (DRL-RES-006).

## Why Paper II, and why only the machine half

Paper II is the only CFI track that survived the G1 novelty review. It survived
narrowed: framing effects, Black-Scholes, Dutch-book auditing, and projection
repair are each established separately, so the differentiable claim is the
*conjunction* — payoff-equivalent financial claims, a deterministic replication
oracle, paired human and model valuation, implied-volatility distortion, and an
explicit calibration-versus-repair trade-off.

The machine half of that conjunction needs no gate that is not already passable:
it is deterministic mathematics and elicited model responses, with no human
subjects and no dataset rights. The human baseline comes from reanalysis of an
eligible public corpus under CFI-003/CFI-203, and that rights review is the
critical path. Building the instrument while the rights record works through G2
lets the two converge instead of queueing.

## What is deliberately absent

- **No estimands, thresholds, or inferential statistics.** Freezing those is a
  G3 protocol decision. `PairedValuation` exposes a raw paired difference and
  stops there.
- **No human data, and no code path that reads any.** G2 has not been passed.
- **No novelty claim.** The pricing and repair machinery is a baseline, on the
  novelty review's explicit finding.
- **No provider calls.** Eliciting model valuations requires a model-family gate;
  this package computes and audits, it does not query.

## Modules

| Module | Packet | Responsibility |
|---|---|---|
| `linalg` | shared | Householder QR least squares and Lawson-Hanson NNLS, in pure Python |
| `payoffs` | CFI-201 | Piecewise-linear payoff primitives and the exact payoff-equivalence oracle |
| `pricing` | CFI-202 | Black-Scholes as a normative oracle, parity invariants, implied volatility |
| `frames` | CFI-201 | Frame taxonomy, and frame pairs that cannot vary the payoff |
| `coherence` | CFI-204 | Arbitrage detection, minimal coherence repair, exploiting portfolio |
| `competence` | CFI-205 | Unframed-control screen excluding subjects that cannot price the claim |
| `beliefs` | CFI-004 | The observable belief-event schema, refusing records it cannot represent |
| `baselines` | CFI-005 | Bayesian, diffusion, OU, and jump estimators, with simulators and a recovery study |
| `viewer` | CFI-007 | Static HTML for a belief path and its fits, with a diagnostic per unidentified estimate |

## Two design decisions that bound the claims

**Payoff equivalence is decided, not sampled.** Every primitive is continuous and
piecewise linear with kinks only at strikes, so two claims are identical
everywhere exactly when they agree on a finite grid of kinks and interior points
and share a terminal slope. Digital and barrier payoffs are excluded because
their discontinuities would break that proof and reduce equivalence to sampling.
`FramePair` refuses construction unless the oracle decides equivalence, so wording
is structurally incapable of changing the payoff.

**Coherence uses the closed cone.** No-arbitrage over a finite state space means
the price vector lies in `C = {A q : q >= 0}`. Detection, repair, repair
distance, and the exploiting portfolio all fall out of one projection onto `C`,
which is a non-negative least-squares problem. Two consequences are limitations
rather than rounding artifacts, and are documented in `coherence.py`: the
strictly-positive cone is not closed, so a *weak* arbitrage on the boundary
reports as coherent; and non-negativity is certified only across the spanned
grid, so the terminal slope is reported separately via
`certificate_is_grid_bounded`.

## Layout note

`COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md` §11 sketches a `research/cfi/` tree
with `shared/` and per-paper directories, and says an implementation agent may
create it "in a focused issue after CFI-004 is approved." This package was
created at the Director's direct instruction ahead of that gate, and the
deviation was **ratified by RES-023 on 2026-08-19**. CFI-004 approval is no
longer a precondition for the package's existence.

That ratification is scoped to layout only. CFI-004 still governs the
belief-event schema work it was written for, and G2 (data rights) and G3
(protocol freeze) are untouched — nothing here is cleared to acquire data or
freeze an estimand. The flat module layout maps onto the sketched tree as shown
in the table above and can be expanded into subpackages without changing the
public API.

## Reproduction

```bash
uv sync --all-packages
uv run pytest tests/cfi -q
```
