---
document_id: DRL-TR-2026-004
title: "Technical Report TR-2026-004: Which Belief Parameters Recover, and Which Are Bounded by the Interval"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-09-18
citation_key: dewitt2026tr004
maturity: prototype
---


# TR-2026-004: Which Belief Parameters Recover, and Which Are Bounded by the Interval

## Citation

DeWitt, Christopher Noxon. 2026. *Technical Report TR-2026-004: Which Belief
Parameters Recover, and Which Are Bounded by the Interval*. Working paper.
Document ID `DRL-TR-2026-004`. Repository path:
`docs/10-research/reports/TR-2026-004-belief-parameter-recovery-sweep.md`.

## Abstract

CFI-005, the parameter-recovery work item of the Computational Finance of
Intelligence research program, previously reported recovery error at one design:
200 replications, 400 observations, `dt = 0.05`. One design cannot separate three
different situations — an estimator whose error shrinks with more data, one whose
error is already at an information limit, and Monte Carlo noise in the
measurement of the bias itself. This report sweeps two axes to separate them,
over 11,850 fitted replications, and finds that the eight parameters across
the three baseline models fall into three distinct classes.

**Class one, convergent.** Volatility, in all three models, has error that falls
with grid refinement at a root-n rate: log-log slopes of −0.470, −0.593, and
−0.632 with r² ≥ 0.978. Its relative bias at the finest grid is under 0.3% in
every model.

**Class two, interval-bounded and unbiased.** The diffusion drift, the
Ornstein-Uhlenbeck level, and the jump drift do not improve at all as the same
interval is sampled more finely — slopes of +0.013, +0.009, and −0.040 — and
none of the three shows a bias distinguishable from Monte Carlo noise at 800
replications (1.1, 1.8, and 0.7 standard errors). The diffusion drift's error
sits at the analytic limit `sigma / sqrt(T)` = 0.253 for the whole sweep. These
estimators are not deficient; they have extracted what a fixed interval contains.

**Class three, genuinely biased.** The Ornstein-Uhlenbeck reversion rate is
biased upward by 14.9 standard errors and the jump intensity downward by 20.3.
Refinement does not remove either. It reduces the intensity bias substantially
(−45.8% to −5.9% relative) while leaving the total error at the Poisson counting
limit, and it makes the reversion-rate bias *worse* (+15.1% to +22.2% relative)
while the total error stays flat.

The practical consequence for the program is narrow and concrete: a protocol
whose conclusion depends on a reversion rate or a jump intensity cannot be
rescued by sampling more often. No protocol has passed the G3 gate, so nothing
here is a pass or a failure of anything.

## 1. Question and scope

**Question.** For each parameter in the CFI baseline model family, is the
recovery error reported at one design a small-sample artifact that more data
removes, an information limit that more data of the same kind cannot move, or an
artifact of how precisely the bias itself was measured?

**Scope.** Simulated data from a model, fitted back with that same model. This
measures recovery under **correct specification only**. It says nothing about
misspecification, nothing about human belief, and nothing about machine belief.
`COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md` §2.1 is explicit that the diffusion
family is a research hypothesis rather than an assertion about how beliefs move;
this report tests instruments, not subjects. No G2 data was used and none is
implicated.

## 2. Why the sweep refines rather than extends

The natural sweep is to lengthen the observation interval. It is not available
here, and the reason is itself a result.

The simulator refuses a path whose belief leaves the representable log-odds range
of ±20.723 rather than silently pinning it at the boundary, because a pinned path
emits zero increments that no estimator can distinguish from a subject who
stopped updating. With the study's drift of 0.4, the mean belief crosses that
bound at about `T = 52`, and in practice the first replication saturates near
`T = 30`: an attempt to extend the diffusion design to 3,200 observations at
`dt = 0.05` — `T = 160` — fails at step 608 with a log-odds of +20.780.

So the sweep holds calendar time fixed at `T = 10` and refines the grid, and it
adds a second axis that grows the replication count at a fixed design. The first
axis asks what more observations of the same interval buy. The second asks how
precisely the bias was measured in the first place.

## 3. Method

```bash
uv run python scripts/run_recovery_sweep.py
uv run python scripts/run_recovery_sweep.py --check   # byte-compare the committed results
```

