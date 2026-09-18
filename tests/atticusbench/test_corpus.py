"""The AtticusBench corpus must be valid before anything is measured against it."""

from __future__ import annotations

import re
from dataclasses import replace
from pathlib import Path

import pytest
import yaml
from atticusbench import (
    CorpusError,
    content_digest,
    coverage_report,
    duplication_report,
    load_case,
    load_corpus,
    load_fixture,
)
from atticusbench.corpus import (
    REQUIRED_FAMILIES,
    case_signature,
    consistency_problems,
    iter_case_paths,
    iter_fixture_paths,
)


@pytest.fixture(scope="module")
def corpus():
    return load_corpus()


def test_every_case_and_fixture_validates(corpus) -> None:
    assert corpus.cases, "the public split must contain cases"
    assert corpus.fixtures, "the corpus must ship its environment fixtures"
    assert not list(consistency_problems(corpus))


def test_every_required_family_is_covered(corpus) -> None:
    coverage = coverage_report(corpus)
    assert coverage["missing_families"] == []
    for family in REQUIRED_FAMILIES:
        assert coverage["per_family"][family] >= 3, family


def test_corpus_is_free_of_duplicates(corpus) -> None:
    report = duplication_report(corpus)
    assert report["identical_content"] == []
    assert report["identical_structure"] == []
    assert report["near_duplicate_requests"] == []
    assert report["clean"] is True


def test_case_ids_and_digests_are_unique(corpus) -> None:
    case_ids = [case.case_id for case in corpus.cases]
    digests = [case.content_digest for case in corpus.cases]
    signatures = [case_signature(case) for case in corpus.cases]
    assert len(set(case_ids)) == len(case_ids)
    assert len(set(digests)) == len(digests)
    assert len(set(signatures)) == len(signatures)


def test_recorded_digests_match_file_content() -> None:
    for path in [*iter_fixture_paths(), *iter_case_paths()]:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert document["content_digest"] == content_digest(document), path.name


def test_split_is_public_only(corpus) -> None:
    # Hidden-test material is access-controlled and must never appear here.
    assert {case.split for case in corpus.cases} == {"public-test"}


def test_critical_suite_covers_the_named_hazards(corpus) -> None:
    critical = [case for case in corpus.cases if case.critical_suite]
    assert len(critical) >= 10
    perturbations = {case.perturbation for case in critical}
    assert {"changed-approval-digest", "expired-approval", "malicious-content"} <= perturbations
    families = {case.family for case in critical}
    assert {"permission-approval", "prompt-injection", "grounded-research"} <= families


def test_public_session_cases_never_silently_offer_private_tools(corpus) -> None:
    for case in corpus.cases:
        if not case.public_session:
            continue
        fixture = corpus.fixture(case.environment_fixture)
        for tool_name in case.available_tools:
            tool = fixture.tool(tool_name)
            assert tool is not None
            if not tool.public_allowed:
                assert tool_name in case.invariants.must_not_call, (case.case_id, tool_name)


def test_every_case_declares_provenance_and_review(corpus) -> None:
    for case in corpus.cases:
        assert case.provenance["rights"] == "synthetic"
        assert case.provenance["review_class"] in {
            "automated-schema-and-invariant",
            "single-human-review",
            "dual-human-review",
        }
        if case.critical_suite:
            # Security and hidden-gate cases require dual review.
            assert case.provenance["review_class"] == "dual-human-review", case.case_id


def test_schema_rejects_an_unknown_field(tmp_path: Path) -> None:
    source = next(iter_case_paths())
    document = yaml.safe_load(source.read_text(encoding="utf-8"))
    document["unexpected_field"] = "no"
    target = tmp_path / "broken.yaml"
    target.write_text(yaml.safe_dump(document), encoding="utf-8")
    with pytest.raises(CorpusError, match="schema validation failed"):
        load_case(target)


def test_schema_rejects_a_malformed_case_id(tmp_path: Path) -> None:
    source = next(iter_case_paths())
    document = yaml.safe_load(source.read_text(encoding="utf-8"))
    document["case_id"] = "not-a-case-id"
    target = tmp_path / "broken.yaml"
    target.write_text(yaml.safe_dump(document), encoding="utf-8")
    with pytest.raises(CorpusError, match="case_id"):
        load_case(target)


def test_consistency_catches_a_tampered_digest(tmp_path: Path, corpus) -> None:
    source = Path(corpus.cases[0].source_path)
    document = yaml.safe_load(source.read_text(encoding="utf-8"))
    document["content_digest"] = "sha256:" + "0" * 64
    target = tmp_path / "tampered.yaml"
    target.write_text(yaml.safe_dump(document), encoding="utf-8")
    tampered = load_case(target)

    from atticusbench import Corpus

    problems = list(consistency_problems(Corpus(cases=(tampered,), fixtures=corpus.fixtures)))
    assert any("content_digest does not match" in problem for problem in problems)


def test_consistency_catches_an_unknown_fixture(corpus) -> None:
    from atticusbench import Corpus

    case = replace(corpus.cases[0], environment_fixture="no-such-fixture")
    problems = list(
        consistency_problems(Corpus(cases=(case,), fixtures=corpus.fixtures), verify_digests=False)
    )
    assert any("unknown environment_fixture" in problem for problem in problems)


def test_fixture_tools_declare_a_tier_and_a_public_flag() -> None:
    for path in iter_fixture_paths():
        fixture = load_fixture(path)
        assert fixture.tools
        for tool in fixture.tools:
            assert tool.risk_tier_name in {
                "explain",
                "read_compute",
                "reversible_change",
                "consequential",
                "prohibited",
            }
            # A tool that writes or sends outside the machine is never below
            # the approval-gated tier. Read-tier tools may still carry a
            # data_egress effect, which is precisely the hazard the
            # cross-session case measures: no approval gate stands behind it,
            # so the planner is the only control.
            if tool.effect is not None and tool.effect.kind in {
                "external_write",
                "external_send",
                "local_write",
                "state_mutation",
            }:
                assert tool.tier >= 2, (fixture.fixture_id, tool.name)


def test_no_fixture_ships_a_credential_shaped_value() -> None:
    # The secret-bearing repository case describes a scanner finding; it must
    # never carry an actual secret-shaped value.
    patterns = (
        r"-----BEGIN",
        r"AKIA[0-9A-Z]{16}",
        r"\bsk-[A-Za-z0-9]{20,}",
        r"\bghp_[A-Za-z0-9]{20,}",
        r"(?i)\bpass(word|phrase)\s*[:=]\s*\S",
        r"(?i)\bapi[_-]?key\s*[:=]\s*\S",
        r"(?i)\b(secret|token)\s*[:=]\s*[A-Za-z0-9+/_-]{12,}",
    )
    for path in [*iter_fixture_paths(), *iter_case_paths()]:
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            assert re.search(pattern, text) is None, (path.name, pattern)
