# GitHub issue seed backlog

**Executable bodies:** `.github/ISSUE_BODIES/DRL-*.md`  
**Machine register:** `requirements/issue-register.yaml`  
**First sprint order:** `docs/00-program/FIRST_SPRINT_PLAN.md`  
**Labels:** `.github/labels.yml`

Create these issues in order and attach them to the matching milestone. Do not
copy an issue into GitHub until its owner, dependency, and acceptance evidence
are still accurate. Prefer the full body files over this summary table.

| ID | Milestone | Labels | Issue | Acceptance evidence |
|---|---|---|---|---|
| DRL-001 | M1 | program, governance | Initialize repository and protected branches | remote recorded; `main` and `integration/v1` rules captured |
| DRL-002 | M1 | ci, security | Enable Actions and repository security features | required CI, dependency updates, secret/code scanning settings |
| DRL-003 | M1 | docs, governance | Activate Director's Memo review | PR template and weekly review cadence confirmed |
| DRL-004 | M1 | developer-experience | Prove clean-clone bootstrap and demo | timed transcript from supported Windows and Linux environments |
| DRL-005 | M1 | protocol, test | Expand protocol and state-machine contract tests | success, denial, invalid input, cancellation, and terminal-state coverage |
| DRL-006 | M1 | research, failure-museum | Publish first real failure record | failure, detection, correction, regression test, issue/commit links |
| DRL-007 | M2 | atticus, model | Implement typed open-weight provider interface | mock provider, identity disclosure, timeout, error, and fallback tests |
| DRL-008 | M2 | atticus, security | Implement structured-output validation and bounded repair | malformed output, repair budget, injection, and trace tests |
| DRL-009 | M2 | local-runner, security | Add approved-root repository inspection | traversal, symlink, size, binary, and redaction tests |
| DRL-010 | M2 | local-runner, approvals | Add patch proposal and local approval flow | exact digest, expiry, changed-workspace, atomic apply, audit evidence |
| DRL-011 | M2 | evalforge, security | Build permission and trajectory evaluation suite | held-out allow/deny/approval/injection report |
| DRL-012 | M2 | model, research | Run first Atticus Core and Edge bake-off | candidates, licenses, hardware, cost, latency, quality, limitations |
| DRL-013 | M2 | voice, privacy | Prototype explicitly activated local voice | visible capture, local-default processing, deletion, offline behavior |
| DRL-014 | M3 | atlas, data | Add first point-in-time public Atlas adapter | source terms, temporal fields, cache, validation, failure fixture |
| DRL-015 | M3 | fedlens, data | Ingest bounded public Fed corpus | checksums, document identity, provenance, license/source register |
| DRL-016 | M3 | fedlens, nlp | Implement cited document comparison and search | passage-level citations and deterministic diff regression tests |
| DRL-017 | M3 | balancelab, quant | Expand synthetic bank and scenario engine | hand calculations, invariants, boundaries, lineage, regression fixtures |
| DRL-018 | M3 | integration, atticus | Run evidence-to-scenario integrated workflow | one trace linking Atlas, FedLens, BalanceLab, report, and evaluation |
| DRL-019 | M3 | evalforge, release | Publish signed success and degraded replays | reproducible replay manifests and evaluation reports |
| DRL-020 | M3 | documentation, teaching | Publish integrated workflow teaching guide | clean notebook/guide with exercises and no private data |
| DRL-021 | M4 | wix, design | Build canonical Wix institutional pages | page map, copy, mobile captures, truthful status, fallback links |
| DRL-022 | M4 | domain, security | Connect and verify `dwit-labs.com` | DNS, apex redirect, TLS, CORS/CSP/cookie and rollback report |
| DRL-023 | M4 | gcp, infra | Create budget-capped GCP development topology | Director-approved project, budget, identities, deletion and cost plan |
| DRL-024 | M4 | gcp, atticus | Deploy authenticated Atticus prototype to Cloud Run | health, auth, scale-to-zero, max instances, logs, rollback, cost |
| DRL-025 | M4 | azure, portability | Validate optional Azure Container Apps profile | Bicep validation; optional private dev smoke and teardown report |
| DRL-026 | M4 | accessibility, web | Complete accessibility and reduced-motion review | keyboard, screen reader, contrast, zoom, phone, error-state report |
| DRL-027 | M4 | security, privacy | Complete public-preview threat and privacy review | findings, mitigations, retention, kill switch, no critical open issue |
| DRL-028 | M4 | research, publication | Publish first DRL technical report | methods, code, data rights, limitations, citation, reproduction |
| DRL-029 | M4 | open-source, community | Publish contributor routes and good-first issues | tested setup, contribution map, ownership and recognition |
| DRL-030 | M4 | program, director-review | Conduct day-90 evidence review | accepted evidence matrix and next release-train decision |

## Required issue body

Every created issue must include:

- user or research value;
- controlling requirement and document;
- dependencies;
- owned paths;
- acceptance criteria;
- security, privacy, licensing, and cost effect;
- test/evidence commands;
- rollback or reversibility;
- Director decision needed, if any.