**Axis 1, grid refinement.** `T = 10` fixed; 100, 200, 400, 800, 1,600, and 3,200
observations, so `dt` runs from 0.1 down to 0.003125; 400 replications per point.
Error against horizon is fitted as `log(error) = intercept + slope * log(n)` by
least squares using the program's own `solve_least_squares`. A slope near −0.5 is
root-n convergence; a slope near zero means more observations of the same
interval bought nothing.

**Axis 2, Monte Carlo precision.** 400 observations and `dt = 0.025` fixed; 50,
100, 200, 400, and 800 replications. Each point reports the bias and the standard
error of that bias, `spread / sqrt(replications)`. A bias is called *resolved*
when it stands at least two standard errors from zero. That is a statement about
the measurement, not about whether the bias is tolerable.

All three baseline designs from the single-point study are carried over unchanged
so the two studies remain comparable. Seed 20260825. Results:
`research/cfi/results/recovery-sweep.json` and `recovery-sweep.csv`.

As a check on the axis itself: the fitted standard-error slopes on axis 2 fall
between −0.42 and −0.54 with r² > 0.99 for all eight parameters, which is the
−0.5 that quadrupling replications to halve a standard error requires.

## 4. Results

### 4.1 Grid refinement: root-mean-square error against observation count

| Model | Parameter | Truth | n=100 | n=3200 | Slope | r² | Relative bias at n=3200 |
|---|---|---|---|---|---|---|---|
| diffusion | `drift` | +0.400 | 0.2319 | 0.2453 | +0.013 | 0.10 | +1.3% |
| diffusion | `volatility` | +0.800 | 0.0564 | 0.0107 | **−0.470** | 0.999 | −0.03% |
| ornstein_uhlenbeck | `reversion_rate` | +1.500 | 0.6238 | 0.6653 | +0.005 | 0.01 | **+22.2%** |
| ornstein_uhlenbeck | `level` | +0.700 | 0.1174 | 0.1228 | +0.009 | 0.05 | −0.2% |
| ornstein_uhlenbeck | `volatility` | +0.600 | 0.0659 | 0.0082 | **−0.593** | 0.994 | −0.3% |
| jump_diffusion | `drift` | +0.000 | 0.1836 | 0.1570 | −0.040 | 0.64 | undefined |
| jump_diffusion | `volatility` | +0.500 | 0.0624 | 0.0063 | **−0.632** | 0.978 | −0.1% |
| jump_diffusion | `jump_intensity` | +0.800 | 0.4164 | 0.2666 | −0.123 | 0.84 | −5.9% |

The jump drift's relative bias is undefined because its truth is exactly zero;
the study records it as null rather than as an infinity.

### 4.2 Monte Carlo precision at 800 replications

| Model | Parameter | Bias | Standard error | Bias / SE | Resolved from noise |
|---|---|---|---|---|---|
| diffusion | `drift` | −0.0101 | 0.0093 | −1.09 | no |
| diffusion | `volatility` | −0.0028 | 0.0010 | −2.84 | yes |
| ornstein_uhlenbeck | `reversion_rate` | **+0.3266** | 0.0219 | **+14.89** | yes |
| ornstein_uhlenbeck | `level` | −0.0085 | 0.0047 | −1.82 | no |
| ornstein_uhlenbeck | `volatility` | −0.0140 | 0.0007 | −19.07 | yes |
| jump_diffusion | `drift` | +0.0041 | 0.0056 | +0.73 | no |
| jump_diffusion | `volatility` | +0.0029 | 0.0007 | +4.23 | yes |
| jump_diffusion | `jump_intensity` | **−0.1708** | 0.0084 | **−20.32** | yes |

Resolution is not severity. The Ornstein-Uhlenbeck volatility bias is resolved at
19 standard errors and is 2.3% of truth; the diffusion drift bias is unresolved
and is 2.5% of truth. The two facts answer different questions: whether a bias
exists, and whether it matters.

### 4.3 Volatility is the only parameter refinement fixes

All three volatility slopes are steeper than −0.5. That is not super-root-n
convergence. At coarse grids these estimates carry bias as well as variance — the
Ornstein-Uhlenbeck volatility's relative bias is −8.9% at 100 observations and
−0.3% at 3,200 — so the early part of the curve drops faster than variance alone
would, which tilts a single fitted slope past −0.5. Read as intended, the result
is that refinement removes the discretization bias first and then keeps reducing
variance at root-n.

### 4.4 The drift is at its information limit, not failing

