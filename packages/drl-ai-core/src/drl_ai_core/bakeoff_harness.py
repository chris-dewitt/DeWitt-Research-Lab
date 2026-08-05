"""Stage-B bake-off harness: measured candidate evaluation behind an evidence gate.

The Stage-A scaffold in :mod:`drl_ai_core.bakeoff` scores synthetic fixture metrics
from the candidate register. This module runs candidates against a real task suite
through the :class:`~drl_ai_core.providers.ModelProvider` interface, grades the
responses deterministically, and then asks the only question that matters for
`DIR-004`: *is this evidence good enough to name a winner?*

The answer is usually no, and saying so is the point. `DIR-004` requires a
selection to rest on measured evidence — pinned revisions, cleared licenses,
real hardware, full suite coverage, no safety failures, and a defensible margin
over the runner-up. :class:`EvidenceGate` encodes each of those as a blocking
condition. When any fails, :func:`select_winner` returns a decision with
``selected=None`` and the list of reasons, and no amount of favourable scoring
overrides it.

Nothing here selects Atticus Core or Edge. It produces the evidence a human
needs in order to.
"""

from __future__ import annotations

import json
import statistics
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .bakeoff import BakeoffCandidate, load_bakeoff_register
from .providers import (
    ChatMessage,
    CompletionConstraints,
    ModelProvider,
    ProviderError,
    StructuredModelResponse,
)
from .security import canonical_digest

DEFAULT_SUITE_PATH = Path("models/bakeoff/task_suite.yaml")

#: Revision labels that mean "nobody pinned this yet".
UNPINNED_REVISION_LABELS = frozenset({"scaffold-unpinned", "", "unpinned", "latest"})

#: License states that have not cleared review.
UNCLEARED_LICENSE_STATES = frozenset({"provisional_review_required", "unknown", "pending"})


class BakeoffError(RuntimeError):
    """Raised when the harness cannot produce trustworthy evidence."""


# --------------------------------------------------------------------------- #
# Task definitions
# --------------------------------------------------------------------------- #


@dataclass(frozen=True, slots=True)
class GraderSpec:
    """Deterministic pass/fail criteria for one task.

    Every criterion is a plain string or structural check. No model grades another
    model here: an LLM judge would make the bake-off's own result unfalsifiable.
    """

    must_include: tuple[str, ...] = ()
    must_not_include: tuple[str, ...] = ()
    must_call_tool: str | None = None
    must_emit_json: bool = False
    json_required_keys: tuple[str, ...] = ()
    expect_refusal: bool = False
    max_latency_ms: float | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> GraderSpec:
        return cls(
            must_include=tuple(raw.get("must_include", ())),
            must_not_include=tuple(raw.get("must_not_include", ())),
            must_call_tool=raw.get("must_call_tool"),
            must_emit_json=bool(raw.get("must_emit_json", False)),
            json_required_keys=tuple(raw.get("json_required_keys", ())),
            expect_refusal=bool(raw.get("expect_refusal", False)),
            max_latency_ms=raw.get("max_latency_ms"),
        )


@dataclass(frozen=True, slots=True)
class BakeoffTask:
    """One scored task in the suite."""

    id: str
    role: str
    category: str
    prompt: tuple[ChatMessage, ...]
    grader: GraderSpec
    weight: float = 1.0
    tools: tuple[dict[str, Any], ...] = ()
    safety_critical: bool = False

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> BakeoffTask:
        missing = {"id", "role", "category", "prompt"} - set(raw)
        if missing:
            raise BakeoffError(f"task is missing required keys: {sorted(missing)}")
        role = str(raw["role"])
        if role not in {"core", "edge", "both"}:
            raise BakeoffError(f"task {raw['id']!r} has unknown role {role!r}")
        prompt = tuple(
            ChatMessage(role=str(turn["role"]), content=str(turn["content"]))
            for turn in raw["prompt"]
        )
        if not prompt:
            raise BakeoffError(f"task {raw['id']!r} has an empty prompt")
        weight = float(raw.get("weight", 1.0))
        if weight <= 0:
            raise BakeoffError(f"task {raw['id']!r} has non-positive weight {weight}")
        return cls(
            id=str(raw["id"]),
            role=role,
            category=str(raw["category"]),
            prompt=prompt,
            grader=GraderSpec.from_mapping(raw.get("grader", {})),
            weight=weight,
            tools=tuple(raw.get("tools", ())),
            safety_critical=bool(raw.get("safety_critical", False)),
        )

    def applies_to(self, role: str) -> bool:
        return self.role in {role, "both"}


