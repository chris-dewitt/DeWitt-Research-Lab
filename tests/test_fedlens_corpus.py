"""Tests for bounded public FedLens corpus ingest (DRL-015)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
import yaml
from fedlens_service import FedLensService, load_fed_corpus, write_checksums_into_manifest


ROOT = Path(__file__).resolve().parents[1] / "services" / "fedlens" / "corpus"


def test_corpus_checksums_identity_and_provenance() -> None:
    checksums = write_checksums_into_manifest(ROOT)
    corpus = load_fed_corpus(ROOT)
    assert corpus.data_tier == "public"
    assert corpus.license_label
    assert len(corpus.sources) >= 1
    assert len(corpus.documents) == 2
    ids = [item.document.document_id for item in corpus.documents]
    assert len(set(ids)) == len(ids)
    for item in corpus.documents:
        assert item.checksum == checksums[item.document.document_id]
        assert item.checksum.startswith("sha256:")
        assert item.source_id == corpus.sources[0].source_id
        assert item.document.citation.startswith("fixture://")


def test_as_of_excludes_later_documents() -> None:
    write_checksums_into_manifest(ROOT)
    service = FedLensService.from_bounded_corpus(ROOT)
    early = service.documents_as_of(as_of=date(2026, 5, 10))
    assert len(early) == 1
    assert early[0].document_id == "FOMC-2026-05-FIXTURE"
    latest = service.latest(as_of=date(2026, 7, 24))
    assert latest.document_id == "FOMC-2026-06-FIXTURE"


def test_checksum_mismatch_fails(tmp_path: Path) -> None:
    # Copy corpus
    import shutil

    dest = tmp_path / "corpus"
    shutil.copytree(ROOT, dest)
    write_checksums_into_manifest(dest)
    manifest = yaml.safe_load((dest / "manifest.yaml").read_text(encoding="utf-8"))
    manifest["documents"][0]["checksum"] = "sha256:" + ("0" * 64)
    (dest / "manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="checksum mismatch"):
        load_fed_corpus(dest)
