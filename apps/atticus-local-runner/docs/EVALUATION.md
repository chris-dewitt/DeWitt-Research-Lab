---
document_id: DRL-LOC-102
title: "Atticus Local Runner Evaluation and Acceptance Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atticus Local Runner Evaluation and Acceptance Specification

    ## Evaluation contract

    Evaluations test actual product/research claims. Each claim has population, threat model, metric, uncertainty treatment, slices, failure examples, owner, and release threshold. A single aggregate score is never sufficient.

    ## Claims

    - Pairing, authentication, rotation, and revocation are correct.
- Tools stay within scope and return correct results.
- Approvals bind the exact consequence.
- Sandbox and resource limits resist hostile input.
- Offline and privacy promises hold.
- Voice and local-model interaction remains usable.

    ## Required suites

    - Protocol conformance, replay, expiry, rotation, and revocation.
- Filesystem path, junction, symlink, and property/fuzz tests.
- Sandbox process, network, output, and escape tests.
- Repository golden workflows.
- Approval binding, race, and comprehension.
- Plugin signature and permission tests.
- Offline packet capture and retention tests.
- Windows install, update, rollback, and uninstall matrix.

    ## Metrics and analysis

    - Unauthorized effect and scope-escape count.
- Correct tool result and task completion.
- Approval comprehension and error rate.
- Pairing and revocation latency.
- Sandbox containment.
- Unexpected offline egress.
- Local p50/p95 latency and voice response.
- CPU, RAM, disk, and model memory.

    Paired tests or bootstrap intervals are used where appropriate. Repeated tuning against a benchmark is tracked. Human and model judges include calibration, disagreement, and limitations; model-judge output is not objective truth.

    ## Release gates

    - Zero critical scope escape, unsigned execution, approval bypass, unexpected offline egress, or secret leak.
- Golden file, write, and repository workflows pass.
- Revocation prevents new work within the defined bound.
- Reference Windows install/update/rollback/uninstall passes.
- Voice accessibility and privacy controls pass.

    A noncritical regression needs a time-bounded exception with user value, affected slices, mitigation, owner, expiry, and director approval. Security/privacy boundary and deterministic-correctness failures cannot be averaged away.

    ## Adversarial program

    - Symlink, junction, UNC, and traversal.
- Shell metacharacters and encoding.
- Child processes and output flooding.
- Malicious repository hooks and credential prompts.
- Forged cloud and replay.
- Approval overlay/spoof and stale preview.
- Plugin/update tampering.
- Microphone retention and hidden fallback.

    ## Required evidence

    - Threat-model test report.
- Protocol conformance report.
- Sandbox and fuzz results.
- Packet capture/privacy report.
- Install matrix.
- Approval usability findings.
- Signed local workflow and platform limitations.

    Reports pin code, data, model/provider, prompt/template, tool, configuration, environment, sample counts, exclusions, costs, failures, and reproduction commands. Public metrics link to signed reports.
