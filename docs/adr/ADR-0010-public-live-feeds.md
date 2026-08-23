---
document_id: DRL-ADR-0010
title: "ADR-0010: Opt-in official public data feeds"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---


# ADR-0010: Opt-in official public data feeds

## Context

Atlas and FedLens currently serve synthetic fixtures. That is correct for CI
and for the default `atticus-demo`. The Director asked for a true pipeline:
changing variables from public feeds (FRED, market yields, Fed communications).

Yahoo Finance was requested. Yahoo's terms of use do not permit unofficial
bulk retrieval or redistribution. Atlas invariants forbid unlicensed
redistribution. Official public APIs exist for the same research questions.

This ADR does **not** select Atticus Core or Edge (**DIR-004**). It does **not**
replace BalanceLab's synthetic bank. It does **not** make live fetches the
default path.

## Decision

1. Keep fixtures as the default and the only CI path.
2. Add an opt-in ingest pipeline that fetches **official** public sources,
   writes a local store with provenance, then lets Atlas/FedLens read the
   store. Ingest and analysis are separate steps. Atticus does not scrape
   the open web during a task.
3. Approved first sources:
   - FRED (St. Louis Fed API) for CPI year-over-year and Treasury constant
     maturity yields, when the operator supplies `FRED_API_KEY`;
   - U.S. Treasury Daily Par Yield Curve (no key) as a yield fallback;
   - Federal Reserve monetary-policy press RSS (U.S. government work).
4. Reject Yahoo Finance and any unofficial market scrape as a DRL source.
5. Host allowlist only. API keys never enter the repository or default logs.
6. Live mode is labeled. Evidence citations are source URLs, not `fixture://`.
7. Until the Director accepts this ADR, the live path is an isolated
   experiment behind `ATTICUS_LIVE_DATA=1` and `scripts/refresh_public_feeds.py`.

## Alternatives considered

- **Yahoo Finance / yfinance.** Rejected: terms and redistribution risk.
- **Always-on live fetches inside Atticus tools.** Rejected: makes CI and
  replay nondeterministic; mixes ingest failure with planning failure.
- **Replace fixtures.** Rejected: the integrated demo and EvalForge gold
  path must stay network-free.

## Consequences

### Positive

- Operator can watch CPI, 2Y, 10Y, and Fed language change across refreshes.
- Rights are recorded in `configs/public-feed-sources.yaml`.
- Default demo remains reproducible.

### Negative

- FRED requires a free operator-owned API key.
- RSS descriptions are short; they are not a full FOMC transcript archive.
- Live `as_of` must be today, not the fixture pin `2026-07-24`.

## Security and privacy

Bounded egress to an allowlisted set of official hosts. No credential in git.
Refresh records store series values and public document text already published
by the source; they do not store prompts.

## Compatibility and migration

No schema change to TaskResult. Fixture tools keep working. Live mode fails
closed if the store is missing.

## Approval

- Proposed by: Cursor cloud agent (Director-requested live feeds)
- Date: 2026-08-23
- Approved by the Director: pending
- Status: IN REVIEW
