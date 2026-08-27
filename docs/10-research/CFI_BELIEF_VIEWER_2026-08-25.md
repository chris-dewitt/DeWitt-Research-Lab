---
document_id: DRL-RES-012
title: "CFI-007 Belief-Trajectory Viewer"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-25
---

# CFI-007 Belief-Trajectory Viewer

## What this is

The exit evidence for CFI-007 is "accessible local viewer and degraded/empty/error
states." This records what was built and, more usefully, the measurement that
decided its design.

CFI-005 gave the Belief Diffusion bridge four estimators and a recovery study,
but both speak only in terminal text. This is the instrument you can look at.

**Local only.** `site/` is gitignored, nothing is published, and
`.github/workflows/publish-pages.yml` is untouched.

## Reproduction

```bash
make belief-site
# or
uv run python scripts/build_belief_site.py --out site/beliefs --metadata
uv run python scripts/build_belief_site.py --list
uv run python scripts/build_belief_site.py --empty-state --out /tmp/empty
```

Seven pages plus an index. Every fixture is generated from a fixed seed rather
than read from a committed file, so the output is byte-identical on any machine
and there is no data file that can drift from the code that produces it.

## The measurement that decided the design

Fit the Ornstein-Uhlenbeck estimator to a pure drifting walk — seed 20260825,
the same path the `diffusion` page shows — and it returns:

| | |
|---|---|
| reversion rate | −0.0242 |
| **fitted level** | **−16.53 log-odds**, which is a probability of 0.000000066 |
| half-life | infinite |
| range the belief actually visited | +0.00 to +9.97 |

The estimator reports a resting point at six-hundred-thousandths of one percent
for a belief that never once dropped below even odds. **Nothing in the return
value says anything is wrong.** The number is not a bug; the model was asked a
question this data cannot answer, and the answer came back with the same
confidence any other would have.

A viewer that printed that level in a table beside the others would be the same
failure recorded in `EVAL-0001` and again in `DRL-RES-011`: an instrument quietly
producing a plausible number instead of refusing. So every estimate on every page
travels with diagnostics.

## What a diagnostic is, and is not

A diagnostic is a statement about **identifiability or resolution** — this output
does not carry the information its name implies. It is never a statement about
whether a value is good. `RecoveryReport` deliberately carries no verdict because
G3 has not been passed, and the renderer inherits that: no page contains a
threshold, a pass, or a failure, and a test asserts it.

| code | fires when | what it says |
|---|---|---|
| `single-increment` | fewer than two increments | drift is that increment, volatility is zero by construction |
| `no-reversion` | reversion rate < 0 | half-life infinite; the fitted "level" is not a level |
| `level-unidentified` | reversion rate == 0 | the estimator found no pull and reported the sample mean |
| `level-off-path` | level outside the visited range | an extrapolation from a weak pull, not an observed resting point |
| `no-jumps-detected` | zero jumps flagged | a detection floor, not a measured absence |
| `jump-scale-unresolved` | exactly one jump | scale is exactly zero because one observation forces it |
| `jump-fraction-high` | more than 10% of increments flagged | the signature DRL-RES-011 traced to a saturating path |
| `one-increment-per-evidence` | `observations <= distinct ids` | every ratio is its own single increment; residuals are zero by construction |
| `zero-residual` | residual scale <= 1e-12 | the fit reproduces the increments exactly, so the residual says nothing |

### Two predicates that had to be measured, not reasoned

The obvious Bayesian predicate — `residual_scale == 0.0` — is wrong in **both
directions**, and only running it showed why:

- With one evidence id per increment and reporting noise of 0.2, the residual
  scale is **exactly 0.0**. Noise does not clear it. It is *repetition*, not
  noise, that makes a residual informative, so the predicate would have fired for
  entirely the wrong reason.
- The noiseless asymmetric fit lands at **1.89 × 10⁻¹³**, not zero, so an equality
  test misses it outright.

The shipped predicate is therefore structural and integer —
`observations <= len(llr_by_evidence)` — with a float epsilon only as a fallback.

Similarly, `reversion_rate == 0.0` is a real sentinel in `fit_ornstein_uhlenbeck`
but is **unreachable from any seeded simulator**; it is kept as its own code, and
the reachable failure is the `< 0` plus off-path level pair above.

## Accessibility