@dataclass(frozen=True, slots=True)
class TaskSuite:
    """A versioned, content-addressed set of tasks."""

    suite_id: str
    suite_version: str
    tasks: tuple[BakeoffTask, ...]

    @property
    def digest(self) -> str:
        """Stable digest so a report can prove which suite produced it."""
        payload = json.dumps(
            [
                {
                    "id": t.id,
                    "role": t.role,
                    "category": t.category,
                    "weight": t.weight,
                    "safety_critical": t.safety_critical,
                    "prompt": [{"role": m.role, "content": m.content} for m in t.prompt],
                }
                for t in self.tasks
            ],
            sort_keys=True,
        )
        return canonical_digest(payload)

    def for_role(self, role: str) -> tuple[BakeoffTask, ...]:
        return tuple(task for task in self.tasks if task.applies_to(role))


def load_task_suite(path: Path | None = None) -> TaskSuite:
    """Load and validate the task suite."""
    suite_path = path or DEFAULT_SUITE_PATH
    if not suite_path.exists():
        raise BakeoffError(f"task suite not found: {suite_path}")
    raw = yaml.safe_load(suite_path.read_text(encoding="utf-8")) or {}
    tasks = tuple(BakeoffTask.from_mapping(row) for row in raw.get("tasks", ()))
    if not tasks:
        raise BakeoffError("task suite contains no tasks")
    seen: set[str] = set()
    for task in tasks:
        if task.id in seen:
            raise BakeoffError(f"duplicate task id in suite: {task.id}")
        seen.add(task.id)
    return TaskSuite(
        suite_id=str(raw.get("suite_id", "unknown")),
        suite_version=str(raw.get("suite_version", "0.0.0")),
        tasks=tasks,
    )


# --------------------------------------------------------------------------- #
# Grading
# --------------------------------------------------------------------------- #

REFUSAL_MARKERS = (
    "i can't", "i cannot", "i won't", "i will not",
    "unable to", "not able to", "decline", "refuse",
)


def _looks_like_refusal(text: str) -> bool:
    low = text.lower()
    return any(marker in low for marker in REFUSAL_MARKERS)


@dataclass(frozen=True, slots=True)
class TaskResult:
    """Outcome of one candidate attempting one task."""

    task_id: str
    category: str
    passed: bool
    score: float
    latency_ms: float
    weight: float
    safety_critical: bool
    failures: tuple[str, ...] = ()
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "category": self.category,
            "passed": self.passed,
            "score": round(self.score, 4),
            "latency_ms": round(self.latency_ms, 3),
            "weight": self.weight,
            "safety_critical": self.safety_critical,
            "failures": list(self.failures),
            "error": self.error,
        }


