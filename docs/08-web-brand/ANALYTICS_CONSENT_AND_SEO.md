---
document_id: DRL-WEB-014
title: "Analytics, Consent, Search, and Social Metadata"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Analytics, Consent, Search, and Social Metadata

## Analytics

Track privacy-conscious product events:

- page/tour/demo starts and completion;
- command palette usage category;
- install/repository/citation clicks;
- live versus replay use;
- error and cold-start experience;
- contribution funnel.

Do not send conversation text, tool arguments, local paths, source excerpts, or private identifiers to product analytics.

## Consent

Essential session/security data is explained separately from optional analytics and trace donation. Settings are accessible after first choice.

## SEO and social

- descriptive titles and abstracts;
- canonical URLs;
- structured metadata for articles/software/datasets where appropriate;
- sitemap by public status;
- social cards using real project visual/evidence;
- robots exclusions for draft/private areas;
- no keyword stuffing or inflated claims.

## Cross-host Wix and application policy

The Wix site and DRL application subdomains must present compatible consent categories and privacy explanations. Wix traffic analytics, product analytics, application operational telemetry, Atticus evaluation traces, and donated research traces are distinct data purposes. Consent to one does not imply consent to another.

`www.dwit-labs.com` is the canonical institutional origin. External applications own canonical URLs on their subdomains. Duplicate long-form technical content is summarized on Wix and points to the repository-backed canonical version. Staging, preview, administrative, private trace, and internal evaluation routes are excluded from indexing.
