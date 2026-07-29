"""Deterministic Fed language comparison over fixture documents."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .citations import CitedComparison, PassageCitation

_HAWKISH = frozenset({"elevated", "persistent", "restrictive", "inflation", "vigilant"})
_DOVISH = frozenset({"slowing", "balanced", "easing", "softening", "patient"})


@dataclass(frozen=True, slots=True)
class FedDocument:
    document_id: str
    title: str
    published_date: date
    text: str
    citation: str


@dataclass(frozen=True, slots=True)
class LanguageComparison:
    previous_id: str
    current_id: str
    added_terms: tuple[str, ...]
    removed_terms: tuple[str, ...]
    tone_delta: int
    interpretation: str


def _terms(text: str) -> set[str]:
    return {token.strip(".,;:!?()[]").lower() for token in text.split()}


def _tone(text: str) -> int:
    terms = _terms(text)
    return len(terms & _HAWKISH) - len(terms & _DOVISH)


class FedLensService:
    """Preserve document identity while comparing policy language."""

    def __init__(self, documents: list[FedDocument] | None = None) -> None:
        self._documents = documents or self.fixture_documents()

    @classmethod
    def from_bounded_corpus(cls, root: Path | None = None) -> FedLensService:
        from .corpus import load_fed_corpus

        corpus = load_fed_corpus(root)
        return cls([item.document for item in corpus.documents])

    @staticmethod
    def fixture_documents() -> list[FedDocument]:
        return [
            FedDocument(
                "FOMC-2026-05-FIXTURE",
                "Earlier synthetic FOMC communication",
                date(2026, 5, 6),
                "Inflation remains elevated. The Committee will remain vigilant and restrictive.",
                "fixture://fedlens/FOMC-2026-05",
            ),
            FedDocument(
                "FOMC-2026-06-FIXTURE",
                "Latest synthetic FOMC communication",
                date(2026, 6, 17),
                (
                    "Inflation remains elevated, while activity is slowing. "
                    "Risks appear more balanced."
                ),
                "fixture://fedlens/FOMC-2026-06",
            ),
        ]

    def documents_as_of(self, *, as_of: date) -> list[FedDocument]:
        return sorted(
            (item for item in self._documents if item.published_date <= as_of),
            key=lambda item: item.published_date,
        )

    def latest(self, *, as_of: date) -> FedDocument:
        documents = self.documents_as_of(as_of=as_of)
        if not documents:
            raise LookupError(f"No Fed communication was public by {as_of.isoformat()}")
        return documents[-1]

    def compare_latest(self, *, as_of: date) -> LanguageComparison:
        documents = self.documents_as_of(as_of=as_of)
        if len(documents) < 2:
            raise LookupError("At least two documents are required for language comparison")
        previous, current = documents[-2:]
        previous_terms = _terms(previous.text)
        current_terms = _terms(current.text)
        delta = _tone(current.text) - _tone(previous.text)
        if delta > 0:
            interpretation = "Language became more hawkish in the deterministic lexicon."
        elif delta < 0:
            interpretation = "Language became less hawkish in the deterministic lexicon."
        else:
            interpretation = "The deterministic lexicon found no net tone change."
        return LanguageComparison(
            previous.document_id,
            current.document_id,
            tuple(sorted(current_terms - previous_terms)),
            tuple(sorted(previous_terms - current_terms)),
            delta,
            interpretation,
        )

    def compare_latest_cited(self, *, as_of: date) -> CitedComparison:
        from .citations import CitedComparison, cited_compare

        documents = self.documents_as_of(as_of=as_of)
        if len(documents) < 2:
            raise LookupError("At least two documents are required for language comparison")
        result = cited_compare(documents[-2], documents[-1])
        if not isinstance(result, CitedComparison):
            raise TypeError("cited_compare must return CitedComparison")
        return result

    def search(self, query: str, *, as_of: date, limit: int = 20) -> list[PassageCitation]:
        from .citations import search_passages

        return search_passages(self.documents_as_of(as_of=as_of), query, limit=limit)
