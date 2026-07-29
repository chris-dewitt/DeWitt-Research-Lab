"""Bounded public Fed corpus loader with checksums and provenance (DRL-015)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from drl_ai_core import canonical_digest

from .service import FedDocument

DEFAULT_CORPUS_ROOT = Path(__file__).resolve().parents[2] / "corpus"


@dataclass(frozen=True, slots=True)
class SourceRegisterEntry:
    source_id: str
    display_name: str
    license_label: str
    terms_url: str
    notes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CorpusDocument:
    document: FedDocument
    checksum: str
    source_id: str
    relative_path: str


@dataclass(frozen=True, slots=True)
class FedCorpus:
    corpus_id: str
    corpus_version: str
    data_tier: str
    license_label: str
    sources: tuple[SourceRegisterEntry, ...]
    documents: tuple[CorpusDocument, ...]


def _sha256_file(path: Path) -> str:
    return f"sha256:{canonical_digest(path.read_text(encoding='utf-8'))}"


def load_fed_corpus(root: Path | None = None) -> FedCorpus:
    corpus_root = root or DEFAULT_CORPUS_ROOT
    manifest_path = corpus_root / "manifest.yaml"
    raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("corpus manifest must be a mapping")
    if raw.get("data_tier") != "public":
        raise ValueError("FedLens bounded corpus must be data_tier=public")

    sources = tuple(
        SourceRegisterEntry(
            source_id=str(row["source_id"]),
            display_name=str(row["display_name"]),
            license_label=str(row["license_label"]),
            terms_url=str(row["terms_url"]),
            notes=tuple(str(item) for item in row.get("notes", [])),
        )
        for row in raw.get("source_register", [])
    )
    source_ids = {entry.source_id for entry in sources}
    if not sources:
        raise ValueError("source_register cannot be empty")

    documents: list[CorpusDocument] = []
    seen_ids: set[str] = set()
    for row in raw.get("documents", []):
        document_id = str(row["document_id"])
        if document_id in seen_ids:
            raise ValueError(f"duplicate document_id {document_id!r}")
        seen_ids.add(document_id)
        source_id = str(row["source_id"])
        if source_id not in source_ids:
            raise ValueError(f"document {document_id!r} references unknown source {source_id!r}")
        relative_path = str(row["relative_path"])
        path = corpus_root / relative_path
        if not path.is_file():
            raise FileNotFoundError(f"missing corpus file: {relative_path}")
        text = path.read_text(encoding="utf-8").strip()
        checksum = _sha256_file(path)
        expected = row.get("checksum")
        if expected and expected != checksum:
            raise ValueError(f"checksum mismatch for {document_id}: {expected} != {checksum}")
        documents.append(
            CorpusDocument(
                document=FedDocument(
                    document_id=document_id,
                    title=str(row["title"]),
                    published_date=date.fromisoformat(str(row["published_date"])),
                    text=text,
                    citation=str(row["citation"]),
                ),
                checksum=checksum,
                source_id=source_id,
                relative_path=relative_path,
            )
        )
    if len(documents) < 2:
        raise ValueError("bounded corpus requires at least two documents")
    return FedCorpus(
        corpus_id=str(raw["corpus_id"]),
        corpus_version=str(raw["corpus_version"]),
        data_tier=str(raw["data_tier"]),
        license_label=str(raw["license_label"]),
        sources=sources,
        documents=tuple(documents),
    )


def write_checksums_into_manifest(root: Path | None = None) -> dict[str, Any]:
    """Helper used by tests to pin checksums after content changes."""

    corpus = load_fed_corpus(root)
    corpus_root = root or DEFAULT_CORPUS_ROOT
    manifest_path = corpus_root / "manifest.yaml"
    raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    by_id = {item.document.document_id: item.checksum for item in corpus.documents}
    for row in raw["documents"]:
        row["checksum"] = by_id[row["document_id"]]
    manifest_path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    return by_id
