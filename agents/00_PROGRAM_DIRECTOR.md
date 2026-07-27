---
document_id: DRL-AGT-000
title: "Agent Mission 00: Program Director and Execution Planner"
version: 3.0.0
status: APPROVED EXECUTION MISSION
owner: DeWitt
last_updated: 2026-07-26
---


    # Agent Mission 00: Program Director and Execution Planner

    ## Mission objective

    Convert the foundation into a dependency-ordered GitHub program: milestones, issues, labels, owners, requirement links, release evidence, and an ADR approval queue. Establish a truthful current-state baseline without implementing product code.

    This mission is executed on a dedicated feature branch and ends in a reviewable pull request. It is not permission to reinterpret the laboratory. The agent must read the root `LABORATORY_BIBLE.md`, `AGENTS.md`, decision register, current `WORKLOG.md`, and all prerequisites below before changing files.

    ## Entry prerequisites

    - Foundation validation passes.
- All controlled documents are present and indexed.
- DeWitt is available to approve major ADRs.

    If a prerequisite is absent, stale, contradictory, or unapproved, stop and create a blocker in the handoff ledger. Do not fill an architectural gap with an undocumented personal preference.

    ## Owned paths

    - docs/00-program/**
- docs/11-operations/**
- agents/**
- .github/ISSUE_TEMPLATE/**
- .github/PULL_REQUEST_TEMPLATE.md
- ROADMAP.md
- WORKLOG.md

    Ownership means primary modification responsibility for this mission. Small necessary changes outside these paths require explicit notation in the worklog; changes to another project's public contract require its owner mission or an ADR.

    ## Forbidden or protected paths

    - Do not modify `LABORATORY_BIBLE.md` except through an approved constitutional ADR.
- Do not commit credentials, private files, employer material, unlicensed corpora, model weights without release policy, or generated secrets.
- Do not weaken security, privacy, evaluation, accessibility, or open-weight requirements to make a demo pass.
- Do not mark a feature or metric complete without evidence.
- Do not choose upstream models, cloud topology changes, or public product scope unilaterally.
- Do not begin implementation work owned by later missions.

    ## Required work packages

    ### WP-00-01: Audit all requirements and create a machine-readable requirement/work-package register.
### WP-00-02: Build a directed dependency graph and critical path with entry/exit gates.
### WP-00-03: Create GitHub milestone, label, issue, and PR templates with requirement/evidence fields.
### WP-00-04: Create initial issue backlog and assign each issue to exactly one mission and one evidence owner.
### WP-00-05: Identify unresolved director decisions and prepare ADR proposals without deciding them.
### WP-00-06: Define release dashboard and weekly program review format.

    Each work package must produce implementation or controlled-document changes, tests or validation evidence, and a worklog entry. Create focused commits after each coherent package.

    ## ADR and director approval triggers

    - Any change to V1 scope or coordinated launch.
- Any new service/package/repository boundary.
- Any reordering that bypasses security, protocol, or evaluation prerequisites.
- Any removal of evidence required by V1 criteria.

    For each trigger, write the ADR first, mark it `PROPOSED`, identify alternatives and consequences, and wait for DeWitt's approval before implementation. The agent may prepare a nonbinding spike in an isolated path if the ADR explicitly allows it.

    ## Verification matrix

    - Run the deep-foundation validator.
- Check every V1 criterion maps to a work package and evidence artifact.
- Check dependency graph has no unexplained cycles.
- Validate issue templates and structured registers parse.
- Review backlog for duplicate or ownerless work.

    Record exact commands, environment, revision, outcomes, skipped checks, and artifact locations. “Tests passed” without commands and evidence is insufficient.

    ## Pull-request deliverables

    - Program backlog and milestone plan.
- Requirement-to-work-package-to-evidence traceability.
- Prioritized ADR queue.
- Updated agent execution plan.
- Program risks, assumptions, and critical-path report.

    The PR description maps each deliverable to requirement IDs and acceptance criteria, names every changed public contract, provides screenshots/reports where relevant, lists risks and limitations, and includes rollback/migration behavior.

    ## Handoff requirements

    - Name the first implementation-ready mission and its exact issue set.
- List all ADRs needing DeWitt approval.
- Provide repository state and validation commands.
- Record any ambiguous or contradictory requirements.

    The next agent must be able to start without reconstructing unstated reasoning. The handoff identifies what is complete, what remains, what failed, decisions/ADRs, changed paths, test commands, produced artifacts, known debt, security/privacy effects, and exact recommended next issue.

    ## Stop conditions

    - Foundation validation fails.
- A constitutional contradiction cannot be resolved without DeWitt.
- A critical requirement has no owner or evidence path.

    ## Definition of mission complete

    - all work packages are complete or explicitly deferred by approved decision;
    - owned documents and contracts are internally consistent;
    - required tests and evidence pass;
    - no critical TODO, placeholder, fake metric, unreviewed license, or silent security weakening remains;
    - feature branch is pushed and a focused PR is opened;
    - `WORKLOG.md` and the sequential handoff ledger are updated;
    - the next mission has a precise, executable starting point.
