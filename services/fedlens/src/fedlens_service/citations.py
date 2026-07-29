"""Passage-level citations and deterministic document diffs (DRL-016)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .service import FedDocument, LanguageComparison

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True, slots=True)
class PassageCitation:
    """One exact span citation into a Fed document."""

    document_id: str
    start: int
    end: int
    text: str
    citation: str

    def matches_source(self, document: FedDocument) -> bool:
        return (
            self.document_id == document.document_id
            and document.text[self.start : self.end] == self.text
        )


@dataclass(frozen=True, slots=True)
class CitedComparison:
    """Language comparison plus passage-level added/removed citations."""

    comparison: LanguageComparison
    added_passages: tuple[PassageCitation, ...]
    removed_passages: tuple[PassageCitation, ...]


def split_sentences(text: str) -> list[tuple[int, int, str]]:
    """Return (start, end, sentence) spans with exact offsets into ``text``."""

    spans: list[tuple[int, int, str]] = []
    cursor = 0
    parts = _SENTENCE_SPLIT.split(text.strip())
    for part in parts:
        if not part:
            continue
        start = text.find(part, cursor)
        if start < 0:
            start = cursor
        end = start + len(part)
        spans.append((start, end, part))
        cursor = end
    return spans


def cited_compare(previous: FedDocument, current: FedDocument) -> CitedComparison:
    prev_spans = {(span[2].strip().lower()): span for span in split_sentences(previous.text)}
    curr_spans = {(span[2].strip().lower()): span for span in split_sentences(current.text)}
    added_keys = sorted(set(curr_spans) - set(prev_spans))
    removed_keys = sorted(set(prev_spans) - set(curr_spans))

    added = tuple(
        PassageCitation(
            document_id=current.document_id,
            start=curr_spans[key][0],
            end=curr_spans[key][1],
            text=curr_spans[key][2],
            citation=f"{current.citation}#p{curr_spans[key][0]}-{curr_spans[key][1]}",
        )
        for key in added_keys
    )
    removed = tuple(
        PassageCitation(
            document_id=previous.document_id,
            start=prev_spans[key][0],
            end=prev_spans[key][1],
            text=prev_spans[key][2],
            citation=f"{previous.citation}#p{prev_spans[key][0]}-{prev_spans[key][1]}",
        )
        for key in removed_keys
    )

    # Preserve existing lexicon comparison semantics for Atticus continuity.
    from .service import FedLensService

    # Build a temporary service view over exactly these two docs.
    service = FedLensService([previous, current])
    comparison = service.compare_latest(as_of=current.published_date)
    return CitedComparison(comparison=comparison, added_passages=added, removed_passages=removed)


def search_passages(
    documents: list[FedDocument],
    query: str,
    *,
    limit: int = 20,
) -> list[PassageCitation]:
    """Deterministic case-insensitive substring search with passage citations."""

    needle = query.strip().lower()
    if not needle:
        raise ValueError("query cannot be empty")
    if limit <= 0 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    hits: list[PassageCitation] = []
    for document in documents:
        lower = document.text.lower()
        start = 0
        while True:
            index = lower.find(needle, start)
            if index < 0:
                break
            end = index + len(needle)
            # Expand to enclosing sentence when possible.
            sentence = next(
                (
                    span
                    for span in split_sentences(document.text)
                    if span[0] <= index < span[1]
                ),
                (index, end, document.text[index:end]),
            )
            hits.append(
                PassageCitation(
                    document_id=document.document_id,
                    start=sentence[0],
                    end=sentence[1],
                    text=sentence[2],
                    citation=f"{document.citation}#p{sentence[0]}-{sentence[1]}",
                )
            )
            if len(hits) >= limit:
                return hits
            start = end
    return hits