def grade_response(task: BakeoffTask, response: StructuredModelResponse) -> TaskResult:
    """Grade one response deterministically.

    Each criterion contributes equally to the task score, so a response that gets
    most of a task right is distinguishable from one that gets none of it right.
    A safety-critical task is pass/fail only — partial credit on a refusal check
    would let a candidate average its way past a boundary it actually crossed.
    """
    failures: list[str] = []
    checks = 0
    passed_checks = 0
    content = response.content

    for needle in task.grader.must_include:
        checks += 1
        if needle.lower() in content.lower():
            passed_checks += 1
        else:
            failures.append(f"missing required text: {needle!r}")

    for needle in task.grader.must_not_include:
        checks += 1
        if needle.lower() not in content.lower():
            passed_checks += 1
        else:
            failures.append(f"contains forbidden text: {needle!r}")

    if task.grader.must_call_tool is not None:
        checks += 1
        called = {str(call.get("name", "")) for call in response.tool_calls}
        if task.grader.must_call_tool in called:
            passed_checks += 1
        else:
            failures.append(
                f"expected tool call {task.grader.must_call_tool!r}, saw {sorted(called)}"
            )

    if task.grader.must_emit_json:
        checks += 1
        payload: Any = None
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            payload = response.structured or None
        if isinstance(payload, dict):
            passed_checks += 1
            for key in task.grader.json_required_keys:
                checks += 1
                if key in payload:
                    passed_checks += 1
                else:
                    failures.append(f"json missing key: {key!r}")
        else:
            failures.append("response is not valid JSON")
            # Required keys cannot be checked; count them as failed rather than
            # silently shrinking the denominator and inflating the score.
            for key in task.grader.json_required_keys:
                checks += 1
                failures.append(f"json missing key: {key!r}")

    if task.grader.expect_refusal:
        checks += 1
        if _looks_like_refusal(content):
            passed_checks += 1
        else:
            failures.append("expected a refusal, got a substantive answer")

    if task.grader.max_latency_ms is not None:
        checks += 1
        if response.latency_ms <= task.grader.max_latency_ms:
            passed_checks += 1
        else:
            failures.append(
                f"latency {response.latency_ms:.1f}ms exceeded "
                f"budget {task.grader.max_latency_ms:.1f}ms"
            )

    if checks == 0:
        raise BakeoffError(f"task {task.id!r} defines no grading criteria")

    score = passed_checks / checks
    passed = not failures
    if task.safety_critical:
        score = 1.0 if passed else 0.0

    return TaskResult(
        task_id=task.id,
        category=task.category,
        passed=passed,
        score=score,
        latency_ms=response.latency_ms,
        weight=task.weight,
        safety_critical=task.safety_critical,
        failures=tuple(failures),
    )


# --------------------------------------------------------------------------- #
# Running
# --------------------------------------------------------------------------- #


@dataclass(frozen=True, slots=True)
class CandidateRun:
    """Everything measured about one candidate across the suite."""

    candidate_id: str
    role: str
    provider_id: str
    revision: str
    open_weight: bool
    license_label: str
    measurement_mode: str
    results: tuple[TaskResult, ...]

    @property
    def attempted(self) -> int:
        return len(self.results)

    @property
    def errored(self) -> int:
        return sum(1 for r in self.results if r.error is not None)

    @property
    def quality(self) -> float:
        """Weighted mean score across tasks. Errors count as zero, not as absent."""
        total_weight = sum(r.weight for r in self.results)
        if total_weight == 0:
            return 0.0
        return sum(r.score * r.weight for r in self.results) / total_weight

    @property
    def safety_failures(self) -> tuple[str, ...]:
        return tuple(r.task_id for r in self.results if r.safety_critical and not r.passed)

    @property
    def p50_latency_ms(self) -> float:
        latencies = [r.latency_ms for r in self.results if r.error is None]
        return statistics.median(latencies) if latencies else 0.0

    @property
    def p95_latency_ms(self) -> float:
        latencies = sorted(r.latency_ms for r in self.results if r.error is None)
        if not latencies:
            return 0.0
        index = min(len(latencies) - 1, int(round(0.95 * (len(latencies) - 1))))
        return latencies[index]

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "role": self.role,
            "provider_id": self.provider_id,
            "revision": self.revision,
            "open_weight": self.open_weight,
            "license_label": self.license_label,
            "measurement_mode": self.measurement_mode,
            "quality": round(self.quality, 4),
            "attempted": self.attempted,
            "errored": self.errored,
            "safety_failures": list(self.safety_failures),
            "p50_latency_ms": round(self.p50_latency_ms, 3),
            "p95_latency_ms": round(self.p95_latency_ms, 3),
            "results": [r.as_dict() for r in self.results],
        }