The diffusion drift estimator uses the interval's total displacement, whose
standard error is `sigma / sqrt(T)`. For `sigma = 0.8` and `T = 10` that is
**0.2530**, and it contains no `n`. Observed error moves non-monotonically
between 0.2319 and 0.2706 across a 32-fold increase in observation count, with no
trend (slope +0.013, r² 0.10), and its bias is unresolved at 800 replications.
The estimator is extracting everything the interval holds.

The earlier single-point study derived this limit and flagged the wide drift
interval so that a future reader would not mistake it for a bug. This sweep is
the empirical confirmation: the limit is a property of the interval, and 3,200
observations of a ten-unit interval are worth no more than 100 for this
parameter. The Ornstein-Uhlenbeck level behaves the same way, flat at 0.12 to
0.14 with an unresolved bias.

**Consequence.** A protocol that needs a tighter drift or level estimate must buy
a longer interval, and the saturation bound in §2 says how much interval is
purchasable at a given drift before the instrument refuses the path. That
trade-off is now quantified rather than assumed.

### 4.5 Two parameters are biased, and refinement does not fix either

**Jump intensity.** The bias improves sharply with refinement, from −45.8%
relative at 100 observations to −5.9% at 3,200: a coarse grid merges or misses
jumps, and a finer grid resolves them. The *total* error stops improving anyway,
flattening near 0.267. That floor has an explanation: with intensity 0.8 over
`T = 10`, a path carries 8 jumps in expectation, and a count-based intensity
estimate over a fixed interval has standard error `lambda / sqrt(lambda * T)` =
0.8/√8 = **0.283**. The observed 0.267 at the finest grid is that limit. Once the
grid is fine enough to see the jumps, the remaining error is Poisson counting
noise over a fixed interval, and refinement cannot touch it.

**Reversion rate.** This one gets worse. The total error is flat — 0.624 at 100
observations, 0.665 at 3,200 — while the relative bias grows from +15.1% to
+22.2%, so refinement is converting variance into bias rather than removing
error. The mechanism is the reparameterisation the single-point study already
identified: least squares attenuates the AR(1) coefficient, and recovering
`kappa` from that coefficient divides by `dt`, so a fixed attenuation is
amplified as the grid is refined. At 800 replications the bias stands at 14.9
standard errors, which settles that it is a property of the estimator and not of
this study's sample size.

**Consequence.** Of the eight parameters, `reversion_rate` is the one a protocol
should not depend on as currently estimated. The candidate remedies — a
bias-corrected or maximum-likelihood Ornstein-Uhlenbeck fit rather than the
least-squares reparameterisation — are estimator changes, and choosing one is
research work with its own recovery study, not a patch.

## 5. What this does not show

- Nothing about human or machine belief. Simulated data, correct specification.
- Nothing about misspecification. Every fit here saw data from its own family. A
  parameter in class one may behave arbitrarily badly under the wrong model.
- Nothing about longer intervals. `T = 10` throughout, for the reason in §2.
- No pass or failure. G3 has not been passed; there is no threshold to compare
  against, and this report deliberately declines to invent one.
- The replication axis is nested: each count is a fresh study from the same base
  seed, so larger counts contain the smaller ones and the standard errors are
  not independent across points on that axis.

## 6. Reproduction and artifacts

```bash
uv run python scripts/run_belief_recovery.py            # the original single-point study
uv run python scripts/run_recovery_sweep.py             # this sweep, both axes
uv run python scripts/run_recovery_sweep.py --check      # byte-compare the committed results
uv run pytest tests/cfi/test_recovery_sweep.py -q       # 18 tests, including the claims above
make recovery-sweep recovery-sweep-check
```

Committed results: `research/cfi/results/recovery-sweep.json` (both axes, per-point
measurements, fitted slopes, limitations) and `recovery-sweep.csv` (one row per
model, point, and parameter). The headline claims in §4.3, §4.4, and §4.5 are
pinned by tests against the committed artifact, so a code change cannot leave
this prose standing while the numbers move.

## 7. Next dependency-unblocking work

1. A bias-corrected Ornstein-Uhlenbeck estimator, with its own recovery study
   against this one as the baseline. This is the only change here that a protocol
   depending on `reversion_rate` would need.
2. An interval-length study for the drift and level parameters, bounded by the
   saturation limit in §2, to turn "buy a longer interval" into a table.
3. A misspecification study: fit each model to data generated by the other two
   and report what recovers. Class one membership is only meaningful once that
   exists.
4. An intensity estimator that uses jump sizes and not only counts, which is the
   only route past the Poisson limit in §4.5 at fixed interval.
