---
document_id: DRL-ATL-106
title: "Atlas Security and Privacy Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atlas Security and Privacy Specification

    ## Objective

    Atlas must stay useful under hostile, malformed, ambiguous, and failure-prone inputs without giving a model authority it does not possess. Models propose. Deterministic systems authenticate, authorize, validate, constrain, execute, audit, and obtain human approval.

    ## Protected assets

    - Source credentials and quotas.
- Rights decisions and corpora.
- Historical time semantics.
- Research snapshots and public credibility.
- User query privacy.

    ## Principal threats

    - Untrusted document instructions.
- SSRF from source URLs.
- Malicious files and parser vulnerabilities.
- Data poisoning.
- Cross-rights leakage.
- Future-data leakage.
- Source credential theft.
- Inference over private query logs.

    ## Required controls

    - Approved source allowlists and connector-specific egress.
- Sandboxed parsing and file type/size checks.
- Checksums, quarantine, and immutable raw objects.
- Rights-aware access and index filters.
- Temporal eligibility enforced in query planning.
- Deterministic unit/calculation validation.
- Workload identity and Secret Manager.

    ## Privacy behavior

    - Public research sources only in the public corpus.
- Queries are separated and minimized.
- No advertising profile.
- Trace donation is opt-in.
- Public snapshots are reviewed for accidental user/query content.

    ## Public abuse controls

    - Query and compute quotas.
- Bounded dates, sources, and result sizes.
- No arbitrary public URL fetch.
- Cached popular demos.
- Authentication for heavy jobs.

    ## Verification

    - Connector fuzz and contract tests.
- Temporal mutation tests.
- Rights/access tests.
- Parser sandbox tests.
- Source poisoning exercises.
- Session isolation tests.
- Incident drill for compromised source or token.

    “Sanitize input,” “encrypt it,” and “use least privilege” are not evidence. Each control identifies the boundary, exact mechanism, negative test, telemetry signal, owner, and incident response.