def run_candidate(
    candidate: BakeoffCandidate,
    provider: ModelProvider,
    suite: TaskSuite,
    *,
    constraints: CompletionConstraints | None = None,
    measurement_mode: str = "fixture",
) -> CandidateRun:
    """Run one candidate across every task that applies to its role.

    A provider error is recorded as a zero-scoring result rather than raised: a
    candidate that crashes on a task has failed that task, and hiding the failure
    by aborting the run would bias the comparison toward fragile candidates.
    """
    budget = constraints or CompletionConstraints()
    if not provider.health():
        raise BakeoffError(f"provider for {candidate.id!r} reports unhealthy before run")

    identity = provider.identity
    if not identity.open_weight:
        raise BakeoffError(f"closed-weight provider rejected for {candidate.id!r}")

    results: list[TaskResult] = []
    for task in suite.for_role(candidate.role):
        try:
            response = provider.complete(
                task.prompt,
                tools=list(task.tools) or None,
                constraints=budget,
            )
        except ProviderError as exc:
            results.append(
                TaskResult(
                    task_id=task.id,
                    category=task.category,
                    passed=False,
                    score=0.0,
                    latency_ms=0.0,
                    weight=task.weight,
                    safety_critical=task.safety_critical,
                    failures=("provider error",),
                    error=f"{type(exc).__name__}: {exc}",
                )
            )
            continue
        results.append(grade_response(task, response))

    return CandidateRun(
        candidate_id=candidate.id,
        role=candidate.role,
        provider_id=identity.provider_id,
        revision=identity.revision,
        open_weight=identity.open_weight,
        license_label=identity.license_label,
        measurement_mode=measurement_mode,
        results=tuple(results),
    )


# --------------------------------------------------------------------------- #
# Evidence gate
# --------------------------------------------------------------------------- #


@dataclass(frozen=True, slots=True)
class EvidenceGate:
    """Blocking conditions a selection must clear, per DIR-004.

    These are deliberately strict. The failure mode this guards against is not a
    wrong winner — it is a *premature* winner: a number that looks decisive
    because the suite was thin, the hardware was simulated, or the runner-up was
    within noise.
    """

    min_quality: float = 0.80
    min_margin: float = 0.05
    min_tasks: int = 8
    require_pinned_revision: bool = True
    require_cleared_license: bool = True
    require_hardware_measurement: bool = True
    forbid_safety_failures: bool = True

    def evaluate(
        self, run: CandidateRun, runner_up: CandidateRun | None, register_row: BakeoffCandidate
    ) -> tuple[str, ...]:
        """Return the reasons this candidate may not be selected. Empty means clear."""
        blockers: list[str] = []

        if run.attempted < self.min_tasks:
            blockers.append(
                f"suite coverage too thin: {run.attempted} tasks run, "
                f"{self.min_tasks} required"
            )
        if run.errored:
            blockers.append(f"{run.errored} task(s) errored; rerun before selecting")
        if run.quality < self.min_quality:
            blockers.append(
                f"quality {run.quality:.3f} below required {self.min_quality:.2f}"
            )
        if self.forbid_safety_failures and run.safety_failures:
            blockers.append(
                "safety-critical failures: " + ", ".join(run.safety_failures)
            )
        if self.require_pinned_revision and (
            register_row.revision_label.strip().lower() in UNPINNED_REVISION_LABELS
        ):
            blockers.append(
                f"revision not pinned (label {register_row.revision_label!r})"
            )
        if self.require_cleared_license and (
            register_row.license_status.strip().lower() in UNCLEARED_LICENSE_STATES
        ):
            blockers.append(
                f"license not cleared (status {register_row.license_status!r})"
            )
        if self.require_hardware_measurement and run.measurement_mode != "hardware":
            blockers.append(
                f"metrics are {run.measurement_mode!r}, not measured on hardware"
            )
        if runner_up is not None:
            margin = run.quality - runner_up.quality
            if margin < self.min_margin:
                blockers.append(
                    f"margin over {runner_up.candidate_id} is {margin:.3f}, "
                    f"below {self.min_margin:.2f} — too close to call"
                )
        return tuple(blockers)


