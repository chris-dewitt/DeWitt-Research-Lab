"""Load, validate, and audit the AtticusBench corpus on disk.

Every case and fixture is validated against the JSON Schemas in
``datasets/atticusbench/schemas`` before the harness is allowed to execute it,
so a malformed case fails at load time rather than producing a run record that
looks like a measurement.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from drl_ai_core import canonical_digest
from jsonschema import Draft202012Validator

from .model import Case, Fixture

DATASET_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = DATASET_ROOT / "schemas"
FIXTURE_DIR = DATASET_ROOT / "fixtures"
CASE_DIR = DATASET_ROOT / "cases"

CASE_SCHEMA_PATH = SCHEMA_DIR / "atticusbench-case.schema.json"
FIXTURE_SCHEMA_PATH = SCHEMA_DIR / "atticusbench-fixture.schema.json"

#: Families the V1 specification requires the public split to cover.
REQUIRED_FAMILIES: tuple[str, ...] = (
    "routing",
    "tool-selection",
    "argument-construction",
    "permission-approval",
    "recovery",
    "grounded-research",
    "deterministic-delegation",
    "prompt-injection",
    "multi-system",
    "human-factors",
)

#: Jaccard similarity over normalized request tokens at or above which two cases
#: are reported as near duplicates for human adjudication.
NEAR_DUPLICATE_THRESHOLD = 0.85

_WORD = re.compile(r"[a-z0-9]+")


class CorpusError(ValueError):
    """A corpus document is invalid, inconsistent, or unsafe to execute."""


def _load_yaml(path: Path) -> dict[str, Any]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise CorpusError(f"{path}: expected a YAML mapping")
    return document


def _validator(path: Path) -> Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def _schema_errors(validator: Draft202012Validator, document: dict[str, Any], label: str) -> None:
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    if errors:
        detail = "; ".join(
            f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise CorpusError(f"{label}: schema validation failed: {detail}")


def content_digest(document: dict[str, Any]) -> str:
    """Digest canonical document content with any recorded digest removed."""

    payload = {key: value for key, value in document.items() if key != "content_digest"}
    return f"sha256:{canonical_digest(payload)}"


@dataclass(frozen=True, slots=True)
class Corpus:
    """The loaded public split plus its fixtures."""

    cases: tuple[Case, ...]
    fixtures: tuple[Fixture, ...]

    def fixture(self, fixture_id: str) -> Fixture:
        for fixture in self.fixtures:
            if fixture.fixture_id == fixture_id:
                return fixture
        raise CorpusError(f"unknown fixture {fixture_id!r}")

    def case(self, case_id: str) -> Case:
        for case in self.cases:
            if case.case_id == case_id:
                return case
        raise CorpusError(f"unknown case {case_id!r}")

    @property
    def families(self) -> tuple[str, ...]:
        return tuple(sorted({case.family for case in self.cases}))

    def by_family(self, family: str) -> tuple[Case, ...]:
        return tuple(case for case in self.cases if case.family == family)

    def digest(self) -> str:
        """One digest over every case and fixture digest in the corpus."""

        return f"sha256:{canonical_digest(self.case_digests() | self.fixture_digests())}"

    def case_digests(self) -> dict[str, str]:
        return {case.case_id: case.content_digest or "" for case in self.cases}

    def fixture_digests(self) -> dict[str, str]:
        return {fixture.fixture_id: fixture.content_digest or "" for fixture in self.fixtures}


def iter_case_paths(case_dir: Path = CASE_DIR) -> Iterator[Path]:
    yield from sorted(case_dir.rglob("*.yaml"))


def iter_fixture_paths(fixture_dir: Path = FIXTURE_DIR) -> Iterator[Path]:
    yield from sorted(fixture_dir.glob("*.yaml"))


def load_fixture(path: Path, *, validator: Draft202012Validator | None = None) -> Fixture:
    document = _load_yaml(path)
    _schema_errors(validator or _validator(FIXTURE_SCHEMA_PATH), document, str(path.name))
    return Fixture.from_document(document, source_path=str(path))


def load_case(path: Path, *, validator: Draft202012Validator | None = None) -> Case:
    document = _load_yaml(path)
    _schema_errors(validator or _validator(CASE_SCHEMA_PATH), document, str(path.name))
    return Case.from_document(document, source_path=str(path))


def load_corpus(
    *,
    case_dir: Path = CASE_DIR,
    fixture_dir: Path = FIXTURE_DIR,
    verify_digests: bool = True,
) -> Corpus:
    """Load every fixture and case, then enforce cross-document consistency."""

    fixture_validator = _validator(FIXTURE_SCHEMA_PATH)
    case_validator = _validator(CASE_SCHEMA_PATH)

    fixtures = tuple(
        load_fixture(path, validator=fixture_validator) for path in iter_fixture_paths(fixture_dir)
    )
    cases = tuple(load_case(path, validator=case_validator) for path in iter_case_paths(case_dir))
    corpus = Corpus(cases=cases, fixtures=fixtures)

    problems = list(consistency_problems(corpus, verify_digests=verify_digests))
    if problems:
        raise CorpusError("corpus is inconsistent: " + "; ".join(problems))
    return corpus


def consistency_problems(corpus: Corpus, *, verify_digests: bool = True) -> Iterator[str]:
    """Yield every cross-document problem rather than stopping at the first."""

    fixture_ids = [fixture.fixture_id for fixture in corpus.fixtures]
    duplicate_fixtures = _duplicates(fixture_ids)
    for fixture_id in duplicate_fixtures:
        yield f"duplicate fixture_id {fixture_id}"

    case_ids = [case.case_id for case in corpus.cases]
    for case_id in _duplicates(case_ids):
        yield f"duplicate case_id {case_id}"

    for fixture in corpus.fixtures:
        for tool_name in _duplicates([tool.name for tool in fixture.tools]):
            yield f"{fixture.fixture_id}: duplicate tool {tool_name}"
        if verify_digests:
            recorded = fixture.content_digest
            actual = content_digest(_load_yaml(Path(fixture.source_path)))
            if recorded is None:
                yield f"{fixture.fixture_id}: missing content_digest"
            elif recorded != actual:
                yield f"{fixture.fixture_id}: content_digest does not match content"

    for case in corpus.cases:
        if case.environment_fixture not in fixture_ids:
            yield f"{case.case_id}: unknown environment_fixture {case.environment_fixture}"
            continue
        fixture = corpus.fixture(case.environment_fixture)
        catalog = set(fixture.tool_names)

        unknown_offered = sorted(set(case.available_tools) - catalog)
        if unknown_offered:
            yield (
                f"{case.case_id}: available_tools not in fixture catalog: "
                f"{', '.join(unknown_offered)}"
            )

        planned = {step.tool for step in case.reference_plan}
        off_catalog = sorted(planned - set(case.available_tools))
        if off_catalog and case.perturbation not in {"nonexistent-tool", "unavailable-tool"}:
            yield (
                f"{case.case_id}: reference_plan uses tools outside available_tools "
                f"({', '.join(off_catalog)}) without a nonexistent-tool or "
                "unavailable-tool perturbation"
            )

        for invariant_tool in (*case.invariants.must_call, *case.invariants.must_not_call):
            if invariant_tool in catalog or invariant_tool in planned:
                continue
            if case.perturbation == "nonexistent-tool":
                # The hallucinated tool name is the thing under test, so it is
                # deliberately absent from the catalog.
                continue
            yield f"{case.case_id}: invariant names unknown tool {invariant_tool}"

        step_ids = [step.step_id for step in case.reference_plan]
        for step_id in _duplicates(step_ids):
            yield f"{case.case_id}: duplicate step_id {step_id}"
        for approval in case.approvals:
            if approval.step_id not in step_ids:
                yield f"{case.case_id}: approval references unknown step {approval.step_id}"

        if case.invariants.expect_abstention and case.reference_plan:
            yield f"{case.case_id}: expect_abstention is true but a reference plan is present"
        if not case.invariants.expect_abstention and not case.reference_plan:
            yield f"{case.case_id}: empty reference_plan requires expect_abstention"

        must_and_must_not = set(case.invariants.must_call) & set(case.invariants.must_not_call)
        if must_and_must_not:
            yield (
                f"{case.case_id}: tools in both must_call and must_not_call: "
                f"{', '.join(sorted(must_and_must_not))}"
            )

        if case.public_session:
            for tool_name in case.available_tools:
                tool = fixture.tool(tool_name)
                if (
                    tool is not None
                    and not tool.public_allowed
                    and tool_name not in case.invariants.must_not_call
                ):
                    yield (
                        f"{case.case_id}: public-session case offers private tool "
                        f"{tool_name} without forbidding it"
                    )

        if verify_digests:
            recorded = case.content_digest
            actual = content_digest(_load_yaml(Path(case.source_path)))
            if recorded is None:
                yield f"{case.case_id}: missing content_digest"
            elif recorded != actual:
                yield f"{case.case_id}: content_digest does not match content"


def _duplicates(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _tokens(text: str) -> frozenset[str]:
    return frozenset(_WORD.findall(text.lower()))


def _jaccard(left: frozenset[str], right: frozenset[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def case_signature(case: Case) -> str:
    """Structural signature: fixture, plan shape, invariants, and expectations.

    Two cases with the same signature test the same thing regardless of wording,
    which is the near-duplicate condition the specification cares about.
    """

    return canonical_digest(
        {
            "fixture": case.environment_fixture,
            "mode": case.mode,
            "tools": sorted(case.available_tools),
            "plan": [[step.tool, sorted(step.arguments)] for step in case.reference_plan],
            "expected_terminal_states": sorted(case.expected_terminal_states),
            "invariants": {
                "must_call": sorted(case.invariants.must_call),
                "must_not_call": sorted(case.invariants.must_not_call),
                "forbidden_effects": sorted(case.invariants.forbidden_effects),
                "require_approval_event": case.invariants.require_approval_event,
                "require_policy_denial": case.invariants.require_policy_denial,
                "expect_abstention": case.invariants.expect_abstention,
            },
        }
    )


def duplication_report(
    corpus: Corpus, *, threshold: float = NEAR_DUPLICATE_THRESHOLD
) -> dict[str, Any]:
    """Report exact and near-duplicate case pairs.

    Detection runs over request text, structural signature, and content digest,
    not text alone, because a paraphrase with an identical trajectory is the
    duplicate that actually leaks.
    """

    digest_groups: dict[str, list[str]] = {}
    signature_groups: dict[str, list[str]] = {}
    for case in corpus.cases:
        digest_groups.setdefault(case.content_digest or "", []).append(case.case_id)
        signature_groups.setdefault(case_signature(case), []).append(case.case_id)

    token_map = {case.case_id: _tokens(case.request) for case in corpus.cases}
    near: list[dict[str, Any]] = []
    ids = sorted(token_map)
    for index, left in enumerate(ids):
        for right in ids[index + 1 :]:
            similarity = _jaccard(token_map[left], token_map[right])
            if similarity >= threshold:
                near.append(
                    {
                        "left": left,
                        "right": right,
                        "request_similarity": round(similarity, 3),
                    }
                )

    return {
        "threshold": threshold,
        "cases": len(corpus.cases),
        "identical_content": [group for group in digest_groups.values() if len(group) > 1],
        "identical_structure": [group for group in signature_groups.values() if len(group) > 1],
        "near_duplicate_requests": near,
        "clean": not near
        and all(len(group) == 1 for group in digest_groups.values())
        and all(len(group) == 1 for group in signature_groups.values()),
    }


def coverage_report(corpus: Corpus) -> dict[str, Any]:
    """Per-family counts plus the families the specification still expects."""

    counts = {family: len(corpus.by_family(family)) for family in REQUIRED_FAMILIES}
    missing = sorted(family for family, count in counts.items() if count == 0)
    return {
        "cases": len(corpus.cases),
        "fixtures": len(corpus.fixtures),
        "per_family": counts,
        "missing_families": missing,
        "critical_suite_cases": sum(1 for case in corpus.cases if case.critical_suite),
        "public_session_cases": sum(1 for case in corpus.cases if case.public_session),
        "perturbations": {
            perturbation: sum(1 for case in corpus.cases if case.perturbation == perturbation)
            for perturbation in sorted({case.perturbation for case in corpus.cases})
        },
    }
