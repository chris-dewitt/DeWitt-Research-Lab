"""Deterministic FedLens passage citations and diff regressions (DRL-016)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from fedlens_service import FedLensService, cited_compare, write_checksums_into_manifest


ROOT = Path(__file__).resolve().parents[1] / "services" / "fedlens" / "corpus"


def test_passage_citations_match_source_text() -> None:
    write_checksums_into_manifest(ROOT)
    service = FedLensService.from_bounded_corpus(ROOT)
    docs = service.documents_as_of(as_of=date(2026, 7, 24))
    cited = cited_compare(docs[0], docs[1])
    assert cited.added_passages or cited.removed_passages
    for passage in (*cited.added_passages, *cited.removed_passages):
        source = next(doc for doc in docs if doc.document_id == passage.document_id)
        assert passage.matches_source(source)
        assert source.text[passage.start : passage.end] == passage.text


def test_cited_compare_regression_snapshot() -> None:
    write_checksums_into_manifest(ROOT)
    service = FedLensService.from_bounded_corpus(ROOT)
    cited = service.compare_latest_cited(as_of=date(2026, 7, 24))
    assert cited.comparison.previous_id == "FOMC-2026-05-FIXTURE"
    assert cited.comparison.current_id == "FOMC-2026-06-FIXTURE"
    assert cited.comparison.tone_delta < 0
    added_text = " ".join(item.text for item in cited.added_passages).lower()
    assert "balanced" in added_text or "slowing" in added_text


def test_search_returns_passage_citations() -> None:
    write_checksums_into_manifest(ROOT)
    service = FedLensService.from_bounded_corpus(ROOT)
    hits = service.search("restrictive", as_of=date(2026, 7, 24))
    assert hits
    assert all("restrictive" in hit.text.lower() for hit in hits)
    docs = {doc.document_id: doc for doc in service.documents_as_of(as_of=date(2026, 7, 24))}
    for hit in hits:
        assert hit.matches_source(docs[hit.document_id])