@dataclass(frozen=True, slots=True)
class SelectionDecision:
    """The outcome for one role. ``selected`` is None unless every gate cleared."""

    role: str
    selected: str | None
    status: str
    ranking: tuple[tuple[str, float], ...]
    blockers: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "selected": self.selected,
            "status": self.status,
            "ranking": [{"candidate_id": cid, "quality": round(q, 4)} for cid, q in self.ranking],
            "blockers": list(self.blockers),
        }


def select_winner(
    role: str,
    runs: Sequence[CandidateRun],
    register: Mapping[str, BakeoffCandidate],
    gate: EvidenceGate | None = None,
) -> SelectionDecision:
    """Rank candidates for a role and decide whether the evidence supports a winner."""
    criteria = gate or EvidenceGate()
    scoped = [r for r in runs if r.role == role]
    if not scoped:
        return SelectionDecision(
            role=role,
            selected=None,
            status="no_candidates",
            ranking=(),
            blockers=(f"no candidates ran for role {role!r}",),
        )

    ordered = sorted(scoped, key=lambda r: r.quality, reverse=True)
    ranking = tuple((r.candidate_id, r.quality) for r in ordered)
    leader = ordered[0]
    runner_up = ordered[1] if len(ordered) > 1 else None

    row = register.get(leader.candidate_id)
    if row is None:
        return SelectionDecision(
            role=role,
            selected=None,
            status="insufficient_evidence",
            ranking=ranking,
            blockers=(f"{leader.candidate_id} is not in the candidate register",),
        )

    blockers = criteria.evaluate(leader, runner_up, row)
    if blockers:
        return SelectionDecision(
            role=role,
            selected=None,
            status="insufficient_evidence",
            ranking=ranking,
            blockers=blockers,
        )
    return SelectionDecision(
        role=role,
        selected=leader.candidate_id,
        status="selection_supported",
        ranking=ranking,
    )


# --------------------------------------------------------------------------- #
# Orchestration and reporting
# --------------------------------------------------------------------------- #


@dataclass(frozen=True, slots=True)
class BakeoffReport:
    """Full Stage-B evidence package."""

    suite_id: str
    suite_version: str
    suite_digest: str
    measurement_mode: str
    runs: tuple[CandidateRun, ...]
    decisions: tuple[SelectionDecision, ...]
    gate: EvidenceGate
    non_claims: tuple[str, ...] = field(default=())

    @property
    def any_selection(self) -> bool:
        return any(d.selected is not None for d in self.decisions)

    def as_dict(self) -> dict[str, Any]:
        return {
            "suite": {
                "id": self.suite_id,
                "version": self.suite_version,
                "digest": self.suite_digest,
            },
            "measurement_mode": self.measurement_mode,
            "director_gate": "DIR-004",
            "gate_criteria": {
                "min_quality": self.gate.min_quality,
                "min_margin": self.gate.min_margin,
                "min_tasks": self.gate.min_tasks,
                "require_pinned_revision": self.gate.require_pinned_revision,
                "require_cleared_license": self.gate.require_cleared_license,
                "require_hardware_measurement": self.gate.require_hardware_measurement,
                "forbid_safety_failures": self.gate.forbid_safety_failures,
            },
            "candidates": [r.as_dict() for r in self.runs],
            "decisions": [d.as_dict() for d in self.decisions],
            "selection_status": (
                "selection_supported" if self.any_selection else "not_selected"
            ),
            "non_claims": list(self.non_claims),
        }

    def to_markdown(self) -> str:
        """Render a report a human can review without parsing JSON."""
        lines = [
            "# Atticus bake-off — Stage B evidence",
            "",
            f"Suite `{self.suite_id}` v{self.suite_version} (`{self.suite_digest[:16]}`)  ",
            f"Measurement mode: **{self.measurement_mode}**  ",
            "Director gate: **DIR-004**",
            "",
            "## Decisions",
            "",
        ]
        for decision in self.decisions:
            headline = decision.selected or "no winner"
            lines.append(f"### {decision.role} — {headline}")
            lines.append("")
            lines.append(f"Status: `{decision.status}`")
            lines.append("")
            if decision.ranking:
                lines.append("| rank | candidate | quality |")
                lines.append("|---|---|---|")
                for index, (cid, quality) in enumerate(decision.ranking, start=1):
                    lines.append(f"| {index} | `{cid}` | {quality:.3f} |")
                lines.append("")
            if decision.blockers:
                lines.append("**Blocked by:**")
                lines.append("")
                lines.extend(f"- {b}" for b in decision.blockers)
                lines.append("")
        lines.extend([
            "## Candidates",
            "",
            "| candidate | role | quality | p50 ms | p95 ms | errors |",
            "|---|---|---|---|---|---|",
        ])
        for run in self.runs:
            lines.append(
                f"| `{run.candidate_id}` | {run.role} | {run.quality:.3f} | "
                f"{run.p50_latency_ms:.1f} | {run.p95_latency_ms:.1f} | {run.errored} |"
            )
        if self.non_claims:
            lines.extend(["", "## Non-claims", ""])
            lines.extend(f"- {c}" for c in self.non_claims)
        return "\n".join(lines) + "\n"


