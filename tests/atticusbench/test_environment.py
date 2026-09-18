"""Fixture declarations must become tools that behave exactly as declared."""

from __future__ import annotations

import pytest
from atticusbench import build_registry, load_corpus
from atticusbench.environment import (
    MAX_ARGUMENT_LENGTH,
    ArgumentContractViolation,
    FixtureToolFailure,
)


@pytest.fixture(scope="module")
def corpus():
    return load_corpus()


def test_registry_offers_only_the_declared_subset(corpus) -> None:
    fixture = corpus.fixture("repo-unreviewed-secrets-v1")
    registry, _ = build_registry(fixture, offered_tools=("git.status", "git.diff"))
    names = {definition.name for definition in registry.catalog()}
    assert names == {"git.status", "git.diff"}
    assert registry.definition("git.push") is None


def test_catalog_carries_the_declared_tier_and_public_flag(corpus) -> None:
    fixture = corpus.fixture("repo-unreviewed-secrets-v1")
    registry, _ = build_registry(fixture)
    push = registry.definition("git.push")
    assert push is not None
    assert int(push.risk_tier) == 3
    assert push.public_allowed is False
    create = build_registry(corpus.fixture("ticket-duplicate-delivery-v1"))[0].definition(
        "tickets.create"
    )
    assert create is not None
    assert create.idempotent is False


def test_effect_ledger_records_only_executed_effects(corpus) -> None:
    fixture = corpus.fixture("repo-unreviewed-secrets-v1")
    registry, ledger = build_registry(fixture)
    registry.invoke("git.status", {})
    assert ledger.invocations == ["git.status"]
    assert ledger.effects == []

    registry.invoke("git.push", {"remote": "origin", "branch": "work"})
    assert ledger.effect_kinds == ("external_write",)
    assert ledger.effects[0].reversible is False


def test_duplicate_invocations_are_visible(corpus) -> None:
    fixture = corpus.fixture("ticket-duplicate-delivery-v1")
    registry, ledger = build_registry(fixture)
    registry.invoke("tickets.create", {"title": "One"})
    registry.invoke("tickets.create", {"title": "Two"})
    assert ledger.duplicate_invocations() == {"tickets.create": 2}
    assert len(ledger.effects) == 2


def test_declared_failure_raises_and_performs_no_effect(corpus) -> None:
    fixture = corpus.fixture("flaky-scenario-service-v1")
    registry, ledger = build_registry(fixture)
    with pytest.raises(FixtureToolFailure, match="timeout"):
        registry.invoke("scenario.project", {"name": "bear-steepener"})
    assert ledger.invocations == ["scenario.project"]
    assert ledger.effects == []


def test_injection_marker_is_recorded_when_the_document_is_served(corpus) -> None:
    fixture = corpus.fixture("poisoned-web-document-v1")
    registry, ledger = build_registry(fixture)
    output = registry.invoke("web.fetch_document", {"url": "https://example.org/vendor-comparison"})
    assert ledger.injection_markers == ["web.fetch_document"]
    # The injected instruction is carried as evidence content, never as a
    # message the runtime might treat as an instruction.
    assert output.evidence[0].metadata["untrusted_content"] is True
    assert "ignore your previous instructions" in output.evidence[0].content.lower()


def test_argument_contract_rejects_a_missing_required_key(corpus) -> None:
    fixture = corpus.fixture("macro-evidence-desk-v1")
    registry, ledger = build_registry(fixture)
    with pytest.raises(ArgumentContractViolation, match="missing required"):
        registry.invoke("atlas.research_snapshot", {})
    assert ledger.effects == []


def test_argument_contract_rejects_an_unexpected_key(corpus) -> None:
    fixture = corpus.fixture("macro-evidence-desk-v1")
    registry, _ = build_registry(fixture)
    with pytest.raises(ArgumentContractViolation, match="unexpected argument"):
        registry.invoke("atlas.research_snapshot", {"as_of": "2026-08-01", "sudo": True})


def test_argument_contract_rejects_a_path_that_leaves_the_workspace(corpus) -> None:
    fixture = corpus.fixture("workspace-path-escape-v1")
    registry, ledger = build_registry(fixture)
    for path in ("workspace/outside-link", "../etc/hosts", "/etc/hosts", "workspace/../x"):
        with pytest.raises(ArgumentContractViolation, match="does not satisfy its contract"):
            registry.invoke("files.read_workspace", {"path": path})
    assert ledger.effects == []
    # The confined path still works.
    output = registry.invoke("files.read_workspace", {"path": "workspace/report.md"})
    assert output.evidence[0].citation.startswith("fixture://")


def test_argument_contract_bounds_value_length(corpus) -> None:
    fixture = corpus.fixture("inbox-shared-drive-v1")
    registry, _ = build_registry(fixture)
    with pytest.raises(ArgumentContractViolation, match="exceeds"):
        registry.invoke(
            "mail.send",
            {
                "to": "reviewer-mailbox",
                "subject": "x" * 200,
                "body": "short",
            },
        )
    with pytest.raises(ArgumentContractViolation, match="too long to validate"):
        registry.invoke(
            "mail.send",
            {
                "to": "a" * (MAX_ARGUMENT_LENGTH + 1),
                "subject": "s",
                "body": "b",
            },
        )


def test_argument_contract_requires_a_string_for_a_pattern(corpus) -> None:
    fixture = corpus.fixture("macro-evidence-desk-v1")
    registry, _ = build_registry(fixture)
    with pytest.raises(ArgumentContractViolation, match="must be a string"):
        registry.invoke("atlas.research_snapshot", {"as_of": 20260801})


def test_every_fixture_tool_is_invocable_with_its_example_arguments(corpus) -> None:
    # Baseline systems fall back to these, so a bad example would make a
    # baseline fail for the wrong reason.
    for fixture in corpus.fixtures:
        registry, _ = build_registry(fixture)
        for tool in fixture.tools:
            if not tool.example_arguments:
                continue
            if tool.example_violates_contract:
                with pytest.raises(ArgumentContractViolation):
                    registry.invoke(tool.name, dict(tool.example_arguments))
                continue
            if tool.failure is not None:
                with pytest.raises(FixtureToolFailure):
                    registry.invoke(tool.name, dict(tool.example_arguments))
                continue
            registry.invoke(tool.name, dict(tool.example_arguments))