The repo commits at `agents/06_BRAND_WEB.md` to "WCAG-oriented keyboard,
screen-reader, contrast, reduced-motion, form, chart, and status semantics." The
existing replay viewer predates that in practice: it has zero ARIA attributes, no
landmarks, no skip link, no table captions, no `scope` on any header, and scroll
containers a keyboard user cannot reach. This viewer closes each of those rather
than copying them.

| | |
|---|---|
| Landmarks | `<header>`, `<nav aria-label>`, `<main id="main" tabindex="-1">`, `<footer>` |
| Skip link | first focusable element, moved off-screen rather than hidden, so it stays in the tab order |
| Chart | `role="img"` with `aria-labelledby` pointing at a real `<title>` and `<desc>`; `focusable="false"` |
| Tables | every one captioned, every `<th>` scoped, row headers included |
| Scroll regions | `tabindex="0" role="region"` named by their caption; focus ring inset so it is not clipped |
| Not colour alone | path solid, even-odds rule dashed 6/5, jump rules dashed 2/4, and every flagged increment also listed by index |
| Motion | the only media query is `prefers-reduced-motion: no-preference`; nothing animates by default |

**No text inside the SVG.** A label sized for a 720-unit viewBox is illegible once
it scales to a 320px screen, so every label lives in the HTML around the figure —
which is simultaneously the small-screen fix and the screen-reader fix.

The chart's `<desc>` ends by promising that the same numbers appear in the tables
below it. A test asserts the promise holds.

## The four states

- **Clean** — chart, landmarks, sampled steps, one panel per estimator, evidence, reproduction, provenance.
- **Degraded** — the same, plus four redundant markers: a derived boolean, a chip carrying the literal word, a prose callout naming each diagnostic, and per-panel and per-row classes. A flagged value is still shown; hiding it would be its own dishonesty.
- **Empty** — the index renders and explains itself. Reachable only through `--empty-state`; a misspelled `--only` raises and exits 1, so the empty state can never be arrived at by accident and read as "there was nothing to show."
- **Error** — the trajectory could not be recorded at all. The refusal is verbatim, and there is no chart, no table and no substitute number.

A fit-level refusal is **degraded**, not error: plottable but unfittable is a
distinct shape, and `walk-fitted-as-reverting` shows all four panel states —
recovered, diagnosed, diagnosed, refused — from a single trajectory.

## The fixtures

| name | state |
|---|---|
| `diffusion` | clean |
| `ornstein-uhlenbeck` | clean |
| `jump-diffusion` | clean — the plain diffusion fit is shown alongside, because ignoring the jumps nearly doubles the volatility it reports (0.970 against 0.511) |
| `bayesian-repeated-evidence` | clean |
| `bayesian-one-shot-evidence` | degraded — the same subject with evidence never repeated |
| `walk-fitted-as-reverting` | degraded — the headline: the `diffusion` path, asked three more questions |
| `saturated-belief` | error — the simulator refusing, which cannot be a committed fixture because there is no artifact, only a refusal |

## Limitations and non-claims

- **Nothing here is evidence about belief.** Every path is synthetic and every page says so. This is an instrument, not a study.
- Diagnostics are a fixed registry, not an inference procedure. They cannot tell you a model is wrong for the data; they tell you a specific output is not identified by it.
- The drift standard error is reported as a row and never compared to the drift. Comparing them would be an inferential threshold, and G3 has not been passed.
- The jump panel's detection threshold is explicitly labelled approximate: it uses the fitted diffusive volatility, because the estimator's internal robust scale is not exposed on the fit and recomputing it here would duplicate logic that could drift.
- `MAX_POLYLINE_POINTS` is a safety valve no shipped fixture reaches — the longest path is 401 points. It is covered by a library test rather than a page, and should not be removed as dead code.
- Accessibility is asserted structurally (landmarks present, headers scoped, captions present, no colour-only encoding). **No assistive technology was used to test it, and no audit was performed.**
- The viewer renders trajectories only. The CFI-005 recovery report still renders as terminal text; unifying them was out of scope.

## Related work

- `research/cfi/src/drl_cfi/viewer.py` — the renderer and the diagnostic registry.
- `scripts/build_belief_site.py` — the build command.
- `docs/10-research/CFI_BELIEF_RECOVERY_2026-08-25.md` (DRL-RES-011) — the study whose measured limits the panels cite.
- `docs/10-research/failures/EVAL-0001-SUBSTRING-GRADERS-MISCLASSIFY-SAFETY.md` — the same class of instrument defect in the evaluation harness.
- `COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md` §2.1, §4, §12.