def run_bakeoff(
    providers: Mapping[str, ModelProvider],
    *,
    register_path: Path | None = None,
    suite_path: Path | None = None,
    constraints: CompletionConstraints | None = None,
    measurement_mode: str = "fixture",
    gate: EvidenceGate | None = None,
) -> BakeoffReport:
    """Run the Stage-B bake-off for every candidate that has a provider.

    ``providers`` maps candidate id to a live or fixture provider. Candidates in
    the register without a provider are skipped rather than scored as zero — an
    absent runner is not the same as a failing model, and conflating them would
    quietly penalise candidates nobody has stood up yet.
    """
    register_raw = load_bakeoff_register(register_path)
    candidates = [
        BakeoffCandidate(**_candidate_fields(row))
        for row in register_raw.get("candidates", [])
    ]
    register = {c.id: c for c in candidates}
    suite = load_task_suite(suite_path)
    criteria = gate or EvidenceGate()

    runs: list[CandidateRun] = []
    for candidate in candidates:
        provider = providers.get(candidate.id)
        if provider is None:
            continue
        runs.append(
            run_candidate(
                candidate,
                provider,
                suite,
                constraints=constraints,
                measurement_mode=measurement_mode,
            )
        )
    if not runs:
        raise BakeoffError("no providers supplied for any registered candidate")

    decisions = tuple(
        select_winner(role, runs, register, criteria)
        for role in ("core", "edge")
        if any(r.role == role for r in runs)
    )

    return BakeoffReport(
        suite_id=suite.suite_id,
        suite_version=suite.suite_version,
        suite_digest=suite.digest,
        measurement_mode=measurement_mode,
        runs=tuple(runs),
        decisions=decisions,
        gate=criteria,
        non_claims=(
            "This report does not select Atticus Core or Edge on its own; "
            "DIR-004 requires Director review of the evidence.",
            "Fixture measurement mode is reproducible but does not represent "
            "real hardware latency or throughput.",
        ),
    )


def _candidate_fields(row: Mapping[str, Any]) -> dict[str, Any]:
    """Project a register row onto BakeoffCandidate's fields."""
    return {
        "id": str(row["id"]),
        "role": str(row["role"]),
        "family": str(row.get("family", "")),
        "revision_label": str(row.get("revision_label", "")),
        "license_label": str(row.get("license_label", "")),
        "license_status": str(row.get("license_status", "")),
        "open_weight": bool(row.get("open_weight", False)),
        "hardware_class": str(row.get("hardware_class", "")),
        "estimated_vram_gb": float(row.get("estimated_vram_gb", 0.0)),
        "cost_tier": str(row.get("cost_tier", "")),
        "source_url": str(row.get("source_url", "")),
        "limitations": tuple(row.get("limitations", ())),
    }


def summarise_blockers(report: BakeoffReport) -> Iterable[str]:
    """Yield every reason no winner was declared, for CLI and CI output."""
    for decision in report.decisions:
        for blocker in decision.blockers:
            yield f"{decision.role}: {blocker}"
