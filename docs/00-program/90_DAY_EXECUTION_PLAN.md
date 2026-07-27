---
document_id: DRL-PRG-090
title: "First 90-Day Repository Execution Plan"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-27
---

# First 90-Day Repository Execution Plan

## Outcome

At day 90, DRL should have a public institutional Wix site, a healthy
repository, a deployed authenticated development Atticus service, an evaluated
local integrated workflow, a first model bake-off report, and a credible public
roadmap. The program must remain achievable for one founder working in bounded
sessions.

## Operating rhythm

- One active implementation issue at a time unless tasks are genuinely independent.
- One weekly Director review of `DIRECTORS_MEMO.md`, costs, risks, and scope.
- One small demonstration every two weeks.
- Every merged feature includes tests, documentation, and a handoff.
- No production credentials or employer-confidential material enter Git.
- Every public claim links to evidence or carries a planned/prototype label.

## Milestone 1 — Repository online and trusted (Days 1–14)

### Week 1

- Create the GitHub repository and upload this foundation.
- Protect `main`; create `integration/v1`.
- Enable Actions, Dependabot, secret scanning, and branch rules.
- Resolve repository slug and security-contact items in the Director's Memo.
- Run the full validation suite in GitHub Actions.
- Convert the seed backlog into GitHub issues and milestones.

### Week 2

- Execute the integrated Atticus demo from a clean clone.
- Harden protocol, policy, approval, and state-machine tests.
- Add release artifacts for test and validation evidence.
- Publish the first architecture overview and contributor quickstart.
- Record the first genuine Failure Museum entry from setup or CI.

### Exit evidence

- Clean-clone setup and demo succeed.
- Required checks block unsafe merges.
- Director's Memo and issue workflow are active.
- No unresolved critical secret, license, or repository-governance finding.

## Milestone 2 — Atticus local alpha (Days 15–35)

### Week 3

- Add a typed provider interface and mock open-weight endpoint.
- Add structured-output validation and bounded repair.
- Expand legal state-transition and cancellation coverage.
- Create an EvalForge policy and trajectory suite.

### Week 4

- Add local runner capability discovery.
- Add approved-root repository inspection and safe command profiles.
- Add patch proposals bound to exact approvals.
- Test traversal, symlink, replay, expiry, redaction, and malicious input.

### Week 5

- Prototype local voice input/output behind explicit activation.
- Add private/public mode separation and local audit export.
- Run the first Atticus Core/Edge candidate bake-off on a small public suite.
- Publish results, limitations, hardware, and cost.

### Exit evidence

- A private local task can inspect a fixture repository and propose—but not
  silently apply—a patch.
- Policy and approval denial paths pass.
- At least two Core and two Edge candidates have reproducible baseline results.

## Milestone 3 — Specialists and integrated research alpha (Days 36–63)

### Week 6

- Replace Atlas fixtures with one public source adapter and point-in-time cache.
- Preserve observation, publication, ingestion, and effective dates.
- Add source licensing and failure behavior.

### Week 7

- Ingest a bounded public Fed corpus into FedLens.
- Implement document identity, versioning, diff, passage citation, and search.
- Add event-study notebook scaffolding without making causal claims.

### Week 8

- Expand BalanceLab's synthetic institution and deterministic tests.
- Add parallel, steepener, flattener, and basis scenarios.
- Publish hand-verifiable fixtures and calculation lineage.

### Week 9

- Run the complete integrated workflow with real public evidence and synthetic
  calculations.
- Submit the same trace to EvalForge.
- Publish a signed replay plus a failure/degraded-mode replay.

### Exit evidence

- Atlas and FedLens return source-linked point-in-time public evidence.
- BalanceLab calculations pass invariant and regression tests.
- Atticus produces a cited report whose narrative matches calculations.

## Milestone 4 — Public laboratory preview (Days 64–90)

### Week 10

- Build the Wix institutional pages and cream-on-black design system.
- Publish mission, systems, research, open source, teaching, About, and honest
  maturity/status pages.
- Connect `www.dwit-labs.com` and test redirects, TLS, accessibility, and SEO.

### Week 11

- Create a budget-capped GCP development project.
- Build and privately deploy the Atticus container to Cloud Run.
- Add workload identity, content-minimized logs, alerts, and rollback.
- Run an Azure Container Apps portability experiment only if time and budget
  allow; it is not on the V1 critical path.

### Week 12

- Add authentication and strict development quotas.
- Connect the Wix launch surface to the separate Atticus application.
- Test CORS, CSP, cookie scope, fallbacks, cold starts, and degraded service.

### Week 13

- Conduct accessibility, security, privacy, license, and claim reviews.
- Publish the first working paper or technical report.
- Publish the public roadmap, contribution routes, and Failure Museum.
- Hold the 90-day Director review and decide the next release train.

### Exit evidence

- Wix is live at the canonical domain with accurate status labels.
- Development Atticus deployment is authenticated, budget-capped, observable,
  and reversible.
- Public artifacts include code, documentation, evaluation, limitations, and
  a reproduction path.

## Day-90 non-goals

- Claiming V1.0 before the full release matrix passes.
- Training a foundation model from scratch.
- Public arbitrary shell or private-runner access.
- Real bank or employer data.
- Always-on GPU infrastructure.
- Production multi-cloud.
- A fictional staff page or inflated institutional history.

## Director dashboard

Track weekly:

- merged issues and escaped defects;
- test and validator status;
- unresolved Director decisions;
- actual cloud and model-compute spend;
- public artifacts and reproductions;
- security/privacy findings;
- setup time from a clean clone;
- integrated workflow success rate;
- claims lacking evidence;
- next single dependency-unblocking issue.
